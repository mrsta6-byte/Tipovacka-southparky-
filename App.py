import streamlit as st
import pandas as pd

# --- KONFIGURACE APLIKACE ---
st.set_page_config(page_title="ZOH 2026 Tipovačka", page_icon="🏒", layout="wide")

# --- CSS STYLY PRO KRÁSNÝ VZHLED ---
st.markdown("""
    <style>
    .big-flag { font-size: 2.5rem; line-height: 1; }
    .team-name { font-weight: bold; font-size: 1.2rem; }
    .score-badge { 
        font-size: 1.5rem; font-weight: bold; 
        background: #f0f2f6; padding: 5px 15px; border-radius: 8px; 
        color: #31333F; border: 1px solid #ddd;
    }
    .match-card {
        background: white; border-radius: 12px; padding: 15px; margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;
    }
    .player-tip-box {
        text-align: center; font-size: 0.9rem; padding: 4px; border-radius: 4px; margin: 2px;
    }
    /* Barvy pro body */
    .points-3 { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; font-weight: bold; }
    .points-1 { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
    .points-0 { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; opacity: 0.7; }
    </style>
""", unsafe_allow_html=True)

# --- DATA: ZÁPASY A VÝSLEDKY (Vše z tvé tabulky) ---
MATCHES = [
    # Středa - Pátek
    {"id": "M1", "date": "Středa 11.02. 16:40", "home": "Slovensko", "away": "Finsko", "result": "1:3"},
    {"id": "M2", "date": "Středa 11.02. 21:10", "home": "Švédsko", "away": "Itálie", "result": "6:1"},
    {"id": "M3", "date": "Čtvrtek 12.02 12:10", "home": "Švýcarsko", "away": "Francie", "result": "6:2"},
    {"id": "M4", "date": "Čtvrtek 12.02 16:40", "home": "Česko", "away": "Kanada", "result": "2:4"},
    {"id": "M5", "date": "Čtvrtek 12.02 21:10", "home": "Lotyšsko", "away": "USA", "result": "2:3"},
    {"id": "M6", "date": "Čtvrtek 12.02 21:10", "home": "Německo", "away": "Dánsko", "result": "4:3"},
    {"id": "M7", "date": "Pátek 13.02. 12:10", "home": "Finsko", "away": "Švédsko", "result": "1:3"},
    {"id": "M8", "date": "Pátek 13.02. 12:10", "home": "Itálie", "away": "Slovensko", "result": "2:4"},
    {"id": "M9", "date": "Pátek 13.02. 16:40", "home": "Francie", "away": "Česko", "result": "0:5"},
    {"id": "M10", "date": "Pátek 13.02. 21:20", "home": "Kanada", "away": "Švýcarsko", "result": "3:1"},
    # Sobota - Neděle
    {"id": "M11", "date": "Sobota 14.02. 12:10", "home": "Německo", "away": "Lotyšsko", "result": "2:2"},
    {"id": "M12", "date": "Sobota 14.02. 12:10", "home": "Švédsko", "away": "Slovensko", "result": "5:1"},
    {"id": "M13", "date": "Sobota 14.02. 16:40", "home": "Finsko", "away": "Itálie", "result": "3:0"},
    {"id": "M14", "date": "Sobota 14.02. 21:10", "home": "USA", "away": "Dánsko", "result": "5:2"},
    {"id": "M15", "date": "Neděle 15.02. 12:10", "home": "Švýcarsko", "away": "Česko", "result": "3:3"}, # Tady je ta remíza!
    {"id": "M16", "date": "Neděle 15.02. 16:40", "home": "Kanada", "away": "Francie", "result": "8:0"},
    {"id": "M17", "date": "Neděle 15.02. 19:10", "home": "Dánsko", "away": "Lotyšsko", "result": "3:2"},
    {"id": "M18", "date": "Neděle 15.02. 21:10", "home": "USA", "away": "Německo", "result": "2:1"},
]

# --- DATA: TIPY HRÁČŮ (Z tvých tabulek) ---
PLAYER_TIPS = {
    'Aďas': {'M1': '1:3', 'M2': '6:1', 'M3': '6:2', 'M4': '2:4', 'M5': '2:3', 'M6': '4:3', 'M7': '1:3', 'M8': '2:4', 'M9': '0:5', 'M10': '3:1', 'M11': '2:2', 'M12': '5:1', 'M13': '3:0', 'M14': '5:2', 'M15': '3:3', 'M16': '8:0', 'M17': '3:2', 'M18': '2:1'},
    'Moli': {'M1': '1:5', 'M2': '8:0'},
    'Cigi ml.': {'M1': '2:4', 'M2': '6:2', 'M3': '3:1', 'M4': '3:5', 'M5': '1:4', 'M6': '4:2', 'M7': '2:3', 'M8': '3:5', 'M9': '1:4', 'M10': '4:1', 'M11': '3:3', 'M12': '6:2', 'M13': '5:0', 'M14': '6:1', 'M15': '4:5', 'M16': '7:0', 'M17': '4:2', 'M18': '5:2'},
    'Mršťa': {'M1': '2:4', 'M2': '7:1', 'M3': '5:2', 'M4': '2:5', 'M5': '2:5', 'M6': '5:3', 'M7': '2:3', 'M8': '1:5', 'M9': '1:6', 'M10': '4:2', 'M11': '3:1', 'M12': '7:3', 'M13': '2:2', 'M14': '4:0', 'M15': '3:5', 'M16': '9:1', 'M17': '3:3', 'M18': '5:4'},
    'Víťa': {'M1': '2:2', 'M2': '4:0', 'M3': '4:1', 'M4': '1:4', 'M5': '1:5', 'M6': '3:2', 'M7': '3:3', 'M8': '3:4', 'M9': '0:3', 'M10': '4:2', 'M11': '3:2', 'M12': '4:0', 'M13': '3:1', 'M14': '6:1', 'M15': '4:2', 'M16': '5:0', 'M17': '3:2', 'M18': '4:3'},
    # Ostatní zatím bez dat, ale připravení
    'Cigi': {}, 'Alesh': {}, 'Fany': {}
}

# --- DATA: TIPY PŘED TURNAJEM (Kompletní) ---
PRE_TIPS = [
    {'Hráč': 'Aďas', 'Vítěz': 'Kanada', '2. místo': 'Česko', '3. místo': 'Švédsko', '4. místo': 'Švýcarsko', 'Střelec': 'MacKinnon', 'Nahrávač': 'Konecny', 'Brankář': 'Vladař', 'MVP': 'MacKinnon'},
    {'Hráč': 'Cigi ml.', 'Vítěz': 'Kanada', '2. místo': 'Švédsko', '3. místo': 'USA', '4. místo': 'Finsko', 'Střelec': 'Celebrini', 'Nahrávač': 'McDavid', 'Brankář': 'Thompson', 'MVP': 'McDavid'},
    {'Hráč': 'Mršťa', 'Vítěz': 'Kanada', '2. místo': 'Švédsko', '3. místo': 'Česko', '4. místo': 'Švýcarsko', 'Střelec': 'Pastrňák', 'Nahrávač': 'Crosby', 'Brankář': 'Genoni', 'MVP': 'Crosby'},
    {'Hráč': 'Víťa', 'Vítěz': 'Kanada', '2. místo': 'USA', '3. místo': 'Česko', '4. místo': 'Švédsko', 'Střelec': 'Matthews', 'Nahrávač': 'McDavid', 'Brankář': 'Saros', 'MVP': 'Raymond'},
    {'Hráč': 'Fany', 'Vítěz': 'Švýcarsko', '2. místo': 'Švédsko', '3. místo': 'Finsko', '4. místo': 'Česko', 'Střelec': 'Petterson', 'Nahrávač': 'Ehlers', 'Brankář': 'Binnington', 'MVP': 'Josi'},
    {'Hráč': 'Moli', 'Vítěz': '-', '2. místo': '-', '3. místo': '-', '4. místo': '-', 'Střelec': '-', 'Nahrávač': '-', 'Brankář': '-', 'MVP': '-'},
    {'Hráč': 'Cigi', 'Vítěz': '-', '2. místo': '-', '3. místo': '-', '4. místo': '-', 'Střelec': '-', 'Nahrávač': '-', 'Brankář': '-', 'MVP': '-'},
    {'Hráč': 'Alesh', 'Vítěz': '-', '2. místo': '-', '3. místo': '-', '4. místo': '-', 'Střelec': '-', 'Nahrávač': '-', 'Brankář': '-', 'MVP': '-'}
]

# Všechny unikátní jména hráčů
PLAYERS = sorted([p['Hráč'] for p in PRE_TIPS])

TEAMS_FLAGS = {
    "Česko": "🇨🇿", "Kanada": "🇨🇦", "Slovensko": "🇸🇰", "Finsko": "🇫🇮",
    "Švédsko": "🇸🇪", "USA": "🇺🇸", "Švýcarsko": "🇨🇭", "Německo": "🇩🇪",
    "Itálie": "🇮🇹", "Lotyšsko": "🇱🇻", "Francie": "🇫🇷", "Dánsko": "🇩🇰"
}

# --- LOGIKA VÝPOČTU BODŮ ---
def calculate_points(tip_str, result_str):
    if not tip_str or not result_str or ":" not in str(tip_str) or ":" not in str(result_str):
        return 0
    try:
        t_h, t_a = map(int, tip_str.split(":"))
        r_h, r_a = map(int, result_str.split(":"))
        
        # 3 body: Přesný výsledek
        if t_h == r_h and t_a == r_a:
            return 3
        
        # 1 bod: Správný vítěz nebo remíza
        t_res = 1 if t_h > t_a else (0 if t_h == t_a else -1)
        r_res = 1 if r_h > r_a else (0 if r_h == r_a else -1)
        
        if t_res == r_res:
            return 1
        return 0
    except:
        return 0

# --- HLAVNÍ APLIKACE ---
def main():
    st.title("🏒 ZOH 2026 - CENTRÁLA")
    
    tab1, tab2, tab3 = st.tabs(["🏆 CELKOVÉ POŘADÍ", "📊 ZÁPASY A BODY", "🔮 TIPY PŘED TURNAJEM"])

    # 1. TABULKA - POŘADÍ
    with tab1:
        st.markdown("### 🥇 Aktuální žebříček")
        ranking = []
        for p in PLAYERS:
            total_pts = 0
            exact_hits = 0
            winner_hits = 0
            p_tips = PLAYER_TIPS.get(p, {})
            
            for m in MATCHES:
                if m.get('result'):
                    pts = calculate_points(p_tips.get(m['id']), m['result'])
                    total_pts += pts
                    if pts == 3: exact_hits += 1
                    if pts == 1: winner_hits += 1
            
            ranking.append({
                "Hráč": p, 
                "Body": total_pts, 
                "Přesné trefy (3b)": exact_hits,
                "Trefený vítěz (1b)": winner_hits
            })
        
        df_rank = pd.DataFrame(ranking).sort_values(by=["Body", "Přesné trefy (3b)"], ascending=False).reset_index(drop=True)
        
        # Stylování tabulky
        st.dataframe(
            df_rank, 
            use_container_width=True,
            height=350,
            column_config={
                "Body": st.column_config.ProgressColumn("Body", format="%d", min_value=0, max_value=60),
            }
        )
        
        if not df_rank.empty:
            leader = df_rank.iloc[0]['Hráč']
            pts = df_rank.iloc[0]['Body']
            st.success(f"👑 Králem tipovačky je zatím **{leader}** se ziskem **{pts} bodů**!")

    # 2. TABULKA - PŘEHLED ZÁPASŮ
    with tab2:
        st.markdown("### 🏒 Detailní rozpis zápasů")
        
        for m in MATCHES:
            res = m.get('result', '---')
            fh = TEAMS_FLAGS.get(m['home'], "")
            fa = TEAMS_FLAGS.get(m['away'], "")
            
            # Karta zápasu
            st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="text-align:center; min-width:80px;">
                        <div class="big-flag">{fh}</div>
                        <div class="team-name">{m['home']}</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:gray; font-size:0.8rem; margin-bottom:5px;">{m['date']}</div>
                        <div class="score-badge">{res}</div>
                    </div>
                    <div style="text-align:center; min-width:80px;">
                        <div class="big-flag">{fa}</div>
                        <div class="team-name">{m['away']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Tipy hráčů pod zápasem
            cols = st.columns(len(PLAYERS))
            for i, p in enumerate(PLAYERS):
                tip = PLAYER_TIPS.get(p, {}).get(m['id'], "-")
                pts = calculate_points(tip, res)
                
                css_class = "points-0"
                pts_label = "0b"
                if res != "---" and tip != "-" and ":" in tip:
                    if pts == 3: 
                        css_class = "points-3"
                        pts_label = "3b"
                    elif pts == 1: 
                        css_class = "points-1"
                        pts_label = "1b"
                else:
                    css_class = ""
                    pts_label = ""

                with cols[i]:
                    st.markdown(f"""
                    <div class="player-tip-box {css_class}">
                        <div style="font-weight:bold; font-size:0.75rem; margin-bottom:2px;">{p}</div>
                        <div>{tip} <span style="font-size:0.7rem;">{pts_label}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    # 3. TABULKA - DLOUHODOBÉ TIPY
    with tab3:
        st.markdown("### 🔮 Kdo co tipoval před turnajem?")
        df_pre = pd.DataFrame(PRE_TIPS)
        
        # Zobrazení s fixnutými sloupci
        st.dataframe(
            df_pre,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Vítěz": st.column_config.TextColumn("🥇 Vítěz", width="medium"),
                "2. místo": st.column_config.TextColumn("🥈 2. místo", width="medium"),
                "3. místo": st.column_config.TextColumn("🥉 3. místo", width="medium"),
                "Střelec": st.column_config.TextColumn("🏒 Střelec", width="medium"),
                "Brankář": st.column_config.TextColumn("🧱 Brankář", width="medium"),
                "MVP": st.column_config.TextColumn("⭐ MVP", width="medium"),
            }
        )

if __name__ == "__main__":
    main()
