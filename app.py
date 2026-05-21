import streamlit as st
import pandas as pd
import random, os, json
from datetime import date
from io import BytesIO

st.set_page_config(page_title="두류 테니스", page_icon="🎾",
                   layout="centered", initial_sidebar_state="collapsed")

# ══════════════════════════════════════
# CSS (아이콘 깨짐 현상 완벽 방지 보강)
# ══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght=400;500;700;900&display=swap');
:root{
  --g0:#1B5E20;--g2:#388E3C;--g3:#66BB6A;--g5:#E8F5E9;
  --nav0:#2E7D32;--nav1:#1565C0;--nav2:#E65100;--nav3:#4A148C;--nav4:#00695C;
  --mc0:#1B5E20;--mc1:#0D47A1;--mc2:#BF360C;--mc3:#4A148C;
  --mc4:#006064;--mc5:#1A237E;--mc6:#880E4F;--mc7:#33691E;
  --tb0:#2E7D32;--tb1:#1565C0;--tb2:#D84315;--tb3:#6A1B9A;
  --tb4:#00695C;--tb5:#283593;--tb6:#AD1457;--tb7:#558B2F;
  --yel:#FFD600;--ora:#FB8C00;
  --bg:#F4F6F9;--card:#fff;--bd:#E0E4EA;
  --r1:10px;--r2:16px;--sh:0 2px 10px rgba(0,0,0,.08);--sh2:0 4px 20px rgba(0,0,0,.13);
}
*{ font-family:'Noto Sans KR',sans-serif!important; box-sizing:border-box; -webkit-tap-highlight-color:transparent; }
.block-container{ padding:0 0.5rem 5rem!important; max-width:520px!important; margin:0 auto!important; background:var(--bg)!important; }
.stApp{ background:var(--bg)!important; }

/* 랭킹 데이터프레임 강제 무조건 가운데 정렬 보완 */
div[data-testid="stDataFrame"], div[data-testid="stDataFrame"] >, div[data-testid="stDataFrame"] * {
  text-align: center !important;
  justify-content: center !important;
  align-items: center !important;
  margin: 0 auto !important;
}

.hdr{ background:linear-gradient(135deg,#1B5E20 0%,#2E7D32 60%,#388E3C 100%); margin:0 -0.5rem 0; padding:14px 18px 0; position:relative; overflow:hidden; box-shadow:var(--sh2); }
.hdr::after{ content:'🎾'; position:absolute; right:14px; top:8px; font-size:2.6rem; opacity:.12; }
.hdr-title{ color:#fff; font-size:1.05rem; font-weight:900; margin:0 0 2px; }
.hdr-sub{ color:rgba(255,255,255,.5); font-size:.58rem; letter-spacing:2px; margin-bottom:0; }
#MainMenu, header, footer { visibility: hidden !important; height: 0 !important; }

.pg-title{ color:#fff; padding:12px 16px; border-radius:var(--r2); margin:0 0 14px; font-size:1rem; font-weight:900; text-align:center; box-shadow:var(--sh2); }
.pg-title.c0{ background:linear-gradient(135deg,var(--nav0),#43A047); }
.pg-title.c1{ background:linear-gradient(135deg,var(--nav1),#1976D2); }
.pg-title.c2{ background:linear-gradient(135deg,var(--nav2),#F4511E); }
.pg-title.c3{ background:linear-gradient(135deg,var(--nav3),#7B1FA2); }
.pg-title.c4{ background:linear-gradient(135deg,var(--nav4),#00897B); }

.sec{ font-size:.85rem; font-weight:800; color:var(--g0); border-left:4px solid var(--g3); padding-left:9px; margin:16px 0 8px; }
.sec-t{ margin-top:24px; }
.ic{ background:var(--card); border-left:4px solid var(--g3); border-radius:var(--r1); padding:10px 14px; margin:7px 0; box-shadow:var(--sh); font-size:.8rem; color:#3a3a5c; }

button[data-baseweb="tab"]{ font-size:.75rem!important; font-weight:700!important; padding:10px 12px!important; border-radius:var(--r1) var(--r1) 0 0!important; }
button[data-baseweb="tab"][aria-selected="true"]{ background:linear-gradient(135deg,var(--g0),var(--g2))!important; color:#fff!important; }
[data-baseweb="tab-list"]{ background:#DDD!important; border-radius:var(--r1) var(--r1) 0 0!important; padding:4px 4px 0!important; gap:2px!important; }

.match-card{ background:var(--card); border-radius:var(--r2); padding:10px; margin:12px 0; box-shadow:var(--sh2); border:1px solid var(--bd); }
.match-no{ display:inline-block; border-radius:20px; padding:3px 12px; font-size:.6rem; font-weight:900; margin-bottom:10px; color:#fff; }
.mc0{background:var(--mc0);} .mc1{background:var(--mc1);} .mc2{background:var(--mc2);} .mc3{background:var(--mc3);}
.mc4{background:var(--mc4);} .mc5{background:var(--mc5);} .mc6{background:var(--mc6);} .mc7{background:var(--mc7);}

.team-name{ border-radius:var(--r1); padding:6px 4px; font-weight:900; font-size:.78rem; text-align:center; color:#fff; box-shadow:var(--sh); min-height:36px; display:flex; align-items:center; justify-content:center; word-break:keep-all; line-height:1.2; margin-bottom:6px; }
.tb0{background:var(--tb0);} .tb1{background:var(--tb1);} .tb2{background:var(--tb2);} .tb3{background:var(--tb3);}
.tb4{background:var(--tb4);} .tb5{background:var(--tb5);} .tb6{background:var(--tb6);} .tb7{background:var(--tb7);}

div.score-btn-wrap [data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; gap: 4px !important; align-items: center !important; }
div.score-btn-wrap [data-testid="stHorizontalBlock"] > div { flex: 1 !important; min-width: 0 !important; }
div.score-btn-wrap [data-testid="stHorizontalBlock"] > div:nth-child(2) { flex: 0 0 35px !important; }
div.score-btn-wrap button, .score-num-display { width: 100% !important; aspect-ratio: 1.1 / 1 !important; height: auto !important; font-size: 1.05rem !important; font-weight: 900 !important; display: flex !important; align-items: center !important; justify-content: center !important; padding: 0 !important; margin: 0 !important; }
div.score-btn-wrap button { background: #E8F5E9 !important; border: 1.5px solid #C8E6C9 !important; color: #1B5E20 !important; border-radius: 8px !important; }
div.score-btn-wrap button:active { background: #A5D6A7 !important; }
.score-num-display { background: #fff; border: 1.5px solid #C8E6C9; border-radius: 8px; color: #1B5E20; }

.vs-col { display: flex !important; align-items: center !important; justify-content: center !important; flex-direction: column; height: 100%; margin-bottom: 25px; }
.vs-badge{ width:30px; height:30px; border-radius:50%; background:linear-gradient(135deg,#FFB74D,var(--ora)); display:flex; align-items:center; justify-content:center; font-weight:900; font-size:.65rem; color:#fff; box-shadow:var(--sh); }

.stButton>button{ border-radius:var(--r2)!important; font-weight:700!important; font-size:.82rem!important; min-height:46px!important; padding:10px 14px!important; }
.stButton>button[kind="primary"]{ background:linear-gradient(135deg,var(--g0),var(--g2))!important; color:#fff!important; border:none!important; box-shadow:0 4px 14px rgba(46,125,50,.35)!important; }

.mx-wrap{ background:var(--card); border-radius:var(--r1); padding:10px; box-shadow:var(--sh); overflow-x:auto; margin:8px 0; border:1px solid var(--bd); }
.mx{ border-collapse:collapse; white-space:nowrap; font-size:.7rem; width:100%; }
.mx th,.mx td{ padding:6px 8px; border:1px solid var(--bd); text-align:center; }
.mx thead th{ background:var(--g0); color:#fff; font-weight:700; }
.mx-grey{ background:#E0E4EA!important; color:#E0E4EA!important; }
.mx-dash{ color:#CCC; }
.mx-sc{ font-weight:800; color:var(--g0); }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# 기본 설정 및 데이터 파일 핸들링
# ══════════════════════════════════════
RANK_FILE = "ranking_master.csv"
MEMBER_FILE = "member_roster.json"
TOUR_FILE = "tournaments.json"
ADMIN_PW = "0502"
COLS_RANK = ["랭킹","이름","현재포인트","3월 포인트","결과","부과점","그룹","비고"]

GCLS = ["mc0","mc1","mc2","mc3","mc4","mc5","mc6","mc7"]
TBCLS = ["tb0","tb1","tb2","tb3","tb4","tb5","tb6","tb7"]
GLBL = ["🟢","🔵","🟠","🟣","🩵","🔴","🟡","⚪"]

KDK_3G = {
    4:  [(1,4,2,3),(1,3,2,4),(1,2,3,4)],
    8:  [(1,2,3,4),(5,6,7,8),(1,8,2,7),(3,6,4,5),(1,4,5,8),(2,3,6,7)],
    12: [(1,2,3,4),(5,6,7,8),(9,10,11,12),(1,3,5,7),(2,4,6,8),(9,11,1,5),(4,8,9,12),(6,7,10,11),(10,12,2,3)]
}
KDK_4G = {
    5:  [(1,2,3,4),(1,3,2,5),(1,4,3,5),(1,5,2,4),(2,3,4,5)],
    6:  [(1,3,2,4),(1,5,4,6),(2,3,5,6),(1,4,3,5),(2,6,3,4),(1,6,2,5)],
    7:  [(1,2,3,4),(5,6,1,7),(2,3,5,7),(1,4,6,7),(3,5,2,4),(1,6,2,5),(4,6,3,7)],
    8:  [(1,2,3,4),(5,6,7,8),(1,3,5,7),(2,4,6,8),(1,5,2,6),(3,7,4,8),(1,6,3,8),(2,5,4,7)],
    9:  [(1,2,3,4),(5,6,7,8),(1,9,5,7),(2,3,6,8),(4,9,3,8),(1,5,2,6),(3,6,4,5),(1,7,8,9),(2,4,7,9)],
    10: [(1,2,3,5),(6,7,8,10),(2,3,4,6),(7,8,1,9),(3,4,5,7),(8,9,2,10),(4,5,6,8),(1,3,9,10),(5,6,7,9),(1,10,2,4)],
    11: [(1,2,3,5),(6,7,8,10),(4,9,1,11),(2,3,6,8),(4,5,7,10),(9,11,2,6),(1,3,7,11),(4,8,5,9),(1,10,2,8),(4,7,6,11),(3,9,5,10)]
}

def load_rank():
    if not os.path.exists(RANK_FILE): return pd.DataFrame(columns=COLS_RANK)
    df = pd.read_csv(RANK_FILE)
    for c in ["현재포인트","3월 포인트","부과점"]:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    if "현재포인트" in df.columns:
        df = df.sort_values("현재포인트", ascending=False).reset_index(drop=True)
        df["랭킹"] = df.index + 1
    return df.fillna("")

def save_rank(df):
    if "현재포인트" in df.columns:
        df = df.sort_values("현재포인트", ascending=False).reset_index(drop=True)
        df["랭킹"] = df.index + 1
    df.to_csv(RANK_FILE, index=False)

def load_members():
    if os.path.exists(MEMBER_FILE):
        with open(MEMBER_FILE, "r", encoding="utf-8") as f: return json.load(f)
    df = load_rank()
    return df["이름"].tolist() if not df.empty else []

def save_members(names):
    with open(MEMBER_FILE, "w", encoding="utf-8") as f: json.dump(names, f, ensure_ascii=False, indent=2)

def load_tours():
    if os.path.exists(TOUR_FILE):
        with open(TOUR_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {}

def save_tours(d):
    with open(TOUR_FILE, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=2)

def df_to_html(df):
    th = "".join(f"<th>{c}</th>" for c in df.columns)
    tb = ""
    for _, r in df.iterrows():
        tb += "<tr>" + "".join(f"<td>{r[c]}</td>" for c in df.columns) + "</tr>"
    return f'<div class="mx-wrap"><table class="mx"><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'

def stats_fixed(matches):
    s = {}
    for m in matches:
        t1, t2 = tuple(m["t1"]), tuple(m["t2"])
        for t in (t1, t2):
            if t not in s: s[t] = {"승":0,"패":0,"득실":0}
        a, b = int(m["s1"]), int(m["s2"])
        if a > b: s[t1]["승"]+=1; s[t2]["패"]+=1
        elif b > a: s[t2]["승"]+=1; s[t1]["패"]+=1
        s[t1]["득실"] += a-b; s[t2]["득실"] += b-a
    return s

def stats_kdk(matches):
    s = {}
    for m in matches:
        p1, p2 = m["t1"], m["t2"]
        for p in p1+p2:
            if p not in s: s[p] = {"승":0,"패":0,"득실":0}
        a, b = int(m["s1"]), int(m["s2"])
        if a > b:
            for p in p1: s[p]["승"]+=1
            for p in p2: s[p]["패"]+=1
        elif b > a:
            for p in p2: s[p]["승"]+=1
            for p in p1: s[p]["패"]+=1
        for p in p1: s[p]["득실"] += a-b
        for p in p2: s[p]["득실"] += b-a
    return s

def rank_pts(rank, mode):
    if mode == "고정페어": return {1:7, 2:5, 3:3}.get(rank, 1)
    return 7 if rank <= 2 else (5 if rank <= 4 else (3 if rank <= 6 else 1))

def grade(rank):
    return "🥇 우승" if rank <= 2 else ("🥈 준우승" if rank <= 4 else ("🥉 3위" if rank <= 6 else "참가"))

def make_kdk(players, gperson):
    n = len(players)
    bp = KDK_3G.get(n) if gperson == 3 else KDK_4G.get(n)
    if not bp: return None, {}
    shuffled = random.sample(players, n)
    n2p = {i+1: shuffled[i] for i in range(n)}
    p2n = {shuffled[i]: i+1 for i in range(n)}
    ms = [{"t1":[n2p[a],n2p[b]], "t2":[n2p[c],n2p[d]], "s1":0, "s2":0} for a,b,c,d in bp]
    return ms, p2n

def make_fixed(players):
    n = len(players)
    pairs = [(players[i], players[n-1-i]) for i in range(n//2)]
    ms = [{"t1":list(pairs[i]), "t2":list(pairs[j]), "s1":0, "s2":0} for i in range(len(pairs)) for j in range(i+1, len(pairs))]
    random.shuffle(ms)
    return ms, {}

def make_singles(players):
    pl = players[:]
    random.shuffle(pl)
    ms = [{"t1":[pl[i]], "t2":[pl[j]], "s1":0, "s2":0} for i in range(len(pl)) for j in range(i+1, len(pl))]
    random.shuffle(ms)
    return ms, {}

def matrix_html(matches, rank_items, is_fixed, p2n):
    if not matches or not rank_items: return ""
    if is_fixed: lab = {t: " &amp; ".join(list(t)) for t in rank_items}
    else: lab = {p: f"{p}({p2n.get(p,'?')})" for p in rank_items}
    mat = {lab[t]: {lab[o]: ("■" if t==o else "—") for o in lab} for t in lab}
    for m in matches:
        a, b = int(m["s1"]), int(m["s2"])
        if a > 0 or b > 0:
            if is_fixed:
                k1, k2 = tuple(m["t1"]), tuple(m["t2"])
                mat[lab[k1]][lab[k2]] = f"{a}:{b}"
                mat[lab[k2]][lab[k1]] = f"{b}:{a}"
            else:
                for x in m["t1"]:
                    for y in m["t2"]:
                        mat[lab[x]][lab[y]] = f"{a}:{b}"
                        mat[lab[y]][lab[x]] = f"{b}:{a}"
    keys = list(lab.values())
    header = "".join(f"<th>{k}</th>" for k in keys)
    body = ""
    for rk in keys:
        body += f"<tr><th>{rk}</th>"
        for ck in keys:
            v = mat[rk][ck]
            if v == "■": body += '<td class="mx-grey">■</td>'
            elif v == "—": body += '<td class="mx-dash">—</td>'
            else: body += f'<td class="mx-sc">{v}</td>'
        body += "</tr>"
    return f'<div class="mx-wrap"><table class="mx"><thead><tr><th></th>{header}</tr></thead><tbody>{body}</tbody></table></div>'

def adj_score(tid, grp, mi, side, delta):
    ts = load_tours()
    m = ts[tid]["groups"][grp]["matches"][mi]
    k = "s1" if side == "A" else "s2"
    m[k] = max(0, int(m[k]) + delta)
    save_tours(ts)

# ══════════════════════════════════════
# 메인 네비게이션
# ══════════════════════════════════════
ss = st.session_state
if "menu" not in ss: ss.menu = "ranking"

MENUS = [
    ("ranking", "🏆", "랭킹"),
    ("schedule","📅", "대진"),
    ("result",  "📊", "결과"),
    ("archive", "📂", "기록"),
    ("admin",   "⚙️", "관리"),
]

st.markdown('<div class="hdr"><div class="hdr-title">🎾 두류 테니스 클럽</div><div class="hdr-sub">DURYU TENNIS CLUB</div></div>', unsafe_allow_html=True)

nav_cols = st.columns(len(MENUS))
for col, (key, icon, label) in zip(nav_cols, MENUS):
    with col:
        if st.button(f"{icon}\n{label}", key=f"nav_{key}", use_container_width=True, type="primary" if ss.menu == key else "secondary"):
            ss.menu = key
            st.rerun()

menu_colors = {"ranking":"#2E7D32","schedule":"#1565C0","result":"#E65100","archive":"#4A148C","admin":"#00695C"}
st.markdown(f'<div style="height:4px;background:{menu_colors.get(ss.menu, "#2E7D32")};margin:0 -0.5rem 14px;box-shadow:0 2px 8px rgba(0,0,0,.2)"></div>', unsafe_allow_html=True)

title_cls = {"ranking":"c0","schedule":"c1","result":"c2","archive":"c3","admin":"c4"}
M = ss.menu

# ─────── 1. 랭킹 탭 ───────
if M == "ranking":
    st.markdown(f"<div class='pg-title {title_cls['ranking']}'>🏆 두류 랭킹 마스터</div>", unsafe_allow_html=True)
    df = load_rank()
    if df.empty:
        st.markdown("<div class='ic'>📭 등록된 랭킹 데이터가 존재하지 않습니다.</div>", unsafe_allow_html=True)
    else:
        d = df.copy()
        medal = ["🥇","🥈","🥉"]
        d.insert(0, "순위", [medal[i] if i < 3 else str(i+1) for i in range(len(d))])
        st.dataframe(d, use_container_width=True, hide_index=True)

# ─────── 2. 대진 탭 ───────
elif M == "schedule":
    ts = load_tours()
    act = [k for k, v in ts.items() if v.get("status") == "진행중"]
    if not act:
        st.markdown(f"<div class='pg-title {title_cls['schedule']}'>📅 대진표 및 경기결과 입력</div>", unsafe_allow_html=True)
        st.markdown("<div class='ic'>⚠️ 현재 진행 중인 공식 대회가 존재하지 않습니다.</div>", unsafe_allow_html=True)
        st.stop()
        
    tid, t_obj = act[-1], ts[act[-1]]
    st.markdown(f"<div class='pg-title {title_cls['schedule']}'>📅 {t_obj['title']}</div>", unsafe_allow_html=True)
    
    if t_obj.get("date") or t_obj.get("place") or t_obj.get("courts"):
        st.markdown(f'<div class="ic">📍 <b>일시:</b> {t_obj.get("date","")} | <b>장소:</b> {t_obj.get("place","")} ({t_obj.get("courts","")}면)</div>', unsafe_allow_html=True)
        
    g_names = list(t_obj["groups"].keys())
    if g_names:
        tabs = st.tabs([f"{GLBL[i%len(GLBL)]} {gn}그룹" for i, gn in enumerate(g_names)])
        for ti, gn in enumerate(g_names):
            with tabs[ti]:
                g_item = t_obj["groups"][gn]
                ms = g_item["matches"]
                mode = g_item["mode"]
                p2n = g_item.get("player_with_number", {})
                is_fx = (mode == "고정페어")
                
                sv = stats_fixed(ms) if is_fx else stats_kdk(ms)
                
                st.markdown("<div class='sec'>📋 조별 현재 순위 상황 (실시간 집계)</div>", unsafe_allow_html=True)
                calc_list = []
                for idx, p_name in enumerate(sorted(list(sv.keys()), key=lambda x:(-sv[x]["승"], -sv[x]["득실"]))):
                    p_txt = " & ".join(list(p_name)) if is_fx else p_name
                    calc_list.append({"순위":idx+1, "팀/선수명":p_txt, "승리":sv[p_name]["승"], "패배":sv[p_name]["패"], "득실점차":sv[p_name]["득실"]})
                if calc_list:
                    st.markdown(df_to_html(pd.DataFrame(calc_list)), unsafe_allow_html=True)
                    
                st.markdown("<div class='sec sec-t'>📊 교차 대진 전적 매트릭스</div>", unsafe_allow_html=True)
                st.markdown(matrix_html(ms, list(sv.keys()), is_fx, p2n), unsafe_allow_html=True)
                
                st.markdown("<div class='sec sec-t'>🎾 실시간 스코어 보드 입력</div>", unsafe_allow_html=True)
                for mi, m in enumerate(ms):
                    t1_txt = " & ".join(m["t1"])
                    t2_txt = " & ".join(m["t2"])
                    
                    st.markdown(f'<div class="match-card"><span class="match-no {GCLS[mi%len(GCLS)]}">MATCH {mi+1}</span>', unsafe_allow_html=True)
                    st.markdown('<div class="score-btn-wrap">', unsafe_allow_html=True)
                    c1, cv, c2 = st.columns([10, 3, 10])
                    
                    with c1:
                        st.markdown(f'<div class="team-name {TBCLS[mi%len(TBCLS)]}">{t1_txt}</div>', unsafe_allow_html=True)
                        cc1 = st.columns(3)
                        if cc1[0].button("－", key=f"m_m1_{gn}_{mi}"): adj_score(tid, gn, mi, "A", -1); st.rerun()
                        cc1[1].markdown(f'<div class="score-num-display">{int(m["s1"])}</div>', unsafe_allow_html=True)
                        if cc1[2].button("＋", key=f"m_p1_{gn}_{mi}"): adj_score(tid, gn, mi, "A", 1); st.rerun()
                        
                    with cv:
                        st.markdown('<div class="vs-col"><div class="vs-badge">VS</div></div>', unsafe_allow_html=True)
                        
                    with c2:
                        st.markdown(f'<div class="team-name {TBCLS[mi%len(TBCLS)]}">{t2_txt}</div>', unsafe_allow_html=True)
                        cc2 = st.columns(3)
                        if cc2[0].button("－", key=f"m_m2_{gn}_{mi}"): adj_score(tid, gn, mi, "B", -1); st.rerun()
                        cc2[1].markdown(f'<div class="score-num-display">{int(m["s2"])}</div>', unsafe_allow_html=True)
                        if cc2[2].button("＋", key=f"m_p2_{gn}_{mi}"): adj_score(tid, gn, mi, "B", 1); st.rerun()
                        
                    st.markdown('</div></div>', unsafe_allow_html=True)

# ─────── 3. 결과 마감 탭 ───────
elif M == "result":
    ts = load_tours()
    act = [k for k, v in ts.items() if v.get("status") == "진행중"]
    if not act:
        st.markdown(f"<div class='pg-title {title_cls['result']}'>📊 당일 최종 경기 결과 마감</div>", unsafe_allow_html=True)
        st.markdown("<div class='ic'>⚠️ 마감 처리할 활성화된 대회가 없습니다.</div>", unsafe_allow_html=True)
        st.stop()
        
    tid, t_obj = act[-1], ts[act[-1]]
    st.markdown(f"<div class='pg-title {title_cls['result']}'>📊 {t_obj['title']} 결과마감 패널</div>", unsafe_allow_html=True)
    
    earn = {}
    for gn, g_item in t_obj["groups"].items():
        st.markdown(f"<div class='sec'>🔷 그룹 {gn} ({g_item['mode']}) 시상 내역</div>", unsafe_allow_html=True)
        sv = stats_fixed(g_item["matches"]) if g_item["mode"] == "고정페어" else stats_kdk(g_item["matches"])
        ranked = sorted(list(sv.keys()), key=lambda x:(-sv[x]["승"], -sv[x]["득실"]))
        
        g_res = []
        for rank_idx, p_item in enumerate(ranked):
            pts = rank_pts(rank_idx+1, g_item["mode"])
            grd = grade(rank_idx+1)
            p_txt = " & ".join(list(p_item)) if g_item["mode"] == "고정페어" else p_item
            g_res.append({"최종 등수":grd, "선수명":p_txt, "최종 전적":f"{sv[p_item]['승']}승 {sv[p_item]['패']}패", "세트 득실":sv[p_item]["득실"], "부여 포인트":f"+{pts}점"})
            
            if g_item["mode"] == "고정페어":
                for individual in list(p_item): earn[individual] = earn.get(individual, 0) + pts
            else: earn[p_item] = earn.get(p_item, 0) + pts
        if g_res:
            st.markdown(df_to_html(pd.DataFrame(g_res)), unsafe_allow_html=True)
            
    if earn:
        st.markdown('<div class="sec sec-t">🏆 금일 누적 획득 예정 포인트</div>', unsafe_allow_html=True)
        res_df = pd.DataFrame(sorted(earn.items(), key=lambda x:-x[1]), columns=["선수명","지급포인트"])
        st.markdown(df_to_html(res_df), unsafe_allow_html=True)
        
    c_fin, c_rst = st.columns(2)
    with c_fin:
        if st.button("🏆 계산된 포인트 마스터 랭킹에 영구 반영", type="primary", use_container_width=True):
            r_master = load_rank()
            for p, p_val in earn.items():
                if p in r_master["이름"].values:
                    r_master.loc[r_master["이름"]==p, "현재포인트"] += p_val
                else:
                    new_r = {c:"" for c in COLS_RANK}; new_r["이름"]=p; new_r["현재포인트"]=p_val
                    r_master = pd.concat([r_master, pd.DataFrame([new_r])], ignore_index=True)
            save_rank(r_master); t_obj["status"]="완료"; save_tours(ts)
            st.success("🎉 당일 전적 데이터 마스터 백엔드 보드 반영 성공!"); st.rerun()

# ─────── 4. 기록실 탭 ───────
elif M == "archive":
    st.markdown(f"<div class='pg-title {title_cls['archive']}'>📂 두류 대회 기록실</div>", unsafe_allow_html=True)
    ts = load_tours()
    done = {k: v for k, v in ts.items() if v.get("status") == "완료"}
    if not done:
        st.markdown("<div class='ic'>📭 역대 완료 처리된 대회 히스토리가 기록되어 있지 않습니다.</div>", unsafe_allow_html=True)
    else:
        sel = st.selectbox("🏆 과거 대회 기록 선택조회", list(done.keys()), format_func=lambda x: done[x]["title"])
        if sel:
            t_past = done[sel]
            st.markdown(f"<div class='ic'>📋 대회명: {t_past['title']} (일시: {t_past.get('date','무기한')})</div>", unsafe_allow_html=True)
            for gn, g_item in t_past["groups"].items():
                st.markdown(f"<div class='sec'>🔷 그룹 {gn} ({g_item['mode']}) 최종 기록 결과</div>", unsafe_allow_html=True)
                sv = stats_fixed(g_item["matches"]) if g_item["mode"] == "고정페어" else stats_kdk(g_item["matches"])
                st.markdown(matrix_html(g_item["matches"], list(sv.keys()), (g_item["mode"]=="고정페어"), g_item.get("player_with_number",{})), unsafe_allow_html=True)

# ─────── 5. 관리자 탭 ───────
elif M == "admin":
    st.markdown(f"<div class='pg-title {title_cls['admin']}'>⚙️ 시스템 백엔드 관리자 패널</div>", unsafe_allow_html=True)
    if st.text_input("🔑 클럽 암호 입력", type="password") == ADMIN_PW:
        t1, t2, t3 = st.tabs(["🏆 랭킹/회원 데이터 제어", "📅 공식 새 대회 개최", "💥 시스템 초기화"])
        
        with t1:
            st.markdown("<div class='sec'>👥 회원 마스터 풀 통합 관리 영역</div>", unsafe_allow_html=True)
            m_list = load_members()
            txt = st.text_area("정회원 명단 제어 (각 이름은 반드시 쉼표(,)로 구분 요망)", value=",".join(m_list), height=140)
            if st.button("👥 정회원 명단 업데이트 반영", type="primary", use_container_width=True):
                save_members([x.strip() for x in txt.split(",") if x.strip()])
                st.success("✅ 회원 데이터 갱신 완료"); st.rerun()
                
            st.markdown("<div class='sec sec-t'>📊 랭킹 마스터 데이터 다이렉트 편집 및 엑셀 다운로드</div>", unsafe_allow_html=True)
            r_df = load_rank()
            if not r_df.empty:
                edited_df = st.data_editor(r_df, use_container_width=True, hide_index=True)
                c_save, c_dl = st.columns(2)
                with c_save:
                    if st.button("💾 데이터프레임 강제 오버라이드 저장", type="primary", use_container_width=True):
                        save_rank(edited_df); st.success("✅ 랭킹 원본 스토리지 변경 성공"); st.rerun()
                with c_dl:
                    out = BytesIO()
                    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
                        edited_df.to_excel(writer, index=False, sheet_name='Ranking')
                    st.download_button("📥 백업용 엑셀 시트 파일 다운로드", data=out.getvalue(), file_name=f"duryu_ranking_{date.today()}.xlsx", use_container_width=True)
            else:
                st.markdown("<div class='ic'>⚠️ 노출할 원본 랭킹 데이터프레임 어레이가 비어있습니다.</div>", unsafe_allow_html=True)
                
        with t2:
            st.markdown("<div class='sec'>📅 당일 기본 메타 세션 구성</div>", unsafe_allow_html=True)
            title = st.text_input("대회 공식 타이틀 명칭", f"{date.today().month}월 두류 테니스 클럽 대회")
            c_meta1, c_meta2, c_meta3 = st.columns(3)
            with c_meta1: dt = st.date_input("대회 일정", date.today())
            with c_meta2: loc = st.text_input("개최 장소", "두류테니스장")
            with c_meta3: ct = st.number_input("사용 코트 수(면)", min_value=1, max_value=10, value=2)
            
            st.markdown("<div class='sec sec-t'>👥 참가선수 선택 및 미등록 외부 인원 수동 추가</div>", unsafe_allow_html=True)
            all_m = load_members()
            selected_box = []
            if all_m:
                st.caption("💡 상단 저장소에 등록된 정회원 원터치 체크")
                cb_cols = st.columns(3)
                for idx, name in enumerate(all_m):
                    with cb_cols[idx % 3]:
                        if st.checkbox(name, key=f"adm_ch_{name}"): selected_box.append(name)
                        
            extra_txt = st.text_input("➕ 미등록/당일 게스트 참가 인원 수동 텍스트 직접 입력 (쉼표 구분)", "")
            extra_list = [x.strip() for x in extra_txt.split(",") if x.strip()]
            
            final_players = list(dict.fromkeys(selected_box + extra_list))
            if final_players:
                st.info(f"📋 당일 취합 완료된 종합 참가 인원 ({len(final_players)}명): " + ", ".join(final_players))
                
            st.markdown("<div class='sec sec-t'>🌿 조 분할 스케줄링 및 대진 로직 바인딩</div>", unsafe_allow_html=True)
            g_cnt = st.number_input("진행할 조 분할 개수 (최대 4개 조)", min_value=1, max_value=4, value=1)
            
            # 🚨 루프 내 고유 키 매핑 분리 및 리스트 초기화 오류 원천 차단 보정
            groups_config = {}
            for gi in range(int(g_cnt)):
                gn = chr(64 + (gi + 1))
                st.markdown(f"**🟢 [그룹 {gn}] 세부 옵션 빌딩**")
                g_p = st.multiselect(f"그룹 {gn} 매칭에 귀속시킬 참가자 선택", final_players, default=final_players if g_cnt==1 else None, key=f"g_sel_p_v2_{gn}")
                g_m = st.selectbox(f"그룹 {gn} 공식 경기 운영 방식", ["KDK (1인 3게임)", "KDK (1인 4게임)", "고정페어", "단식 풀리그"], key=f"g_sel_m_v2_{gn}")
                groups_config[gn] = {"players": g_p, "mode": g_m}
                
            if st.button("🚀 설정 세션 기반 자동 대진 매트릭스 동시 생성", type="primary", use_container_width=True):
                if not final_players:
                    st.error("❌ 선택되었거나 수동 입력창에 감지된 유효 참가자 데이터가 영(0)명입니다.")
                else:
                    tours = load_tours()
                    g_data = {}
                    for gn, conf in groups_config.items():
                        pl = conf["players"]
                        m = conf["mode"]
                        if not pl: continue
                        
                        if "KDK" in m:
                            gp = 3 if "3게임" in m else 4
                            ms, p2n = make_kdk(pl, gp)
                            if ms is None:
                                st.error(f"❌ 그룹 {gn}: 입력 인원수({len(pl)}명)에 매칭되는 정형 KDK 대진 파트너 트리 알고리즘이 부재합니다. 인원수를 검토하세요.")
                                st.stop()
                            g_data[gn] = {"matches": ms, "mode": "KDK", "games": gp, "player_with_number": p2n}
                        elif m == "고정페어":
                            ms, p2n = make_fixed(pl)
                            g_data[gn] = {"matches": ms, "mode": "고정페어", "player_with_number": p2n}
                        else:
                            ms, p2n = make_singles(pl)
                            g_data[gn] = {"matches": ms, "mode": "단식", "player_with_number": p2n}
                            
                    tours[f"tour_{int(random.random()*100000)}"] = {
                        "title": title, "date": str(dt), "place": loc, "courts": str(ct), "status": "진행중", "groups": g_data
                    }
                    save_tours(tours)
                    st.success("🎉 당일 맞춤형 대진표 시트 매트릭스 구축 완료! '대진' 탭에서 실시간 스코어 기록을 시작하세요."); st.rerun()
                    
        with t3:
            st.markdown("<div class='sec'>🚨 로컬 DB 원천 강제 셧다운 초기화</div>", unsafe_allow_html=True)
            st.warning("⚠️ 주의: 해당 삭제 버튼을 가동할 시 역대 로그 데이터 및 마스터 랭킹 보드가 완전 영구 격리 삭제됩니다.")
            if st.button("💥 시스템 내부 파일 완전 강제 초기화 초기 포맷", use_container_width=True):
                for fl in [RANK_FILE, MEMBER_FILE, TOUR_FILE]:
                    if os.path.exists(fl): os.remove(fl)
                st.success("💥 초기화 리셋 완료"); st.rerun()
