import streamlit as st
import pandas as pd

# --- KONFIGURACE APLIKACE ---
st.set_page_config(page_title="ZOH 2026", page_icon="🏒", layout="centered")

# --- SEZNAM HRÁČŮ ---
PLAYERS = ["Aďas", "Moli", "Cigi", "Cigi ml.", "Mršťa", "Víťa", "Alesh", "Fany"]

# --- BARVY A VLAJKY TÝMŮ ---
TEAMS_CONFIG = {
    "Česko": {"flag": "🇨🇿", "color": "#11457e"},
    "Kanada": {"flag": "🇨🇦", "color": "#ff0000"},
    "Slovensko": {"flag": "🇸🇰", "color": "#0b4ea2"},
    "Finsko": {"flag": "🇫🇮", "color": "#003580"},
    "Švédsko": {"flag": "🇸🇪", "color": "#fecc00"},
    "USA": {"flag": "🇺🇸", "color": "#0a3161"},
    "Švýcarsko": {"flag": "🇨🇭", "color": "#d52b1e"},
    "Německo": {"flag": "🇩🇪", "color": "#dd0000"},
    "Itálie": {"flag": "🇮🇹", "color": "#009246"},
    "Lotyšsko": {"flag": "🇱🇻", "color": "#9e3039"},
    "Francie": {"flag": "🇫🇷", "color": "#002395"},
    "Dánsko": {"flag": "🇩🇰", "color": "#c60c30"},
}

# --- DATA: TIPY PŘED TURNAJEM (Vytaženo z tvého CSV) ---
PRE_TOURNAMENT_DATA = [
    {"Hráč": "Aďas", "Vítěz": "🇨🇦 Kanada", "2. místo": "🇨🇿 Česko", "3. místo": "🇸🇪 Švédsko", "4. místo": "🇨🇭 Švýcarsko", "Střelec": "N. MacKinnon", "Nahrávač": "T. Konecny", "Brankář": "D. Vladař", "Hráč turnaje": "N. MacKinnon"},
    {"Hráč": "Cigi ml.", "Vítěz": "🇨🇦 Kanada", "2. místo": "🇸🇪 Švédsko", "3. místo": "🇺🇸 USA", "4. místo": "🇫🇮 Finsko", "Střelec": "M. Celebrini", "Nahrávač": "C. McDavid", "Brankář": "L. Thompson", "Hráč turnaje": "C. McDavid"},
    {"Hráč": "Mršťa", "Vítěz": "🇨🇦 Kanada", "2. místo": "🇸🇪 Švédsko", "3. místo": "🇨🇿 Česko", "4. místo": "🇨🇭 Švýcarsko", "Střelec": "D. Pastrňák", "Nahrávač": "S. Crosby", "Brankář": "L. Genoni", "Hráč turnaje": "S. Crosby"},
    {"Hráč": "Víťa", "Vítěz": "🇨🇦 Kanada", "2. místo": "🇺🇸 USA", "3. místo": "🇨🇿 Česko", "4. místo": "🇸🇪 Švédsko", "Střelec": "A. Matthews", "Nahrávač": "C. McDavid", "Brankář": "J. Saros", "Hráč turnaje": "L. Raymond"},
    {"Hráč": "Fany", "Vítěz": "🇨🇭 Švýcarsko", "2. místo": "🇸🇪 Švédsko", "3. místo": "🇫🇮 Finsko", "4. místo": "🇨🇿 Česko", "Střelec": "E. Petterson", "Nahrávač": "N. Ehlers", "Brankář": "J. Binnington", "Hráč turnaje": "R. Josi"},
    {"Hráč": "Moli", "Vítěz": "-", "2. místo": "-", "3. místo": "-", "4. místo": "-", "Střelec": "-", "Nahrávač": "-", "Brankář": "-", "Hráč turnaje": "-"},
    {"Hráč": "Cigi", "Vítěz": "-", "2. místo": "-", "3. místo": "-", "4. místo": "-", "Střelec": "-", "Nahrávač": "-", "Brankář": "-", "Hráč turnaje": "-"},
    {"Hráč": "Alesh", "Vítěz": "-", "2. místo": "-", "3. místo": "-", "4. místo": "-", "Střelec": "-", "Nahrávač": "-", "Brankář": "-", "Hráč turnaje": "-"},
]

# --- ROZPIS ZÁPASŮ ---
MATCHES = [
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
    {"id": "SN_1", "date": "Sobota 14.02. 12:10", "home": "Německo", "away": "Lotyšsko"},
    {"id": "SN_2", "date": "Sobota 14.02. 12:10", "home": "Švédsko", "away": "Slovensko"},
    {"id": "SN_3", "date": "Sobota 14.02. 16:40", "home": "Finsko", "away": "Itálie"},
    {"id": "SN_4", "date": "Sobota 14.02. 21:10", "home": "USA", "away": "Dánsko"},
    {"id": "SN_5", "date": "Neděle 15.02. 12:10", "home": "Švýcarsko", "away": "Česko"},
    {"id": "SN_6", "date": "Neděle 15.02. 16:40", "home": "Kanada", "away": "Francie"},
    {"id": "SN_7", "date": "Neděle 15.02. 19:10", "home": "Dánsko", "away": "Lotyšsko"},
    {"id": "SN_8", "date": "Neděle 15.02. 21:10", "home": "USA", "away": "Německo"},
]

def render_match_card(match):
    h_team = match["home"]
    a_team = match["away"]
    h_cfg = TEAMS_CONFIG.get(h_team, {"color": "#555", "flag": "", "text": "white"})
    a_cfg = TEAMS_CONFIG.get(a_team, {"color": "#555", "flag": "", "text": "white"})
    
    st.markdown(f"""
    <div style="background-color: white; border-radius: 10px; padding: 10px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); color: black;">
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
    
    cols = st.columns([2, 0.5, 2])
    with cols[0]:
        st.text_input(f"skóre {h_team}", key=f"h_{match['id']}", label_visibility="collapsed", placeholder="-")
    with cols[2]:
        st.text_input(f"skóre {a_team}", key=f"a_{match['id']}", label_visibility="collapsed", placeholder="-")
    st.checkbox("🃏 Banker (2x)", key=f"b_{match['id']}")
    st.divider()

# --- HLAVNÍ LOGIKA ---
def main():
    st.title("🏒 ZOH 2026 Tipovačka")

    # Záložky pro přepínání obsahu
    tab1, tab2 = st.tabs(["📝 Zadat tipy", "🔮 Tipy před turnajem"])

    # --- ZÁLOŽKA 1: ZADÁVÁNÍ ---
    with tab1:
        selected_player = st.selectbox("Kdo jsi?", PLAYERS)
        st.info(f"Hráč: **{selected_player}**")
        
        with st.expander("Zobrazit zápasy k tipování", expanded=True):
            for match in MATCHES:
                render_match_card(match)
        
        if st.button("📋 VYGENEROVAT ZPRÁVU", type="primary"):
            report_text = f"🏒 *TIPY - {selected_player.upper()}* 🏒\n-----------------------------\n"
            count = 0
            for match in MATCHES:
                h_val = st.session_state.get(f"h_{match['id']}", "")
                a_val = st.session_state.get(f"a_{match['id']}", "")
                banker = st.session_state.get(f"b_{match['id']}", False)
                if h_val and a_val:
                    banker_mark = " 🔥 BANKER" if banker else ""
                    report_text += f"{match['home']} vs {match['away']} -> *{h_val}:{a_val}*{banker_mark}\n"
                    count += 1
            
            if count > 0:
                st.code(report_text, language="markdown")
            else:
                st.error("Nezadal jsi žádné výsledky!")

    # --- ZÁLOŽKA 2: PŘEHLED DLOUHODOBÝCH TIPŮ ---
    with tab2:
        st.subheader("🔮 Kdo vyhraje olympiádu?")
        st.caption("Přehled tipů všech hráčů (z tabulky)")
        
        # Vytvoření tabulky
        df = pd.DataFrame(PRE_TOURNAMENT_DATA)
        
        # Zobrazení tabulky
        st.dataframe(
            df,
            column_config={
                "Hráč": st.column_config.TextColumn("Hráč", width="small"),
                "Vítěz": st.column_config.TextColumn("🥇 Vítěz"),
                "2. místo": st.column_config.TextColumn("🥈 2. místo"),
                "3. místo": st.column_config.TextColumn("🥉 3. místo"),
            },
            hide_index=True,
            use_container_width=True
        )
        
        st.markdown("---")
        st.subheader("🏆 Individuální ceny")
        # Druhá část tabulky pro individuální ceny (aby se to vešlo na mobil)
        st.dataframe(
            df[["Hráč", "Střelec", "Nahrávač", "Brankář", "Hráč turnaje"]],
            hide_index=True,
            use_container_width=True
        )

if __name__ == "__main__":
    main()
