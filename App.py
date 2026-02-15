import streamlit as st
import pandas as pd

# --- KONFIGURACE A DESIGN ---
st.set_page_config(page_title="ZOH 2026 - Tipovačka", page_icon="🏒", layout="wide")

st.markdown("""
<style>
    .match-card {
        background: white; border-radius: 15px; padding: 20px; margin-bottom: 25px;
        border-left: 10px solid #003399; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .score-badge {
        font-size: 2.2rem; font-weight: 900; background: #1a1a1a; padding: 8px 25px;
        border-radius: 12px; color: white; min-width: 120px; text-align: center;
    }
    .team-name { font-weight: 800; font-size: 1.2rem; text-transform: uppercase; }
    .tip-grid {
        display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;
        padding-top: 15px; border-top: 1px solid #eee;
    }
    .tip-box {
        border-radius: 8px; padding: 10px; text-align: center; min-width: 90px;
        border: 1px solid #ddd; position: relative;
    }
    .banker-icon {
        position: absolute; top: -10px; right: -5px; background: #d7141a;
        color: white; font-size: 0.7rem; padding: 2px 6px; border-radius: 5px; font-weight: bold;
    }
    .res-3 { background-color: #d4edda !important; color: #155724 !important; border-color: #c3e6cb !important; }
    .res-1 { background-color: #fff3cd !important; color: #856404 !important; border-color: #ffeeba !important; }
    .res-0 { background-color: #f8f9fa !important; color: #6c757d !important; }
</style>
""", unsafe_allow_html=True)

# --- 1. DATA: ZÁPASY SKUPINY ---
MATCHES = [
    {"id": "M1", "date": "11.02.", "home": "Slovensko", "away": "Finsko", "res": "4:1"},
    {"id": "M2", "date": "11.02.", "home": "Švédsko", "away": "Itálie", "res": "5:2"},
    {"id": "M3", "date": "12.02.", "home": "Švýcarsko", "away": "Francie", "res": "4:0"},
    {"id": "M4", "date": "12.02.", "home": "Česko", "away": "Kanada", "res": "0:5"},
    {"id": "M5", "date": "12.02.", "home": "Lotyšsko", "away": "USA", "res": "1:5"},
    {"id": "M6", "date": "12.02.", "home": "Německo", "away": "Dánsko", "res": "3:1"},
    {"id": "M7", "date": "13.02.", "home": "Finsko", "away": "Švédsko", "res": "4:1"},
    {"id": "M8", "date": "13.02.", "home": "Itálie", "away": "Slovensko", "res": "2:3"},
    {"id": "M9", "date": "13.02.", "home": "Francie", "away": "Česko", "res": "3:6"},
    {"id": "M10", "date": "13.02.", "home": "Kanada", "away": "Švýcarsko", "res": "5:1"},
    {"id": "M11", "date": "14.02.", "home": "Německo", "away": "Lotyšsko", "res": "3:4"},
    {"id": "M12", "date": "14.02.", "home": "Švédsko", "away": "Slovensko", "res": "5:3"},
    {"id": "M13", "date": "14.02.", "home": "Finsko", "away": "Itálie", "res": "11:0"},
    {"id": "M14", "date": "14.02.", "home": "USA", "away": "Dánsko", "res": "6:3"},
    {"id": "M15", "date": "15.02.", "home": "Švýcarsko", "away": "Česko", "res": "3:3"},
    {"id": "M16", "date": "15.02.", "home": "Kanada", "away": "Francie", "res": "8:0"},
    {"id": "M17", "date": "15.02.", "home": "Dánsko", "away": "Lotyšsko", "res": "3:2"},
    {"id": "M18", "date": "15.02.", "home": "USA", "away": "Německo", "res": "2:1"},
]

# --- 2. DATA: PLAY-OFF ROZPIS ---
PLAYOFF_BRACKET = [
    {"id": "P1", "r": "Osmifinále", "h": "Česko", "a": "Dánsko"},
    {"id": "P2", "r": "Osmifinále", "h": "Švédsko", "a": "Lotyšsko"},
    {"id": "P3", "r": "Osmifinále", "h": "Švýcarsko", "a": "Francie"},
    {"id": "P4", "r": "Osmifinále", "h": "Německo", "a": "Itálie"},
    {"id": "Q1", "r": "Čtvrtfinále", "h": "Kanada", "a": "Vítěz P4"},
    {"id": "Q2", "r": "Čtvrtfinále", "h": "USA", "a": "Vítěz P3"},
    {"id": "Q3", "r": "Čtvrtfinále", "h": "Slovensko", "a": "Vítěz P1"},
    {"id": "Q4", "r": "Čtvrtfinále", "h": "Finsko", "a": "Vítěz P2"},
]

# --- 3. DATA: TIPY (Ručně ověřeno z CSV) ---
TIPS = {
    'Aďas': {
        'M1':'1:3', 'M2':'6:1', 'M3':'6:2', 'M4':'2:4', 'M5':'2:3', 'M6':'4:3', 'M7':'1:3', 'M8':'2:4', 
        'M9':('0:5', True), 'M10':'3:1', 'M11':'2:2', 'M12':('5:1', True), 'M13':'3:0', 'M14':'5:2', 
        'M15':'3:3', 'M16':'8:0', 'M17':'3:2', 'M18':'2:1'
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
    'Moli': {'M1':'1:5', 'M2':'8:0'},
    'Alesh': {}, 'Cigi': {}, 'Fany': {}
}

# --- 4. DATA: PŘED TURNAJEM ---
PRE_DATA = [
    {'Hráč': 'Aďas', 'Vítěz': 'Kanada', '2.': 'Česko', '3.': 'Švédsko', '4.': 'Švýcarsko', 'Střelec': 'MacKinnon', 'Nahrávač': 'Konecny', 'Brankář': 'Vladař', 'MVP': 'MacKinnon'},
    {'Hráč': 'Cigi ml.', 'Vítěz': 'Kanada', '2.': 'Švédsko', '3.': 'USA', '4.': 'Finsko', 'Střelec': 'Celebriny', 'Nahrávač': 'McDavid', 'Brankář': 'Thompson ', 'MVP': 'McDavid'},
    {'Hráč': 'Mršťa', 'Vítěz': 'Kanada', '2.': 'Švédsko ', '3.': 'Česko ', '4.': 'Švýcarsko ', 'Střelec': 'Pastrňák', 'Nahrávač': 'Crosby', 'Brankář': 'Genoni', 'MVP': 'Crosby'},
    {'Hráč': 'Víťa', 'Vítěz': 'Kanada', '2.': 'USA', '3.': 'Česko ', '4.': 'Švédsko', 'Střelec': 'Matthews', 'Nahrávač': 'McDavid', 'Brankář': 'Juuse Saros', 'MVP': 'Raymond'},
    {'Hráč': 'Fany', 'Vítěz': 'Švýcarsko ', '2.': 'Švédsko ', '3.': 'Finsko ', '4.': 'Česko ', 'Střelec': 'Petterson', 'Nahrávač': 'Ehlers', 'Brankář': 'Binnington', 'MVP': 'Josi'},
]

FLAGS = {"Česko": "🇨🇿", "Kanada": "🇨🇦", "Slovensko": "🇸🇰", "Finsko": "🇫🇮", "Švédsko": "🇸🇪", "Itálie": "🇮🇹", "USA": "🇺🇸", "Německo": "🇩🇪", "Lotyšsko": "🇱🇻", "Francie": "🇫🇷", "Dánsko": "🇩🇰", "Švýcarsko": "🇨🇭"}
PLAYERS = sorted(['Aďas', 'Víťa', 'Cigi ml.', 'Mršťa', 'Moli', 'Cigi', 'Alesh', 'Fany'])

# --- POMOCNÉ FUNKCE ---
def calc_pts(tip_raw, res):
    if not tip_raw or not res: return 0
    tip = tip_raw[0] if isinstance(tip_raw, tuple) else tip_raw
    banker = tip_raw[1] if isinstance(tip_raw, tuple) else False
    try:
        th, ta = map(int, tip.split(":"))
        rh, ra = map(int, res.split(":"))
        pts = 0
        if th == rh and ta == ra: pts = 3
        elif (th > ta and rh > ra) or (th < ta and rh < ra) or (th == ta and rh == ra): pts = 1
        return pts * 2 if banker else pts
    except: return 0

# --- APLIKACE ---
st.title("🏒 ZOH 2026 - Oficiální Tipovačka")

tabs = st.tabs(["🏆 Tabulka", "📅 Základní skupiny", "🔥 Play-off", "🔮 Dlouhodobé", "✍️ Můj Tip"])

with tabs[0]:
    ranking = []
    for p in PLAYERS:
        total = sum(calc_pts(TIPS.get(p, {}).get(m['id']), m['res']) for m in MATCHES if m['res'])
        hits = sum(1 for m in MATCHES if m['res'] and calc_pts(TIPS.get(p, {}).get(m['id']), m['res']) >= 3)
        ranking.append({"Hráč": p, "Body": total, "Přesné trefy": hits})
    st.table(pd.DataFrame(ranking).sort_values(["Body", "Přesné trefy"], ascending=False).reset_index(drop=True))

with tabs[1]:
    for m in MATCHES:
        res = m['res'] or "?:?"
        # HTML pro jeden zápas
        html = f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="text-align:center; width:30%;"><span style="font-size:2.5rem;">{FLAGS.get(m['home'])}</span><div class="team-name">{m['home']}</div></div>
                <div class="score-badge">{res}</div>
                <div style="text-align:center; width:30%;"><span style="font-size:2.5rem;">{FLAGS.get(m['away'])}</span><div class="team-name">{m['away']}</div></div>
            </div>
            <div class="tip-grid">
        """
        for p in PLAYERS:
            tip_raw = TIPS.get(p, {}).get(m['id'])
            if not tip_raw: continue
            tip = tip_raw[0] if isinstance(tip_raw, tuple) else tip_raw
            banker = tip_raw[1] if isinstance(tip_raw, tuple) else False
            pts = calc_pts(tip_raw, m['res'])
            
            css = ""
            if m['res']:
                if pts >= 3: css = "res-3"
                elif pts >= 1: css = "res-1"
                else: css = "res-0"
            
            b_tag = '<div class="banker-icon">🃏 BANKER</div>' if banker else ""
            pts_tag = f'<div style="font-weight:bold; font-size:0.8rem;">{pts}b</div>' if m['res'] else ""
            
            html += f"""
            <div class="tip-box {css}">
                {b_tag}
                <div style="font-size:0.7rem; color:#555;">{p}</div>
                <div style="font-weight:bold;">{tip}</div>
                {pts_tag}
            </div>
            """
        html += "</div></div>"
        st.markdown(html, unsafe_allow_html=True)

with tabs[2]:
    for p in PLAYOFF_BRACKET:
        st.markdown(f"""
        <div class="match-card" style="border-left: 8px solid #ffcc00;">
            <div style="text-align:center; font-weight:bold; color:#555; margin-bottom:10px;">{p['r']}</div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="text-align:center; width:35%;"><span style="font-size:2rem;">{FLAGS.get(p['h'],'🏒')}</span><div class="team-name">{p['h']}</div></div>
                <div style="font-size:1.5rem; font-weight:bold; color:#ccc;">VS</div>
                <div style="text-align:center; width:35%;"><span style="font-size:2rem;">{FLAGS.get(p['a'],'🏒')}</span><div class="team-name">{p['a']}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tabs[3]:
    st.dataframe(pd.DataFrame(PRE_DATA), use_container_width=True, hide_index=True)

with tabs[4]:
    st.subheader("✍️ Generátor tipů na Play-off")
    name = st.selectbox("Vyber své jméno", PLAYERS)
    user_tips = {}
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Osmifinále**")
        for m in PLAYOFF_BRACKET[:4]:
            user_tips[m['h']] = st.text_input(f"{m['h']} - {m['a']}", key=m['id'], placeholder="např. 3:1")
    with col2:
        st.markdown("**Čtvrtfinále**")
        for m in PLAYOFF_BRACKET[4:]:
            user_tips[m['h']] = st.text_input(f"{m['h']} - {m['a']}", key=m['id'], placeholder="např. 2:4")
    
    if st.button("Zobrazit náhled mých tipů"):
        st.code(f"Hráč: {name}\n" + "\n".join([f"{k}: {v}" for k, v in user_tips.items() if v]))
