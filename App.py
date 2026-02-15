import streamlit as st
import pandas as pd

# --- KONFIGURACE ---
st.set_page_config(page_title="ZOH 2026 - Tipovačka", page_icon="🏒", layout="wide")

# --- KOMPLETNÍ STYLOVÁNÍ ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    
    .main-title { font-size: 3rem; font-weight: 900; text-align: center; color: #1e3a8a; margin-bottom: 30px; }
    
    .match-card {
        background: #ffffff; border-radius: 20px; padding: 25px; margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #e5e7eb;
    }
    
    .score-area {
        display: flex; justify-content: space-around; align-items: center;
        background: #f8fafc; border-radius: 15px; padding: 15px; margin-bottom: 20px;
    }
    
    .score-box {
        font-size: 2.5rem; font-weight: 900; color: #1e293b; background: white;
        padding: 5px 25px; border-radius: 12px; border: 3px solid #1e3a8a;
    }
    
    .flag { font-size: 3.5rem; display: block; line-height: 1; }
    .team-label { font-weight: 800; font-size: 1.1rem; color: #475569; text-transform: uppercase; margin-top: 5px; }
    
    .tips-container {
        display: flex; flex-wrap: wrap; gap: 12px; justify-content: center;
    }
    
    .player-chip {
        min-width: 100px; padding: 10px; border-radius: 12px; text-align: center;
        position: relative; border: 2px solid #f1f5f9; background: #fff;
    }
    
    .banker-badge {
        position: absolute; top: -10px; right: -5px; background: #ef4444; color: white;
        font-size: 0.6rem; font-weight: 900; padding: 2px 6px; border-radius: 6px;
    }
    
    /* Barvy výsledků */
    .res-win { background-color: #dcfce7 !important; border-color: #22c55e !important; color: #166534 !important; }
    .res-draw { background-color: #fef9c3 !important; border-color: #eab308 !important; color: #854d0e !important; }
    .res-none { background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; color: #64748b !important; }
    
    .points-label { font-size: 0.75rem; font-weight: 900; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# --- KONSTANTY A DATA ---
FLAGS = {
    "Slovensko": "🇸🇰", "Finsko": "🇫🇮", "Švédsko": "🇸🇪", "Itálie": "🇮🇹", "Švýcarsko": "🇨🇭",
    "Francie": "🇫🇷", "Česko": "🇨🇿", "Kanada": "🇨🇦", "Lotyšsko": "🇱🇻", "USA": "🇺🇸",
    "Německo": "🇩🇪", "Dánsko": "🇩🇰"
}

# Zápasy ze souborů
GROUP_MATCHES = [
    {"id": "M1", "home": "Slovensko", "away": "Finsko", "res": "4:1"},
    {"id": "M2", "home": "Švédsko", "away": "Itálie", "res": "5:2"},
    {"id": "M3", "home": "Švýcarsko", "away": "Francie", "res": "4:0"},
    {"id": "M4", "home": "Česko", "away": "Kanada", "res": "0:5"},
    {"id": "M5", "home": "Lotyšsko", "away": "USA", "res": "1:5"},
    {"id": "M6", "home": "Německo", "away": "Dánsko", "res": "3:1"},
    {"id": "M7", "home": "Finsko", "away": "Švédsko", "res": "4:1"},
    {"id": "M8", "home": "Itálie", "away": "Slovensko", "res": "2:3"},
    {"id": "M9", "home": "Francie", "away": "Česko", "res": "3:6"},
    {"id": "M10", "home": "Kanada", "away": "Švýcarsko", "res": "5:1"},
    {"id": "M11", "home": "Německo", "away": "Lotyšsko", "res": "3:4"},
    {"id": "M12", "home": "Švédsko", "away": "Slovensko", "res": "5:3"},
    {"id": "M13", "home": "Finsko", "away": "Itálie", "res": "11:0"},
    {"id": "M14", "home": "USA", "away": "Dánsko", "res": "6:3"},
    {"id": "M15", "home": "Švýcarsko", "away": "Česko", "res": "3:3"},
    {"id": "M16", "home": "Kanada", "away": "Francie", "res": "8:0"},
    {"id": "M17", "home": "Dánsko", "away": "Lotyšsko", "res": "3:2"},
    {"id": "M18", "home": "USA", "away": "Německo", "res": "2:1"},
]

# Tipy hráčů (včetně Bankerů dle zdvojených bodů v tabulce)
PLAYER_TIPS = {
    'Aďas': {
        'M1':'1:3', 'M2':'6:1', 'M3':'6:2', 'M4':'2:4', 'M5':'2:3', 'M6':'4:3', 'M7':'1:3', 'M8':'2:4', 
        'M9':('0:5', True), 'M10':'3:1', 'M11':'2:2', 'M12':('5:1', True), 'M13':'3:0', 'M14':'5:2', 'M15':'3:3',
        'M16':'8:0', 'M17':'3:2', 'M18':'2:1'
    },
    'Víťa': {
        'M1':'2:2', 'M2':'4:0', 'M3':'4:1', 'M4':'1:4', 'M5':'2:6', 'M6':'3:2', 'M7':'3:3', 'M8':'3:4', 
        'M9':'0:3', 'M10':'4:2', 'M11':'3:2', 'M12':'4:0', 'M13':'3:1', 'M14':'6:1', 'M15':'4:2',
        'M16':'5:0', 'M17':'3:2', 'M18':'4:3'
    },
    'Cigi ml.': {
        'M1':'2:4', 'M2':'6:2', 'M3':'3:1', 'M4':'3:5', 'M5':'1:4', 'M6':'4:2', 'M7':'2:3', 'M8':'3:5',
        'M9':'1:4', 'M10':'4:1', 'M11':'3:3', 'M12':'6:2', 'M13':'5:0', 'M14':'6:1', 'M15':'4:5',
        'M16':'7:0', 'M17':'4:2', 'M18':'5:2'
    },
    'Mršťa': {
        'M1':'2:4', 'M2':'7:1', 'M3':'5:2', 'M4':'2:5', 'M5':'2:5', 'M6':'5:3', 'M7':'2:3', 'M8':'1:5',
        'M9':'1:6', 'M10':'4:2', 'M11':'3:1', 'M12':'7:3', 'M13':'2:2', 'M14':('4:0', True), 'M15':'3:5',
        'M16':'9:1', 'M17':'3:3', 'M18':'5:4'
    },
    'Fany': {
        'M1':'1:4', 'M2':'5:0', 'M3':'3:2', 'M4':'2:4', 'M5':'3:4', 'M6':'2:1'
    }
}

PRE_TIPS = [
    {"Hráč": "Aďas", "Vítěz": "Kanada", "2.": "Česko", "3.": "Švédsko", "4.": "Švýcarsko", "Střelec": "MacKinnon", "Brankář": "Vladař", "MVP": "MacKinnon"},
    {"Hráč": "Cigi ml.", "Vítěz": "Kanada", "2.": "Švédsko", "3.": "USA", "4.": "Finsko", "Střelec": "Celebriny", "Brankář": "Thompson", "MVP": "McDavid"},
    {"Hráč": "Mršťa", "Vítěz": "Kanada", "2.": "Švédsko", "3.": "Česko", "4.": "Švýcarsko", "Střelec": "Pastrňák", "Brankář": "Genoni", "MVP": "Crosby"},
    {"Hráč": "Víťa", "Vítěz": "Kanada", "2.": "USA", "3.": "Česko", "4.": "Švédsko", "Střelec": "Matthews", "Brankář": "Saros", "MVP": "Raymond"},
]

# --- POMOCNÉ FUNKCE ---
def calculate_points(tip_val, result_val):
    if not tip_val or not result_val: return 0
    t_raw = tip_val[0] if isinstance(tip_val, tuple) else tip_val
    is_banker = tip_val[1] if isinstance(tip_val, tuple) else False
    
    try:
        th, ta = map(int, t_raw.split(":"))
        rh, ra = map(int, result_val.split(":"))
        pts = 0
        if th == rh and ta == ra: pts = 3
        elif (th > ta and rh > ra) or (th < ta and rh < ra) or (th == ta and rh == ra): pts = 1
        return pts * 2 if is_banker else pts
    except: return 0

# --- HLAVNÍ STRUKTURA ---
st.markdown('<div class="main-title">🏒 ZOH 2026 TIPŮ CENTRÁLA</div>', unsafe_allow_html=True)

tabs = st.tabs(["🏆 POŘADÍ", "📅 SKUPINY", "🔥 PLAY-OFF", "🔮 PŘED TURNAJEM", "✍️ MŮJ TIP"])

# TAB 1: POŘADÍ
with tabs[0]:
    ranking = []
    players = sorted(PLAYER_TIPS.keys())
    for p in players:
        total_pts = sum(calculate_points(PLAYER_TIPS[p].get(m['id']), m['res']) for m in GROUP_MATCHES)
        exact_hits = sum(1 for m in GROUP_MATCHES if calculate_points(PLAYER_TIPS[p].get(m['id']), m['res']) in [3, 6])
        ranking.append({"Hráč": p, "Body": total_pts, "Přesné trefy": exact_hits})
    
    df_rank = pd.DataFrame(ranking).sort_values(["Body", "Přesné trefy"], ascending=False).reset_index(drop=True)
    st.dataframe(df_rank, use_container_width=True, hide_index=True)

# TAB 2: SKUPINY
with tabs[1]:
    for m in GROUP_MATCHES:
        res = m['res'] or "?:?"
        html = f"""
        <div class="match-card">
            <div class="score-area">
                <div style="text-align:center;"><span class="flag">{FLAGS.get(m['home'])}</span><div class="team-label">{m['home']}</div></div>
                <div class="score-box">{res}</div>
                <div style="text-align:center;"><span class="flag">{FLAGS.get(m['away'])}</span><div class="team-label">{m['away']}</div></div>
            </div>
            <div class="tips-container">
        """
        for p in players:
            tip_data = PLAYER_TIPS[p].get(m['id'])
            if not tip_data: continue
            
            pts = calculate_points(tip_data, m['res'])
            is_banker = tip_data[1] if isinstance(tip_data, tuple) else False
            tip_str = tip_data[0] if isinstance(tip_data, tuple) else tip_data
            
            # Barevná logika
            cls = "res-none"
            if m['res']:
                if pts >= 3: cls = "res-win"
                elif pts >= 1: cls = "res-draw"
            
            banker_html = '<div class="banker-badge">🃏 BANKER</div>' if is_banker else ''
            html += f"""
                <div class="player-chip {cls}">
                    {banker_html}
                    <div style="font-size:0.7rem; font-weight:700;">{p}</div>
                    <div style="font-size:1.1rem; font-weight:900;">{tip_str}</div>
                    <div class="points-label">{pts}b</div>
                </div>
            """
        html += "</div></div>"
        st.markdown(html, unsafe_allow_html=True)

# TAB 3: PLAY-OFF
with tabs[2]:
    st.info("Základní skupiny skončily. Zde je rozpis play-off. Tipujte v záložce Můj Tip!")
    po_matches = [
        ("Osmifinále", "Česko", "Dánsko"),
        ("Osmifinále", "Švédsko", "Lotyšsko"),
        ("Osmifinále", "Švýcarsko", "Francie"),
        ("Osmifinále", "Německo", "Itálie")
    ]
    for r, h, a in po_matches:
        st.markdown(f"""
        <div class="match-card" style="border-left-color:#eab308;">
            <div style="text-align:center; font-weight:900; color:#eab308; margin-bottom:10px;">{r}</div>
            <div class="score-area" style="background:white; border:1px solid #eee;">
                <div style="text-align:center;"><span class="flag">{FLAGS.get(h)}</span><div class="team-label">{h}</div></div>
                <div style="font-weight:900; color:#cbd5e1;">VS</div>
                <div style="text-align:center;"><span class="flag">{FLAGS.get(a)}</span><div class="team-label">{a}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# TAB 4: PŘED TURNAJEM
with tabs[3]:
    st.table(pd.DataFrame(PRE_TIPS))

# TAB 5: MŮJ TIP GENERÁTOR
with tabs[4]:
    st.subheader("Zadej své tipy a pošli je klukům")
    c1, c2 = st.columns(2)
    with c1:
        p_name = st.selectbox("Vyber své jméno", players)
        t1 = st.text_input("Česko - Dánsko", placeholder="např. 4:1")
        t2 = st.text_input("Švédsko - Lotyšsko", placeholder="např. 5:2")
    with c2:
        is_b = st.selectbox("Banker na zápas:", ["Žádný", "Česko-Dánsko", "Švédsko-Lotyšsko"])
        t3 = st.text_input("Švýcarsko - Francie", placeholder="např. 3:0")
        t4 = st.text_input("Německo - Itálie", placeholder="např. 2:1")
    
    if st.button("Vygenerovat přehled pro chat"):
        res_txt = f"🏒 MOJE TIPY - {p_name.upper()}\n"
        res_txt += f"🇨🇿 CZE-DEN: {t1} {'🃏' if is_b == 'Česko-Dánsko' else ''}\n"
        res_txt += f"🇸🇪 SWE-LAT: {t2} {'🃏' if is_b == 'Švédsko-Lotyšsko' else ''}\n"
        res_txt += f"🇨🇭 SUI-FRA: {t3}\n"
        res_txt += f"🇩🇪 GER-ITA: {t4}"
        st.code(res_txt)
