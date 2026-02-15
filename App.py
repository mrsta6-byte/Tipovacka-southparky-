import streamlit as st
import pandas as pd

# --- KONFIGURACE ---
st.set_page_config(page_title="ZOH 2026 - Tipovačka PRO", page_icon="🏒", layout="wide")

# --- DESIGN (Všechny styly v jednom bloku) ---
st.markdown("""
<style>
    .match-card { background: white; border-radius: 15px; padding: 25px; margin-bottom: 25px; border-left: 10px solid #c8102e; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: black; }
    .score-badge { font-size: 2.5rem; font-weight: 900; background: #2b2d42; padding: 10px 30px; border-radius: 12px; color: #edf2f4; border: 2px solid #8d99ae; }
    .flag { font-size: 3.5rem; display: block; margin-bottom: 10px; }
    .team-name { font-weight: 800; font-size: 1.3rem; text-transform: uppercase; letter-spacing: 1px; }
    .tip-box { border-radius: 10px; padding: 10px; text-align: center; margin: 5px; border: 2px solid #edf2f4; min-width: 95px; position: relative; display: inline-block; vertical-align: top; }
    .banker-label { color: white; background: #d90429; font-size: 0.65rem; padding: 2px 6px; border-radius: 5px; position: absolute; top: -12px; right: 8px; font-weight: 900; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
    .pts-3 { background-color: #d8f3dc; border-color: #2d6a4f; color: #1b4332; }
    .pts-1 { background-color: #fff3b0; border-color: #f9c74f; color: #5e503f; }
    .pts-0 { background-color: #fbc4ab; border-color: #f08080; color: #6d1a1a; opacity: 0.8; }
</style>
""", unsafe_allow_html=True)

# --- DATA: ZÁPASY (Podle tvého posledního souboru) ---
MATCHES = [
    {"id": "M1", "date": "11.02. 16:40", "home": "Slovensko", "away": "Finsko", "res": "4:1"},
    {"id": "M2", "date": "11.02. 21:10", "home": "Švédsko", "away": "Itálie", "res": "5:2"},
    {"id": "M3", "date": "12.02. 12:10", "home": "Švýcarsko", "away": "Francie", "res": "4:0"},
    {"id": "M4", "date": "12.02. 16:40", "home": "Česko", "away": "Kanada", "res": "0:5"},
    {"id": "M5", "date": "12.02. 21:10", "home": "Lotyšsko", "away": "USA", "res": "1:5"},
    {"id": "M6", "date": "12.02. 21:10", "home": "Německo", "away": "Dánsko", "res": "3:1"},
    {"id": "M7", "date": "13.02. 12:10", "home": "Finsko", "away": "Švédsko", "res": "4:1"},
    {"id": "M8", "date": "13.02. 12:10", "home": "Itálie", "away": "Slovensko", "res": "2:3"},
    {"id": "M9", "date": "13.02. 16:40", "home": "Francie", "away": "Česko", "res": "3:6"},
    {"id": "M10", "date": "13.02. 21:20", "home": "Kanada", "away": "Švýcarsko", "res": "5:1"},
    {"id": "M11", "date": "14.02. 12:10", "home": "Německo", "away": "Lotyšsko", "res": "3:4"},
    {"id": "M12", "date": "14.02. 12:10", "home": "Švédsko", "away": "Slovensko", "res": "5:3"},
    {"id": "M13", "date": "14.02. 16:40", "home": "Finsko", "away": "Itálie", "res": "11:0"},
    {"id": "M14", "date": "14.02. 21:10", "home": "USA", "away": "Dánsko", "res": "6:3"},
    {"id": "M15", "date": "15.02. 12:10", "home": "Švýcarsko", "away": "Česko", "res": "3:3"},
    {"id": "M16", "date": "15.02. 16:40", "home": "Kanada", "away": "Francie", "res": None},
    {"id": "M17", "date": "15.02. 19:10", "home": "Dánsko", "away": "Lotyšsko", "res": None},
    {"id": "M18", "date": "15.02. 21:10", "home": "USA", "away": "Německo", "res": None},
]

# --- DATA: TIPY (Zkontrolováno a opraveno: Víťa M5 = 2:6) ---
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
    'Alesh': {}, 'Cigi': {}, 'Fany': {}
}

# --- DATA: PŘED TURNAJEM (Kompletní) ---
PRE_DATA = [
    {'Hráč': 'Aďas', 'Vítěz': '🇨🇦 Kanada', '2.': '🇨🇿 Česko', '3.': '🇸🇪 Švédsko', '4.': '🇨🇭 Švýcarsko', 'Střelec': 'MacKinnon', 'Nahrávač': 'Konecny', 'Brankář': 'Vladař', 'MVP': 'MacKinnon'},
    {'Hráč': 'Cigi ml.', 'Vítěz': '🇨🇦 Kanada', '2.': '🇸🇪 Švédsko', '3.': '🇺🇸 USA', '4.': '🇫🇮 Finsko', 'Střelec': 'Celebriny', 'Nahrávač': 'McDavid', 'Brankář': 'Thompson ', 'MVP': 'McDavid'},
    {'Hráč': 'Mršťa', 'Vítěz': '🇨🇦 Kanada', '2.': '🇸🇪 Švédsko ', '3.': '🇨🇿 Česko ', '4.': '🇨🇭 Švýcarsko ', 'Střelec': 'Pastrňák', 'Nahrávač': 'Crosby', 'Brankář': 'Genoni', 'MVP': 'Crosby'},
    {'Hráč': 'Víťa', 'Vítěz': '🇨🇦 Kanada', '2.': '🇺🇸 USA', '3.': '🇨🇿 Česko ', '4.': '🇸🇪 Švédsko', 'Střelec': 'Matthews', 'Nahrávač': 'McDavid', 'Brankář': 'Juuse Saros', 'MVP': 'Raymond'},
    {'Hráč': 'Fany', 'Vítěz': '🇨🇭 Švýcarsko ', '2.': '🇸🇪 Švédsko ', '3.': '🇫🇮 Finsko ', '4.': '🇨🇿 Česko ', 'Střelec': 'Petterson', 'Nahrávač': 'Ehlers', 'Brankář': 'Binnington', 'MVP': 'Josi'},
]

PLAYERS = sorted(['Aďas', 'Moli', 'Cigi', 'Cigi ml.', 'Mršťa', 'Víťa', 'Alesh', 'Fany'])
FLAGS = {"Česko": "🇨🇿", "Kanada": "🇨🇦", "Slovensko": "🇸🇰", "Finsko": "🇫🇮", "Švédsko": "🇸🇪", "Itálie": "🇮🇹", "USA": "🇺🇸", "Německo": "🇩🇪", "Lotyšsko": "🇱🇻", "Francie": "🇫🇷", "Dánsko": "🇩🇰", "Švýcarsko": "🇨🇭"}

# --- POMOCNÁ LOGIKA ---
def get_points(tip, res, banker=False):
    if not tip or not res: return 0
    try:
        th, ta = map(int, tip.split(":"))
        rh, ra = map(int, res.split(":"))
        pts = 0
        if th == rh and ta == ra: pts = 3
        elif (th > ta and rh > ra) or (th < ta and rh < ra) or (th == ta and rh == ra): pts = 1
        return pts * 2 if banker else pts
    except: return 0

# --- APLIKACE ---
st.title("🏒 ZOH 2026 - TIPY")

tab1, tab2, tab3 = st.tabs(["🏆 ŽEBŘÍČEK", "📊 ZÁPASY", "🔮 PŘED TURNAJEM"])

with tab1:
    ranking = []
    for p in PLAYERS:
        pts = sum(get_points(TIPS.get(p, {}).get(m['id'], {}).get('t'), m['res'], TIPS.get(p, {}).get(m['id'], {}).get('b')) for m in MATCHES if m['res'])
        hits = sum(1 for m in MATCHES if m['res'] and get_points(TIPS.get(p, {}).get(m['id'], {}).get('t'), m['res']) >= 3)
        ranking.append({"Hráč": p, "Body": pts, "Přesné trefy": hits})
    df = pd.DataFrame(ranking).sort_values(["Body", "Přesné trefy"], ascending=False).reset_index(drop=True)
    st.table(df)

with tab2:
    for m in MATCHES:
        res = m['res'] or "?:?"
        # Skládáme celý HTML blok pro zápas
        match_html = f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-around; align-items:center; text-align:center;">
                <div style="width:30%;"><span class="flag">{FLAGS.get(m['home'], '')}</span><span class="team-name">{m['home']}</span></div>
                <div class="score-badge">{res}</div>
                <div style="width:30%;"><span class="flag">{FLAGS.get(m['away'], '')}</span><span class="team-name">{m['away']}</span></div>
            </div>
            <div style="display:flex; flex-wrap:wrap; justify-content:center; margin-top:20px;">
        """
        
        for p in PLAYERS:
            tip_data = TIPS.get(p, {}).get(m['id'], {})
            tip = tip_data.get('t', '-')
            banker = tip_data.get('b', False)
            pts = get_points(tip, m['res'], banker)
            
            css = ""
            if m['res']:
                if (pts == 3 or (banker and pts == 6)): css = "pts-3"
                elif pts >= 1: css = "pts-1"
                else: css = "pts-0"
            
            b_tag = '<div class="banker-label">🃏 BANKER</div>' if banker else ""
            pts_display = f'<div style="font-size:0.8rem; font-weight:bold; margin-top:3px;">{pts}b</div>' if m['res'] else ''
            
            match_html += f"""
                <div class="tip-box {css}">
                    {b_tag}
                    <div style="font-size:0.75rem; color:#4a4e69; font-weight:bold;">{p}</div>
                    <div style="font-weight:900; font-size:1.2rem;">{tip}</div>
                    {pts_display}
                </div>
            """
            
        match_html += "</div></div>"
        st.markdown(match_html, unsafe_allow_html=True)

with tab3:
    st.markdown("### 🔮 Tipy na celkové umístění a hráče")
    st.dataframe(pd.DataFrame(PRE_DATA), use_container_width=True, hide_index=True)
