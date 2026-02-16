import streamlit as st
import pandas as pd

# --- KONFIGURACE ---
st.set_page_config(page_title="ZOH 2026 - Tipovačka", page_icon="🏒", layout="wide")

# --- DESIGN ---
st.markdown("""
<style>
    /* Hlavní kontejner zápasu */
    .match-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 8px solid #0033a0; /* Česká modrá */
    }
    
    /* Skóre uprostřed */
    .score-badge {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1a1a1a;
        background: #f8f9fa;
        padding: 5px 20px;
        border-radius: 8px;
        min-width: 120px;
        text-align: center;
        border: 1px solid #dee2e6;
    }
    
    /* Názvy týmů */
    .team-name {
        font-weight: 700;
        font-size: 1.1rem;
        text-transform: uppercase;
        color: #333;
        margin-top: 5px;
    }
    
    /* Vlajky */
    .flag { font-size: 3rem; line-height: 1; }
    
    /* Grid pro tipy hráčů */
    .tips-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
        gap: 10px;
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid #eee;
    }
    
    /* Kartička tipu */
    .tip-box {
        background: #fff;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 8px;
        text-align: center;
        position: relative;
    }
    
    /* Banker odznak */
    .banker-badge {
        position: absolute;
        top: -8px;
        right: -5px;
        background-color: #dc3545;
        color: white;
        font-size: 0.6rem;
        font-weight: bold;
        padding: 2px 6px;
        border-radius: 4px;
        box-shadow: 0 2px 2px rgba(0,0,0,0.2);
    }
    
    /* Barvy bodů */
    .pts-3 { background-color: #d1e7dd !important; border-color: #badbcc !important; color: #0f5132 !important; }
    .pts-1 { background-color: #fff3cd !important; border-color: #ffecb5 !important; color: #664d03 !important; }
    .pts-0 { background-color: #f8d7da !important; border-color: #f5c2c7 !important; opacity: 0.7; }
    
    /* Playoff styly */
    .playoff-header {
        text-align: center;
        font-weight: bold;
        color: #6c757d;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. DATA: ZÁPASY SKUPINY (Kompletní a opravené) ---
MATCHES = [
    # Středa
    {"id": "M1", "h": "Slovensko", "a": "Finsko", "res": "4:1"},
    {"id": "M2", "h": "Švédsko", "a": "Itálie", "res": "5:2"},
    # Čtvrtek
    {"id": "M3", "h": "Švýcarsko", "a": "Francie", "res": "4:0"},
    {"id": "M4", "h": "Česko", "a": "Kanada", "res": "0:5"},
    {"id": "M5", "h": "Lotyšsko", "a": "USA", "res": "1:5"},
    {"id": "M6", "h": "Německo", "a": "Dánsko", "res": "3:1"},
    # Pátek
    {"id": "M7", "h": "Finsko", "a": "Švédsko", "res": "4:1"},
    {"id": "M8", "h": "Itálie", "a": "Slovensko", "res": "2:3"},
    {"id": "M9", "h": "Francie", "a": "Česko", "res": "3:6"},
    {"id": "M10", "h": "Kanada", "a": "Švýcarsko", "res": "5:1"},
    # Sobota
    {"id": "M11", "h": "Německo", "a": "Lotyšsko", "res": "3:4"},
    {"id": "M12", "h": "Švédsko", "a": "Slovensko", "res": "5:3"},
    {"id": "M13", "h": "Finsko", "a": "Itálie", "res": "11:0"},
    {"id": "M14", "h": "USA", "a": "Dánsko", "res": "6:3"},
    # Neděle
    {"id": "M15", "h": "Švýcarsko", "a": "Česko", "res": "3:3"},
    {"id": "M16", "h": "Kanada", "a": "Francie", "res": "10:2"},
    {"id": "M17", "h": "Dánsko", "a": "Lotyšsko", "res": "3:2"},
    {"id": "M18", "h": "USA", "a": "Německo", "res": "2:1"},
]

# --- 2. DATA: PLAY-OFF ROZPIS ---
# Round of 16 (Osmifinále) - Úterý
# QF (Čtvrtfinále) - Středa
PLAYOFF = [
    {"stage": "Osmifinále", "date": "Úterý 17.02.", "h": "Česko", "a": "Dánsko"},
    {"stage": "Osmifinále", "date": "Úterý 17.02.", "h": "Švédsko", "a": "Lotyšsko"},
    {"stage": "Osmifinále", "date": "Úterý 17.02.", "h": "Švýcarsko", "a": "Francie"},
    {"stage": "Osmifinále", "date": "Úterý 17.02.", "h": "Německo", "a": "Itálie"},
    {"stage": "Čtvrtfinále", "date": "Středa 18.02.", "h": "Kanada", "a": "vítěz GER/ITA"},
    {"stage": "Čtvrtfinále", "date": "Středa 18.02.", "h": "USA", "a": "vítěz SUI/FRA"},
    {"stage": "Čtvrtfinále", "date": "Středa 18.02.", "h": "Finsko", "a": "vítěz SWE/LAT"},
    {"stage": "Čtvrtfinále", "date": "Středa 18.02.", "h": "Slovensko", "a": "vítěz CZE/DEN"},
]

# --- 3. DATA: TIPY HRÁČŮ ---
# Format: 'MatchID': ('Tip', IsBankerBoolean)
TIPS = {
    'Aďas': {
        'M1':('1:3',False), 'M2':('6:1',False), 'M3':('6:2',False), 'M4':('2:4',False), 'M5':('2:3',False), 'M6':('4:3',False),
        'M7':('1:3',False), 'M8':('2:4',False), 'M9':('0:5',True), 'M10':('3:1',False), # M9 Banker
        'M11':('2:2',False), 'M12':('5:1',True), 'M13':('3:0',False), 'M14':('5:2',False), # M12 Banker
        'M15':('3:3',False), 'M16':('8:0',False), 'M17':('3:2',False), 'M18':('2:1',False)
    },
    'Víťa': {
        'M1':('2:2',False), 'M2':('4:0',False), 'M3':('4:1',False), 'M4':('1:4',False), 'M5':('2:6',False), 'M6':('3:2',False),
        'M7':('3:3',False), 'M8':('3:4',False), 'M9':('0:3',False), 'M10':('4:2',False),
        'M11':('3:2',False), 'M12':('4:0',False), 'M13':('3:1',False), 'M14':('6:1',False),
        'M15':('4:2',False), 'M16':('5:0',False), 'M17':('3:2',False), 'M18':('4:3',False)
    },
    'Cigi ml.': {
        'M1':('2:4',False), 'M2':('6:2',False), 'M3':('3:1',False), 'M4':('3:5',False), 'M5':('1:4',False), 'M6':('4:2',False),
        'M7':('2:3',False), 'M8':('3:5',False), 'M9':('1:4',False), 'M10':('4:1',False),
        'M11':('3:3',False), 'M12':('6:2',False), 'M13':('5:0',False), 'M14':('6:1',False),
        'M15':('4:5',False), 'M16':('7:0',False), 'M17':('4:2',False), 'M18':('5:2',False)
    },
    'Mršťa': {
        'M1':('2:4',False), 'M2':('7:1',False), 'M3':('5:2',False), 'M4':('2:5',False), 'M5':('2:5',False), 'M6':('5:3',False),
        'M7':('2:3',False), 'M8':('1:5',False), 'M9':('1:6',False), 'M10':('4:2',False),
        'M11':('3:1',False), 'M12':('7:3',False), 'M13':('2:2',False), 'M14':('4:0',True), # M14 Banker
        'M15':('3:5',False), 'M16':('9:1',False), 'M17':('3:3',False), 'M18':('5:4',False)
    },
    'Fany': {
        'M1':('1:4',False), 'M2':('5:0',False), 'M3':('3:2',False), 'M4':('2:4',False), 'M5':('3:4',False), 'M6':('2:1',False)
    },
    'Moli': {'M1':('1:5',False), 'M2':('8:0',False)}
}

# --- 4. DATA: PŘED TURNAJEM ---
PRE_DATA = [
    {"Hráč": "Aďas", "Vítěz": "Kanada", "2. místo": "Česko", "3. místo": "Švédsko", "4. místo": "Švýcarsko", "Střelec": "MacKinnon", "Brankář": "Vladař", "MVP": "MacKinnon"},
    {"Hráč": "Cigi ml.", "Vítěz": "Kanada", "2. místo": "Švédsko", "3. místo": "USA", "4. místo": "Finsko", "Střelec": "Celebriny", "Brankář": "Thompson", "MVP": "McDavid"},
    {"Hráč": "Mršťa", "Vítěz": "Kanada", "2. místo": "Švédsko", "3. místo": "Česko", "4. místo": "Švýcarsko", "Střelec": "Pastrňák", "Brankář": "Genoni", "MVP": "Crosby"},
    {"Hráč": "Víťa", "Vítěz": "Kanada", "2. místo": "USA", "3. místo": "Česko", "4. místo": "Švédsko", "Střelec": "Matthews", "Brankář": "Saros", "MVP": "Raymond"},
    {"Hráč": "Fany", "Vítěz": "Švýcarsko", "2. místo": "Švédsko", "3. místo": "Finsko", "4. místo": "Česko", "Střelec": "Petterson", "Brankář": "Binnington", "MVP": "Josi"},
]

FLAGS = {"Česko": "🇨🇿", "Kanada": "🇨🇦", "Slovensko": "🇸🇰", "Finsko": "🇫🇮", "Švédsko": "🇸🇪", "Itálie": "🇮🇹", "USA": "🇺🇸", "Německo": "🇩🇪", "Lotyšsko": "🇱🇻", "Francie": "🇫🇷", "Dánsko": "🇩🇰", "Švýcarsko": "🇨🇭"}
PLAYERS = sorted(list(TIPS.keys()))

# --- LOGIKA BODOVÁNÍ ---
def calculate_points(tip_tuple, res_str):
    if not tip_tuple or not res_str: return 0
    tip, is_banker = tip_tuple
    try:
        th, ta = map(int, tip.split(":"))
        rh, ra = map(int, res_str.split(":"))
        points = 0
        
        # Přesný výsledek = 3 body
        if th == rh and ta == ra:
            points = 3
        # Správný vítěz/remíza = 1 bod
        elif (th > ta and rh > ra) or (th < ta and rh < ra) or (th == ta and rh == ra):
            points = 1
            
        return points * 2 if is_banker else points
    except:
        return 0

# --- APLIKACE ---
st.title("🏒 ZOH 2026 - TIPY CENTRÁLA")

tabs = st.tabs(["🏆 TABULKA", "📅 SKUPINY", "🔥 PLAY-OFF", "🔮 PŘED TURNAJEM", "✍️ GENERÁTOR"])

# 1. TABULKA
with tabs[0]:
    ranking = []
    for p in PLAYERS:
        total_pts = sum(calculate_points(TIPS[p].get(m['id']), m['res']) for m in MATCHES)
        # Počet přesných tref (3 nebo 6 bodů)
        exact_hits = sum(1 for m in MATCHES if calculate_points(TIPS[p].get(m['id']), m['res']) in [3, 6])
        ranking.append({"Hráč": p, "Body": total_pts, "Přesné trefy": exact_hits})
    
    st.dataframe(pd.DataFrame(ranking).sort_values(["Body", "Přesné trefy"], ascending=False).reset_index(drop=True), use_container_width=True)

# 2. SKUPINY
with tabs[1]:
    for m in MATCHES:
        res = m['res']
        # Vytvoříme HTML pro tipy všech hráčů najednou
        tips_html = ""
        for p in PLAYERS:
            tip_data = TIPS[p].get(m['id'])
            if not tip_data: continue
            
            tip_val, is_banker = tip_data
            pts = calculate_points(tip_data, res)
            
            # CSS třída pro barvu
            css_class = "pts-0"
            if pts >= 3: css_class = "pts-3"
            elif pts >= 1: css_class = "pts-1"
            
            banker_html = '<div class="banker-badge">🃏</div>' if is_banker else ''
            
            tips_html += f"""
            <div class="tip-box {css_class}">
                {banker_html}
                <div style="font-size:0.7rem; color:#6c757d; font-weight:bold;">{p}</div>
                <div style="font-size:1.1rem; font-weight:900;">{tip_val}</div>
                <div style="font-size:0.8rem; font-weight:bold;">{pts}b</div>
            </div>
            """
            
        # Celá karta zápasu
        st.markdown(f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="width:35%; text-align:center;">
                    <span class="flag">{FLAGS.get(m['h'], '')}</span>
                    <div class="team-name">{m['h']}</div>
                </div>
                <div class="score-badge">{res}</div>
                <div style="width:35%; text-align:center;">
                    <span class="flag">{FLAGS.get(m['a'], '')}</span>
                    <div class="team-name">{m['a']}</div>
                </div>
            </div>
            <div class="tips-grid">{tips_html}</div>
        </div>
        """, unsafe_allow_html=True)

# 3. PLAY-OFF
with tabs[2]:
    st.info("Pavouk play-off. Tipy zadávejte v záložce Generátor.")
    for game in PLAYOFF:
        st.markdown(f"""
        <div class="match-card" style="border-left-color: #ffc107;">
            <div class="playoff-header">{game['stage']} • {game['date']}</div>
            <div style="display:flex; justify-content:space-around; align-items:center;">
                <div style="width:40%; text-align:center;">
                    <span class="flag">{FLAGS.get(game['h'], '🏒')}</span>
                    <div class="team-name">{game['h']}</div>
                </div>
                <div style="font-size:1.5rem; font-weight:900; color:#dee2e6;">VS</div>
                <div style="width:40%; text-align:center;">
                    <span class="flag">{FLAGS.get(game['a'], '🏒')}</span>
                    <div class="team-name">{game['a']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 4. PŘED TURNAJEM
with tabs[3]:
    st.dataframe(pd.DataFrame(PRE_DATA), use_container_width=True)

# 5. GENERÁTOR TIPŮ
with tabs[4]:
    st.markdown("### ✍️ Zadej své tipy na Play-off")
    me = st.selectbox("Jméno hráče:", PLAYERS)
    
    col1, col2 = st.columns(2)
    user_tips = {}
    
    with col1:
        st.markdown("**Osmifinále (Úterý)**")
        for g in PLAYOFF[:4]:
            key = f"{g['h']}-{g['a']}"
            user_tips[key] = st.text_input(f"{g['h']} vs {g['a']}", key=key, placeholder="např. 3:1")
            
    with col2:
        st.markdown("**Čtvrtfinále (Středa)**")
        for g in PLAYOFF[4:]:
            key = f"{g['h']}-{g['a']}"
            user_tips[key] = st.text_input(f"{g['h']} vs {g['a']}", key=key, placeholder="např. 2:2")

    if st.button("Generovat zprávu pro chat"):
        msg = f"🏒 *TIPY PLAY-OFF - {me.upper()}* 🏒\n\n"
        for k, v in user_tips.items():
            if v:
                msg += f"✅ {k}: {v}\n"
        st.text_area("Zkopíruj tento text:", value=msg, height=200)
