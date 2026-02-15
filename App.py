import streamlit as st
import pandas as pd

# --- KONFIGURACE ---
st.set_page_config(page_title="ZOH 2026 - Tipovačka", page_icon="🏒", layout="wide")

# --- DESIGN (Vše v jednom bloku, aby se nerozbil kód) ---
st.markdown("""
<style>
    .match-card { background: white; border-radius: 15px; padding: 20px; margin-bottom: 25px; border-left: 10px solid #003399; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .score-badge { font-size: 2.2rem; font-weight: 900; background: #1a1a1a; padding: 8px 25px; border-radius: 12px; color: white; min-width: 120px; text-align: center; }
    .team-name { font-weight: 800; font-size: 1.2rem; text-transform: uppercase; color: #1a1a1a; }
    .tip-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px; padding-top: 10px; border-top: 1px solid #eee; justify-content: center; }
    .tip-box { border-radius: 10px; padding: 10px; text-align: center; min-width: 90px; border: 2px solid #e2e8f0; position: relative; background: #f8fafc; }
    .banker-icon { position: absolute; top: -12px; right: -5px; background: #ef4444; color: white; font-size: 0.65rem; padding: 2px 6px; border-radius: 6px; font-weight: 900; }
    .res-3 { background-color: #dcfce7 !important; border-color: #22c55e !important; color: #166534 !important; }
    .res-1 { background-color: #fef9c3 !important; border-color: #eab308 !important; color: #854d0e !important; }
    .res-0 { background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }
</style>
""", unsafe_allow_html=True)

# --- 1. DATA: ZÁPASY SKUPINY ---
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
    {"id": "M17", "h": "Dánsko", "a": "Lotyšsko", "res": "3:2"},
    {"id": "M18", "h": "USA", "a": "Německo", "res": "2:1"},
]

# --- 2. DATA: TIPY HRÁČŮ ---
TIPS = {
    'Aďas': {
        'M1':'1:3','M2':'6:1','M3':'6:2','M4':'2:4','M5':'2:3','M6':'4:3','M7':'1:3','M8':'2:4','M9':('0:5',True),
        'M10':'3:1','M11':'2:2','M12':('5:1',True),'M13':'3:0','M14':'5:2','M15':'3:3','M16':'8:0','M17':'3:2','M18':'2:1'
    },
    'Víťa': {
        'M1':'2:2','M2':'4:0','M3':'4:1','M4':'1:4','M5':'2:6','M6':'3:2','M7':'3:3','M8':'3:4','M9':'0:3',
        'M10':'4:2','M11':'3:2','M12':'4:0','M13':'3:1','M14':'6:1','M15':'4:2','M16':'5:0','M17':'3:2','M18':'4:3'
    },
    'Cigi ml.': {
        'M1':'2:4','M2':'6:2','M3':'3:1','M4':'3:5','M5':'1:4','M6':'4:2','M7':'2:3','M8':'3:5','M9':'1:4',
        'M10':'4:1','M11':'3:3','M12':'6:2','M13':'5:0','M14':'6:1','M15':'4:5','M16':'7:0','M17':'4:2','M18':'5:2'
    },
    'Mršťa': {
        'M1':'2:4','M2':'7:1','M3':'5:2','M4':'2:5','M5':'2:5','M6':'5:3','M7':'2:3','M8':'1:5','M9':'1:6',
        'M10':'4:2','M11':'3:1','M12':'7:3','M13':'2:2','M14':('4:0',True),'M15':'3:5','M16':'9:1','M17':'3:3','M18':'5:4'
    }
}

# --- 3. DATA: PŘED TURNAJEM ---
PRE_DATA = [
    {"Hráč": "Aďas", "Vítěz": "Kanada", "2. místo": "Česko", "3. místo": "Švédsko", "4. místo": "Švýcarsko", "Střelec": "MacKinnon", "Nahrávač": "Konecny", "Brankář": "Vladař", "MVP": "MacKinnon"},
    {"Hráč": "Cigi ml.", "Vítěz": "Kanada", "2. místo": "Švédsko", "3. místo": "USA", "4. místo": "Finsko", "Střelec": "Celebriny", "Nahrávač": "McDavid", "Brankář": "Thompson", "MVP": "McDavid"},
    {"Hráč": "Mršťa", "Vítěz": "Kanada", "2. místo": "Švédsko", "3. místo": "Česko", "4. místo": "Švýcarsko", "Střelec": "Pastrňák", "Nahrávač": "Crosby", "Brankář": "Genoni", "MVP": "Crosby"},
    {"Hráč": "Víťa", "Vítěz": "Kanada", "2. místo": "USA", "3. místo": "Česko", "4. místo": "Švédsko", "Střelec": "Matthews", "Nahrávač": "McDavid", "Brankář": "Juuse Saros", "MVP": "Lukas Raymond"},
    {"Hráč": "Fany", "Vítěz": "Švýcarsko", "2. místo": "Švédsko", "3. místo": "Finsko", "4. místo": "Česko", "Střelec": "Elias Petterson", "Nahrávač": "Nikolaj Ehlers", "Brankář": "Jordan Binnington", "MVP": "Roman Josi"},
]

FLAGS = {"Česko": "🇨🇿", "Kanada": "🇨🇦", "Slovensko": "🇸🇰", "Finsko": "🇫🇮", "Švédsko": "🇸🇪", "Itálie": "🇮🇹", "USA": "🇺🇸", "Německo": "🇩🇪", "Lotyšsko": "🇱🇻", "Francie": "🇫🇷", "Dánsko": "🇩🇰", "Švýcarsko": "🇨🇭"}
PLAYERS = sorted(list(TIPS.keys()))

def get_pts(tip_raw, res):
    if not tip_raw or not res: return 0
    tip = tip_raw[0] if isinstance(tip_raw, tuple) else tip_raw
    banker = tip_raw[1] if isinstance(tip_raw, tuple) else False
    try:
        th, ta = map(int, tip.split(":"))
        rh, ra = map(int, res.split(":"))
        pts = 0
        if th == rh and ta == ra: pts = 3
        elif (th > ta and rh > ra) or (th < ta and rh < ra) or (th == ta and rh == ra): pts = 1
        return pts * 2 if banker else pts
    except: return 0

# --- APP ---
st.title("🏒 ZOH 2026 - TIPY CENTRÁLA")

tabs = st.tabs(["🏆 TABULKA", "📅 SKUPINY", "🔥 PLAY-OFF", "🔮 PŘED TURNAJEM", "✍️ GENERÁTOR"])

with tabs[0]:
    rank = []
    for p in PLAYERS:
        pts = sum(get_pts(TIPS[p].get(m['id']), m['res']) for m in MATCHES)
        rank.append({"Hráč": p, "Body": pts})
    st.table(pd.DataFrame(rank).sort_values("Body", ascending=False).reset_index(drop=True))

with tabs[1]:
    for m in MATCHES:
        res = m['res'] or "?:?"
        tipy_html = "".join([
            f'<div class="tip-box {"res-3" if get_pts(TIPS[p].get(m["id"]), m["res"]) >= 3 else "res-1" if get_pts(TIPS[p].get(m["id"]), m["res"]) >= 1 else "res-0"}">'
            f'{"<div class=\'banker-icon\'>🃏 BANKER</div>" if isinstance(TIPS[p].get(m["id"]), tuple) else ""}'
            f'<div style="font-size:0.7rem; color:#64748b;">{p}</div>'
            f'<div style="font-weight:900; font-size:1.1rem;">{TIPS[p].get(m["id"])[0] if isinstance(TIPS[p].get(m["id"]), tuple) else TIPS[p].get(m["id"], "-")}</div>'
            f'<div style="font-size:0.8rem; font-weight:bold;">{get_pts(TIPS[p].get(m["id"]), m["res"])}b</div></div>'
            for p in PLAYERS if m["id"] in TIPS[p]
        ])
        
        st.markdown(f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-around; align-items:center;">
                <div style="width:30%; text-align:center;"><span style="font-size:3rem;">{FLAGS.get(m['h'])}</span><div class="team-name">{m['h']}</div></div>
                <div class="score-badge">{res}</div>
                <div style="width:30%; text-align:center;"><span style="font-size:3rem;">{FLAGS.get(m['a'])}</span><div class="team-name">{m['a']}</div></div>
            </div>
            <div class="tip-grid">{tipy_html}</div>
        </div>
        """, unsafe_allow_html=True)

with tabs[2]:
    po = [("Osmifinále", "Česko", "Dánsko"), ("Osmifinále", "Švédsko", "Lotyšsko"), ("Osmifinále", "Švýcarsko", "Francie"), ("Osmifinále", "Německo", "Itálie")]
    for r, h, a in po:
        st.markdown(f"""<div class="match-card" style="border-left-color:#eab308;"><div style="text-align:center; font-weight:900; color:#eab308;">{r}</div>
            <div style="display:flex; justify-content:space-around; align-items:center;">
                <div style="width:30%; text-align:center;"><span style="font-size:2.5rem;">{FLAGS.get(h)}</span><div class="team-name">{h}</div></div>
                <div style="font-size:1.5rem; font-weight:900; color:#cbd5e1;">VS</div>
                <div style="width:30%; text-align:center;"><span style="font-size:2.5rem;">{FLAGS.get(a)}</span><div class="team-name">{a}</div></div>
            </div></div>""", unsafe_allow_html=True)

with tabs[3]:
    st.subheader("🔮 Tipy odevzdané před začátkem turnaje")
    st.table(pd.DataFrame(PRE_DATA))

with tabs[4]:
    st.subheader("✍️ Generátor tipů na play-off")
    me = st.selectbox("Vyber své jméno", PLAYERS)
    c1, c2 = st.columns(2)
    t1 = c1.text_input("Česko - Dánsko", placeholder="0:0")
    t2 = c1.text_input("Švédsko - Lotyšsko", placeholder="0:0")
    t3 = c2.text_input("Švýcarsko - Francie", placeholder="0:0")
    t4 = c2.text_input("Německo - Itálie", placeholder="0:0")
    
    if st.button("Vygenerovat text pro WhatsApp/Chat"):
        res_txt = f"🏒 TIPY {me.upper()}:\n🇨🇿 CZE-DEN: {t1}\n🇸🇪 SWE-LAT: {t2}\n🇨🇭 SUI-FRA: {t3}\n🇩🇪 GER-ITA: {t4}"
        st.code(res_txt)
