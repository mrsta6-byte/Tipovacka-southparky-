import streamlit as st
import pandas as pd

# --- KONFIGURACE ---
st.set_page_config(page_title="ZOH 2026 - Tipovačka FINÁLE", page_icon="🏒", layout="wide")

# --- DESIGN ---
st.markdown("""
<style>
    .match-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 15px; border-left: 8px solid #003087; box-shadow: 0 2px 8px rgba(0,0,0,0.1); color: #1a1a1a; }
    .score-badge { font-size: 1.8rem; font-weight: 800; background: #1a1a1a; padding: 5px 20px; border-radius: 8px; color: white; min-width: 100px; text-align: center; }
    .flag { font-size: 2.5rem; display: block; margin-bottom: 5px; }
    .team-name { font-weight: 700; font-size: 1.1rem; text-transform: uppercase; }
    .tip-box { border-radius: 6px; padding: 5px; text-align: center; margin: 3px; border: 1px solid #ddd; min-width: 80px; display: inline-block; vertical-align: top; background: #f8f9fa; }
    .banker-label { background: #d90429; color: white; font-size: 0.6rem; padding: 2px 4px; border-radius: 3px; display: block; margin-bottom: 2px; font-weight: bold; }
    .pts-3 { background-color: #d1e7dd !important; border-color: #badbcc !important; color: #0f5132 !important; }
    .pts-1 { background-color: #fff3cd !important; border-color: #ffecb5 !important; color: #664d03 !important; }
    .pts-0 { background-color: #f8d7da !important; border-color: #f5c2c7 !important; color: #842029 !important; }
    .playoff-header { background: #003087; color: white; padding: 10px; border-radius: 10px 10px 0 0; text-align: center; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 1. DATA: ZÁKLADNÍ SKUPINY (Všechny odehrané zápasy) ---
MATCHES = [
    # Středa 11.02.
    {"id": "M1", "date": "11.02.", "home": "Slovensko", "away": "Finsko", "res": "4:1"},
    {"id": "M2", "date": "11.02.", "home": "Švédsko", "away": "Itálie", "res": "5:2"},
    # Čtvrtek 12.02.
    {"id": "M3", "date": "12.02.", "home": "Švýcarsko", "away": "Francie", "res": "4:0"},
    {"id": "M4", "date": "12.02.", "home": "Česko", "away": "Kanada", "res": "0:5"},
    {"id": "M5", "date": "12.02.", "home": "Lotyšsko", "away": "USA", "res": "1:5"},
    {"id": "M6", "date": "12.02.", "home": "Německo", "away": "Dánsko", "res": "3:1"},
    # Pátek 13.02.
    {"id": "M7", "date": "13.02.", "home": "Finsko", "away": "Švédsko", "res": "4:1"},
    {"id": "M8", "date": "13.02.", "home": "Itálie", "away": "Slovensko", "res": "2:3"},
    {"id": "M9", "date": "13.02.", "home": "Francie", "away": "Česko", "res": "3:6"},
    {"id": "M10", "date": "13.02.", "home": "Kanada", "away": "Švýcarsko", "res": "5:1"},
    # Sobota 14.02.
    {"id": "M11", "date": "14.02.", "home": "Německo", "away": "Lotyšsko", "res": "3:4"},
    {"id": "M12", "date": "14.02.", "home": "Švédsko", "away": "Slovensko", "res": "5:3"},
    {"id": "M13", "date": "14.02.", "home": "Finsko", "away": "Itálie", "res": "11:0"},
    {"id": "M14", "date": "14.02.", "home": "USA", "away": "Dánsko", "res": "6:3"},
    # Neděle 15.02.
    {"id": "M15", "date": "15.02.", "home": "Švýcarsko", "away": "Česko", "res": "3:3"},
    {"id": "M16", "date": "15.02.", "home": "Kanada", "away": "Francie", "res": "8:0"},
    {"id": "M17", "date": "15.02.", "home": "Dánsko", "away": "Lotyšsko", "res": "3:2"},
    {"id": "M18", "date": "15.02.", "home": "USA", "away": "Německo", "res": "2:1"},
]

# --- 2. DATA: PAVOUK PLAY-OFF (Opraveno dle tvých instrukcí) ---
PLAYOFF = [
    # Osmifinále (Předkolo)
    {"id": "OF1", "round": "OSMIFINÁLE", "date": "Úterý 17.02.", "home": "Česko", "away": "Dánsko"},
    {"id": "OF2", "round": "OSMIFINÁLE", "date": "Úterý 17.02.", "home": "Švédsko", "away": "Lotyšsko"}, # Opraveno
    {"id": "OF3", "round": "OSMIFINÁLE", "date": "Úterý 17.02.", "home": "Švýcarsko", "away": "Francie"},
    {"id": "OF4", "round": "OSMIFINÁLE", "date": "Úterý 17.02.", "home": "Německo", "away": "Itálie"},
    # Čtvrtfinále (Nasazení přímo postupující)
    {"id": "QF1", "round": "ČTVRTFINÁLE", "date": "Středa 18.02.", "home": "Kanada", "away": "vítěz OF4"},
    {"id": "QF2", "round": "ČTVRTFINÁLE", "date": "Středa 18.02.", "home": "USA", "away": "vítěz OF3"},
    {"id": "QF3", "round": "ČTVRTFINÁLE", "date": "Středa 18.02.", "home": "Finsko", "away": "vítěz OF2"}, # Doplněno
    {"id": "QF4", "round": "ČTVRTFINÁLE", "date": "Středa 18.02.", "home": "Slovensko", "away": "vítěz OF1"}, # Doplněno
]

# --- 3. DATA: TIPY HRÁČŮ (Kompletní ruční přepis všech 18 kol) ---
# Formát: 'M_ID': {'t': 'TIP', 'b': True/False (Banker)}
TIPS = {
    'Aďas': {
        'M1': {'t':'1:3','b':False}, 'M2': {'t':'6:1','b':False}, 'M3': {'t':'6:2','b':False}, 'M4': {'t':'2:4','b':False}, 'M5': {'t':'2:3','b':False}, 'M6': {'t':'4:3','b':False},
        'M7': {'t':'1:3','b':False}, 'M8': {'t':'2:4','b':False}, 'M9': {'t':'0:5','b':True}, 'M10':{'t':'3:1','b':False}, 'M11':{'t':'2:2','b':False}, 'M12':{'t':'5:1','b':True},
        'M13':{'t':'3:0','b':False}, 'M14':{'t':'5:2','b':False}, 'M15':{'t':'3:3','b':False}, 'M16':{'t':'8:0','b':False}, 'M17':{'t':'3:2','b':False}, 'M18':{'t':'2:1','b':False}
    },
    'Víťa': {
        'M1': {'t':'2:2','b':False}, 'M2': {'t':'4:0','b':False}, 'M3': {'t':'4:1','b':False}, 'M4': {'t':'1:4','b':False}, 'M5': {'t':'2:6','b':False}, 'M6': {'t':'3:2','b':False},
        'M7': {'t':'3:3','b':False}, 'M8': {'t':'3:4','b':False}, 'M9': {'t':'0:3','b':False}, 'M10':{'t':'4:2','b':False}, 'M11':{'t':'3:2','b':False}, 'M12':{'t':'4:0','b':False},
        'M13':{'t':'3:1','b':False}, 'M14':{'t':'6:1','b':False}, 'M15':{'t':'4:2','b':False}, 'M16':{'t':'5:0','b':False}, 'M17':{'t':'3:2','b':False}, 'M18':{'t':'4:3','b':False}
    },
    'Cigi ml.': {
        'M1': {'t':'2:4','b':False}, 'M2': {'t':'6:2','b':False}, 'M3': {'t':'3:1','b':False}, 'M4': {'t':'3:5','b':False}, 'M5': {'t':'1:4','b':False}, 'M6': {'t':'4:2','b':False},
        'M7': {'t':'2:3','b':False}, 'M8': {'t':'3:5','b':False}, 'M9': {'t':'1:4','b':False}, 'M10':{'t':'4:1','b':False}, 'M11':{'t':'3:3','b':False}, 'M12':{'t':'6:2','b':False},
        'M13':{'t':'5:0','b':False}, 'M14':{'t':'6:1','b':False}, 'M15':{'t':'4:5','b':False}, 'M16':{'t':'7:0','b':False}, 'M17':{'t':'4:2','b':False}, 'M18':{'t':'5:2','b':False}
    },
    'Mršťa': {
        'M1': {'t':'2:4','b':False}, 'M2': {'t':'7:1','b':False}, 'M3': {'t':'5:2','b':False}, 'M4': {'t':'2:5','b':False}, 'M5': {'t':'2:5','b':False}, 'M6': {'t':'5:3','b':False},
        'M7': {'t':'2:3','b':False}, 'M8': {'t':'1:5','b':False}, 'M9': {'t':'1:6','b':False}, 'M10':{'t':'4:2','b':False}, 'M11':{'t':'3:1','b':False}, 'M12':{'t':'7:3','b':False},
        'M13':{'t':'2:2','b':False}, 'M14':{'t':'4:0','b':True}, 'M15':{'t':'3:5','b':False}, 'M16':{'t':'9:1','b':False}, 'M17':{'t':'3:3','b':False}, 'M18':{'t':'5:4','b':False}
    },
    'Moli': {'M1': {'t':'1:5','b':False}, 'M2': {'t':'8:0','b':False}}, # Moli má jen první dva tipy
    'Alesh': {}, 'Cigi': {}, 'Fany': {}
}

# --- 4. DATA: PŘED TURNAJEM (Kompletní) ---
PRE_DATA = [
    {'Hráč': 'Aďas', '🥇 Vítěz': 'Kanada', '🥈 2.místo': 'Česko', '🥉 3.místo': 'Švédsko', '🏅 4.místo': 'Švýcarsko', '🏒 Střelec': 'MacKinnon', '🍎 Nahrávač': 'Konecny', '🧱 Brankář': 'Vladař', '⭐ MVP': 'MacKinnon'},
    {'Hráč': 'Cigi ml.', '🥇 Vítěz': 'Kanada', '🥈 2.místo': 'Švédsko', '🥉 3.místo': 'USA', '🏅 4.místo': 'Finsko', '🏒 Střelec': 'Celebriny', '🍎 Nahrávač': 'McDavid', '🧱 Brankář': 'Thompson ', '⭐ MVP': 'McDavid'},
    {'Hráč': 'Mršťa', '🥇 Vítěz': 'Kanada', '🥈 2.místo': 'Švédsko ', '🥉 3.místo': 'Česko ', '🏅 4.místo': 'Švýcarsko ', '🏒 Střelec': 'Pastrňák', '🍎 Nahrávač': 'Crosby', '🧱 Brankář': 'Genoni', '⭐ MVP': 'Crosby'},
    {'Hráč': 'Víťa', '🥇 Vítěz': 'Kanada', '🥈 2.místo': 'USA', '🥉 3.místo': 'Česko ', '🏅 4.místo': 'Švédsko', '🏒 Střelec': 'Matthews', '🍎 Nahrávač': 'McDavid', '🧱 Brankář': 'Juuse Saros', '⭐ MVP': 'Raymond'},
    {'Hráč': 'Fany', '🥇 Vítěz': 'Švýcarsko ', '🥈 2.místo': 'Švédsko ', '🥉 3.místo': 'Finsko ', '🏅 4.místo': 'Česko ', '🏒 Střelec': 'Petterson', '🍎 Nahrávač': 'Ehlers', '🧱 Brankář': 'Binnington', '⭐ MVP': 'Josi'},
]

FLAGS = {"Česko": "🇨🇿", "Kanada": "🇨🇦", "Slovensko": "🇸🇰", "Finsko": "🇫🇮", "Švédsko": "🇸🇪", "Itálie": "🇮🇹", "USA": "🇺🇸", "Německo": "🇩🇪", "Lotyšsko": "🇱🇻", "Francie": "🇫🇷", "Dánsko": "🇩🇰", "Švýcarsko": "🇨🇭"}

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

tabs = st.tabs(["🏆 TABULKA", "📊 ZÁKLADNÍ SKUPINY", "🔥 PLAY-OFF", "🔮 DLOUHODOBÉ"])

# 1. TABULKA
with tabs[0]:
    ranking = []
    # Seznam všech hráčů
    all_players = sorted(list(set(list(TIPS.keys()) + [p['Hráč'] for p in PRE_DATA])))
    
    for p in all_players:
        player_tips = TIPS.get(p, {})
        pts = 0
        hits = 0
        for m in MATCHES:
            t = player_tips.get(m['id'], {}).get('t')
            b = player_tips.get(m['id'], {}).get('b', False)
            p_match = get_points(t, m['res'], b)
            pts += p_match
            if m['res'] and get_points(t, m['res']) >= 3: hits += 1
        ranking.append({"Hráč": p, "Body": pts, "Přesné trefy": hits})
        
    st.table(pd.DataFrame(ranking).sort_values(["Body", "Přesné trefy"], ascending=False).reset_index(drop=True))

# 2. ZÁKLADNÍ SKUPINY
with tabs[1]:
    for m in MATCHES:
        res = m['res'] or "?:?"
        # HTML Karta zápasu
        html = f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="text-align:center; width:30%;"><span class="flag">{FLAGS.get(m['home'],'')}</span><div class="team-name">{m['home']}</div></div>
                <div class="score-badge">{res}</div>
                <div style="text-align:center; width:30%;"><span class="flag">{FLAGS.get(m['away'],'')}</span><div class="team-name">{m['away']}</div></div>
            </div>
            <div style="text-align:center; margin-top:15px;">
        """
        # Tipy hráčů
        for p in all_players:
            p_data = TIPS.get(p, {}).get(m['id'], {})
            tip = p_data.get('t', '-')
            banker = p_data.get('b', False)
            pts = get_points(tip, m['res'], banker)
            
            # CSS třída pro barvu
            css = ""
            if m['res']:
                if pts >= 3: css = "pts-3" # Zelená
                elif pts == 1: css = "pts-1" # Žlutá
                else: css = "pts-0" # Červená
            
            banker_html = '<span class="banker-label">🃏 BANKER</span>' if banker else ''
            pts_html = f'<div style="font-size:0.8rem; font-weight:bold;">{pts}b</div>' if m['res'] else ''
            
            if tip != "-":
                html += f"""
                <div class="tip-box {css}">
                    {banker_html}
                    <div style="font-size:0.7rem; color:#555;">{p}</div>
                    <div style="font-weight:bold; font-size:1.1rem;">{tip}</div>
                    {pts_html}
                </div>
                """
        html += "</div></div>"
        st.markdown(html, unsafe_allow_html=True)

# 3. PLAY-OFF
with tabs[2]:
    st.info("⚠️ Zde zatím nejsou vypsané tipy. Až budou kurzy, doplníme!")
    for p in PLAYOFF:
        html = f"""
        <div class="match-card" style="border-left-color: #ffcc00;">
            <div class="playoff-header">{p['round']}</div>
            <div style="display:flex; justify-content:space-between; align-items:center; padding-top:10px;">
                <div style="text-align:center; width:30%;"><span class="flag">{FLAGS.get(p['home'],'🏒')}</span><div class="team-name">{p['home']}</div></div>
                <div style="font-size:1.5rem; font-weight:bold;">VS</div>
                <div style="text-align:center; width:30%;"><span class="flag">{FLAGS.get(p['away'],'🏒')}</span><div class="team-name">{p['away']}</div></div>
            </div>
            <div style="text-align:center; color:gray; margin-top:10px;">📅 {p['date']}</div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

# 4. DLOUHODOBÉ
with tabs[3]:
    st.dataframe(pd.DataFrame(PRE_DATA), use_container_width=True, hide_index=True)
