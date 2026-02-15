import streamlit as st
import pandas as pd

# --- KONFIGURACE ---
st.set_page_config(page_title="ZOH 2026 - Tipovačka ELITE", page_icon="🏒", layout="wide")

# --- KOMPLETNÍ CSS STYLY ---
st.markdown("""
<style>
    .match-container { background: white; border-radius: 15px; padding: 20px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-left: 10px solid #c8102e; color: #1a1a1a; }
    .match-header { display: flex; justify-content: space-around; align-items: center; text-align: center; border-bottom: 2px solid #f0f2f6; padding-bottom: 15px; margin-bottom: 15px; }
    .score-badge { font-size: 2.2rem; font-weight: 900; background: #2b2d42; padding: 8px 25px; border-radius: 12px; color: #edf2f4; min-width: 120px; }
    .flag { font-size: 3rem; display: block; }
    .team-name { font-weight: 800; font-size: 1.2rem; text-transform: uppercase; }
    .tip-card { border-radius: 10px; padding: 10px; text-align: center; border: 1px solid #ddd; min-width: 95px; position: relative; display: inline-block; margin: 5px; }
    .banker-label { background: #d90429; color: white; font-size: 0.6rem; padding: 2px 5px; border-radius: 4px; position: absolute; top: -10px; right: 5px; font-weight: bold; }
    .pts-3 { background-color: #d8f3dc !important; border-color: #2d6a4f !important; color: #1b4332 !important; }
    .pts-1 { background-color: #fff3b0 !important; border-color: #f9c74f !important; color: #5e503f !important; }
    .pts-0 { background-color: #fbc4ab !important; border-color: #f08080 !important; color: #6d1a1a !important; }
</style>
""", unsafe_allow_html=True)

# --- DATA: ZÁKLADNÍ SKUPINY (Odehrané) ---
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

# --- DATA: NADCHÁZEJÍCÍ PLAY-OFF (Z internetu) ---
PLAYOFF_MATCHES = [
    {"id": "P1", "date": "Úterý 17.02. 12:10", "home": "Švýcarsko", "away": "Francie", "type": "Osmifinále"},
    {"id": "P2", "date": "Úterý 17.02. 12:10", "home": "Německo", "away": "Itálie", "type": "Osmifinále"},
    {"id": "P3", "date": "Úterý 17.02. 16:40", "home": "Česko", "away": "Lotyšsko", "type": "Osmifinále"},
    {"id": "P4", "date": "Úterý 17.02. 21:10", "home": "Švédsko", "away": "Dánsko", "type": "Osmifinále"},
    {"id": "P5", "date": "Středa 18.02. 12:10", "home": "Kanada", "away": "Vítěz P3", "type": "Čtvrtfinále"},
    {"id": "P6", "date": "Středa 18.02. 16:40", "home": "USA", "away": "Vítěz P4", "type": "Čtvrtfinále"},
]

# --- DATA: TIPY (Víťa M5 opraven na 2:6) ---
TIPS = {
    'Aďas': {'M1':'1:3', 'M2':'6:1', 'M3':'6:2', 'M4':'2:4', 'M5':'2:3', 'M6':'4:3', 'M12':'5:1', 'M15':'3:3', 'M9':'0:5'},
    'Víťa': {'M1':'2:2', 'M2':'4:0', 'M3':'4:1', 'M4':'1:4', 'M5':'2:6', 'M12':'4:0', 'M15':'4:2'},
    'Cigi ml.': {'M1':'2:4', 'M5':'1:4', 'M12':'6:2', 'M15':'4:5'},
    'Mršťa': {'M1':'2:4', 'M5':'2:5', 'M12':'7:3', 'M15':'3:5', 'M14':'4:0'},
}
# Bankeři (Příklad)
BANKERS = {'Aďas': ['M12', 'M9'], 'Mršťa': ['M14']}

# --- DATA: PŘED TURNAJEM ---
PRE_DATA = [
    {'Hráč': 'Aďas', 'Vítěz': '🇨🇦 Kanada', '2.': '🇨🇿 Česko', '3.': '🇸🇪 Švédsko', '4.': '🇨🇭 Švýcarsko', 'Střelec': 'MacKinnon', 'Nahrávač': 'Konecny', 'Brankář': 'Vladař', 'MVP': 'MacKinnon'},
    {'Hráč': 'Cigi ml.', 'Vítěz': '🇨🇦 Kanada', '2.': '🇸🇪 Švédsko', '3.': '🇺🇸 USA', '4.': '🇫🇮 Finsko', 'Střelec': 'Celebriny', 'Nahrávač': 'McDavid', 'Brankář': 'Thompson ', 'MVP': 'McDavid'},
    {'Hráč': 'Mršťa', 'Vítěz': '🇨🇦 Kanada', '2.': '🇸🇪 Švédsko ', '3.': '🇨🇿 Česko ', '4.': '🇨🇭 Švýcarsko ', 'Střelec': 'Pastrňák', 'Nahrávač': 'Crosby', 'Brankář': 'Genoni', 'MVP': 'Crosby'},
    {'Hráč': 'Víťa', 'Vítěz': '🇨🇦 Kanada', '2.': '🇺🇸 USA', '3.': '🇨🇿 Česko ', '4.': '🇸🇪 Švédsko', 'Střelec': 'Matthews', 'Nahrávač': 'McDavid', 'Brankář': 'Juuse Saros', 'MVP': 'Raymond'},
    {'Hráč': 'Fany', 'Vítěz': '🇨🇭 Švýcarsko ', '2.': '🇸🇪 Švédsko ', '3.': '🇫🇮 Finsko ', '4.': '🇨🇿 Česko ', 'Střelec': 'Petterson', 'Nahrávač': 'Ehlers', 'Brankář': 'Binnington', 'MVP': 'Josi'},
]

FLAGS = {"Slovensko": "🇸🇰", "Finsko": "🇫🇮", "Švédsko": "🇸🇪", "Itálie": "🇮🇹", "Švýcarsko": "🇨🇭", "Francie": "🇫🇷", "Česko": "🇨🇿", "Kanada": "🇨🇦", "Lotyšsko": "🇱🇻", "USA": "🇺🇸", "Německo": "🇩🇪", "Dánsko": "🇩🇰"}

def get_pts(tip, res, banker=False):
    if not tip or not res: return 0
    try:
        th, ta = map(int, tip.split(":"))
        rh, ra = map(int, res.split(":"))
        pts = 0
        if th == rh and ta == ra: pts = 3
        elif (th > ta and rh > ra) or (th < ta and rh < ra) or (th == ta and rh == ra): pts = 1
        return pts * 2 if banker else pts
    except: return 0

# --- APP ---
st.sidebar.title("🩺 Zdravotní okénko")
st.sidebar.warning("Nezapomeň na purinovou dietu! 🥤 K hokeji dnes raději vodu nebo čaj, ať tě zítra netrápí klouby.")

st.title("🏒 ZOH 2026 - ELITNÍ TIPOVAČKA")

tabs = st.tabs(["🏆 ŽEBŘÍČEK", "📊 ZÁKLADNÍ SKUPINY", "🔥 PLAY-OFF", "🔮 PŘED TURNAJEM"])

with tabs[0]:
    st.subheader("Aktuální pořadí skupiny")
    ranking = []
    players = sorted(list(set(list(TIPS.keys()) + [p['Hráč'] for p in PRE_DATA])))
    for p in players:
        pts = sum(get_pts(TIPS.get(p, {}).get(m['id']), m['res'], m['id'] in BANKERS.get(p, [])) for m in MATCHES if m['res'])
        ranking.append({"Hráč": p, "Body": pts})
    st.table(pd.DataFrame(ranking).sort_values("Body", ascending=False))

with tabs[1]:
    for m in MATCHES:
        res = m['res'] or "?:?"
        html = f'<div class="match-container"><div class="match-header"><div class="team-box"><span class="flag">{FLAGS.get(m["home"],"")}</span><div class="team-name">{m["home"]}</div></div><div class="score-badge">{res}</div><div class="team-box"><span class="flag">{FLAGS.get(m["away"],"")}</span><div class="team-name">{m["away"]}</div></div></div><div class="tips-grid">'
        for p in players:
            tip = TIPS.get(p, {}).get(m['id'], '-')
            banker = m['id'] in BANKERS.get(p, [])
            pts = get_pts(tip, m['res'], banker)
            cls = "pts-3" if pts >= 3 else ("pts-1" if pts >= 1 else "pts-0") if m['res'] else ""
            html += f'<div class="tip-card {cls}">{"<div class='banker-label'>🃏 BANKER</div>" if banker else ""}<div style="font-size:0.7rem;">{p}</div><b>{tip}</b>{f"<div>{pts}b</div>" if m["res"] else ""}</div>'
        html += '</div></div>'
        st.markdown(html, unsafe_allow_html=True)

with tabs[2]:
    st.info("Zde jsou zápasy play-off. Tipujte včas!")
    for m in PLAYOFF_MATCHES:
        html = f'<div class="match-container" style="border-left-color: #ffcc00;"><div class="match-header"><div class="team-box"><span class="flag">{FLAGS.get(m["home"],"🏒")}</span><div class="team-name">{m["home"]}</div></div><div class="score-badge">VS</div><div class="team-box"><span class="flag">{FLAGS.get(m["away"],"🏒")}</span><div class="team-name">{m["away"]}</div></div></div><div style="text-align:center; color:gray;">{m["type"]} | {m["date"]}</div></div>'
        st.markdown(html, unsafe_allow_html=True)

with tabs[3]:
    st.dataframe(pd.DataFrame(PRE_DATA), hide_index=True)
