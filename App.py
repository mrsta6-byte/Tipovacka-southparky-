import streamlit as st
import pandas as pd

# --- KONFIGURACE ---
st.set_page_config(page_title="ZOH 2026 - Tipovačka PRO", page_icon="🏒", layout="wide")

# --- KOMPLETNÍ STYLY ---
st.markdown("""
<style>
    .match-card {
        background: #ffffff; border-radius: 12px; padding: 18px; margin-bottom: 20px;
        border-left: 8px solid #003087; box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }
    .score-badge {
        font-size: 2.2rem; font-weight: 900; background: #1a1a1a; padding: 5px 20px;
        border-radius: 8px; color: white; min-width: 100px; text-align: center;
    }
    .team-name { font-weight: 800; font-size: 1.1rem; text-transform: uppercase; color: #1a1a1a; }
    .tip-grid {
        display: flex; flex-wrap: wrap; gap: 8px; margin-top: 15px;
        padding-top: 10px; border-top: 1px solid #f0f0f0; justify-content: center;
    }
    .tip-box {
        border-radius: 8px; padding: 8px; text-align: center; min-width: 80px;
        border: 1px solid #ddd; background: #f8fafc; position: relative;
    }
    .banker-tag {
        position: absolute; top: -10px; right: -5px; background: #dc2626;
        color: white; font-size: 0.6rem; padding: 2px 5px; border-radius: 4px; font-weight: bold;
    }
    .res-3 { background-color: #dcfce7 !important; border-color: #22c55e !important; color: #166534 !important; }
    .res-1 { background-color: #fef9c3 !important; border-color: #eab308 !important; color: #854d0e !important; }
    .res-0 { background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; color: #475569 !important; }
</style>
""", unsafe_allow_html=True)

# --- DATA: ZÁPASY SKUPINY ---
MATCHES = [
    {"id": "M1", "h": "Slovensko", "a": "Finsko", "res": "4:1"},
    {"id": "M2", "h": "Švédsko", "a": "Itálie", "res": "5:2"},
    {"id": "M3", "h": "Švýcarsko", "a": "Francie", "res": "4:0"},
    {"id": "M4", "h": "Česko", "a": "Kanada", "res": "0:5"},
    {"id": "M5", "h": "Lotyšsko", "a": "USA", "res": "1:5"},
    {"id": "M6", "h": "Německo", "a": "Dánsko", "res": "3:1"},
    {"id": "M7", "h": "Finsko", "a": "Švédsko", "res": "4:1"},
    {"id": "M8", "h": "Itálie", "a": "Slovensko", "res": "2:3"},
    {"id": "M9", "h": "Francie", "a": "Česko", "res": "3:6"},
    {"id": "M10", "h": "Kanada", "a": "Švýcarsko", "res": "5:1"},
    {"id": "M11", "h": "Německo", "a": "Lotyšsko", "res": "3:4"},
    {"id": "M12", "h": "Švédsko", "a": "Slovensko", "res": "5:3"},
    {"id": "M13", "h": "Finsko", "a": "Itálie", "res": "11:0"},
    {"id": "M14", "h": "USA", "a": "Dánsko", "res": "6:3"},
    {"id": "M15", "h": "Švýcarsko", "a": "Česko", "res": "3:3"},
    {"id": "M16", "h": "Kanada", "a": "Francie", "res": "10:2"},
    {"id": "M17", "h": "Dánsko", "a": "Lotyšsko", "res": "4:2"},
    {"id": "M18", "h": "USA", "a": "Německo", "res": "5:1"},
]

TIPS = {
    'Aďas': {'M1':('1:3',0),'M9':('0:5',2),'M12':('5:1',2),'M15':('3:3',0),'M16':('8:0',0),'M17':('3:2',0),'M18':('2:1',0)},
    'Víťa': {'M1':('2:2',0),'M5':('2:6',0),'M15':('4:2',0),'M16':('5:0',0),'M17':('3:2',0),'M18':('4:3',0)},
    'Cigi ml.': {'M1':('2:4',0),'M15':('4:5',0),'M16':('7:0',0),'M17':('4:2',0),'M18':('5:2',0)},
    'Mršťa': {'M1':('2:4',0),'M14':('4:0',2),'M15':('3:5',0),'M16':('9:1',0),'M17':('3:3',0),'M18':('5:4',0)}
}

# --- DATA: PLAY-OFF (Opravené časy) ---
PLAYOFF = [
    {"r": "Osmifinále", "d": "Úterý 12:10", "h": "Švýcarsko", "a": "Itálie", "n": "USA"},
    {"r": "Osmifinále", "d": "Úterý 12:10", "h": "Německo", "a": "Francie", "n": "Slovensko"},
    {"r": "Osmifinále", "d": "Úterý 16:40", "h": "Česko", "a": "Dánsko", "n": "Kanada"},
    {"r": "Osmifinále", "d": "Úterý 21:10", "h": "Švédsko", "a": "Lotyšsko", "n": "Finsko"},
]

FLAGS = {"Česko": "🇨🇿", "Kanada": "🇨🇦", "Slovensko": "🇸🇰", "Finsko": "🇫🇮", "Švédsko": "🇸🇪", "Itálie": "🇮🇹", "USA": "🇺🇸", "Německo": "🇩🇪", "Lotyšsko": "🇱🇻", "Francie": "🇫🇷", "Dánsko": "🇩🇰", "Švýcarsko": "🇨🇭"}
PLAYERS = ['Aďas', 'Víťa', 'Cigi ml.', 'Mršťa']

def get_pts(tip_raw, res):
    if not tip_raw or not res: return 0
    t, b = tip_raw
    try:
        th, ta = map(int, t.split(":"))
        rh, ra = map(int, res.split(":"))
        p = 3 if (th==rh and ta==ra) else (1 if (th>ta and rh>ra) or (th<ta and rh<ra) or (th==ta and rh==ra) else 0)
        return p*2 if b==2 else p
    except: return 0

st.sidebar.title("🥤 Purinový Barometr")
st.sidebar.info("Hokej je stres! Pamatuj na dietu. Dnes doporučujeme: Čistá voda s citronem 🍋")

st.title("🏒 ZOH 2026 - TIPOVAČKA MILÁNO")
tab1, tab2, tab3, tab4 = st.tabs(["🏆 TABULKA", "📊 SKUPINY", "🔥 PLAY-OFF", "✍️ GENERÁTOR"])

with tab1:
    rank = []
    for p in PLAYERS:
        pts = sum(get_pts(TIPS.get(p, {}).get(m['id']), m['res']) for m in MATCHES)
        hits = sum(1 for m in MATCHES if get_pts(TIPS.get(p, {}).get(m['id']), m['res']) in [3,6])
        rank.append({"Hráč": p, "Body": pts, "Přesné trefy": hits})
    st.table(pd.DataFrame(rank).sort_values(["Body", "Přesné trefy"], ascending=False).reset_index(drop=True))

with tab2:
    for m in MATCHES:
        res = m['res'] or "?:?"
        tipy = "".join([f'<div class="tip-box {"res-3" if get_pts(TIPS.get(p, {}).get(m["id"]), res) in [3,6] else "res-1" if get_pts(TIPS.get(p, {}).get(m["id"]), res)>0 else "res-0"}">{"<div class=\'banker-tag\'>🃏</div>" if TIPS.get(p, {}).get(m["id"], ("",0))[1]==2 else ""}<div style="font-size:0.7rem; color:gray;">{p}</div><b>{TIPS.get(p, {}).get(m["id"], ("-",0))[0]}</b></div>' for p in PLAYERS])
        st.markdown(f'<div class="match-card"><div style="display:flex; justify-content:space-around; align-items:center; text-align:center;"><div style="width:30%;"><span style="font-size:3rem;">{FLAGS.get(m["h"])}</span><div class="team-name">{m["h"]}</div></div><div class="score-badge">{res}</div><div style="width:30%;"><span style="font-size:3rem;">{FLAGS.get(m["a"])}</span><div class="team-name">{m["a"]}</div></div></div><div class="tip-grid">{tipy}</div></div>', unsafe_allow_html=True)

with tab3:
    for g in PLAYOFF:
        st.markdown(f'<div class="match-card" style="border-left-color: #facc15;"><div style="text-align:center; font-weight:bold; color:gray; margin-bottom:10px;">{g["r"]} • {g["d"]}</div><div style="display:flex; justify-content:space-around; align-items:center; text-align:center;"><div style="width:35%;"><span style="font-size:2.5rem;">{FLAGS.get(g["h"])}</span><div class="team-name">{g["h"]}</div></div><div style="font-size:1.5rem; font-weight:bold; color:#ccc;">VS</div><div style="width:35%;"><span style="font-size:2.5rem;">{FLAGS.get(g["a"])}</span><div class="team-name">{g["a"]}</div></div></div><div style="text-align:center; font-size:0.8rem; color:gray; margin-top:10px;">Vítěz narazí ve čtvrtfinále na: <b>{g["n"]}</b></div></div>', unsafe_allow_html=True)

with tab4:
    st.subheader("✍️ Generátor tipů")
    me = st.selectbox("Vyber jméno", PLAYERS)
    c1, c2 = st.columns(2)
    t1 = c1.text_input("Švýcarsko - Itálie")
    t2 = c1.text_input("Německo - Francie")
    t3 = c2.text_input("Česko - Dánsko")
    t4 = c2.text_input("Švédsko - Lotyšsko")
    if st.button("Uložit a vygenerovat text"):
        st.code(f"Tipy {me}:\nSUI-ITA: {t1}\nGER-FRA: {t2}\nCZE-DEN: {t3}\nSWE-LAT: {t4}")
