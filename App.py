import streamlit as st
import pandas as pd

# --- KONFIGURACE APLIKACE ---
st.set_page_config(page_title="ZOH 2026 Tipovačka", page_icon="🏒", layout="wide")

# --- DATA: ZÁPASY (Vytaženo přesně z tvé tabulky) ---
MATCHES = [
    {"id": "M1", "date": "Středa 11.02. 16:40", "home": "Slovensko", "away": "Finsko"},
    {"id": "M2", "date": "Středa 11.02. 21:10", "home": "Švédsko", "away": "Itálie"},
    {"id": "M3", "date": "Čtvrtek 12.02 12:10", "home": "Švýcarsko", "away": "Francie"},
    {"id": "M4", "date": "Čtvrtek 12.02 16:40", "home": "Česko", "away": "Kanada"},
    {"id": "M5", "date": "Čtvrtek 12.02 21:10", "home": "Lotyšsko", "away": "USA"},
    {"id": "M6", "date": "Čtvrtek 12.02 21:10", "home": "Německo", "away": "Dánsko"},
    {"id": "M7", "date": "Pátek 13.02. 12:10", "home": "Finsko", "away": "Švédsko"},
    {"id": "M8", "date": "Pátek 13.02. 12:10", "home": "Itálie", "away": "Slovensko"},
    {"id": "M9", "date": "Pátek 13.02. 16:40", "home": "Francie", "away": "Česko"},
    {"id": "M10", "date": "Pátek 13.02. 21:20", "home": "Kanada", "away": "Švýcarsko"},
    {"id": "M11", "date": "Sobota 14.02. 12:10", "home": "Německo", "away": "Lotyšsko"},
    {"id": "M12", "date": "Sobota 14.02. 12:10", "home": "Švédsko", "away": "Slovensko"},
    {"id": "M13", "date": "Sobota 14.02. 16:40", "home": "Finsko", "away": "Itálie"},
    {"id": "M14", "date": "Sobota 14.02. 21:10", "home": "USA", "away": "Dánsko"},
    {"id": "M15", "date": "Neděle 15.02. 12:10", "home": "Švýcarsko", "away": "Česko"},
    {"id": "M16", "date": "Neděle 15.02. 16:40", "home": "Kanada", "away": "Francie"},
    {"id": "M17", "date": "Neděle 15.02. 19:10", "home": "Dánsko", "away": "Lotyšsko"},
    {"id": "M18", "date": "Neděle 15.02. 21:10", "home": "USA", "away": "Německo"},
]

# --- DATA: HISTORICKÉ TIPY (Vytaženo z tvých CSV souborů) ---
PLAYER_TIPS = {
    'Aďas': {'M1': '1:3', 'M2': '6:1', 'M3': '6:2', 'M4': '2:4', 'M5': '2:3', 'M6': '4:3', 'M7': '1:3', 'M8': '2:4', 'M9': '0:5', 'M10': '3:1', 'M11': '2:2', 'M12': '5:1', 'M13': '3:0', 'M14': '5:2', 'M15': '3:3', 'M16': '8:0', 'M17': '3:2', 'M18': '2:1'},
    'Moli': {'M1': '1:5', 'M2': '8:0'},
    'Cigi ml.': {'M1': '2:4', 'M2': '6:2', 'M3': '3:1', 'M4': '3:5', 'M5': '1:4', 'M6': '4:2', 'M7': '2:3', 'M8': '3:5', 'M9': '1:4', 'M10': '4:1', 'M11': '3:3', 'M12': '6:2', 'M13': '5:0', 'M14': '6:1', 'M15': '4:5', 'M16': '7:0', 'M17': '4:2', 'M18': '5:2'},
    'Mršťa': {'M1': '2:4', 'M2': '7:1', 'M3': '5:2', 'M4': '2:5', 'M5': '2:5', 'M6': '5:3', 'M7': '2:3', 'M8': '1:5', 'M9': '1:6', 'M10': '4:2', 'M11': '3:1', 'M12': '7:3', 'M13': '2:2', 'M14': '4:0', 'M15': '3:5', 'M16': '9:1', 'M17': '3:3', 'M18': '5:4'},
    'Víťa': {'M1': '2:2', 'M2': '4:0', 'M3': '4:1', 'M4': '1:4', 'M5': '1:5', 'M6': '3:2', 'M7': '3:3', 'M8': '3:4', 'M9': '0:3', 'M10': '4:2', 'M11': '3:2', 'M12': '4:0', 'M13': '3:1', 'M14': '6:1', 'M15': '4:2', 'M16': '5:0', 'M17': '3:2', 'M18': '4:3'}
}

# --- DATA: TIPY PŘED TURNAJEM (Vytaženo) ---
PRE_TIPS = [
    {'Hráč': 'Aďas', 'Vítěz': 'Kanada', '2. místo': 'Česko', '3. místo': 'Švédsko', 'Střelec': 'Nathan MacKinnon'},
    {'Hráč': 'Cigi ml.', 'Vítěz': 'Kanada', '2. místo': 'Švédsko', '3. místo': 'USA', 'Střelec': 'Celebriny'},
    {'Hráč': 'Mršťa', 'Vítěz': 'Kanada', '2. místo': 'Švédsko ', '3. místo': 'Česko ', 'Střelec': 'Pastrňák'},
    {'Hráč': 'Víťa', 'Vítěz': 'Kanada', '2. místo': 'USA', '3. místo': 'Česko ', 'Střelec': 'Matthews'},
    {'Hráč': 'Fany', 'Vítěz': 'Švýcarsko ', '2. místo': 'Švédsko ', '3. místo': 'Finsko ', 'Střelec': 'Elias Petterson'}
]

PLAYERS = sorted(list(set(list(PLAYER_TIPS.keys()) + [p['Hráč'] for p in PRE_TIPS])))

TEAMS_FLAGS = {
    "Česko": "🇨🇿", "Kanada": "🇨🇦", "Slovensko": "🇸🇰", "Finsko": "🇫🇮",
    "Švédsko": "🇸🇪", "USA": "🇺🇸", "Švýcarsko": "🇨🇭", "Německo": "🇩🇪",
    "Itálie": "🇮🇹", "Lotyšsko": "🇱🇻", "Francie": "🇫🇷", "Dánsko": "🇩🇰"
}

# --- FUNKCE PRO VÝPOČET BODŮ ---
def calculate_points(tip_str, result_str):
    if not tip_str or not result_str or ":" not in str(tip_str) or ":" not in str(result_str):
        return 0
    try:
        t_h, t_a = map(int, tip_str.split(":"))
        r_h, r_a = map(int, result_str.split(":"))
        
        # Přesný výsledek = 3 body
        if t_h == r_h and t_a == r_a:
            return 3
        
        # Správný vítěz/remíza = 1 bod
        # 1 = Domácí, 0 = Remíza, -1 = Hosté
        t_res = 1 if t_h > t_a else (0 if t_h == t_a else -1)
        r_res = 1 if r_h > r_a else (0 if r_h == r_a else -1)
        
        if t_res == r_res:
            return 1
        return 0
    except:
        return 0

# --- HLAVNÍ APLIKACE ---
def main():
    st.title("🏒 ZOH 2026 - Oficiální Tipovačka")
    
    # 1. ČÁST - ZADÁNÍ VÝSLEDKŮ (ADMIN)
    with st.expander("✍️ Zadat/Upravit výsledky zápasů (Klikni sem)", expanded=False):
        st.caption("Zde zadej skutečné výsledky, jakmile zápas skončí. Body se přepočítají automaticky.")
        results_input = {}
        cols = st.columns(4)
        for i, m in enumerate(MATCHES):
            with cols[i % 4]:
                # Klíč v session state pro uchování výsledku
                key = f"res_{m['id']}"
                val = st.text_input(f"{m['home']} vs {m['away']}", key=key, placeholder="např. 3:1")
                if val:
                    results_input[m['id']] = val

    # 2. ČÁST - TABULKA A PŘEHLED
    tab1, tab2, tab3 = st.tabs(["🏆 Žebříček", "📊 Přehled Tipů", "🔮 Tipy před turnajem"])

    with tab1:
        st.subheader("Aktuální pořadí")
        ranking = []
        for p in PLAYERS:
            total_pts = 0
            exact_hits = 0
            p_tips = PLAYER_TIPS.get(p, {})
            
            for m_id, result in results_input.items():
                tip = p_tips.get(m_id)
                pts = calculate_points(tip, result)
                total_pts += pts
                if pts == 3: exact_hits += 1
            
            ranking.append({"Hráč": p, "Body": total_pts, "Přesné trefy (3b)": exact_hits})
        
        df_rank = pd.DataFrame(ranking).sort_values(by=["Body", "Přesné trefy (3b)"], ascending=False).reset_index(drop=True)
        # Zvýraznění prvního
        st.dataframe(df_rank, use_container_width=True)
        if not df_rank.empty:
            leader = df_rank.iloc[0]['Hráč']
            st.success(f"👑 Aktuálně vede: **{leader}**")

    with tab2:
        st.subheader("Detailní přehled zápasů")
        
        for m in MATCHES:
            res = results_input.get(m['id'], "---")
            fh = TEAMS_FLAGS.get(m['home'], "")
            fa = TEAMS_FLAGS.get(m['away'], "")
            
            # Karta zápasu
            with st.container():
                st.markdown(f"""
                <div style="background:#f0f2f6; padding:10px; border-radius:8px; margin-bottom:5px;">
                    <div style="font-weight:bold; font-size:1.1em;">
                        {fh} {m['home']} vs {m['away']} {fa} <span style="float:right; color:#d7141a;">{res}</span>
                    </div>
                    <div style="font-size:0.8em; color:gray;">{m['date']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Tipy hráčů pod zápasem
                cols = st.columns(len(PLAYERS))
                for i, p in enumerate(PLAYERS):
                    tip = PLAYER_TIPS.get(p, {}).get(m['id'], "-")
                    pts = calculate_points(tip, res)
                    
                    color = "black"
                    bg = "transparent"
                    if res != "---":
                        if pts == 3: bg = "#d4edda"; color = "#155724" # Zelená
                        elif pts == 1: bg = "#fff3cd"; color = "#856404" # Žlutá
                        else: bg = "#f8d7da"; color = "#721c24" # Červená
                    
                    with cols[i]:
                        st.markdown(f"""
                        <div style="text-align:center; background:{bg}; color:{color}; border-radius:5px; padding:2px;">
                            <div style="font-size:0.7em; font-weight:bold;">{p}</div>
                            <div>{tip}</div>
                        </div>
                        """, unsafe_allow_html=True)
            st.divider()

    with tab3:
        st.subheader("🔮 Dlouhodobé sázky")
        st.dataframe(pd.DataFrame(PRE_TIPS), use_container_width=True)

if __name__ == "__main__":
    main()
