import streamlit as st
import pandas as pd

# --- KONFIGURACE ---
st.set_page_config(page_title="ZOH 2026 - Tipovačka PRO", page_icon="🏒", layout="wide")

# --- KOMPLETNÍ CSS STYLY ---
st.markdown("""
<style>
    .match-container {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 10px solid #c8102e;
        color: #1a1a1a;
    }
    .match-header {
        display: flex;
        justify-content: space-around;
        align-items: center;
        text-align: center;
        border-bottom: 2px solid #f0f2f6;
        padding-bottom: 15px;
        margin-bottom: 15px;
    }
    .team-box { width: 30%; }
    .score-badge {
        font-size: 2.2rem;
        font-weight: 900;
        background: #2b2d42;
        padding: 8px 25px;
        border-radius: 12px;
        color: #edf2f4;
        min-width: 120px;
    }
    .flag { font-size: 3rem; display: block; }
    .team-name { font-weight: 800; font-size: 1.2rem; text-transform: uppercase; }
    .tips-grid {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
    }
    .tip-card {
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        border: 1px solid #ddd;
        min-width: 90px;
        position: relative;
    }
    .banker-label {
        background: #d90429;
        color: white;
        font-size: 0.6rem;
        padding: 2px 5px;
        border-radius: 4px;
        position: absolute;
        top: -10px;
        right: 5px;
        font-weight: bold;
    }
    .pts-3 { background-color: #d8f3dc !important; border-color: #2d6a4f !important; color: #1b4332 !important; }
    .pts-1 { background-color: #fff3b0 !important; border-color: #f9c74f !important; color: #5e503f !important; }
    .pts-0 { background-color: #fbc4ab !important; border-color: #f08080 !important; color: #6d1a1a !important; }
</style>
""", unsafe_allow_html=True)

# --- DATA ---
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
    {"id": "M16", "date": "15.02.", "home": "Kanada", "away": "Francie", "res": None},
    {"id": "M17", "date": "15.02.", "home": "Dánsko", "away": "Lotyšsko", "res": None},
    {"id": "M18", "date": "15.02.", "home": "USA", "away": "Německo", "res": None},
]

TIPS = {
    'Aďas': {
        'M1': {'t': '1:3', 'b': False}, 'M2': {'t': '6:1', 'b': False}, 'M3': {'t': '6:2', 'b': False}, 'M4': {'t': '2:4', 'b': False}, 'M5': {'t': '2:3', 'b': False}, 'M6': {'t': '4:3', 'b': False}, 'M7': {'t': '1:3', 'b': False}, 'M8': {'t': '2:4', 'b': False}, 'M9': {'t': '0:5', 'b': True}, 'M10': {'t': '3:1', 'b': False},
        'M11': {'t': '2:2', 'b': False}, 'M12': {'t': '5:1', 'b': True}, 'M13': {'t': '3:0', 'b': False}, 'M14': {'t': '5:2', 'b': False}, 'M15': {'t': '3:3', 'b': False}, 'M16': {'t': '8:0', 'b': False}, 'M17': {'t': '3:2', 'b': False}, 'M18': {'t': '2:1', 'b': False}
    },
    'Víťa': {
        'M1': {'t': '2:2', 'b': False}, 'M2': {'t': '4:0', 'b': False}, 'M3': {'t': '4:1', 'b': False}, 'M4': {'t': '1:4', 'b': False}, 'M5': {'t': '2:6', 'b': False}, 'M6': {'t': '3:2', 'b': False}, 'M7': {'t': '3:3', 'b': False}, 'M8': {'t': '3:4', 'b': False}, 'M9': {'t': '0:3', 'b': False}, 'M10': {'t': '4:2', 'b': False},
        'M11': {'t': '3:2', 'b': False}, 'M12': {'t': '4:0', 'b': False}, 'M13': {'t': '3:1', 'b': False}, 'M14': {'t': '6:1', 'b': False}, 'M15': {'t': '4:2', 'b': False}, 'M16': {'t': '5:0', 'b': False}, 'M17': {'t': '3:2', 'b': False}, 'M18': {'t': '4:3', 'b': False}
    },
    'Cigi ml.': {
        'M1': {'t': '2:4', 'b': False}, 'M2': {'t': '6:2', 'b': False}, 'M3': {'t': '3:1', 'b': False}, 'M4': {'t': '3:5', 'b': False}, 'M5': {'t': '1:4', 'b': False}, 'M6': {'t': '4:2', 'b': False}, 'M7': {'t': '2:3', 'b': False}, 'M8': {'t': '3:5', 'b': False}, 'M9': {'t': '1:4', 'b': False}, 'M10': {'t': '4:1', 'b': False},
        'M11': {'t': '3:3', 'b': False}, 'M12': {'t': '6:2', 'b': False}, 'M13': {'t': '5:0', 'b': False}, 'M14': {'t': '6:1', 'b': False}, 'M15': {'t': '4:5', 'b': False}, 'M16': {'t': '7:0', 'b': False}, 'M17': {'t': '4:2', 'b': False}, 'M18': {'t': '5:2', 'b': False}
    },
    'Mršťa': {
        'M1': {'t': '2:4', 'b': False}, 'M2': {'t': '7:1', 'b': False}, 'M3': {'t': '5:2', 'b': False}, 'M4': {'t': '2:5', 'b': False}, 'M5': {'t': '2:5', 'b': False}, 'M6': {'t': '5:3', 'b': False}, 'M7': {'t': '2:3', 'b': False}, 'M8': {'t': '1:5', 'b': False}, 'M9': {'t': '1:6', 'b': False}, 'M10': {'t': '4:2', 'b': False},
        'M11': {'t': '3:1', 'b': False}, 'M12': {'t': '7:3', 'b': False}, 'M13': {'t': '2:2', 'b': False}, 'M14': {'t': '4:0', 'b': True}, 'M15': {'t': '3:5', 'b': False}, 'M16': {'t': '9:1', 'b': False}, 'M17': {'t': '3:3', 'b': False}, 'M18': {'t': '5:4', 'b': False}
    },
    'Moli': {'M1': {'t': '1:5', 'b': False}, 'M2': {'t': '8:0', 'b': False}},
}

PRE_TIPS = [
    {'Hráč': 'Aďas', '🥇 Vítěz': 'Kanada', '🥈 2.': 'Česko', '🥉 3.': 'Švédsko', '🏅 4.': 'Švýcarsko', '🏒 Střelec': 'MacKinnon', '🍎 Nahrávač': 'Konecny', '🧱 Brankář': 'Vladař', '⭐ MVP': 'MacKinnon'},
    {'Hráč': 'Cigi ml.', '🥇 Vítěz': 'Kanada', '🥈 2.': 'Švédsko', '🥉 3.': 'USA', '🏅 4.': 'Finsko', '🏒 Střelec': 'Celebriny', '🍎 Nahrávač': 'McDavid', '🧱 Brankář': 'Thompson', '⭐ MVP': 'McDavid'},
    {'Hráč': 'Mršťa', '🥇 Vítěz': 'Kanada', '🥈 2.': 'Švédsko', '🥉 3.': 'Česko', '🏅 4.': 'Švýcarsko', '🏒 Střelec': 'Pastrňák', '🍎 Nahrávač': 'Crosby', '🧱 Brankář': 'Genoni', '⭐ MVP': 'Crosby'},
    {'Hráč': 'Víťa', '🥇 Vítěz': 'Kanada', '🥈 2.': 'USA', '🥉 3.': 'Česko', '🏅 4.': 'Švédsko', '🏒 Střelec': 'Matthews', '🍎 Nahrávač': 'McDavid', '🧱 Brankář': 'Juuse Saros', '⭐ MVP': 'Lukas Raymond'},
    {'Hráč': 'Fany', '🥇 Vítěz': 'Švýcarsko', '🥈 2.': 'Švédsko', '🥉 3.': 'Finsko', '🏅 4.': 'Česko', '🏒 Střelec': 'Petterson', '🍎 Nahrávač': 'Ehlers', '🧱 Brankář': 'Binnington', '⭐ MVP': 'Roman Josi'},
]

FLAGS = {"Slovensko": "🇸🇰", "Finsko": "🇫🇮", "Švédsko": "🇸🇪", "Itálie": "🇮🇹", "Švýcarsko": "🇨🇭", "Francie": "🇫🇷", "Česko": "🇨🇿", "Kanada": "🇨🇦", "Lotyšsko": "🇱🇻", "USA": "🇺🇸", "Německo": "🇩🇪", "Dánsko": "🇩🇰"}

def get_pts(tip, res, banker=False):
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
st.title("🏒 ZOH 2026 - TIPY")

tab1, tab2, tab3 = st.tabs(["🏆 ŽEBŘÍČEK", "📊 ZÁPASY", "🔮 PŘED TURNAJEM"])

with tab1:
    results = []
    players_list = sorted(list(set(list(TIPS.keys()) + [p['Hráč'] for p in PRE_TIPS])))
    for p in players_list:
        total = sum(get_pts(TIPS.get(p, {}).get(m['id'], {}).get('t'), m['res'], TIPS.get(p, {}).get(m['id'], {}).get('b')) for m in MATCHES if m['res'])
        hits = sum(1 for m in MATCHES if m['res'] and get_pts(TIPS.get(p, {}).get(m['id'], {}).get('t'), m['res']) >= 3)
        results.append({"Hráč": p, "Body": total, "Přesné trefy": hits})
    st.table(pd.DataFrame(results).sort_values(["Body", "Přesné trefy"], ascending=False))

with tab2:
    for m in MATCHES:
        res = m['res'] or "?:?"
        # Generujeme kompletní HTML pro jednu kartu zápasu
        match_html = f"""
        <div class="match-container">
            <div class="match-header">
                <div class="team-box"><span class="flag">{FLAGS.get(m['home'],'')}</span><div class="team-name">{m['home']}</div></div>
                <div><div style="color:gray; font-size:0.8rem; margin-bottom:5px;">{m['date']}</div><div class="score-badge">{res}</div></div>
                <div class="team-box"><span class="flag">{FLAGS.get(m['away'],'')}</span><div class="team-name">{m['away']}</div></div>
            </div>
            <div class="tips-grid">
        """
        for p in sorted(TIPS.keys()):
            tip_data = TIPS[p].get(m['id'], {})
            tip = tip_data.get('t', '-')
            banker = tip_data.get('b', False)
            pts = get_pts(tip, m['res'], banker)
            
            cls = ""
            if m['res']:
                if pts >= 3: cls = "pts-3"
                elif pts >= 1: cls = "pts-1"
                else: cls = "pts-0"
            
            b_icon = '<div class="banker-label">🃏 BANKER</div>' if banker else ""
            match_html += f"""
                <div class="tip-card {cls}">
                    {b_icon}
                    <div style="font-size:0.75rem; color:#666; font-weight:bold;">{p}</div>
                    <div style="font-weight:900; font-size:1.1rem;">{tip}</div>
                    {f'<div style="font-size:0.8rem; font-weight:bold; margin-top:2px;">{pts}b</div>' if m['res'] else ''}
                </div>
            """
        match_html += "</div></div>"
        st.markdown(match_html, unsafe_allow_html=True)

with tab3:
    st.dataframe(pd.DataFrame(PRE_TIPS), hide_index=True, use_container_width=True)
