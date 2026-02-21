import streamlit as st
import pandas as pd
import numpy as np

# --- KONFIGURACE ---
st.set_page_config(page_title="ZOH 2026 - FULL STATS", page_icon="🏒", layout="wide")

# --- CSS STYLY PRO PŘEHLEDNOST ---
st.markdown("""
<style>
    .match-header {
        background-color: #f0f2f6; padding: 10px; border-radius: 10px 10px 0 0;
        border-bottom: 2px solid #ddd; display: flex; justify-content: space-between; align-items: center;
    }
    .match-body {
        border: 1px solid #ddd; border-top: none; border-radius: 0 0 10px 10px;
        padding: 10px; background-color: white; margin-bottom: 20px;
    }
    .score-big { font-size: 1.5rem; font-weight: bold; background: #333; color: white; padding: 2px 12px; border-radius: 5px; }
    .tip-row { 
        display: flex; justify-content: space-between; border-bottom: 1px solid #eee; padding: 4px 0; font-size: 0.95rem;
    }
    .tip-row:last-child { border-bottom: none; }
    .points-3 { color: #155724; background-color: #d4edda; font-weight: bold; padding: 0 5px; border-radius: 4px; }
    .points-1 { color: #856404; background-color: #fff3cd; font-weight: bold; padding: 0 5px; border-radius: 4px; }
    .points-0 { color: #721c24; background-color: #f8d7da; padding: 0 5px; border-radius: 4px; }
    .banker-icon { color: red; font-weight: bold; margin-left: 5px; }
    .total-row { font-weight: bold; background-color: #e6f3ff; }
</style>
""", unsafe_allow_html=True)

# --- FUNKCE PRO NAČÍTÁNÍ DAT ---
def clean_score(val):
    """Opraví formát skóre (např. z Excel času 04:01:00 na 4:1)"""
    if pd.isna(val): return None
    s = str(val).strip()
    if s == 'nan' or s == '': return None
    # Oprava času z Excelu
    if s.count(':') == 2:
        parts = s.split(':')
        try:
            return f"{int(parts[0])}:{int(parts[1])}"
        except:
            return s
    return s

def parse_csv_data(filename, phase_label):
    """
    Univerzální funkce pro načtení dat.
    Předpoklad:
    Row 2 (index): Hlavička zápasu (Datum, Týmy)
    Row 3 (index): Výsledek
    Row 4+ (index): Hráči
    Sloupce: Sudé = Tip, Liché (Sudé+1) = Body
    """
    try:
        df = pd.read_csv(filename, header=None)
    except Exception as e:
        st.error(f"Chyba při čtení souboru {filename}: {e}")
        return [], {}

    matches = []
    player_data = {} # {Player: {MatchID: {tip: str, pts: float}}}

    # 1. Najít zápasy (procházíme sloupce od indexu 2)
    # Hledáme sloupce, kde je v řádku 2 text (info o zápase)
    for col in range(2, df.shape[1]):
        # Kontrola: Je to sloupec s tipem? (Obvykle sudé indexy 2, 4, 6...)
        # Musíme ověřit, zda je vedle sloupec s body.
        
        raw_header = df.iloc[2, col]
        if pd.isna(raw_header): continue
        
        # Pokud je to sloupec s body (číslo, ne text zápasu), přeskočíme
        # Ale text zápasu je často rozbitý na více řádků.
        header_str = str(raw_header)
        if len(header_str) < 5: continue # Příliš krátké na popis zápasu

        # ID zápasu
        m_id = f"{phase_label}_{col}"
        
        # Parsování týmů a data
        # Formát obvykle: "Datum\nČas\nDomácí - \nHosté"
        parts = header_str.replace('\r', '').split('\n')
        teams = "Neznámý zápas"
        date = ""
        
        if len(parts) >= 1:
            # Hledáme řádek s pomlčkou "-" pro týmy
            team_part = next((p for p in parts if "-" in p), None)
            if team_part:
                teams = team_part.replace("-", "vs").strip()
            # Pokud je tam "vs" rozděleno novým řádkem (z Excelu), zkusíme spojit
            else:
                 # Fallback: vezmeme poslední části
                 teams = header_str.replace('\n', ' ')

        # Výsledek (o řádek níž)
        res_raw = df.iloc[3, col]
        result = clean_score(res_raw)

        matches.append({
            'id': m_id,
            'desc': header_str.replace('\n', ' '), # Celý popis pro zobrazení
            'teams': teams,
            'result': result,
            'col_tip': col,
            'col_pts': col + 1, # Předpoklad: body jsou hned vedle
            'phase': phase_label
        })

    # 2. Načíst tipy hráčů
    # Hráči začínají od řádku index 4
    for r in range(4, df.shape[0]):
        p_name = df.iloc[r, 1] # Jméno je ve sloupci 1 (B)
        if pd.isna(p_name) or str(p_name).strip() == "": continue
        
        p_name = str(p_name).strip()
        if p_name not in player_data: player_data[p_name] = {}

        for m in matches:
            # Načíst tip
            if m['col_tip'] < df.shape[1]:
                tip_val = clean_score(df.iloc[r, m['col_tip']])
            else:
                tip_val = None
            
            # Načíst body (pokud existuje sloupec)
            pts_val = 0
            if m['col_pts'] < df.shape[1]:
                try:
                    p_raw = df.iloc[r, m['col_pts']]
                    pts_val = float(p_raw) if pd.notna(p_raw) else 0
                except:
                    pts_val = 0
            
            player_data[p_name][m['id']] = {
                'tip': tip_val,
                'pts': pts_val
            }

    return matches, player_data

# --- NAČTENÍ SOUBORŮ ---
# Používáme názvy souborů, které jsi nahrál
m1, p1 = parse_csv_data('ZOH 2026 husty-6.xlsx - středa - pátek.csv', 'Skupina A')
m2, p2 = parse_csv_data('ZOH 2026 husty-6.xlsx - sobota - neděle.csv', 'Skupina B')
m3, p3 = parse_csv_data('ZOH 2026 husty-6.xlsx - Play off.csv', 'Play-off')

# Sloučení dat
ALL_MATCHES = m1 + m2 + m3
ALL_PLAYERS = set(list(p1.keys()) + list(p2.keys()) + list(p3.keys()))

# Sloučení tipů do jednoho slovníku
MASTER_DATA = {player: {} for player in ALL_PLAYERS}
for p in ALL_PLAYERS:
    if p in p1: MASTER_DATA[p].update(p1[p])
    if p in p2: MASTER_DATA[p].update(p2[p])
    if p in p3: MASTER_DATA[p].update(p3[p])

# --- PŘED TURNAJEM ---
def load_pre_tournament():
    try:
        df = pd.read_csv('ZOH 2026 husty-6.xlsx - Tipy před Turnajem.csv', header=None)
        # Ořízneme prázdné řádky nahoře (hledáme hlavičku "Vítěz")
        start_row = 0
        for i in range(10):
            row_vals = df.iloc[i].astype(str).values
            if "Vítěz" in " ".join(row_vals):
                start_row = i
                break
        
        # Načteme data od hlavičky dolů
        clean_df = df.iloc[start_row:].reset_index(drop=True)
        # První řádek jako header
        clean_df.columns = clean_df.iloc[0]
        clean_df = clean_df[1:]
        # Vyhodíme prázdné sloupce
        clean_df = clean_df.dropna(axis=1, how='all')
        # Vyhodíme řádky kde není jméno hráče (sloupec 1)
        clean_df = clean_df[clean_df.iloc[:, 1].notna()]
        return clean_df
    except:
        return pd.DataFrame()

df_pre = load_pre_tournament()

# --- APLIKACE: UI ---

st.title("🏆 ZOH 2026 - Kompletní Přehled")

tabs = st.tabs(["📊 CELKOVÁ TABULKA", "🗓️ ZÁPASY & BODY (DETAIL)", "🔮 PŘED TURNAJEM", "🔥 PLAY-OFF PAVOUK"])

# 1. TABULKA
with tabs[0]:
    st.header("Celkové pořadí")
    ranking = []
    for p in ALL_PLAYERS:
        total = 0
        exact_hits = 0
        match_hits = 0
        for m in ALL_MATCHES:
            data = MASTER_DATA[p].get(m['id'])
            if data:
                pts = data['pts']
                total += pts
                if pts >= 3: exact_hits += 1 # Předpoklad: 3 a víc bodů je přesná
                elif pts > 0: match_hits += 1
        
        ranking.append({
            "Hráč": p,
            "Celkem bodů": int(total) if total.is_integer() else total,
            "Přesné trefy (3b+)": exact_hits,
            "Trefy vítěze (1b+)": match_hits
        })
    
    df_rank = pd.DataFrame(ranking).sort_values("Celkem bodů", ascending=False).reset_index(drop=True)
    st.dataframe(df_rank, use_container_width=True, height=500)

# 2. DETAIL ZÁPASŮ
with tabs[1]:
    st.header("Detailní rozpis bodů po zápasech")
    st.info("Zde vidíš přesně, kolik bodů kdo dostal za každý zápas (čteno přímo z Excelu).")

    for m in ALL_MATCHES:
        # Přeskočit prázdné zápasy
        if not m['teams'] or m['teams'] == "Neznámý zápas": continue
        
        res_display = m['result'] if m['result'] else "⏳"
        
        with st.container():
            st.markdown(f"""
            <div class="match-header">
                <div>
                    <div style="font-size:0.8rem; color:#666;">{m['desc']}</div>
                    <div style="font-weight:bold; font-size:1.1rem;">{m['teams']}</div>
                </div>
                <div class="score-big">{res_display}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Tabulka tipů pro tento zápas
            # Seřadíme hráče podle získaných bodů v tomto zápase
            match_tips = []
            for p in ALL_PLAYERS:
                d = MASTER_DATA[p].get(m['id'], {'tip': '-', 'pts': 0})
                match_tips.append({'p': p, 't': d['tip'], 'pts': d['pts']})
            
            # Sort by points desc
            match_tips.sort(key=lambda x: x['pts'], reverse=True)
            
            # Vykreslení řádků
            st.markdown('<div class="match-body">', unsafe_allow_html=True)
            cols = st.columns([2, 2, 1])
            cols[0].markdown("**Hráč**")
            cols[1].markdown("**Tip**")
            cols[2].markdown("**Body**")
            
            for mt in match_tips:
                p_name = mt['p']
                tip = mt['t'] if mt['t'] else "-"
                pts = mt['pts']
                
                pts_class = "points-0"
                if pts >= 3: pts_class = "points-3"
                elif pts > 0: pts_class = "points-1"
                
                # Zobrazit řádek
                c1, c2, c3 = st.columns([2, 2, 1])
                c1.write(p_name)
                c2.write(tip)
                c3.markdown(f'<span class="{pts_class}">{pts}</span>', unsafe_allow_html=True)
                
            st.markdown('</div>', unsafe_allow_html=True)

# 3. PŘED TURNAJEM
with tabs[2]:
    st.header("Kompletní tipy před turnajem")
    st.dataframe(df_pre, use_container_width=True)

# 4. PLAY-OFF PAVOUK
with tabs[3]:
    st.header("Play-off Pavouk")
    
    # Filtrace jen playoff zápasů
    po_matches = [m for m in ALL_MATCHES if m['phase'] == 'Play-off']
    
    if not po_matches:
        st.warning("Zatím žádná data pro play-off.")
    else:
        # Jednoduché zobrazení karet
        for m in po_matches:
            if not m['result']: continue
            
             # Contextual trigger
            
            st.markdown(f"""
            <div style="border:1px solid #ccc; padding:15px; border-radius:10px; margin-bottom:10px; border-left: 5px solid #ffcc00; background:white;">
                <div style="font-weight:bold; color:#555;">{m['desc'].splitlines()[0] if m['desc'] else 'Play-off'}</div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px;">
                    <span style="font-size:1.2rem; font-weight:bold;">{m['teams']}</span>
                    <span style="font-size:1.5rem; background:#222; color:white; padding:5px 15px; border-radius:5px;">{m['result']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

