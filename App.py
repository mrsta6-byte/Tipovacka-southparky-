import streamlit as st

# --- KONFIGURACE APLIKACE ---
st.set_page_config(page_title="ZOH 2026", page_icon="🏒", layout="centered")

# --- SEZNAM HRÁČŮ ---
PLAYERS = ["Aďas", "Moli", "Cigi", "Cigi ml.", "Mršťa", "Víťa", "Alesh", "Fany"]

# --- BARVY A VLAJKY TÝMŮ ---
TEAMS_CONFIG = {
    "Česko": {"flag": "🇨🇿", "color": "#11457e", "text": "white"},
    "Kanada": {"flag": "🇨🇦", "color": "#ff0000", "text": "white"},
    "Slovensko": {"flag": "🇸🇰", "color": "#0b4ea2", "text": "white"},
    "Finsko": {"flag": "🇫🇮", "color": "#003580", "text": "white"},
    "Švédsko": {"flag": "🇸🇪", "color": "#fecc00", "text": "black"},
    "USA": {"flag": "🇺🇸", "color": "#0a3161", "text": "white"},
    "Švýcarsko": {"flag": "🇨🇭", "color": "#d52b1e", "text": "white"},
    "Německo": {"flag": "🇩🇪", "color": "#dd0000", "text": "white"},
    "Itálie": {"flag": "🇮🇹", "color": "#009246", "text": "white"},
    "Lotyšsko": {"flag": "🇱🇻", "color": "#9e3039", "text": "white"},
    "Francie": {"flag": "🇫🇷", "color": "#002395", "text": "white"},
    "Dánsko": {"flag": "🇩🇰", "color": "#c60c30", "text": "white"},
}

# --- ROZPIS ZÁPASŮ (Vytaženo z tvého Excelu) ---
MATCHES = [
    # STŘEDA - PÁTEK
    {"id": "WF_1", "date": "Středa 11.02. 16:40", "home": "Slovensko", "away": "Finsko"},
    {"id": "WF_2", "date": "Středa 11.02. 21:10", "home": "Švédsko", "away": "Itálie"},
    {"id": "WF_3", "date": "Čtvrtek 12.02. 12:10", "home": "Švýcarsko", "away": "Francie"},
    {"id": "WF_4", "date": "Čtvrtek 12.02. 16:40", "home": "Česko", "away": "Kanada"},
    {"id": "WF_5", "date": "Čtvrtek 12.02. 21:10", "home": "Lotyšsko", "away": "USA"},
    {"id": "WF_6", "date": "Čtvrtek 12.02. 21:10", "home": "Německo", "away": "Dánsko"},
    {"id": "WF_7", "date": "Pátek 13.02. 12:10", "home": "Finsko", "away": "Švédsko"},
    {"id": "WF_8", "date": "Pátek 13.02. 12:10", "home": "Itálie", "away": "Slovensko"},
    {"id": "WF_9", "date": "Pátek 13.02. 16:40", "home": "Francie", "away": "Česko"},
    {"id": "WF_10", "date": "Pátek 13.02. 21:20", "home": "Kanada", "away": "Švýcarsko"},
    # SOBOTA - NEDĚLE
    {"id": "SN_1", "date": "Sobota 14.02. 12:10", "home": "Německo", "away": "Lotyšsko"},
    {"id": "SN_2", "date": "Sobota 14.02. 12:10", "home": "Švédsko", "away": "Slovensko"},
    {"id": "SN_3", "date": "Sobota 14.02. 16:40", "home": "Finsko", "away": "Itálie"},
    {"id": "SN_4", "date": "Sobota 14.02. 21:10", "home": "USA", "away": "Dánsko"},
    {"id": "SN_5", "date": "Neděle 15.02. 12:10", "home": "Švýcarsko", "away": "Česko"},
    {"id": "SN_6", "date": "Neděle 15.02. 16:40", "home": "Kanada", "away": "Francie"},
    {"id": "SN_7", "date": "Neděle 15.02. 19:10", "home": "Dánsko", "away": "Lotyšsko"},
    {"id": "SN_8", "date": "Neděle 15.02. 21:10", "home": "USA", "away": "Německo"},
]

# --- FUNKCE PRO VYKRESLENÍ ZÁPASU ---
def render_match_card(match):
    h_team = match["home"]
    a_team = match["away"]
    h_cfg = TEAMS_CONFIG.get(h_team, {"color": "#555", "flag": "", "text": "white"})
    a_cfg = TEAMS_CONFIG.get(a_team, {"color": "#555", "flag": "", "text": "white"})
    
    # Karta zápasu
    st.markdown(f"""
    <div style="background-color: white; border-radius: 10px; padding: 10px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
        <div style="text-align: center; font-size: 0.8em; color: gray; margin-bottom: 5px;">📅 {match['date']}</div>
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="text-align: center; width: 40%; font-weight: bold; color: {h_cfg['color']};">
                <div style="font-size: 2em;">{h_cfg['flag']}</div>
                {h_team}
            </div>
            <div style="font-weight: bold; color: #ddd;">VS</div>
            <div style="text-align: center; width: 40%; font-weight: bold; color: {a_cfg['color']};">
                <div style="font-size: 2em;">{a_cfg['flag']}</div>
                {a_team}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Vstupy
    cols = st.columns([2, 0.5, 2])
    with cols[0]:
        h_score = st.text_input(f"skóre {h_team}", key=f"h_{match['id']}", label_visibility="collapsed", placeholder="-")
    with cols[2]:
        a_score = st.text_input(f"skóre {a_team}", key=f"a_{match['id']}", label_visibility="collapsed", placeholder="-")
    
    # Banker
    is_banker = st.checkbox("🃏 Banker (2x)", key=f"b_{match['id']}")
    st.divider()

# --- HLAVNÍ APLIKACE ---
def main():
    st.markdown("<h2 style='text-align: center;'>🏒 TIPY ZOH 2026</h2>", unsafe_allow_html=True)
    
    # Výběr hráče
    selected_player = st.selectbox("Kdo jsi?", PLAYERS)
    st.info(f"Zadáváš tipy pro hráče: **{selected_player}**")
    
    with st.expander("📝 Zadat tipy (Klikni pro otevření)", expanded=True):
        for match in MATCHES:
            render_match_card(match)
    
    # Tlačítko pro generování
    if st.button("📋 VYGENEROVAT ZPRÁVU PRO SKUPINU", type="primary"):
        report_text = f"🏒 *TIPY - {selected_player.upper()}* 🏒\n"
        report_text += f"-----------------------------\n"
        
        count = 0
        for match in MATCHES:
            # Načtení hodnot ze session state
            h_val = st.session_state.get(f"h_{match['id']}", "")
            a_val = st.session_state.get(f"a_{match['id']}", "")
            banker = st.session_state.get(f"b_{match['id']}", False)
            
            if h_val and a_val:
                banker_mark = " 🔥 BANKER" if banker else ""
                report_text += f"{match['home']} vs {match['away']} -> *{h_val}:{a_val}*{banker_mark}\n"
                count += 1
        
        if count > 0:
            st.success("Zpráva vygenerována! Zkopíruj kód níže:")
            st.code(report_text, language="markdown")
            st.caption("👆 Klikni na ikonku kopírování vpravo nahoře a vlož to do Messengeru.")
        else:
            st.error("Nezadal jsi žádné výsledky!")

if __name__ == "__main__":
    main()
