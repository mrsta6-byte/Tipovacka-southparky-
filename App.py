import streamlit as st
import pandas as pd

# --- KONFIGURACE ---
st.set_page_config(page_title="ZOH 2026 - VÝSLEDKY", page_icon="🏒", layout="wide")

# --- DATA (Hardcoded z tvých souborů) ---

# 1. PŘED TURNAJEM (Kompletní tabulka)
PRE_TOURNAMENT_DATA = [
    {"Hráč": "Aďas", "Vítěz": "Kanada", "2. místo": "Česko", "3. místo": "Švédsko", "4. místo": "Švýcarsko", "Střelec": "MacKinnon", "Nahrávač": "Konecny", "Brankář": "Vladař", "MVP": "MacKinnon"},
    {"Hráč": "Cigi ml.", "Vítěz": "Kanada", "2. místo": "Švédsko", "3. místo": "USA", "4. místo": "Finsko", "Střelec": "Celebriny", "Nahrávač": "McDavid", "Brankář": "Thompson", "MVP": "McDavid"},
    {"Hráč": "Mršťa", "Vítěz": "Kanada", "2. místo": "Švédsko", "3. místo": "Česko", "4. místo": "Švýcarsko", "Střelec": "Pastrňák", "Nahrávač": "Crosby", "Brankář": "Genoni", "MVP": "Crosby"},
    {"Hráč": "Víťa", "Vítěz": "Kanada", "2. místo": "USA", "3. místo": "Česko", "4. místo": "Švédsko", "Střelec": "Matthews", "Nahrávač": "McDavid", "Brankář": "Saros", "MVP": "Raymond"},
    {"Hráč": "Fany", "Vítěz": "Švýcarsko", "2. místo": "Švédsko", "3. místo": "Finsko", "4. místo": "Česko", "Střelec": "Petterson", "Nahrávač": "Ehlers", "Brankář": "Binnington", "MVP": "Josi"},
    # Ostatní (Moli, Cigi, Alesh) neměli v souboru vyplněné předturnajové tipy
]

# 2. VŠECHNY ZÁPASY (Skupiny + Playoff)
# Struktura: ID, Popis, Výsledek, {Hráč: [Tip, Body]}
MATCHES_DATA = [
    # STŘEDA - PÁTEK
    {"id": "G1", "desc": "Slovensko - Finsko", "res": "4:1", "tips": {"Aďas": ["1:3", 0], "Moli": ["-", 0], "Cigi": ["-", 0], "Cigi ml.": ["2:4", 0], "Mršťa": ["2:4", 0], "Víťa": ["2:2", 0], "Alesh": ["-", 0], "Fany": ["-", 0]}},
    {"id": "G2", "desc": "Švédsko - Itálie", "res": "5:2", "tips": {"Aďas": ["6:1", 1], "Moli": ["-", 0], "Cigi": ["-", 0], "Cigi ml.": ["6:2", 1], "Mršťa": ["7:1", 1], "Víťa": ["4:0", 1], "Alesh": ["-", 0], "Fany": ["-", 0]}},
    {"id": "G3", "desc": "Švýcarsko - Francie", "res": "4:0", "tips": {"Aďas": ["6:2", 1], "Moli": ["-", 0], "Cigi": ["-", 0], "Cigi ml.": ["3:1", 1], "Mršťa": ["5:2", 1], "Víťa": ["4:1", 1], "Alesh": ["-", 0], "Fany": ["-", 0]}},
    {"id": "G4", "desc": "Česko - Kanada", "res": "0:5", "tips": {"Aďas": ["2:4", 1], "Moli": ["-", 0], "Cigi": ["-", 0], "Cigi ml.": ["3:5", 1], "Mršťa": ["2:5", 1], "Víťa": ["1:4", 1], "Alesh": ["-", 0], "Fany": ["-", 0]}},
    {"id": "G5", "desc": "Lotyšsko - USA", "res": "1:5", "tips": {"Aďas": ["2:3", 1], "Moli": ["-", 0], "Cigi": ["-", 0], "Cigi ml.": ["1:4", 1], "Mršťa": ["2:5", 1], "Víťa": ["2:6", 1], "Alesh": ["-", 0], "Fany": ["-", 0]}},
    {"id": "G6", "desc": "Německo - Dánsko", "res": "3:1", "tips": {"Aďas": ["4:3", 1], "Moli": ["-", 0], "Cigi": ["-", 0], "Cigi ml.": ["4:2", 1], "Mršťa": ["5:3", 1], "Víťa": ["3:2", 1], "Alesh": ["-", 0], "Fany": ["-", 0]}},
    {"id": "G7", "desc": "Finsko - Švédsko", "res": "4:1", "tips": {"Aďas": ["1:3", 0], "Moli": ["-", 0], "Cigi": ["-", 0], "Cigi ml.": ["2:3", 0], "Mršťa": ["2:3", 0], "Víťa": ["3:3", 0], "Alesh": ["-", 0], "Fany": ["-", 0]}},
    {"id": "G8", "desc": "Itálie - Slovensko", "res": "2:3", "tips": {"Aďas": ["2:4", 1], "Moli": ["-", 0], "Cigi": ["-", 0], "Cigi ml.": ["3:5", 1], "Mršťa": ["1:5", 1], "Víťa": ["3:4", 1], "Alesh": ["-", 0], "Fany": ["-", 0]}},
    {"id": "G9", "desc": "Francie - Česko", "res": "3:6", "tips": {"Aďas": ["0:5", 2], "Moli": ["-", 0], "Cigi": ["-", 0], "Cigi ml.": ["1:4", 1], "Mršťa": ["1:6", 1], "Víťa": ["0:3", 1], "Alesh": ["-", 0], "Fany": ["-", 0]}},
    {"id": "G10", "desc": "Kanada - Švýcarsko", "res": "5:1", "tips": {"Aďas": ["3:1", 1], "Moli": ["-", 0], "Cigi": ["-", 0], "Cigi ml.": ["4:1", 1], "Mršťa": ["4:2", 1], "Víťa": ["4:2", 1], "Alesh": ["-", 0], "Fany": ["-", 0]}},
    
    # SOBOTA - NEDĚLE
    {"id": "G11", "desc": "Německo - Lotyšsko", "res": "3:4", "tips": {"Aďas": ["2:2", 0], "Cigi ml.": ["3:3", 0], "Mršťa": ["3:1", 0], "Víťa": ["3:2", 0]}},
    {"id": "G12", "desc": "Švédsko - Slovensko", "res": "5:3", "tips": {"Aďas": ["5:1", 2], "Cigi ml.": ["6:2", 1], "Mršťa": ["7:3", 1], "Víťa": ["4:0", 1]}},
    {"id": "G13", "desc": "Finsko - Itálie", "res": "11:0", "tips": {"Aďas": ["3:0", 1], "Cigi ml.": ["5:0", 1], "Mršťa": ["2:2", 0], "Víťa": ["3:1", 1]}},
    {"id": "G14", "desc": "USA - Dánsko", "res": "6:3", "tips": {"Aďas": ["5:2", 1], "Cigi ml.": ["6:1", 1], "Mršťa": ["4:0", 2], "Víťa": ["6:1", 1]}},
    {"id": "G15", "desc": "Švýcarsko - Česko", "res": "3:3", "tips": {"Aďas": ["3:3", 3], "Cigi ml.": ["4:5", 0], "Mršťa": ["3:5", 0], "Víťa": ["4:2", 0]}},
    {"id": "G16", "desc": "Kanada - Francie", "res": "10:2", "tips": {"Aďas": ["8:0", 1], "Cigi ml.": ["7:0", 1], "Mršťa": ["9:1", 1], "Víťa": ["5:0", 1]}},
    {"id": "G17", "desc": "Dánsko - Lotyšsko", "res": "4:2", "tips": {"Aďas": ["3:2", 1], "Cigi ml.": ["4:2", 1], "Mršťa": ["3:3", 0], "Víťa": ["3:2", 1]}},
    {"id": "G18", "desc": "USA - Německo", "res": "5:1", "tips": {"Aďas": ["2:1", 1], "Cigi ml.": ["5:2", 1], "Mršťa": ["5:4", 1], "Víťa": ["4:3", 1]}},

    # PLAY-OFF
    {"id": "PO1", "desc": "Německo - Francie", "res": "5:1", "phase": "Osmifinále", "tips": {"Aďas": ["5:2", 1], "Cigi ml.": ["4:3", 1], "Mršťa": ["3:1", 1], "Víťa": ["5:3", 1]}},
    {"id": "PO2", "desc": "Švýcarsko - Itálie", "res": "3:0", "phase": "Osmifinále", "tips": {"Aďas": ["6:1", 1], "Cigi ml.": ["5:2", 1], "Mršťa": ["6:2", 1], "Víťa": ["5:1", 1]}},
    {"id": "PO3", "desc": "Česko - Dánsko", "res": "3:2", "phase": "Osmifinále", "tips": {"Aďas": ["5:1", 1], "Cigi ml.": ["4:2", 1], "Mršťa": ["6:3", 1], "Víťa": ["4:3", 1]}},
    {"id": "PO4", "desc": "Švédsko - Lotyšsko", "res": "5:1", "phase": "Osmifinále", "tips": {"Aďas": ["4:2", 1], "Cigi ml.": ["5:3", 1], "Mršťa": ["5:3", 1], "Víťa": ["2:1", 1]}},
    
    {"id": "PO5", "desc": "Slovensko - Německo", "res": "6:2", "phase": "Čtvrtfinále", "tips": {"Aďas": ["-", 0], "Cigi ml.": ["4:3", 1], "Mršťa": ["5:5", 0], "Víťa": ["-", 0]}},
    {"id": "PO6", "desc": "Kanada - Česko", "res": "3:3", "phase": "Čtvrtfinále", "tips": {"Aďas": ["-", 0], "Cigi ml.": ["5:1", 0], "Mršťa": ["7:2", 0], "Víťa": ["-", 0]}},
    {"id": "PO7", "desc": "Finsko - Švýcarsko", "res": "2:2", "phase": "Čtvrtfinále", "tips": {"Aďas": ["-", 0], "Cigi ml.": ["4:4", 0], "Mršťa": ["1:3", 0], "Víťa": ["-", 0]}},
    {"id": "PO8", "desc": "USA - Švédsko", "res": "1:1", "phase": "Čtvrtfinále", "tips": {"Aďas": ["4:2", 0], "Cigi ml.": ["3:5", 0], "Mršťa": ["3:3", 0], "Víťa": ["5:4", 0]}},
    
    {"id": "PO9", "desc": "Kanada - Finsko", "res": "3:2", "phase": "Semifinále", "tips": {"Aďas": ["3:2", 3], "Cigi ml.": ["6:1", 1], "Mršťa": ["3:3", 0], "Víťa": ["4:4", 0]}},
    {"id": "PO10", "desc": "USA - Slovensko", "res": "6:2", "phase": "Semifinále", "tips": {"Aďas": ["3:2", 1], "Cigi ml.": ["4:2", 1], "Mršťa": ["3:5", 0], "Víťa": ["3:3", 0]}},
]

# --- STYLY ---
st.markdown("""
<style>
    .match-card { background: white; border-radius: 10px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #0044cc; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .po-card { background: white; border-radius: 10px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #ffaa00; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .score { font-size: 1.5rem; font-weight: bold; background: #222; color: white; padding: 2px 10px; border-radius: 5px; }
    .pts-badge { font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 0.9rem; }
    .pts-3 { background: #d4edda; color: #155724; }
    .pts-1 { background: #fff3cd; color: #856404; }
    .pts-0 { background: #f8d7da; color: #721c24; }
    .header-row { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 10px; }
    .tip-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 10px; }
    .tip-box { background: #f9f9f9; padding: 5px; border-radius: 5px; text-align: center; border: 1px solid #eee; }
</style>
""", unsafe_allow_html=True)

# --- APLIKACE ---
st.title("🏆 ZOH 2026 - TIPOVAČKA (FINÁLNÍ DATA)")

tabs = st.tabs(["📊 TABULKA", "🗓️ ZÁPASY & BODY", "🔥 PLAY-OFF", "🔮 PŘED TURNAJEM"])

# 1. TABULKA
with tabs[0]:
    st.header("Celkové pořadí")
    
    # Seznam všech hráčů
    all_players = set()
    for m in MATCHES_DATA:
        all_players.update(m.get("tips", {}).keys())
    
    # Výpočet bodů
    ranking = []
    for p in all_players:
        total = 0
        exacts = 0
        match_wins = 0
        for m in MATCHES_DATA:
            if p in m["tips"]:
                tip, pts = m["tips"][p]
                total += pts
                if pts >= 3: exacts += 1
                elif pts > 0: match_wins += 1
        
        ranking.append({"Hráč": p, "Body": total, "Přesné trefy": exacts})
    
    df_rank = pd.DataFrame(ranking).sort_values(["Body", "Přesné trefy"], ascending=False).reset_index(drop=True)
    
    # Podbarvení top 3
    def highlight_rows(row):
        if row.name == 0: return ['background-color: gold'] * len(row)
        if row.name == 1: return ['background-color: silver'] * len(row)
        if row.name == 2: return ['background-color: #cd7f32'] * len(row)
        return [''] * len(row)

    st.dataframe(df_rank.style.apply(highlight_rows, axis=1), use_container_width=True)

# 2. DETAIL ZÁPASŮ
with tabs[1]:
    st.header("Detailní přehled zápasů")
    for m in MATCHES_DATA:
        if "phase" in m: continue # Playoff dáme vedle
        
        with st.container():
            st.markdown(f"""
            <div class="match-card">
                <div class="header-row">
                    <span style="font-weight:bold; font-size:1.1rem;">{m['desc']}</span>
                    <span class="score">{m['res']}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Tipy
            cols = st.columns(4)
            idx = 0
            for p, val in m["tips"].items():
                tip, pts = val
                if tip == "-": continue
                
                color_class = "pts-3" if pts >= 3 else ("pts-1" if pts > 0 else "pts-0")
                with cols[idx % 4]:
                    st.markdown(f"""
                    <div class="tip-box">
                        <div style="font-size:0.8rem; color:#666;">{p}</div>
                        <div style="font-weight:bold;">{tip}</div>
                        <div class="pts-badge {color_class}">{pts}b</div>
                    </div>
                    """, unsafe_allow_html=True)
                idx += 1
            st.markdown("</div>", unsafe_allow_html=True)

# 3. PLAY-OFF
with tabs[2]:
    st.header("Play-off Pavouk")
    po_matches = [m for m in MATCHES_DATA if "phase" in m]
    
    for m in po_matches:
        st.markdown(f"### {m['phase']}")
        st.markdown(f"""
        <div class="po-card">
            <div class="header-row">
                <span style="font-weight:bold; font-size:1.1rem;">{m['desc']}</span>
                <span class="score">{m['res']}</span>
            </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(4)
        idx = 0
        for p, val in m["tips"].items():
            tip, pts = val
            if tip == "-": continue
            
            color_class = "pts-3" if pts >= 3 else ("pts-1" if pts > 0 else "pts-0")
            with cols[idx % 4]:
                st.markdown(f"""
                <div class="tip-box">
                    <div style="font-size:0.8rem; color:#666;">{p}</div>
                    <div style="font-weight:bold;">{tip}</div>
                    <div class="pts-badge {color_class}">{pts}b</div>
                </div>
                """, unsafe_allow_html=True)
            idx += 1
        st.markdown("</div>", unsafe_allow_html=True)

# 4. PŘED TURNAJEM
with tabs[3]:
    st.header("Tipy před turnajem (Kompletní)")
    st.dataframe(pd.DataFrame(PRE_TOURNAMENT_DATA), use_container_width=True)

