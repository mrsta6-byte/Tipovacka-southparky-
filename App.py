import streamlit as st
import pandas as pd
from datetime import datetime

# --- KONFIGURACE APLIKACE ---
st.set_page_config(page_title="ZOH 2026 Tipovačka", page_icon="🏒", layout="centered")

# --- DATA (Simulace tvého Excelu) ---
# V reálu bychom toto tahali přímo z Google Sheets API
PLAYERS = ["Aďas", "Moli", "Cigi", "Cigi ml.", "Mršťa", "Víťa", "Alesh", "Fany"]

TEAMS_CONFIG = {
    "Česko": {"flag": "🇨🇿", "color": "linear-gradient(135deg, #11457e 30%, #d7141a 70%)", "text": "white"},
    "Kanada": {"flag": "🇨🇦", "color": "linear-gradient(135deg, #ff0000 50%, #ffffff 50%)", "text": "black"},
    "Slovensko": {"flag": "🇸🇰", "color": "linear-gradient(135deg, #0b4ea2 30%, #ee1c25 70%)", "text": "white"},
    "Finsko": {"flag": "🇫🇮", "color": "linear-gradient(135deg, #ffffff 40%, #003580 60%)", "text": "black"},
    "Švédsko": {"flag": "🇸🇪", "color": "linear-gradient(135deg, #fecc00 40%, #006aa7 60%)", "text": "black"},
    "USA": {"flag": "🇺🇸", "color": "linear-gradient(135deg, #0a3161 30%, #b31942 70%)", "text": "white"},
    "Švýcarsko": {"flag": "🇨🇭", "color": "#d52b1e", "text": "white"},
    "Německo": {"flag": "🇩🇪", "color": "linear-gradient(135deg, #000000 33%, #dd0000 33%, #dd0000 66%, #ffce00 66%)", "text": "white"},
    "Itálie": {"flag": "🇮🇹", "color": "linear-gradient(135deg, #009246 33%, #ffffff 33%, #ffffff 66%, #ce2b37 66%)", "text": "black"},
    "Lotyšsko": {"flag": "🇱🇻", "color": "#9e3039", "text": "white"},
    "Francie": {"flag": "🇫🇷", "color": "linear-gradient(135deg, #002395 33%, #ffffff 33%, #ffffff 66%, #ed2939 66%)", "text": "black"},
    "Dánsko": {"flag": "🇩🇰", "color": "#c60c30", "text": "white"},
}

# Zápasy vytažené z tvých souborů
MATCHES = [
    {"id": 1, "date": "Středa 11.02. 16:40", "home": "Slovensko", "away": "Finsko"},
    {"id": 2, "date": "Středa 11.02. 21:10", "home": "Švédsko", "away": "Itálie"},
    {"id": 3, "date": "Čtvrtek 12.02. 16:40", "home": "Česko", "away": "Kanada"},
    {"id": 4, "date": "Čtvrtek 12.02. 21:10", "home": "Lotyšsko", "away": "USA"},
    {"id": 5, "date": "Pátek 13.02. 12:10", "home": "Finsko", "away": "Švédsko"},
    {"id": 6, "date": "Neděle 15.02. 12:10", "home": "Švýcarsko", "away": "Česko"},
]

# --- CSS STYLY PRO DRESY A VZHLED ---
st.markdown("""
    <style>
    .match-card {
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-weight: bold;
    }
    .vs-badge {
        background-color: white;
        color: black;
        padding: 5px 10px;
        border-radius: 50%;
        font-size: 0.8em;
        font-weight: bold;
        margin: 0 10px;
    }
    .big-font { font-size: 20px !important; }
    </style>
""", unsafe_allow_html=True)

# --- FUNKCE PRO VYKRESLENÍ ZÁPASU ---
def render_match(match, key_prefix):
    home_team = match["home"]
    away_team = match["away"]
    
    h_conf = TEAMS_CONFIG.get(home_team, {"color": "#ddd", "flag": "", "text": "black"})
    a_conf = TEAMS_CONFIG.get(away_team, {"color": "#ddd", "flag": "", "text": "black"})

    # Vizuální hlavička zápasu (Dresy)
    st.markdown(f"""
    <div style="display: flex; border-radius: 12px; overflow: hidden; margin-bottom: 10px;">
        <div style="flex: 1; background: {h_conf['color']}; color: {h_conf['text']}; padding: 15px; text-align: center;">
            <div style="font-size: 2em;">{h_conf['flag']}</div>
            <div>{home_team}</div>
        </div>
        <div style="width: 40px; background: #333; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold;">
            VS
        </div>
        <div style="flex: 1; background: {a_conf['color']}; color: {a_conf['text']}; padding: 15px; text-align: center;">
            <div style="font-size: 2em;">{a_conf['flag']}</div>
            <div>{away_team}</div>
        </div>
    </div>
    <div style="text-align: center; color: gray; font-size: 0.8em; margin-bottom: 5px;">
        📅 {match['date']}
    </div>
    """, unsafe_allow_html=True)

    # Vstupy pro tipování
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        st.number_input(f"{home_team}", min_value=0, max_value=20, key=f"{key_prefix}_h", label_visibility="collapsed")
    with c2:
        st.number_input(f"{away_team}", min_value=0, max_value=20, key=f"{key_prefix}_a", label_visibility="collapsed")
    with c3:
        st.checkbox("Banker", key=f"{key_prefix}_banker", help="Dvojnásobné body za přesný výsledek")
    
    st.divider()

# --- HLAVNÍ ROZHRANÍ ---

def main():
    st.title("🏒 ZOH 2026 - Tipovačka")
    
    # Boční panel
    with st.sidebar:
        st.header("Kdo jsi?")
        selected_user = st.selectbox("Vyber své jméno:", PLAYERS)
        
        st.markdown("---")
        mode = st.radio("Menu:", ["📝 Zadat tipy", "🏆 Tabulka", "📜 Pravidla"])

    if mode == "📝 Zadat tipy":
        st.subheader(f"Ahoj {selected_user}, zadej své tipy:")
        st.info("💡 Tip: Banker ti zdvojnásobí body, pokud trefíš přesný výsledek!")
        
        # Formulář s tipy
        with st.form("tips_form"):
            for match in MATCHES:
                render_match(match, f"{selected_user}_{match['id']}")
            
            submitted = st.form_submit_button("💾 Uložit tipy do tabulky", type="primary")
            if submitted:
                st.balloons()
                st.success(f"Tipy pro hráče {selected_user} byly úspěšně odeslány! (Simulace)")

    elif mode == "🏆 Tabulka":
        st.subheader("Aktuální pořadí")
        # Simulovaná data pro ukázku
        data = {
            "Hráč": ["Aďas", "Mršťa", "Cigi ml.", "Víťa", "Moli"],
            "Body": [15, 12, 12, 9, 8],
            "Přesné výsledky": [3, 2, 2, 1, 1],
            "Bankeři": [1, 0, 1, 0, 0]
        }
        df = pd.DataFrame(data)
        st.dataframe(df, hide_index=True, use_container_width=True)

    elif mode == "📜 Pravidla":
        st.markdown("""
        ### Pravidla a Bodování
        * **Přesné skóre:** 3 body (např. tip 3:0, výsledek 3:0)
        * **Správný vítěz/remíza:** 1 bod (např. tip 3:0, výsledek 3:1)
        * **Banker:** 1x za kolo. Pokud trefíš přesný výsledek, body se násobí 2x.
        * **Bonus:** 5 bodů za předturnajové tipy.
        * *Tipuje se pouze základní hrací doba (60 min).*
        """)

if __name__ == "__main__":
    main()
