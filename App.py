import streamlit as st
import pandas as pd

# --- KONFIGURACE ---
st.set_page_config(page_title="ZOH 2026 - Oficiální Tipovačka", page_icon="🏒", layout="wide")

# --- DESIGN ---
st.markdown("""
<style>
    .match-card { background: white; border-radius: 15px; padding: 20px; margin-bottom: 15px; border-left: 10px solid #003399; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: black; }
    .score-badge { font-size: 2rem; font-weight: 900; background: #f0f2f6; padding: 5px 20px; border-radius: 10px; color: #1a1a1a; border: 1px solid #ddd; }
    .flag { font-size: 3rem; display: block; margin-bottom: 5px; }
    .team-name { font-weight: 800; font-size: 1.1rem; text-transform: uppercase; }
    .tip-box { border-radius: 8px; padding: 8px; text-align: center; margin: 3px; border: 1px solid #eee; min-width: 85px; position: relative; }
    .banker-tag { color: white; background: #d7141a; font-size: 0.6rem; padding: 1px 4px; border-radius: 4px; position: absolute; top: -8px; right: 5px; font-weight: bold; }
    .pts-3 { background-color: #d4edda; border-color: #28a745; color: #155724; font-weight: bold; }
    .pts-1 { background-color: #fff3cd; border-color: #ffc107; color: #856404; }
    .pts-0 { background-color: #f8d7da; border-color: #dc3545; color: #721c24; opacity: 0.8; }
</style>
""", unsafe_allow_html=True)

# --- DATA: ZÁPASY ---
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

# --- DATA: TIPY (Přesně podle tvých souborů) ---
TIPS = {
    'Aďas': {
        'M1': {'t': '1:3', 'b': False}, 'M2': {'t': '6:1', 'b': False}, 'M3': {'t': '6:2', 'b': False}, 'M4': {'t': '2:4', 'b': False}, 'M5': {'t': '2:3', 'b': False}, 'M6': {'t': '4:3', 'b': False}, 'M7': {'t': '1:3', 'b': False}, 'M8': {'t': '2:4', 'b': False}, 'M9': {'t': '0:5', 'b': False}, 'M10': {'t': '3:1', 'b': False},
        'M11': {'t': '2:2', 'b': False}, 'M12': {'t': '5:1', 'b': True}, 'M13': {'t': '3:0', 'b': False}, 'M14': {'t': '5:2', 'b': False}, 'M15': {'t': '3:3', 'b': False}, 'M16': {'t': '8:0', 'b': False}, 'M17': {'t': '3:2', 'b': False}, 'M18': {'t': '2:1', 'b': False}
    },
    'Víťa': {
        'M1': {'t': '2:2', 'b': False}, 'M2': {'t': '4:0', 'b': False}, 'M3': {'t': '4:1', 'b': False}, 'M4': {'t': '1:4', 'b': False}, 'M5': {'t': '1:5', 'b': False}, 'M6': {'t': '3:2', 'b': False}, 'M7': {'t': '3:3', 'b': False}, 'M8': {'t': '3:4', 'b': False}, 'M9': {'t': '0:3', 'b': False}, 'M10': {'t': '4:2', 'b': False},
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
    {'Hráč': 'Aďas', 'Vítěz': '🇨🇦 Kanada', '2. místo': '🇨🇿 Česko', '3. místo': '🇸🇪 Švédsko', '4. místo': '🇨🇭 Švýcarsko', 'Střelec': 'MacKinnon', 'Nahrávač': 'Konecny', 'Brankář': 'Vladař', 'MVP': 'MacKinnon'},
    {'Hráč': 'Cigi ml.', 'Vítěz': '🇨🇦 Kanada', '2. místo': '🇸🇪 Švédsko', '3. místo': '🇺🇸 USA', '4. místo': '🇫🇮 Finsko', 'Střelec': 'Celebriny', 'Nahrávač': 'McDavid', 'Brankář': 'Thompson', 'MVP': 'McDavid'},
    {'Hráč': 'Mršťa', 'Vítěz': '🇨🇦 Kanada', '2. místo': '🇸🇪 Švédsko', '3. místo': '🇨🇿 Česko', '4. místo': '🇨🇭 Švýcarsko', 'Střelec': 'Pastrňák', 'Nahrávač': 'Crosby', 'Brankář': 'Genoni', 'MVP': 'Crosby'},
    {'Hráč': 'Víťa', 'Vítěz': '🇨🇦 Kanada', '2. místo': '🇺🇸 USA', '3. místo': '🇨🇿 Česko', '4. místo': '🇸🇪 Švédsko', 'Střelec': 'Matthews', 'Nahrávač': 'McDavid', 'Brankář': 'Juuse Saros', 'MVP': 'Raymond'},
    {'Hráč': 'Fany', 'Vítěz': '🇨🇭 Švýcarsko', '2. místo': '🇸🇪 Švédsko', '3. místo': '🇫🇮 Finsko', '4. místo': '🇨🇿 Česko', 'Střelec': 'Petterson', 'Nahrávač': 'Ehlers', 'Brankář': 'Binnington', 'MVP': 'Josi'},
]

FLAGS = {"Česko": "🇨🇿", "Kanada": "🇨🇦", "Slovensko": "🇸🇰", "Finsko": "🇫🇮", "Švédsko": "🇸🇪", "Itálie": "🇮🇹", "USA": "🇺🇸", "Německo": "🇩🇪", "Lotyšsko": "🇱🇻", "Francie": "🇫🇷", "Dánsko": "🇩🇰", "Švýcarsko": "🇨🇭"}

# --- LOGIKA ---
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

# --- APP ---
st.title("🏒 ZOH 2026 - CENTRÁLA")

tab1, tab2, tab3 = st.tabs(["🏆 ŽEBŘÍČEK", "📊 ZÁPASY", "🔮 PŘED TURNAJEM"])

with tab1:
    results = []
    for p in TIPS.keys():
        pts = sum(get_points(TIPS[p].get(m['id'], {}).get('t'), m['res'], TIPS[p].get(m['id'], {}).get('b')) for m in MATCHES if m['res'])
        hits = sum(1 for m in MATCHES if m['res'] and get_points(TIPS[p].get(m['id'], {}).get('t'), m['res']) >= 3)
        results.append({"Hráč": p, "Body": pts, "Přesné trefy": hits})
    df = pd.DataFrame(results).sort_values(["Body", "Přesné trefy"], ascending=False)
    st.table(df)

with tab2:
    for m in MATCHES:
        res = m['res'] or "?:?"
        with st.container():
            st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content:space-around; align-items:center; text-align:center;">
                    <div style="width:30%;"><span class="flag">{FLAGS.get(m['home'], '')}</span><span class="team-name">{m['home']}</span></div>
                    <div class="score-badge">{res}</div>
                    <div style="width:30%;"><span class="flag">{FLAGS.get(m['away'], '')}</span><span class="team-name">{m['away']}</span></div>
                </div>
                <div style="display:flex; flex-wrap:wrap; justify-content:center; margin-top:15px;">
            """, unsafe_allow_html=True)
            
            for p in TIPS.keys():
                tip_data = TIPS[p].get(m['id'], {})
                tip = tip_data.get('t', '-')
                banker = tip_data.get('b', False)
                pts = get_points(tip, m['res'], banker)
                
                # Barva podle úspěchu
                css = "pts-3" if (pts == 3 or (banker and pts == 6)) else ("pts-1" if pts >= 1 else "pts-0")
                if not m['res']: css = ""
                
                b_mark = '<div class="banker-tag">🃏 BANKER</div>' if banker else ""
                
                st.markdown(f"""
                    <div class="tip-box {css}">
                        {b_mark}
                        <div style="font-size:0.7rem; color:gray; font-weight:bold;">{p}</div>
                        <div style="font-weight:bold; font-size:1.1rem;">{tip}</div>
                        {f'<div style="font-size:0.75rem; font-weight:900;">{pts}b</div>' if m['res'] else ''}
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)

with tab3:
    st.markdown("### 🔮 Tipy na celkové umístění a individuální ceny")
    st.dataframe(pd.DataFrame(PRE_DATA), use_container_width=True, hide_index=True)
