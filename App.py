import streamlit as st
import pandas as pd

# --- KONFIGURACE ---
st.set_page_config(page_title="ZOH 2026 - Tipovačka", page_icon="🏒", layout="wide")

# --- CSS STYLY (Opraveno pro čisté zobrazení) ---
st.markdown("""
<style>
    .match-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 8px solid #0033a0;
    }
    .match-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        padding-bottom: 15px;
        border-bottom: 1px solid #f0f2f5;
    }
    .score-badge {
        font-size: 2.2rem;
        font-weight: 800;
        color: #111827;
        background: #f3f4f6;
        padding: 5px 20px;
        border-radius: 10px;
        min-width: 100px;
        text-align: center;
    }
    .team-container { width: 35%; text-align: center; }
    .team-name { font-weight: 700; font-size: 1.1rem; text-transform: uppercase; color: #374151; margin-top: 5px; }
    .flag { font-size: 3rem; line-height: 1; display: block; }
    
    /* Grid pro tipy */
    .tips-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(85px, 1fr));
        gap: 10px;
    }
    
    .tip-box {
        background: #fff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 8px;
        text-align: center;
        position: relative;
    }
    
    .player-name { font-size: 0.7rem; color: #6b7280; font-weight: 600; }
    .tip-value { font-size: 1.1rem; font-weight: 900; color: #111827; }
    .points-val { font-size: 0.8rem; font-weight: 700; }
    
    /* Bankeři a statusy */
    .banker-badge {
        position: absolute; top: -8px; right: -5px;
        background: #ef4444; color: white;
        font-size: 0.6rem; font-weight: 800;
        padding: 1px 5px; border-radius: 4px;
    }
    
    .pts-3 { background-color: #dcfce7 !important; border-color: #86efac !important; color: #166534 !important; }
    .pts-1 { background-color: #fef9c3 !important; border-color: #fde047 !important; color: #854d0e !important; }
    .pts-0 { background-color: #f9fafb !important; border-color: #e5e7eb !important; color: #9ca3af !important; }
    
    .playoff-label {
        text-align: center; font-weight: 700; color: #ef4444; 
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. DATA: ZÁPASY SKUPINY ---
MATCHES = [
    {"id": "M1", "h": "Slovensko", "a": "Finsko", "res": "4:1"},
    {"id": "M2", "h": "Švédsko", "a": "Itálie", "res": "5:2"},
    {"id": "M3", "h": "Švýcarsko", "a": "Francie", "res": "4:0"},
    {"id": "M4", "h": "Česko", "a": "Kanada", "res": "0:5"},
    {"id": "M5", "h": "Lotyšsko", "a": "USA", "res": "1:5"},
    {"id": "M6", "h": "Německo", "a": "Dánsko", "res": "3:1"},
    {"id": "M7", "h": "Finsko", "a": "Švédsko", "res": "4:1"},
    {"id": "M8", "h": "Itálie", "a": "Slovensko", "res": "2:3"},
    {"id": "M9", "h": "Francie", "a": "Česko", "res": "3:6"},
    {"id": "M10", "h": "Kanada", "a": "Švýcarsko", "res": "5:1"},
    {"id": "M11", "h": "Německo", "a": "Lotyšsko", "res": "3:4"},
    {"id": "M12", "h": "Švédsko", "a": "Slovensko", "res": "5:3"},
    {"id": "M13", "h": "Finsko", "a": "Itálie", "res": "11:0"},
    {"id": "M14", "h": "USA", "a": "Dánsko", "res": "6:3"},
    {"id": "M15", "h": "Švýcarsko", "a": "Česko", "res": "3:3"},
    {"id": "M16", "h": "Kanada", "a": "Francie", "res": "10:2"},
    {"id": "M17", "h": "Dánsko", "a": "Lotyšsko", "res": "3:2"},
    {"id": "M18", "h": "USA", "a": "Německo", "res": "2:1"},
]

# --- 2. DATA: PLAY-OFF (Opravený pavouk) ---
PLAYOFF = [
    # Osmifinále (Předkolo)
    {"stage": "Osmifinále", "date": "Úterý 17.02.", "h": "Česko", "a": "Dánsko", "code": "OF1"},
    {"stage": "Osmifinále", "date": "Úterý 17.02.", "h": "Švédsko", "a": "Lotyšsko", "code": "OF2"},
    {"stage": "Osmifinále", "date": "Úterý 17.02.", "h": "Švýcarsko", "a": "Francie", "code": "OF3"},
    {"stage": "Osmifinále", "date": "Úterý 17.02.", "h": "Německo", "a": "Itálie", "code": "OF4"},
    # Čtvrtfinále
    {"stage": "Čtvrtfinále", "date": "Středa 18.02.", "h": "Kanada", "a": "vítěz OF1 (CZE/DEN)", "code": "QF1"},
    {"stage": "Čtvrtfinále", "date": "Středa 18.02.", "h": "Finsko", "a": "vítěz OF2 (SWE/LAT)", "code": "QF2"},
    {"stage": "Čtvrtfinále", "date": "Středa 18.02.", "h": "USA", "a": "vítěz OF3 (SUI/FRA)", "code": "QF3"},
    {"stage": "Čtvrtfinále", "date": "Středa 18.02.", "h": "Slovensko", "a": "vítěz OF4 (GER/ITA)", "code": "QF4"},
]

# --- 3. DATA: TIPY HRÁČŮ ---
# Format: 'ID': ('TIP', IsBanker)
TIPS = {
    'Aďas': {
        'M1':('1:3',False), 'M2':('6:1',False), 'M3':('6:2',False), 'M4':('2:4',False), 'M5':('2:3',False), 'M6':('4:3',False),
        'M7':('1:3',False), 'M8':('2:4',False), 'M9':('0:5',True), 'M10':('3:1',False),
        'M11':('2:2',False), 'M12':('5:1',True), 'M13':('3:0',False), 'M14':('5:2',False),
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
        'M11':('3:1',False), 'M12':('7:3',False), 'M13':('2:2',False), 'M14':('4:0',True),
        'M15':('3:5',False), 'M16':('9:1',False), 'M17':('3:3',False), 'M18':('5:4',False)
    },
    'Fany': {
        'M1':('1:4',False), 'M2':('5:0',False), 'M3':('3:2',False), 'M4':('2:4',False), 'M5':('3:4',False), 'M6':('2:1',False)
    },
    'Moli': {'M1':('1:5',False), 'M2':('8:0',False)}, 'Alesh':{}, 'Cigi':{}
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
PLAYERS = sorted([p for p in TIPS.keys() if len(TIPS[p]) > 0])

# --- LOGIKA BODOVÁNÍ ---
def get_pts(tip_tuple, res_str):
    if not tip_tuple or not res_str: return 0
    tip, is_banker = tip_tuple
    try:
        th, ta = map(int, tip.split(":"))
        rh, ra = map(int, res_str.split(":"))
        pts = 0
        if th == rh and ta == ra: pts = 3
        elif (th > ta and rh > ra) or (th < ta and rh < ra) or (th == ta and rh == ra): pts = 1
        return pts * 2 if is_banker else pts
    except: return 0

# --- APLIKACE ---
st.title("🏒 ZOH 2026 - CENTRÁLA")

tabs = st.tabs(["🏆 TABULKA", "📅 SKUPINY", "🔥 PLAY-OFF", "🔮 PŘED TURNAJEM", "✍️ GENERÁTOR"])

# 1. TABULKA
with tabs[0]:
    rank = []
    for p in PLAYERS:
        pts = sum(get_pts(TIPS[p].get(m['id']), m['res']) for m in MATCHES)
        hits = sum(1 for m in MATCHES if get_pts(TIPS[p].get(m['id']), m['res']) in [3, 6])
        rank.append({"Hráč": p, "Body": pts, "Přesné trefy": hits})
    st.dataframe(pd.DataFrame(rank).sort_values(["Body", "Přesné trefy"], ascending=False).reset_index(drop=True), use_container_width=True)

# 2. SKUPINY (Opraveno renderování HTML)
with tabs[1]:
    for m in MATCHES:
        res = m['res']
        # HTML pro celou gridu tipů se vygeneruje najednou
        tips_html = ""
        for p in PLAYERS:
            tip_data = TIPS[p].get(m['id'])
            if not tip_data: continue
            
            tip_val, is_banker = tip_data
            pts = get_pts(tip_data, res)
            
            css = "pts-0"
            if pts >= 3: css = "pts-3"
            elif pts >= 1: css = "pts-1"
            
            banker_html = '<div class="banker-badge">🃏</div>' if is_banker else ''
            
            tips_html += f"""
            <div class="tip-box {css}">
                {banker_html}
                <div class="player-name">{p}</div>
                <div class="tip-value">{tip_val}</div>
                <div class="points-val">{pts}b</div>
            </div>
            """
            
        # Vykreslení karty zápasu
        st.markdown(f"""
        <div class="match-card">
            <div class="match-header">
                <div class="team-container">
                    <span class="flag">{FLAGS.get(m['h'], '')}</span>
                    <div class="team-name">{m['h']}</div>
                </div>
                <div class="score-badge">{res}</div>
                <div class="team-container">
                    <span class="flag">{FLAGS.get(m['a'], '')}</span>
                    <div class="team-name">{m['a']}</div>
                </div>
            </div>
            <div class="tips-grid">{tips_html}</div>
        </div>
        """, unsafe_allow_html=True)

# 3. PLAY-OFF
with tabs[2]:
    st.info("Play-off pavouk pro rok 2026. Tipy zadávejte v záložce Generátor.")
    for g in PLAYOFF:
        st.markdown(f"""
        <div class="match-card" style="border-left-color: #ef4444; padding: 15px;">
            <div class="playoff-label">{g['stage']} • {g['date']}</div>
            <div class="match-header" style="border-bottom:none; margin-bottom:0;">
                <div class="team-container" style="width:40%;">
                    <span class="flag">{FLAGS.get(g['h'], '🏒')}</span>
                    <div class="team-name">{g['h']}</div>
                </div>
                <div style="font-size:1.5rem; font-weight:900; color:#d1d5db;">VS</div>
                <div class="team-container" style="width:40%;">
                    <span class="flag">{FLAGS.get(g['a'], '🏒')}</span>
                    <div class="team-name">{g['a']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 4. PŘED TURNAJEM
with tabs[3]:
    st.table(pd.DataFrame(PRE_DATA))

# 5. GENERÁTOR
with tabs[4]:
    st.subheader("✍️ Zadej tipy na Play-off")
    me = st.selectbox("Kdo jsi?", PLAYERS)
    
    col1, col2 = st.columns(2)
    user_tips = {}
    
    with col1:
        st.markdown("##### 🎱 Osmifinále")
        for g in PLAYOFF[:4]:
            code = g['code']
            user_tips[code] = st.text_input(f"{g['h']} vs {g['a']}", key=code)
            
    with col2:
        st.markdown("##### 🏆 Čtvrtfinále")
        for g in PLAYOFF[4:]:
            code = g['code']
            user_tips[code] = st.text_input(f"{g['h']} vs {g['a']}", key=code)
            
    if st.button("Generovat text"):
        txt = f"🏒 *TIPY PLAY-OFF - {me.upper()}* 🏒\n"
        has_tips = False
        for g in PLAYOFF:
            code = g['code']
            val = user_tips.get(code)
            if val:
                txt += f"\n{g['h']} vs {g['a']}: *{val}*"
                has_tips = True
        
        if has_tips:
            st.code(txt, language="text")
        else:
            st.warning("Zadej alespoň jeden tip.")
