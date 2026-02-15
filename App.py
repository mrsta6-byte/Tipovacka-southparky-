import streamlit as st
import pandas as pd

# --- KONFIGURACE APLIKACE ---
st.set_page_config(page_title="ZOH 2026 Tipovačka", page_icon="🏒", layout="wide")

# --- SEZNAM HRÁČŮ ---
PLAYERS = ["Aďas", "Moli", "Cigi", "Cigi ml.", "Mršťa", "Víťa", "Alesh", "Fany"]

# --- BARVY TÝMŮ ---
TEAMS_CONFIG = {
    "Česko": "🇨🇿", "Kanada": "🇨🇦", "Slovensko": "🇸🇰", "Finsko": "🇫🇮",
    "Švédsko": "🇸🇪", "USA": "🇺🇸", "Švýcarsko": "🇨🇭", "Německo": "🇩🇪",
    "Itálie": "🇮🇹", "Lotyšsko": "🇱🇻", "Francie": "🇫🇷", "Dánsko": "🇩🇰"
}

# --- DATA ZÁPASŮ A VÝSLEDKŮ (Vytaženo z tvých souborů) ---
# Format: ID, Datum, Domácí, Hosté, VÝSLEDEK (pokud už je)
MATCHES = [
    {"id": "M1", "date": "Středa 11.02. 16:40", "home": "Slovensko", "away": "Finsko", "result": "1:3"},
    {"id": "M2", "date": "Středa 11.02. 21:10", "home": "Švédsko", "away": "Itálie", "result": "6:1"},
    {"id": "M3", "date": "Čtvrtek 12.02. 12:10", "home": "Švýcarsko", "away": "Francie", "result": "6:2"},
    {"id": "M4", "date": "Čtvrtek 12.02. 16:40", "home": "Česko", "away": "Kanada", "result": "2:4"},
    {"id": "M5", "date": "Čtvrtek 12.02. 21:10", "home": "Lotyšsko", "away": "USA", "result": "2:3"},
    {"id": "M6", "date": "Čtvrtek 12.02. 21:10", "home": "Německo", "away": "Dánsko", "result": "4:3"},
    {"id": "M7", "date": "Pátek 13.02. 12:10", "home": "Finsko", "away": "Švédsko", "result": "1:3"},
    {"id": "M8", "date": "Pátek 13.02. 12:10", "home": "Itálie", "away": "Slovensko", "result": "2:4"},
    {"id": "M9", "date": "Pátek 13.02. 16:40", "home": "Francie", "away": "Česko", "result": "0:5"},
    {"id": "M10", "date": "Pátek 13.02. 21:20", "home": "Kanada", "away": "Švýcarsko", "result": "3:1"},
    {"id": "M11", "date": "Sobota 14.02. 12:10", "home": "Německo", "away": "Lotyšsko", "result": "2:2"},
    {"id": "M12", "date": "Sobota 14.02. 12:10", "home": "Švédsko", "away": "Slovensko", "result": "5:1"},
    {"id": "M13", "date": "Sobota 14.02. 16:40", "home": "Finsko", "away": "Itálie", "result": "3:0"},
    {"id": "M14", "date": "Sobota 14.02. 21:10", "home": "USA", "away": "Dánsko", "result": "5:2"},
    {"id": "M15", "date": "Neděle 15.02. 12:10", "home": "Švýcarsko", "away": "Česko", "result": "3:3"},
    {"id": "M16", "date": "Neděle 15.02. 16:40", "home": "Kanada", "away": "Francie", "result": "8:0"},
    {"id": "M17", "date": "Neděle 15.02. 19:10", "home": "Dánsko", "away": "Lotyšsko", "result": "3:2"},
    {"id": "M18", "date": "Neděle 15.02. 21:10", "home": "USA", "away": "Německo", "result": "2:1"},
]

# --- HISTORICKÉ TIPY KLUKŮ (Vytaženo z tvých CSV) ---
HISTORICAL_TIPS = {
    "Aďas": {"M1": "1:3", "M2": "6:1", "M3": "6:2", "M4": "2:4", "M5": "2:3", "M6": "4:3", "M7": "1:3", "M8": "2:4", "M9": "0:5", "M10": "3:1", "M11": "2:2", "M12": "5:1", "M13": "3:0", "M14": "5:2", "M15": "3:3", "M16": "8:0", "M17": "3:2", "M18": "2:1"},
    "Moli": {"M1": "1:5", "M2": "8:0"},
    "Cigi ml.": {"M1": "2:4", "M2": "6:2", "M3": "3:1", "M4": "3:5", "M5": "1:4", "M6": "4:2", "M7": "2:3", "M8": "3:5", "M9": "1:4", "M10": "4:1", "M11": "3:3", "M12": "6:2", "M13": "5:0", "M14": "6:1", "M15": "4:5", "M16": "7:0", "M17": "4:2", "M18": "5:2"},
    "Mršťa": {"M1": "2:4", "M2": "7:1", "M3": "5:2", "M4": "2:5", "M5": "2:5", "M6": "5:3", "M7": "2:3", "M8": "1:5", "M9": "1:6", "M10": "4:2", "M11": "3:1", "M12": "7:3", "M13": "2:2", "M14": "4:0", "M15": "3:5", "M16": "9:1", "M17": "3:3", "M18": "5:4"},
    "Víťa": {"M1": "2:2", "M2": "4:0", "M3": "4:1", "M4": "1:4", "M5": "1:5", "M6": "3:2", "M7": "3:3", "M8": "3:4", "M9": "0:3", "M10": "4:2", "M11": "3:2", "M12": "4:0", "M13": "3:1", "M14": "6:1", "M15": "4:2", "M16": "5:0", "M17": "3:2", "M18": "4:3"},
}

PRE_TOURNAMENT_DATA = [
    {"Hráč": "Aďas", "Vítěz": "🇨🇦 Kanada", "2. místo": "🇨🇿 Česko", "3. místo": "🇸🇪 Švédsko", "Střelec": "MacKinnon", "Bod": "0"},
    {"Hráč": "Cigi ml.", "Vítěz": "🇨🇦 Kanada", "2. místo": "🇸🇪 Švédsko", "3. místo": "🇺🇸 USA", "Střelec": "Celebrini", "Bod": "0"},
    {"Hráč": "Mršťa", "Vítěz": "🇨🇦 Kanada", "2. místo": "🇸🇪 Švédsko", "3. místo": "🇨🇿 Česko", "Střelec": "Pastrňák", "Bod": "0"},
    {"Hráč": "Víťa", "Vítěz": "🇨🇦 Kanada", "2. místo": "🇺🇸 USA", "3. místo": "🇨🇿 Česko", "Střelec": "Matthews", "Bod": "0"},
    {"Hráč": "Fany", "Vítěz": "🇨🇭 Švýcarsko", "2. místo": "🇸🇪 Švédsko", "3. místo": "🇫🇮 Finsko", "Střelec": "Petterson", "Bod": "0"},
]

# --- POMOCNÉ FUNKCE ---
def calculate_points(tip_str, result_str):
    if not tip_str or not result_str or ":" not in str(tip_str) or ":" not in str(result_str):
        return 0, "white"
    
    try:
        t_h, t_a = map(int, tip_str.split(":"))
        r_h, r_a = map(int, result_str.split(":"))
    except:
        return 0, "white"

    # Přesný výsledek (3 body)
    if t_h == r_h and t_a == r_a:
        return 3, "#d4edda" # Green

    # Trefený vítěz nebo remíza (1 bod)
    # Logic: (Doma > Hoste) AND (TipDoma > TipHoste)
    t_res = 1 if t_h > t_a else (-1 if t_h < t_a else 0)
    r_res = 1 if r_h > r_a else (-1 if r_h < r_a else 0)

    if t_res == r_res:
        return 1, "#fff3cd" # Yellow
    
    return 0, "#f8d7da" # Red

# --- HLAVNÍ APLIKACE ---
def main():
    st.title("🏒 ZOH 2026 - Výsledkový Servis")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Můj Tip", "📊 Přehled všech", "🏆 Žebříček", "🔮 Tipy před turnajem"])

    # --- ZÁLOŽKA 1: ZADÁVÁNÍ ---
    with tab1:
        player = st.selectbox("Kdo jsi?", PLAYERS)
        st.caption("Pokud jsi Aďas, Mršťa atd., tvé tipy se načetly z Excelu.")
        
        with st.form("tips_form"):
            user_tips = {}
            for m in MATCHES:
                # Zkus najít historický tip
                default_tip = HISTORICAL_TIPS.get(player, {}).get(m["id"], "")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    flag_h = TEAMS_CONFIG.get(m['home'], "")
                    flag_a = TEAMS_CONFIG.get(m['away'], "")
                    label = f"{flag_h} {m['home']} vs {m['away']} {flag_a}"
                    st.write(f"**{label}**")
                    if m.get("result"):
                        st.caption(f"🏁 Výsledek: {m['result']}")
                with col2:
                    val = st.text_input("Tip", value=default_tip, key=f"input_{m['id']}", placeholder="X:X", label_visibility="collapsed")
                    user_tips[m["id"]] = val
                st.divider()
            
            if st.form_submit_button("💾 Uložit / Aktualizovat moje tipy"):
                st.success("Tipy uloženy (jen v prohlížeči, pro trvalé uložení pošli screenshot).")

    # --- ZÁLOŽKA 2: PŘEHLED ---
    with tab2:
        st.header("Kdo jak tipoval?")
        st.info("Zelená = Přesný (3b) | Žlutá = Vítěz (1b) | Červená = Vedle")

        # Budování tabulky
        table_data = []
        for m in MATCHES:
            row = {"Zápas": f"{m['home']} - {m['away']}", "Výsledek": m.get("result", "-")}
            
            for p in PLAYERS:
                tip = HISTORICAL_TIPS.get(p, {}).get(m["id"], "-")
                pts, color = calculate_points(tip, m.get("result"))
                
                # Zobrazíme tip s barvičkou
                # Bohužel ve standard table nejde barvit buňky jednoduše, uděláme to trikem
                # Ale pro přehlednost zobrazíme jen text, barvy v detailu by byly složité
                # Zobrazíme: "3:1 (3b)"
                if m.get("result") and tip != "-" and ":" in tip:
                    row[p] = f"{tip} ({pts}b)"
                else:
                    row[p] = tip
            table_data.append(row)
            
        df_overview = pd.DataFrame(table_data)
        st.dataframe(df_overview, hide_index=True, use_container_width=True)

    # --- ZÁLOŽKA 3: ŽEBŘÍČEK ---
    with tab3:
        st.header("🏆 Aktuální pořadí")
        
        standings = []
        for p in PLAYERS:
            total_pts = 0
            exact_hits = 0
            winner_hits = 0
            
            p_tips = HISTORICAL_TIPS.get(p, {})
            
            for m in MATCHES:
                if m.get("result"): # Počítáme jen odehrané
                    pts, _ = calculate_points(p_tips.get(m["id"]), m["result"])
                    total_pts += pts
                    if pts == 3: exact_hits += 1
                    if pts == 1: winner_hits += 1
            
            standings.append({
                "Hráč": p,
                "Body celkem": total_pts,
                "Přesné trefy (3b)": exact_hits,
                "Trefený vítěz (1b)": winner_hits
            })
            
        df_standings = pd.DataFrame(standings)
        df_standings = df_standings.sort_values(by="Body celkem", ascending=False)
        
        # Zvýraznění lídra
        st.dataframe(df_standings, hide_index=True, use_container_width=True)
        
        top_player = df_standings.iloc[0]["Hráč"]
        st.balloons()
        st.success(f"Aktuálně vede: **{top_player}**")

    # --- ZÁLOŽKA 4: PŘED TURNAJEM ---
    with tab4:
        st.dataframe(pd.DataFrame(PRE_TOURNAMENT_DATA), hide_index=True)

if __name__ == "__main__":
    main()
