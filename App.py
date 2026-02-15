import streamlit as st
import pandas as pd

# --- KONFIGURACE A STYLY ---
st.set_page_config(page_title="ZOH 2026 - Oficiální Tipovačka", page_icon="🏒", layout="wide")

st.markdown("""
<style>
    .match-card {
        background: #ffffff; border-radius: 15px; padding: 20px; margin-bottom: 25px;
        border-left: 10px solid #003399; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .score-badge {
        font-size: 2.2rem; font-weight: 900; background: #1a1a1a; padding: 5px 25px;
        border-radius: 10px; color: white; min-width: 100px; text-align: center;
    }
    .team-name { font-weight: 800; font-size: 1.2rem; text-transform: uppercase; color: #1a1a1a; }
    .tip-grid {
        display: flex; flex-wrap: wrap; gap: 8px; margin-top: 15px;
        padding-top: 10px; border-top: 1px solid #eee; justify-content: center;
    }
    .tip-box {
        border-radius: 8px; padding: 8px; text-align: center; min-width: 85px;
        border: 1px solid #ddd; background: #f8f9fa; position: relative;
    }
    .banker-tag {
        position: absolute; top: -10px; right: -5px; background: #d7141a;
        color: white; font-size: 0.6rem; padding: 2px 5px; border-radius: 4px; font-weight: bold;
    }
    .res-3 { background-color: #d4edda !important; border-color: #22c55e !important; color: #155724 !important; }
    .res-1 { background-color: #fff3cd !important; border-color: #eab308 !important; color: #856404 !important; }
    .res-0 { background-color: #f8d7da !important; border-color: #dc3545 !important; color: #721c24 !important; }
</style>
""", unsafe_allow_html=True)

# --- 1. DATA: ZÁKLADNÍ SKUPINY ---
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
    {"id": "M16", "h": "Kanada", "a": "Francie", "res": "8:0"},
    {"id": "M17", "h": "Dánsko", "a": "Lotyšsko", "res": "3:2"},
    {"id": "M18", "h": "USA", "a": "Německo", "res": "2:1"},
]

# --- 2. DATA: TIPY (Zkontrolováno z CSV) ---
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
    },
    'Moli': {'M1':'1:5','M2':'8:0'}, 'Alesh':{}, 'Cigi':{}, 'Fany':{}
}

# --- 3. DATA: PLAY-OFF ROZPIS ---
PLAYOFF = [
    {"r": "Osmifinále", "h": "Česko", "a": "Dánsko", "d": "Úterý 17.02."},
    {"r": "Osmifinále", "h": "Švédsko", "a": "Lotyšsko", "d": "Úterý 17.02."},
    {"r": "Osmifinále", "h": "Švýcarsko", "a": "Francie", "d": "Úterý 17.02."},
    {"r": "Osmifinále", "h": "Německo", "a": "Itálie", "d": "Úterý 17.02."},
    {"r": "Čtvrtfinále", "h": "Kanada", "a": "vítěz GER/ITA", "d": "Středa 18.02."},
    {"r": "Čtvrtfinále", "h": "USA", "a": "vítěz SUI/FRA", "d": "Středa 18.02."},
    {"r": "Čtvrtfinále", "h": "Finsko", "a": "vítěz SWE/LAT", "d": "Středa 18.02."},
    {"r": "Čtvrtfinále", "h": "Slovensko", "a": "vítěz CZE/DEN", "d": "Středa 18.02."},
]

FLAGS = {"Česko": "🇨🇿", "Kanada": "🇨🇦", "Slovensko": "🇸🇰", "Finsko": "🇫🇮", "Švédsko": "🇸🇪", "Itálie": "🇮🇹", "USA": "🇺🇸", "Německo": "🇩🇪", "Lotyšsko": "🇱🇻", "Francie": "🇫🇷", "Dánsko": "🇩🇰", "Švýcarsko": "🇨🇭"}
PLAYERS = sorted(['Aďas', 'Víťa', 'Cigi ml.', 'Mršťa', 'Moli', 'Cigi', 'Alesh', 'Fany'])

def get_pts(tip_raw, res):
    if not tip_raw or not res: return 0
    t = tip_raw[0] if isinstance(tip_raw, tuple) else tip_raw
    b = tip_raw[1] if isinstance(tip_raw, tuple) else False
    try:
        th, ta = map(int, t.split(":"))
        rh, ra = map(int, res.split(":"))
        p = 0
        if th == rh and ta == ra: p = 3
        elif (th > ta and rh > ra) or (th < ta and rh < ra) or (th == ta and rh == ra): p = 1
        return p * 2 if b else p
    except: return 0

# --- APLIKACE ---
st.title("🏒 ZOH 2026 - CENTRÁLA")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏆 TABULKA", "📊 SKUPINY", "🔥 PAVOUK", "🔮 DLOUHODOBÉ", "✍️ MŮJ TIP"])

with tab1:
    rank = []
    for p in PLAYERS:
        total = sum(get_pts(TIPS.get(p, {}).get(m['id']), m['res']) for m in MATCHES if m['res'])
        hits = sum(1 for m in MATCHES if m['res'] and get_pts(TIPS.get(p, {}).get(m['id']), m['res']) >= 3)
        rank.append({"Hráč": p, "Body": total, "Trefy": hits})
    st.table(pd.DataFrame(rank).sort_values(["Body", "Trefy"], ascending=False).reset_index(drop=True))

with tab2:
    for m in MATCHES:
        res = m['res'] or "?:?"
        tipy_html = ""
        for p in PLAYERS:
            tr = TIPS.get(p, {}).get(m['id'])
            if not tr: continue
            tip = tr[0] if isinstance(tr, tuple) else tr
            banker = tr[1] if isinstance(tr, tuple) else False
            pts = get_pts(tr, m['res'])
            
            css = ""
            if m['res']:
                if pts >= 3: css = "res-3"
                elif pts >= 1: css = "res-1"
                else: css = "res-0"
            
            b_tag = '<div class="banker-tag">🃏</div>' if banker else ""
            tipy_html += f'<div class="tip-box {css}">{b_tag}<div style="font-size:0.7rem; color:gray;">{p}</div><b>{tip}</b>{f"<div>{pts}b</div>" if m["res"] else ""}</div>'
        
        full_card = f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-around; align-items:center; text-align:center;">
                <div style="width:30%;"><span style="font-size:2.5rem;">{FLAGS.get(m['h'])}</span><div class="team-name">{m['h']}</div></div>
                <div class="score-badge">{res}</div>
                <div style="width:30%;"><span style="font-size:2.5rem;">{FLAGS.get(m['a'])}</span><div class="team-name">{m['a']}</div></div>
            </div>
            <div class="tip-grid">{tipy_html}</div>
        </div>
        """
        st.markdown(full_card, unsafe_allow_html=True)

with tab3:
    for p in PLAYOFF:
        st.markdown(f"""
        <div class="match-card" style="border-left-color: #ffcc00;">
            <div style="text-align:center; font-weight:bold; color:gray; margin-bottom:10px;">{p['r']} • {p['d']}</div>
            <div style="display:flex; justify-content:space-around; align-items:center; text-align:center;">
                <div style="width:30%;"><span style="font-size:2rem;">{FLAGS.get(p['h'],'🏒')}</span><div class="team-name">{p['h']}</div></div>
                <div style="font-size:1.5rem; font-weight:bold; color:#ccc;">VS</div>
                <div style="width:30%;"><span style="font-size:2rem;">{FLAGS.get(p['a'],'🏒')}</span><div class="team-name">{p['a']}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.info("Zde jsou dlouhodobé tipy před turnajem.")
    # Tady by byla tabulka PRE_DATA, kterou jsi posílal dříve

with tab5:
    st.subheader("✍️ Tipni si na Play-off")
    name = st.selectbox("Kdo jsi?", PLAYERS)
    c1, c2 = st.columns(2)
    t1 = c1.text_input("Česko - Dánsko")
    t2 = c2.text_input("Švédsko - Lotyšsko")
    if st.button("Vygenerovat náhled"):
        st.code(f"Hráč: {name}\n🇨🇿 CZE-DEN: {t1}\n🇸🇪 SWE-LAT: {t2}")
