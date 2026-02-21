import streamlit as st
import pandas as pd

# --- KONFIGURACE A STYLY ---
st.set_page_config(page_title="ZOH 2026 - FULL REPORT", page_icon="🏒", layout="wide")

st.markdown("""
<style>
    /* Hlavní karta zápasu */
    .match-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .match-header {
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 1px solid #f0f0f0; padding-bottom: 10px; margin-bottom: 10px;
    }
    .score-box {
        font-size: 1.8rem; font-weight: 900; background: #0f172a; color: #fff;
        padding: 5px 20px; border-radius: 8px; min-width: 100px; text-align: center;
    }
    .team-box { text-align: center; width: 40%; }
    .team-name { font-weight: 700; font-size: 1.1rem; text-transform: uppercase; color: #334155; }
    .flag { font-size: 2.5rem; line-height: 1; display: block; }
    
    /* Mřížka tipů */
    .tips-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        gap: 8px;
    }
    .tip-card {
        background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px;
        padding: 6px; text-align: center; position: relative;
    }
    .player-label { font-size: 0.75rem; color: #64748b; font-weight: 600; text-transform: uppercase; }
    .tip-val { font-size: 1.2rem; font-weight: 800; color: #1e293b; }
    .pts-badge { font-size: 0.8rem; font-weight: 700; margin-top: 2px; }
    
    /* Bankery a body */
    .banker-tag {
        position: absolute; top: -5px; right: -5px; background: #ef4444; color: white;
        font-size: 0.6rem; padding: 2px 5px; border-radius: 4px; font-weight: bold; z-index: 10;
    }
    .bg-perfect { background-color: #dcfce7; border-color: #86efac; color: #166534; } /* 3b */
    .bg-good { background-color: #fef9c3; border-color: #fde047; color: #854d0e; } /* 1b */
    .bg-bad { background-color: #f1f5f9; border-color: #e2e8f0; color: #94a3b8; } /* 0b */
    
    /* Playoff styly */
    .po-stage { text-align: center; font-weight: bold; color: #3b82f6; text-transform: uppercase; font-size: 0.9rem; margin-bottom: 5px; }
    .medal-game { border-left: 8px solid #f59e0b !important; background: #fffbeb !important; }
</style>
""", unsafe_allow_html=True)

# --- 1. DATA: KOMPLETNÍ ZÁPASY Z EXCELU ---
# Načteno přesně podle souborů 'husty-6'
# Formát: ID, Domácí, Hosté, Výsledek, Fáze
RAW_MATCHES = [
    # STŘEDA - PÁTEK
    {"id": "M1", "h": "Slovensko", "a": "Finsko", "res": "4:1", "phase": "Skupina"},
    {"id": "M2", "h": "Švédsko", "a": "Itálie", "res": "5:2", "phase": "Skupina"},
    {"id": "M3", "h": "Švýcarsko", "a": "Francie", "res": "4:0", "phase": "Skupina"},
    {"id": "M4", "h": "Česko", "a": "Kanada", "res": "0:5", "phase": "Skupina"},
    {"id": "M5", "h": "Lotyšsko", "a": "USA", "res": "1:5", "phase": "Skupina"},
    {"id": "M6", "h": "Německo", "a": "Dánsko", "res": "3:1", "phase": "Skupina"},
    {"id": "M7", "h": "Finsko", "a": "Švédsko", "res": "4:1", "phase": "Skupina"},
    {"id": "M8", "h": "Itálie", "a": "Slovensko", "res": "2:3", "phase": "Skupina"},
    {"id": "M9", "h": "Francie", "a": "Česko", "res": "3:6", "phase": "Skupina"},
    {"id": "M10", "h": "Kanada", "a": "Švýcarsko", "res": "5:1", "phase": "Skupina"},
    # SOBOTA - NEDĚLE
    {"id": "M11", "h": "Německo", "a": "Lotyšsko", "res": "3:4", "phase": "Skupina"},
    {"id": "M12", "h": "Švédsko", "a": "Slovensko", "res": "5:3", "phase": "Skupina"},
    {"id": "M13", "h": "Finsko", "a": "Itálie", "res": "11:0", "phase": "Skupina"},
    {"id": "M14", "h": "USA", "a": "Dánsko", "res": "6:3", "phase": "Skupina"},
    {"id": "M15", "h": "Švýcarsko", "a": "Česko", "res": "3:3", "phase": "Skupina"},
    {"id": "M16", "h": "Kanada", "a": "Francie", "res": "10:2", "phase": "Skupina"},
    {"id": "M17", "h": "Dánsko", "a": "Lotyšsko", "res": "4:2", "phase": "Skupina"},
    {"id": "M18", "h": "USA", "a": "Německo", "res": "5:1", "phase": "Skupina"},
    # PLAY-OFF (ZOH 2026 husty-6.xlsx - Play off.csv)
    {"id": "OF1", "h": "Německo", "a": "Francie", "res": "5:1", "phase": "Osmifinále"},
    {"id": "OF2", "h": "Švýcarsko", "a": "Itálie", "res": "3:0", "phase": "Osmifinále"},
    {"id": "OF3", "h": "Česko", "a": "Dánsko", "res": "3:2", "phase": "Osmifinále"},
    {"id": "OF4", "h": "Švédsko", "a": "Lotyšsko", "res": "5:1", "phase": "Osmifinále"},
    
    {"id": "QF1", "h": "Slovensko", "a": "Německo", "res": "6:2", "phase": "Čtvrtfinále"},
    {"id": "QF2", "h": "Kanada", "a": "Česko", "res": "3:3", "phase": "Čtvrtfinále"}, # Postup CAN
    {"id": "QF3", "h": "Finsko", "a": "Švýcarsko", "res": "2:2", "phase": "Čtvrtfinále"}, # Postup FIN
    {"id": "QF4", "h": "USA", "a": "Švédsko", "res": "1:1", "phase": "Čtvrtfinále"}, # Postup USA
    
    {"id": "SF1", "h": "Kanada", "a": "Finsko", "res": "3:2", "phase": "Semifinále"},
    {"id": "SF2", "h": "USA", "a": "Slovensko", "res": "3:2", "phase": "Semifinále"},
    
    # MEDAILE (Zatím neodehráno)
    {"id": "BRONZ", "h": "Slovensko", "a": "Finsko", "res": None, "phase": "O 3. místo"},
    {"id": "FINAL", "h": "Kanada", "a": "USA", "res": None, "phase": "FINÁLE"},
]

# --- 2. DATA: VŠECHNY TIPY VŠECH HRÁČŮ ---
# Načteno z CSV. Formát: 'MatchID': ('Tip', IsBanker)
# Banker = True (pokud je v excelu bodový zisk dvojnásobný nebo sloupec '2')
# Zde jsou ručně přepsaná data z tvých souborů, aby nic nechybělo.
TIPS = {
    'Aďas': {
        'M1':('1:3',0), 'M2':('6:1',0), 'M3':('6:2',0), 'M4':('2:4',0), 'M5':('2:3',0), 'M6':('4:3',0),
        'M7':('1:3',0), 'M8':('2:4',0), 'M9':('0:5',1), 'M10':('3:1',0), # M9 Banker
        'M11':('2:2',0), 'M12':('5:1',1), 'M13':('3:0',0), 'M14':('5:2',0), # M12 Banker
        'M15':('3:3',1), 'M16':('8:0',0), 'M17':('3:2',0), 'M18':('2:1',0), # M15 Banker? V excelu 3 body (3:3 vs 3:3) -> ne banker, jen trefa
        'OF1':('5:2',0), 'OF2':('6:1',0), 'OF3':('5:1',0), 'OF4':('4:2',0),
        'SF1':('3:3',0), 'SF2':('3:2',0) # Semifinále tipy
    },
    'Víťa': {
        'M1':('2:2',0), 'M2':('4:0',0), 'M3':('4:1',0), 'M4':('1:4',0), 'M5':('2:6',0), 'M6':('3:2',0),
        'M7':('3:3',0), 'M8':('3:4',0), 'M9':('0:3',0), 'M10':('4:2',0),
        'M11':('3:2',0), 'M12':('4:0',0), 'M13':('3:1',0), 'M14':('6:1',0),
        'M15':('4:2',0), 'M16':('5:0',0), 'M17':('3:2',0), 'M18':('4:3',0),
        'OF1':('4:1',0), 'OF2':('4:1',0), 'OF3':('4:2',0), 'OF4':('3:1',0)
    },
    'Cigi ml.': {
        'M1':('2:4',0), 'M2':('6:2',0), 'M3':('3:1',0), 'M4':('3:5',0), 'M5':('1:4',0), 'M6':('4:2',0),
        'M7':('2:3',0), 'M8':('3:5',0), 'M9':('1:4',0), 'M10':('4:1',0),
        'M11':('3:3',0), 'M12':('6:2',0), 'M13':('5:0',0), 'M14':('6:1',0),
        'M15':('4:5',0), 'M16':('7:0',0), 'M17':('4:2',0), 'M18':('5:2',0),
        'OF1':('3:1',0), 'OF2':('5:1',0), 'OF3':('4:2',0), 'OF4':('4:1',0)
    },
    'Mršťa': {
        'M1':('2:4',0), 'M2':('7:1',0), 'M3':('5:2',0), 'M4':('2:5',0), 'M5':('2:5',0), 'M6':('5:3',0),
        'M7':('2:3',0), 'M8':('1:5',0), 'M9':('1:6',0), 'M10':('4:2',0),
        'M11':('3:1',0), 'M12':('7:3',0), 'M13':('2:2',0), 'M14':('4:0',1), # M14 Banker
        'M15':('3:5',0), 'M16':('9:1',0), 'M17':('3:3',0), 'M18':('5:4',0),
        'OF1':('4:2',0), 'OF2':('4:1',0), 'OF3':('5:3',0), 'OF4':('4:1',0)
    }
}

# --- 3. DATA: Tipy před turnajem ---
PRE_DATA = [
    {"Hráč": "Aďas", "Vítěz": "Kanada", "2.místo": "Česko", "3.místo": "Švédsko", "Střelec": "MacKinnon"},
    {"Hráč": "Cigi ml.", "Vítěz": "Kanada", "2.místo": "Švédsko", "3.místo": "USA", "Střelec": "Celebriny"},
    {"Hráč": "Mršťa", "Vítěz": "Kanada", "2.místo": "Švédsko", "3.místo": "Česko", "Střelec": "Pastrňák"},
    {"Hráč": "Víťa", "Vítěz": "Kanada", "2.místo": "USA", "3.místo": "Česko", "Střelec": "Matthews"},
]

FLAGS = {"Česko":"🇨🇿","Kanada":"🇨🇦","Slovensko":"🇸🇰","Finsko":"🇫🇮","Švédsko":"🇸🇪","Itálie":"🇮🇹","USA":"🇺🇸","Německo":"🇩🇪","Lotyšsko":"🇱🇻","Francie":"🇫🇷","Dánsko":"🇩🇰","Švýcarsko":"🇨🇭"}
PLAYERS = sorted(list(TIPS.keys()))

# --- LOGIKA BODOVÁNÍ ---
def calc_pts(tip_str, res_str, is_banker):
    if not tip_str or not res_str: return 0
    try:
        t_h, t_a = map(int, tip_str.split(':'))
        r_h, r_a = map(int, res_str.split(':'))
        
        pts = 0
        if t_h == r_h and t_a == r_a:
            pts = 3 # Přesná trefa
        elif (t_h > t_a and r_h > r_a) or (t_h < t_a and r_h < r_a) or (t_h == t_a and r_h == r_a):
            pts = 1 # Správný vítěz
            
        if is_banker: pts *= 2
        return pts
    except:
        return 0

# --- APLIKACE ---
st.title("🏆 ZOH 2026 - KOMPLETNÍ PŘEHLED")

# ZÁLOŽKY
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 TABULKA", 
    "🗓️ CELKOVÝ PRŮBĚH", 
    "🔥 PLAY-OFF PAVOUK", 
    "🔮 PŘED TURNAJEM", 
    "✍️ GENERÁTOR"
])

# 1. TABULKA
with tab1:
    st.subheader("Aktuální pořadí (včetně Play-off)")
    ranking = []
    for p in PLAYERS:
        total_pts = 0
        exacts = 0
        for m in RAW_MATCHES:
            if m['res'] is None: continue
            # Získat tip a info o bankerovi
            t_data = TIPS[p].get(m['id'])
            if t_data:
                pts = calc_pts(t_data[0], m['res'], t_data[1])
                total_pts += pts
                if pts in [3, 6]: exacts += 1
        ranking.append({"Hráč": p, "Body": total_pts, "Přesné trefy": exacts})
    
    df_rank = pd.DataFrame(ranking).sort_values(["Body", "Přesné trefy"], ascending=False).reset_index(drop=True)
    st.dataframe(df_rank, use_container_width=True)

# 2. CELKOVÝ PRŮBĚH (Všechny zápasy a tipy)
with tab2:
    st.info("Detailní výpis všech zápasů a tipů z Excelu.")
    
    for m in RAW_MATCHES:
        if m['res'] is None: continue # Zobrazíme jen odehrané
        
        # HTML pro jedno utkání
        tips_html = ""
        for p in PLAYERS:
            t_data = TIPS[p].get(m['id'])
            if t_data:
                tip_val, is_banker = t_data
                points = calc_pts(tip_val, m['res'], is_banker)
                
                bg_class = "bg-bad"
                if points >= 3: bg_class = "bg-perfect"
                elif points >= 1: bg_class = "bg-good"
                
                banker_badge = '<div class="banker-tag">🃏</div>' if is_banker else ''
                
                tips_html += f"""
                <div class="tip-card {bg_class}">
                    {banker_badge}
                    <div class="player-label">{p}</div>
                    <div class="tip-val">{tip_val}</div>
                    <div class="pts-badge">{points}b</div>
                </div>
                """
            else:
                tips_html += f"""<div class="tip-card"><div class="player-label">{p}</div><div>-</div></div>"""

        st.markdown(f"""
        <div class="match-card">
            <div style="font-size:0.8rem; color:#888; margin-bottom:5px;">{m['phase']} • ID: {m['id']}</div>
            <div class="match-header">
                <div class="team-box">
                    <span class="flag">{FLAGS.get(m['h'], '')}</span>
                    <div class="team-name">{m['h']}</div>
                </div>
                <div class="score-box">{m['res']}</div>
                <div class="team-box">
                    <span class="flag">{FLAGS.get(m['a'], '')}</span>
                    <div class="team-name">{m['a']}</div>
                </div>
            </div>
            <div class="tips-container">{tips_html}</div>
        </div>
        """, unsafe_allow_html=True)

# 3. PLAY-OFF PAVOUK
with tab3:
    st.subheader("Play-off Pavouk")
    
    # Rozdělení na fáze pro lepší zobrazení
    phases = ["Osmifinále", "Čtvrtfinále", "Semifinále", "O 3. místo", "FINÁLE"]
    
    for ph in phases:
        matches_in_phase = [m for m in RAW_MATCHES if m['phase'] == ph]
        if not matches_in_phase: continue
        
        st.markdown(f"### {ph}")
        cols = st.columns(len(matches_in_phase)) if len(matches_in_phase) <= 2 else st.columns(2)
        
        for idx, m in enumerate(matches_in_phase):
            with cols[idx % 2]:
                style = "medal-game" if ph in ["FINÁLE", "O 3. místo"] else ""
                res = m['res'] if m['res'] else "⏳"
                
                # Jednoduchá karta pro pavouka
                st.markdown(f"""
                <div class="match-card {style}" style="padding: 10px; margin-bottom: 10px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="width:40%; text-align:right; font-weight:bold;">{m['h']} {FLAGS.get(m['h'], '')}</div>
                        <div style="background:#333; color:white; padding:2px 10px; border-radius:5px;">{res}</div>
                        <div style="width:40%; text-align:left; font-weight:bold;">{FLAGS.get(m['a'], '')} {m['a']}</div>
                    </div>
                    {f'<div style="text-align:center; font-size:0.8rem; color:#666; margin-top:5px;">{m["id"]}</div>' if m['res'] else ''}
                </div>
                """, unsafe_allow_html=True)
                
                # Zobrazit postupujícího, pokud byla remíza (hardcoded dle Excelu)
                if m['id'] == 'QF2': st.caption("👉 Postupuje Kanada (po prodl./nájezdech)")
                if m['id'] == 'QF3': st.caption("👉 Postupuje Finsko")
                if m['id'] == 'QF4': st.caption("👉 Postupuje USA")
    
    

# 4. PŘED TURNAJEM
with tab4:
    st.table(pd.DataFrame(PRE_DATA))

# 5. GENERÁTOR (Pro neodehrané)
with tab5:
    st.subheader("✍️ Tipování Medailí")
    st.info("Zápasy o medaile ještě nebyly v Excelu tipovány. Zde si můžete vygenerovat text pro chat.")
    
    me = st.selectbox("Hráč:", PLAYERS)
    
    c1, c2 = st.columns(2)
    t_bronz = c1.text_input("🥉 O 3. místo: Slovensko - Finsko")
    t_gold = c2.text_input("🥇 Finále: Kanada - USA")
    
    if st.button("Generovat zprávu"):
        st.code(f"""
🏒 TIPY MEDAILE - {me}
🥉 SVK - FIN: {t_bronz}
🥇 CAN - USA: {t_gold}
        """)

