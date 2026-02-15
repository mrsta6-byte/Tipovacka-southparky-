import streamlit as st
import pandas as pd

# --- KONFIGURACE ---
st.set_page_config(page_title="ZOH 2026 - Tipovačka PRO", page_icon="🏒", layout="wide")

# --- DESIGN ---
st.markdown("""
<style>
    .match-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        border-left: 8px solid #003087;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #1a1a1a;
    }
    .score-badge {
        font-size: 2rem;
        font-weight: 800;
        background: #1a1a1a;
        padding: 5px 20px;
        border-radius: 8px;
        color: white;
        min-width: 90px;
        text-align: center;
    }
    .flag { font-size: 2.5rem; display: block; margin-bottom: 5px; }
    .team-name { font-weight: 700; font-size: 1.1rem; text-transform: uppercase; }
    
    /* Grid pro tipy */
    .tips-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
        gap: 8px;
        margin-top: 15px;
        border-top: 1px solid #eee;
        padding-top: 10px;
    }
    
    .tip-box {
        border-radius: 6px;
        padding: 5px;
        text-align: center;
        border: 1px solid #ddd;
        background: #f8f9fa;
        position: relative;
    }
    
    .banker-label {
        background: #d90429;
        color: white;
        font-size: 0.6rem;
        padding: 1px 4px;
        border-radius: 3px;
        position: absolute;
        top: -8px;
        right: 2px;
        font-weight: bold;
    }
    
    .pts-3 { background-color: #d1e7dd !important; border-color: #badbcc !important; color: #0f5132 !important; }
    .pts-1 { background-color: #fff3cd !important; border-color: #ffecb5 !important; color: #664d03 !important; }
    .pts-0 { background-color: #f8d7da !important; border-color: #f5c2c7 !important; color: #842029 !important; }
</style>
""", unsafe_allow_html=True)

# --- 1. DATA: ZÁPASY (Opravené výsledky) ---
MATCHES = [
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

# --- 2. DATA: PLAY-OFF (Pavouk) ---
PLAYOFF = [
    {"id": "OF1", "round": "Osmifinále", "date": "17.02.", "home": "Česko", "away": "Dánsko"},
    {"id": "OF2", "round": "Osmifinále", "date": "17.02.", "home": "Švédsko", "away": "Lotyšsko"},
    {"id": "OF3", "round": "Osmifinále", "date": "17.02.", "home": "Švýcarsko", "away": "Francie"},
    {"id": "OF4", "round": "Osmifinále", "date": "17.02.", "home": "Německo", "away": "Itálie"},
    {"id": "QF1", "round": "Čtvrtfinále", "date": "18.02.", "home": "Kanada", "away": "vítěz OF4"},
    {"id": "QF2", "round": "Čtvrtfinále", "date": "18.02.", "home": "USA", "away": "vítěz OF3"},
    {"id": "QF3", "round": "Čtvrtfinále", "date": "18.02.", "home": "Finsko", "away": "vítěz OF2"},
    {"id": "QF4", "round": "Čtvrtfinále", "date": "18.02.", "home": "Slovensko", "away": "vítěz OF1"},
]

# --- 3. DATA: TIPY (Znovu zkontrolováno) ---
TIPS = {
    'Aďas': {'M1':{'t':'1:3','b':False},'M2':{'t':'6:1','b':False},'M3':{'t':'6:2','b':False},'M4':{'t':'2:4','b':False},'M5':{'t':'2:3','b':False},'M6':{'t':'4:3','b':False},'M7':{'t':'1:3','b':False},'M8':{'t':'2:4','b':False},'M9':{'t':'0:5','b':True},'M10':{'t':'3:1','b':False},'M11':{'t':'2:2','b':False},'M12':{'t':'5:1','b':True},'M13':{'t':'3:0','b':False},'M14':{'t':'5:2','b':False},'M15':{'t':'3:3','b':False},'M16':{'t':'8:0','b':False},'M17':{'t':'3:2','b':False},'M18':{'t':'2:1','b':False}},
    'Víťa': {'M1':{'t':'2:2','b':False},'M2':{'t':'4:0','b':False},'M3':{'t':'4:1','b':False},'M4':{'t':'1:4','b':False},'M5':{'t':'2:6','b':False},'M6':{'t':'3:2','b':False},'M7':{'t':'3:3','b':False},'M8':{'t':'3:4','b':False},'M9':{'t':'0:3','b':False},'M10':{'t':'4:2','b':False},'M11':{'t':'3:2','b':False},'M12':{'t':'4:0','b':False},'M13':{'t':'3:1','b':False},'M14':{'t':'6:1','b':False},'M15':{'t':'4:2','b':False},'M16':{'t':'5:0','b':False},'M17':{'t':'3:2','b':False},'M18':{'t':'4:3','b':False}},
    'Cigi ml.': {'M1':{'t':'2:4','b':False},'M2':{'t':'6:2','b':False},'M3':{'t':'3:1','b':False},'M4':{'t':'3:5','b':False},'M5':{'t':'1:4','b':False},'M6':{'t':'4:2','b':False},'M7':{'t':'2:3','b':False},'M8':{'t':'3:5','b':False},'M9':{'t':'1:4','b':False},'M10':{'t':'4:1','b':False},'M11':{'t':'3:3','b':False},'M12':{'t':'6:2','b':False},'M13':{'t':'5:0','b':False},'M14':{'t':'6:1','b':False},'M15':{'t':'4:5','b':False},'M16':{'t':'7:0','b':False},'M17':{'t':'4:2','b':False},'M18':{'t':'5:2','b':False}},
    'Mršťa': {'M1':{'t':'2:4','b':False},'M2':{'t':'7:1','b':False},'M3':{'t':'5:2','b':False},'M4':{'t':'2:5','b':False},'M5':{'t':'2:5','b':False},'M6':{'t':'5:3','b':False},'M7':{'t':'2:3','b':False},'M8':{'t':'1:5','b':False},'M9':{'t':'1:6','b':False},'M10':{'t':'4:2','b':False},'M11':{'t':'3:1','b':False},'M12':{'t':'7:3','b':False},'M13':{'t':'2:2','b':False},'M14':{'t':'4:0','b':True},'M15':{'t':'3:5','b':False},'M16':{'t':'9:1','b':False},'M17':{'t':'3:3','b':False},'M18':{'t':'5:4','b':False}},
    'Moli': {'M1':{'t':'1:5','b':False},'M2':{'t':'8:0','b':False}},
    'Cigi': {}, 'Alesh': {}, 'Fany': {}
}

# --- 4. DATA: PŘED TURNAJEM ---
PRE_DATA = [
    {'Hráč': 'Aďas', '🥇 Vítěz': 'Kanada', '🥈 2.místo': 'Česko', '🥉 3.místo': 'Švédsko', '🏅 4.místo': 'Švýcarsko', '🏒 Střelec': 'MacKinnon', '🍎 Nahrávač': 'Konecny', '🧱 Brankář': 'Vladař', '⭐ MVP': 'MacKinnon'},
    {'Hráč': 'Cigi ml.', '🥇 Vítěz': 'Kanada', '🥈 2.místo': 'Švédsko', '🥉 3.místo': 'USA', '🏅 4.místo': 'Finsko', '🏒 Střelec': 'Celebriny', '🍎 Nahrávač': 'McDavid', '🧱 Brankář': 'Thompson ', '⭐ MVP': 'McDavid'},
    {'Hráč': 'Mršťa', '🥇 Vítěz': 'Kanada', '🥈 2.místo': 'Švédsko ', '🥉 3.místo': 'Česko ', '🏅 4.místo': 'Švýcarsko ', '🏒 Střelec': 'Pastrňák', '🍎 Nahrávač': 'Crosby', '🧱 Brankář': 'Genoni', '⭐ MVP': 'Crosby'},
    {'Hráč': 'Víťa', '🥇 Vítěz': 'Kanada', '🥈 2.místo': 'USA', '🥉 3.místo': 'Česko ', '🏅 4.místo': 'Švédsko', '🏒 Střelec': 'Matthews', '🍎 Nahrávač': 'McDavid', '🧱 Brankář': 'Juuse Saros', '⭐ MVP': 'Raymond'},
    {'Hráč': 'Fany', '🥇 Vítěz': 'Švýcarsko ', '🥈 2.místo': 'Švédsko ', '🥉 3.místo': 'Finsko ', '🏅 4.místo': 'Česko ', '🏒 Střelec': 'Petterson', '🍎 Nahrávač': 'Ehlers', '🧱 Brankář': 'Binnington', '⭐ MVP': 'Josi'},
]

FLAGS = {"Česko": "🇨🇿", "Kanada": "🇨🇦", "Slovensko": "🇸🇰", "Finsko": "🇫🇮", "Švédsko": "🇸🇪", "Itálie": "🇮🇹", "USA": "🇺🇸", "Německo": "🇩🇪", "Lotyšsko": "🇱🇻", "Francie": "🇫🇷", "Dánsko": "🇩🇰", "Švýcarsko": "🇨🇭"}
PLAYERS = sorted(['Aďas', 'Víťa', 'Cigi ml.', 'Mršťa', 'Moli', 'Cigi', 'Alesh', 'Fany'])

# --- LOGIKA ---
def get_points(tip, res, banker=False):
    if not tip or not res or tip == "-": return 0
    try:
        th, ta = map(int, tip.split(":"))
        rh, ra = map(int, res.split(":"))
        pts = 0
        if th == rh and ta == ra: pts = 3
        elif (th > ta and rh > ra) or (th < ta and rh < ra) or (th == ta and rh == ra): pts = 1
        return pts * 2 if banker else pts
    except: return 0

# --- APP ---
st.title("🏒 ZOH 2026 - CENTRÁLA")

tabs = st.tabs(["🏆 TABULKA", "📊 SKUPINY", "🔥 PAVOUK", "🔮 DLOUHODOBÉ", "✍️ MŮJ TIP"])

# 1. TABULKA
with tabs[0]:
    ranking = []
    for p in PLAYERS:
        pts = 0
        hits = 0
        for m in MATCHES:
            t = TIPS.get(p, {}).get(m['id'], {}).get('t')
            b = TIPS.get(p, {}).get(m['id'], {}).get('b', False)
            p_match = get_points(t, m['res'], b)
            pts += p_match
            if m['res'] and get_points(t, m['res']) >= 3: hits += 1
        ranking.append({"Hráč": p, "Body": pts, "Přesné trefy": hits})
    st.table(pd.DataFrame(ranking).sort_values(["Body", "Přesné trefy"], ascending=False).reset_index(drop=True))

# 2. SKUPINY (Oprava HTML)
with tabs[1]:
    for m in MATCHES:
        res = m['res'] or "?:?"
        # Generujeme čistý HTML blok
        html_content = f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="text-align:center; width:30%;"><span class="flag">{FLAGS.get(m['home'],'')}</span><div class="team-name">{m['home']}</div></div>
                <div class="score-badge">{res}</div>
                <div style="text-align:center; width:30%;"><span class="flag">{FLAGS.get(m['away'],'')}</span><div class="team-name">{m['away']}</div></div>
            </div>
            <div class="tips-grid">
        """
        for p in PLAYERS:
            t_data = TIPS.get(p, {}).get(m['id'], {})
            tip = t_data.get('t', '-')
            banker = t_data.get('b', False)
            pts = get_points(tip, m['res'], banker)
            
            css = ""
            if m['res'] and tip != "-":
                if pts >= 3: css = "pts-3"
                elif pts == 1: css = "pts-1"
                else: css = "pts-0"
            
            b_label = '<span class="banker-label">🃏</span>' if banker else ''
            pts_label = f'<div style="font-size:0.8rem; font-weight:bold;">{pts}b</div>' if m['res'] else ''
            
            if tip != "-":
                html_content += f"""
                <div class="tip-box {css}">
                    {b_label}
                    <div style="font-size:0.7rem; color:#555;">{p}</div>
                    <div style="font-weight:bold; font-size:1.1rem;">{tip}</div>
                    {pts_label}
                </div>
                """
        html_content += "</div></div>"
        st.markdown(html_content, unsafe_allow_html=True)

# 3. PAVOUK PLAY-OFF
with tabs[2]:
    for p in PLAYOFF:
        st.markdown(f"""
        <div class="match-card" style="border-left-color: #ffcc00;">
            <div style="text-align:center; font-weight:bold; color:#003087; margin-bottom:10px;">{p['round']} • {p['date']}</div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="text-align:center; width:35%;"><span class="flag">{FLAGS.get(p['home'],'🏒')}</span><div class="team-name">{p['home']}</div></div>
                <div style="font-size:1.5rem; font-weight:bold; color:#aaa;">VS</div>
                <div style="text-align:center; width:35%;"><span class="flag">{FLAGS.get(p['away'],'🏒')}</span><div class="team-name">{p['away']}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 4. DLOUHODOBÉ
with tabs[3]:
    st.dataframe(pd.DataFrame(PRE_DATA), use_container_width=True, hide_index=True)

# 5. MŮJ TIP (Generátor)
with tabs[4]:
    st.subheader("✍️ Zadej své tipy na Play-off")
    me = st.selectbox("Kdo jsi?", PLAYERS)
    
    col1, col2 = st.columns(2)
    my_tips = {}
    with col1:
        st.markdown("**Osmifinále**")
        for m in PLAYOFF[:4]:
            my_tips[m['id']] = st.text_input(f"{m['home']} vs {m['away']}", key=f"tip_{m['id']}")
            
    with col2:
        st.markdown("**Čtvrtfinále**")
        for m in PLAYOFF[4:]:
            my_tips[m['id']] = st.text_input(f"{m['home']} vs {m['away']}", key=f"tip_{m['id']}")

    if st.button("Generovat náhled"):
        st.success(f"Tipy hráče: {me}")
        for m in PLAYOFF:
            if m['id'] in my_tips and my_tips[m['id']]:
                st.write(f"**{m['home']} vs {m['away']}** -> {my_tips[m['id']]}")
