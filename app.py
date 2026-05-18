import streamlit as st
import pandas as pd
import random, os, json
from datetime import date
from io import BytesIO

# ══════════════════════════════════════════════════════════════
# 앱 설정
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="두류 테니스",
    page_icon="🎾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════
# CSS (모바일 강제 가로 정렬 + 슬림 1:1:1 비율 반영)
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

:root {
  /* 그린 계열 */
  --g0:#1B5E20; --g1:#2E7D32; --g2:#388E3C; --g3:#66BB6A; --g4:#C8E6C9; --g5:#E8F5E9;
  /* 메뉴 색상 (5개 메뉴) */
  --nav0:#2E7D32;  /* 랭킹 - 딥그린 */
  --nav1:#1565C0;  /* 대진 - 딥블루 */
  --nav2:#E65100;  /* 결과 - 딥오렌지 */
  --nav3:#4A148C;  /* 기록 - 딥퍼플 */
  --nav4:#00695C;  /* 관리 - 딥틸 */
  /* 매치 카드 색상 */
  --mc0:#1B5E20; --mc1:#0D47A1; --mc2:#BF360C; --mc3:#4A148C; --mc4:#006064;
  --mc5:#1A237E; --mc6:#880E4F; --mc7:#33691E;
  /* 팀박스 색상 */
  --tb0:#2E7D32; --tb1:#1565C0; --tb2:#D84315; --tb3:#6A1B9A; --tb4:#00695C;
  --tb5:#283593; --tb6:#AD1457; --tb7:#558B2F;
  /* 기본 */
  --yel:#FFD600; --ora:#FB8C00;
  --bg:#F4F6F9; --card:#fff; --bd:#E0E4EA;
  --r1:10px; --r2:16px; --r3:24px;
  --sh:0 2px 10px rgba(0,0,0,.08);
  --sh2:0 4px 20px rgba(0,0,0,.13);
  --tx:#1a1a2e; --tx2:#3a3a5c;
}

*{ font-family:'Noto Sans KR',sans-serif!important; box-sizing:border-box; -webkit-tap-highlight-color:transparent; }
.block-container{ padding:0 0.7rem 5rem!important; max-width:520px!important; margin:0 auto!important; background:var(--bg)!important; }
.stApp{ background:var(--bg)!important; }

/* ── 헤더 ── */
.hdr{
  background:linear-gradient(135deg,#1B5E20 0%,#2E7D32 60%,#388E3C 100%);
  margin:0 -0.7rem 0; padding:14px 18px 0; position:relative; overflow:hidden; box-shadow:var(--sh2);
}
.hdr::after{ content:'🎾'; position:absolute; right:14px; top:8px; font-size:2.6rem; opacity:.12; }
.hdr-title{ color:#fff; font-size:1.05rem; font-weight:900; margin:0 0 2px; }
.hdr-sub{ color:rgba(255,255,255,.5); font-size:.58rem; letter-spacing:2px; margin-bottom:0; }

/* ── 네비게이션 탭바 ── */
.nav-wrapper{
  display:flex; margin:0 -0.7rem 14px; overflow:hidden;
  box-shadow:0 3px 12px rgba(0,0,0,.18);
}
.nav-btn{
  flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center;
  padding:9px 2px 10px; cursor:pointer; border:none; outline:none;
  font-size:.62rem; font-weight:700; line-height:1.35;
  color:rgba(255,255,255,.72); transition:all .15s; min-height:56px;
  border-bottom:3px solid transparent; gap:1px;
}
.nav-btn .nav-icon{ font-size:1.1rem; line-height:1; }
.nav-btn.n0{ background:var(--nav0); }
.nav-btn.n1{ background:var(--nav1); }
.nav-btn.n2{ background:var(--nav2); }
.nav-btn.n3{ background:var(--nav3); }
.nav-btn.n4{ background:var(--nav4); }
.nav-btn.active{ color:#fff; border-bottom:3px solid var(--yel); filter:brightness(1.15); }
.nav-btn:not(.active){ filter:brightness(0.75); }

/* ── 페이지 타이틀 ── */
.pg-title{
  color:#fff; padding:12px 16px; border-radius:var(--r2);
  margin:0 0 14px; font-size:1rem; font-weight:900; text-align:center; box-shadow:var(--sh2);
}
.pg-title.c0{ background:linear-gradient(135deg,var(--nav0),#43A047); }
.pg-title.c1{ background:linear-gradient(135deg,var(--nav1),#1976D2); }
.pg-title.c2{ background:linear-gradient(135deg,var(--nav2),#F4511E); }
.pg-title.c3{ background:linear-gradient(135deg,var(--nav3),#7B1FA2); }
.pg-title.c4{ background:linear-gradient(135deg,var(--nav4),#00897B); }

/* ── 섹션 헤더 ── */
.sec{
  font-size:.85rem; font-weight:800; color:var(--g0); border-left:4px solid var(--g3);
  padding-left:9px; margin:16px 0 8px;
}

/* ── 탭 ── */
button[data-baseweb="tab"]{
  font-size:.7rem!important; font-weight:700!important; padding:9px 6px!important;
  border-radius:var(--r1) var(--r1) 0 0!important; min-height:42px!important;
}
button[data-baseweb="tab"][aria-selected="true"]{
  background:linear-gradient(135deg,var(--g0),var(--g2))!important; color:#fff!important;
}
[data-baseweb="tab-list"]{
  background:#DDD!important; border-radius:var(--r1) var(--r1) 0 0!important;
  padding:4px 4px 0!important; gap:2px!important;
}

/* ── 데이터프레임 강제 가운데 정렬 ── */
div[data-testid="stDataFrame"] iframe {
  width: 100%;
}
div[data-testid="stDataFrame"] *, 
div[data-testid="stDataFrame"] [role="gridcell"], 
div[data-testid="stDataFrame"] [role="columnheader"] {
  text-align: center !important;
  justify-content: center !important;
  align-items: center !important;
}

/* ══════════════════════════════════════════════════════════════
   ★ 모바일 화면 가로 강제 한 줄 고정 고도화 디자인 (핵심 수정)
══════════════════════════════════════════════════════════════ */
.match-card{
  background:var(--card); border-radius:var(--r2); padding:12px 10px 14px;
  margin:12px 0; box-shadow:var(--sh2); border:1px solid var(--bd);
}
.match-no{
  display:inline-block; border-radius:20px; padding:3px 14px;
  font-size:.6rem; font-weight:900; margin-bottom:10px; color:#fff;
}
.mc0{background:var(--mc0);} .mc1{background:var(--mc1);} .mc2{background:var(--mc2);}
.mc3{background:var(--mc3);} .mc4{background:var(--mc4);} .mc5{background:var(--mc5);}
.mc6{background:var(--mc6);} .mc7{background:var(--mc7);}

/* 팀 이름 박스 */
.team-name{
  border-radius:var(--r1); padding:6px 4px; font-weight:900; font-size:.82rem;
  text-align:center; color:#fff; box-shadow:var(--sh); min-height:40px;
  display:flex; align-items:center; justify-content:center; word-break:keep-all; line-height:1.2;
  margin-bottom: 6px;
}
.tb0{background:var(--tb0);} .tb1{background:var(--tb1);} .tb2{background:var(--tb2);}
.tb3{background:var(--tb3);} .tb4{background:var(--tb4);} .tb5{background:var(--tb5);}
.tb6{background:var(--tb6);} .tb7{background:var(--tb7);}

/* 🔥 모바일에서도 절대 세로로 떨어지지 않도록 무조건 가로 1열 강제 배정 */
div.score-btn-wrap [data-testid="stHorizontalBlock"] {
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  width: 100% !important;
  gap: 3px !important;
  align-items: center !important;
}

/* 내부에 있는 [-], [숫자], [+] 컬럼 세 개를 정확히 가로 1:1:1 비율 균등 분할 */
div.score-btn-wrap [data-testid="stHorizontalBlock"] > div {
  flex: 1 !important;
  min-width: 0 !important;
  max-width: 33.333% !important;
  width: 33.333% !important;
}

/* 캡처 사진처럼 납작하고 이쁜 가로 스케일 정사각 콤팩트 패널 디자인 */
div.score-btn-wrap button, .score-num-display {
  width: 100% !important;
  aspect-ratio: 1 / 1 !important; /* 가로세로 완벽 1:1 비율 */
  height: auto !important;
  font-size: 1.1rem !important;    /* 숫자가 작아지지 않게 조절 */
  font-weight: 900 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 !important;
  margin: 0 !important;
}

/* 버튼 디자인 튜닝 */
div.score-btn-wrap button {
  background: #E8F5E9 !important;
  border: 1.5px solid #C8E6C9 !important;
  color: #1B5E20 !important;
  border-radius: 8px !important;
}
div.score-btn-wrap button:active {
  background: #A5D6A7 !important;
}

/* 숫자 패널 디자인 */
.score-num-display {
  background: #fff; 
  border: 1.5px solid #C8E6C9; 
  border-radius: 8px;
  color: #1B5E20;
}

/* 중간 VS 마크 정렬 */
.vs-col {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  height: 100% !important;
}
.vs-badge{
  width:30px; height:30px; border-radius:50%;
  background:linear-gradient(135deg,#FFB74D,var(--ora));
  display:flex; align-items:center; justify-content:center;
  font-weight:900; font-size:.6rem; color:#fff; box-shadow:var(--sh);
}

/* ── streamlit 버튼 공통 ── */
.stButton>button{
  border-radius:var(--r2)!important; font-weight:700!important; font-size:.82rem!important;
  min-height:50px!important; padding:10px 14px!important;
}
.stButton>button[kind="primary"]{
  background:linear-gradient(135deg,var(--g0),var(--g2))!important; color:#fff!important;
  border:none!important; box-shadow:0 4px 14px rgba(46,125,50,.35)!important;
}

/* ── 매트릭스 / KDK 테이블 ── */
.mx-wrap, .kdk{
  background:var(--card); border-radius:var(--r1); padding:10px;
  box-shadow:var(--sh); overflow-x:auto; margin:8px 0; border:1px solid var(--bd);
}
.mx, .kdk table{ border-collapse:collapse; white-space:nowrap; font-size:.68rem; width:100%; }
.mx th,.mx td, .kdk th,.kdk td{ padding:6px 7px; border:1px solid var(--bd); text-align:center; }
.mx thead th, .kdk thead th{ background:var(--g0); color:#fff; font-weight:700; }
.mx-grey{ background:#D0D0D0!important; color:#D0D0D0!important; }
.mx-dash{ color:#CCC; }
.mx-sc{ font-weight:800; color:var(--g0); }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 데이터 처리 로직 및 상수 (이전과 동일)
# ══════════════════════════════════════════════════════════════
RANK_FILE   = "ranking_master.csv"
MEMBER_FILE = "member_roster.json"
TOUR_FILE   = "tournaments.json"
ADMIN_PW    = "0502"
COLS_RANK   = ["랭킹","이름","현재포인트","3월 포인트","결과","부과점","그룹","비고"]

GCLS  = ["mc0","mc1","mc2","mc3","mc4","mc5","mc6","mc7"]
TBCLS = ["tb0","tb1","tb2","tb3","tb4","tb5","tb6","tb7"]
GLBL  = ["🟢","🔵","🟠","🟣","🩵","🔴","🟡","⚪"]

KDK_3G = {
    4:  [(1,4,2,3),(1,3,2,4),(1,2,3,4)],
    8:  [(1,2,3,4),(5,6,7,8),(1,8,2,7),(3,6,4,5),(1,4,5,8),(2,3,6,7)],
    12: [(1,2,3,4),(5,6,7,8),(9,10,11,12),(1,3,5,7),(2,4,6,8),
         (9,11,1,5),(4,8,9,12),(6,7,10,11),(10,12,2,3)],
}
KDK_4G = {
    5:  [(1,2,3,4),(1,3,2,5),(1,4,3,5),(1,5,2,4),(2,3,4,5)],
    6:  [(1,3,2,4),(1,5,4,6),(2,3,5,6),(1,4,3,5),(2,6,3,4),(1,6,2,5)],
    7:  [(1,2,3,4),(5,6,1,7),(2,3,5,7),(1,4,6,7),(3,5,2,4),(1,6,2,5),(4,6,3,7)],
    8:  [(1,2,3,4),(5,6,7,8),(1,3,5,7),(2,4,6,8),(1,5,2,6),(3,7,4,8),(1,6,3,8),(2,5,4,7)],
    9:  [(1,2,3,4),(5,6,7,8),(1,9,5,7),(2,3,6,8),(4,9,3,8),(1,5,2,6),(3,6,4,5),(1,7,8,9),(2,4,7,9)],
    10: [(1,2,3,5),(6,7,8,10),(2,3,4,6),(7,8,1,9),(3,4,5,7),(8,9,2,10),
         (4,5,6,8),(1,3,9,10),(5,6,7,9),(1,10,2,4)],
    11: [(1,2,3,5),(6,7,8,10),(4,9,1,11),(2,3,6,8),(4,5,7,10),(9,11,2,6),
         (1,3,7,11),(4,8,5,9),(1,10,2,8),(4,7,6,11),(3,9,5,10)],
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
        with open(MEMBER_FILE, "r") as f: return json.load(f)
    df = load_rank()
    return df["이름"].tolist() if not df.empty else []

def save_members(names):
    with open(MEMBER_FILE, "w") as f: json.dump(names, f, ensure_ascii=False, indent=2)

def load_tours():
    if os.path.exists(TOUR_FILE):
        with open(TOUR_FILE, "r") as f: return json.load(f)
    return {}

def save_tours(d):
    with open(TOUR_FILE, "w") as f: json.dump(d, f, ensure_ascii=False, indent=2)

def to_excel(df):
    buf = BytesIO()
    df.to_excel(buf, index=False)
    return buf.getvalue()

def stats_fixed(matches):
    s = {}
    for m in matches:
        t1, t2 = tuple(m["t1"]), tuple(m["t2"])
        for t in (t1, t2):
            if t not in s: s[t] = {"승":0,"패":0,"득실":0}
        a, b = int(m["s1"]), int(m["s2"])
        if a > b:   s[t1]["승"]+=1; s[t2]["패"]+=1
        elif b > a: s[t2]["승"]+=1; s[t1]["패"]+=1
        s[t1]["득실"] += a-b
        s[t2]["득실"] += b-a
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
    if rank <= 2: return 7
    if rank <= 4: return 5
    if rank <= 6: return 3
    return 1

def grade(rank):
    if rank <= 2: return "🥇 우승"
    if rank <= 4: return "🥈 준우승"
    if rank <= 6: return "🥉 3위"
    return "참가"

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
    ms = [{"t1":list(pairs[i]), "t2":list(pairs[j]), "s1":0, "s2":0}
          for i in range(len(pairs)) for j in range(i+1, len(pairs))]
    random.shuffle(ms)
    return ms, {}

def make_singles(players):
    pl = players[:]
    random.shuffle(pl)
    ms = [{"t1":[pl[i]], "t2":[pl[j]], "s1":0, "s2":0}
          for i in range(len(pl)) for j in range(i+1, len(pl))]
    random.shuffle(ms)
    return ms, {}

def kdk_html(n, gperson, p2n):
    bp = KDK_3G.get(n) if gperson == 3 else KDK_4G.get(n)
    if not bp: return ""
    n2p = {v: k for k, v in p2n.items()}
    title = f"KDK 1인 {gperson}게임 — {n}명"
    rows = ""
    for i, (a,b,c,d) in enumerate(bp):
        t1 = f"{n2p.get(a,a)}({a}) &amp; {n2p.get(b,b)}({b})"
        t2 = f"{n2p.get(c,c)}({c}) &amp; {n2p.get(d,d)}({d})"
        rows += (f"<tr><td style='text-align:center'>"
                 f"<span style='background:#1B5E20;color:#fff;border-radius:20px;"
                 f"padding:2px 9px;font-size:.6rem;font-weight:700'>{i+1}</span>"
                 f"</td><td style='text-align:left;white-space:nowrap'>{t1} vs {t2}</td></tr>")
    return (f'<div class="kdk"><div style="font-size:.75rem;font-weight:800;'
            f'color:#1B5E20;margin-bottom:6px">📋 {title}</div>'
            f'<table><thead><tr><th style="width:38px">순서</th><th>대진</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')

def show_kdk(n, gperson, p2n):
    st.markdown(kdk_html(n, gperson, p2n), unsafe_allow_html=True)

def matrix_html(matches, rank_items, is_fixed, p2n):
    if not matches or not rank_items: return ""
    if is_fixed: lab = {t: " &amp; ".join(list(t)) for t in rank_items}
    else:        lab = {p: f"{p}({p2n.get(p,'?')})" for p in rank_items}
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
    header = "".join(f"<th style='white-space:nowrap'>{k}</th>" for k in keys)
    body = ""
    for rk in keys:
        body += f"<tr><th style='white-space:nowrap'>{rk}</th>"
        for ck in keys:
            v = mat[rk][ck]
            if v == "■":   body += '<td class="mx-grey">■</td>'
            elif v == "—": body += '<td class="mx-dash">—</td>'
            else:          body += f'<td class="mx-sc">{v}</td>'
        body += "</tr>"
    return (f'<div class="mx-wrap"><table class="mx">'
            f'<thead><tr><th></th>{header}</tr></thead>'
            f'<tbody>{body}</tbody></table></div>')

def adj_score(tid, grp, mi, side, delta):
    tours = load_tours()
    m = tours[tid]["groups"][grp]["matches"][mi]
    key = "s1" if side == "A" else "s2"
    m[key] = max(0, int(m[key]) + delta)
    save_tours(tours)

# ══════════════════════════════════════════════════════════════
# 세션 초기화 및 메뉴 구성
# ══════════════════════════════════════════════════════════════
ss = st.session_state
if "is_admin" not in ss: ss.is_admin = False
if "menu" not in ss: ss.menu = "ranking"

MENUS = [
    ("ranking", "🏆", "랭킹", "n0"),
    ("schedule","📅", "대진", "n1"),
    ("result",  "📊", "결과", "n2"),
    ("archive", "📂", "기록", "n3"),
    ("admin",   "⚙️", "관리", "n4"),
]

st.markdown('<div class="hdr"><div class="hdr-title">🎾 두류 테니스 클럽</div>'
            '<div class="hdr-sub">DURYU TENNIS CLUB</div></div>', unsafe_allow_html=True)

nav_cols = st.columns(len(MENUS))
for col, (key, icon, label, nc) in zip(nav_cols, MENUS):
    with col:
        if st.button(f"{icon}\n{label}", key=f"nav_{key}", use_container_width=True, type="primary" if ss.menu == key else "secondary"):
            ss.menu = key
            st.rerun()

menu_colors = {"ranking":"#2E7D32","schedule":"#1565C0","result":"#E65100","archive":"#4A148C","admin":"#00695C"}
st.markdown(f'<div style="height:4px;background:{menu_colors.get(ss.menu, "#2E7D32")};margin:0 -0.7rem 14px;box-shadow:0 2px 8px rgba(0,0,0,.2)"></div>', unsafe_allow_html=True)

title_cls = {"ranking":"c0","schedule":"c1","result":"c2","archive":"c3","admin":"c4"}
M = ss.menu

# 랭킹 탭
if M == "ranking":
    st.markdown(f"<div class='pg-title {title_cls['ranking']}'>🏆 두류 랭킹</div>", unsafe_allow_html=True)
    df = load_rank()
    if df.empty:
        st.markdown("<div class='ic'>📭 등록된 랭킹이 없습니다.</div>", unsafe_allow_html=True)
    else:
        medal = ["🥇","🥈","🥉"]
        d = df.copy()
        d.insert(0, "순위", [medal[i] if i < 3 else str(i+1) for i in range(len(d))])
        st.dataframe(d, use_container_width=True, hide_index=True, column_config={c: st.column_config.TextColumn(c, width="small") for c in d.columns})

# 대진 탭 (핵심 수정 구역)
elif M == "schedule":
    tours = load_tours()
    active = [k for k, v in tours.items() if v.get("status") == "진행중"]
    if not active:
        st.markdown(f"<div class='pg-title {title_cls['schedule']}'>📅 대진표</div>", unsafe_allow_html=True)
        st.markdown("<div class='ic'>⚠️ 진행 중인 대회가 없습니다.</div>", unsafe_allow_html=True)
        st.stop()

    tid, tour = active[-1], tours[active[-1]]
    st.markdown(f"<div class='pg-title {title_cls['schedule']}'>📅 {tour['title']}</div>", unsafe_allow_html=True)
    gnames = list(tour["groups"].keys())
    
    if gnames:
        tabs = st.tabs([f"{GLBL[i%len(GLBL)]} {g}" for i, g in enumerate(gnames)])
        for ti, g in enumerate(gnames):
            with tabs[ti]:
                gi, ms, mode = tour["groups"][g], tour["groups"][g]["matches"], tour["groups"][g]["mode"]
                p2n, fx = gi.get("player_with_number", {}), (mode == "고정페어")
                sv = stats_fixed(ms) if fx else stats_kdk(ms)
                
                st.markdown("<div class='sec'>📋 전적 매트릭스</div>", unsafe_allow_html=True)
                st.markdown(matrix_html(ms, list(sv.keys()), fx, p2n), unsafe_allow_html=True)
                
                st.markdown("<div class='sec'>🎾 경기 입력</div>", unsafe_allow_html=True)
                for mi, m in enumerate(ms):
                    t1s, t2s = " & ".join(m["t1"]), " & ".join(m["t2"])
                    
                    st.markdown(f'<div class="match-card"><span class="match-no {GCLS[mi%len(GCLS)]}">MATCH {mi+1}</span>', unsafe_allow_html=True)
                    
                    # 좌팀, VS마크, 우팀 정렬 구조
                    m_col1, m_vs, m_col2 = st.columns([10, 3, 10])
                    
                    with m_col1:
                        st.markdown(f'<div class="team-name {TBCLS[mi%len(TBCLS)]}">{t1s}</div>', unsafe_allow_html=True)
                        st.markdown('<div class="score-btn-wrap">', unsafe_allow_html=True)
                        ctrl = st.columns(3)
                        if ctrl[0].button("－", key=f"btn_m_A_{g}_{mi}"): adj_score(tid, g, mi, "A", -1); st.rerun()
                        ctrl[1].markdown(f'<div class="score-num-display">{int(m["s1"])}</div>', unsafe_allow_html=True)
                        if ctrl[2].button("＋", key=f"btn_p_A_{g}_{mi}"): adj_score(tid, g, mi, "A", 1); st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)

                    with m_vs:
                        st.markdown('<div style="height:42px;"></div>', unsafe_allow_html=True)
                        st.markdown('<div class="vs-col"><div class="vs-badge">VS</div></div>', unsafe_allow_html=True)

                    with m_col2:
                        st.markdown(f'<div class="team-name {TBCLS[mi%len(TBCLS)]}">{t2s}</div>', unsafe_allow_html=True)
                        st.markdown('<div class="score-btn-wrap">', unsafe_allow_html=True)
                        ctrl = st.columns(3)
                        if ctrl[0].button("－", key=f"btn_m_B_{g}_{mi}"): adj_score(tid, g, mi, "B", -1); st.rerun()
                        ctrl[1].markdown(f'<div class="score-num-display">{int(m["s2"])}</div>', unsafe_allow_html=True)
                        if ctrl[2].button("＋", key=f"btn_p_B_{g}_{mi}"): adj_score(tid, g, mi, "B", 1); st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    st.markdown('</div>', unsafe_allow_html=True)

# 결과 마감 탭
elif M == "result":
    tours = load_tours()
    active = [k for k, v in tours.items() if v.get("status") == "진행중"]
    if active:
        stid2, t2 = active[-1], tours[active[-1]]
        st.markdown(f"<div class='pg-title {title_cls['result']}'>📊 {t2['title']} 마감</div>", unsafe_allow_html=True)
        earn = {}
        for gn, gi in t2["groups"].items():
            sv = stats_fixed(gi["matches"]) if gi["mode"] == "고정페어" else stats_kdk(gi["matches"])
            ranked = sorted(list(sv.keys()), key=lambda x: (-sv[x]["승"], -sv[x]["득실"]))
            for i, item in enumerate(ranked):
                pt = rank_pts(i+1, gi["mode"])
                if gi["mode"] == "고정페어":
                    for p in list(item): earn[p] = earn.get(p, 0) + pt
                else: earn[item] = earn.get(item, 0) + pt
        if earn:
            ef = pd.DataFrame(earn.items(), columns=["선수","획득포인트"])
            st.dataframe(ef, use_container_width=True)
            if st.button("🏆 랭킹 반영", type="primary", use_container_width=True):
                dr = load_rank()
                for p, pt in earn.items():
                    if p in dr["이름"].values: dr.loc[dr["이름"]==p, "현재포인트"] += pt
                save_rank(dr); tours[stid2]["status"] = "완료"; save_tours(tours)
                st.success("✅ 반영 완료!"); st.rerun()

# 기록 아카이브 탭
elif M == "archive":
    st.markdown(f"<div class='pg-title {title_cls['archive']}'>📂 대회 기록실</div>", unsafe_allow_html=True)
    ts = load_tours()
    done = {k: v for k, v in ts.items() if v.get("status") == "완료"}
    if done:
        sel = st.selectbox("🏆 대회 선택", list(done.keys()), format_func=lambda x: done[x]["title"])
        if sel:
            t = done[sel]
            for gn, gi in t["groups"].items():
                st.markdown(f"<div class='sec'>🔷 그룹: {gn} ({gi['mode']})</div>", unsafe_allow_html=True)
                sv = stats_fixed(gi["matches"]) if gi["mode"] == "고정페어" else stats_kdk(gi["matches"])
                st.markdown(matrix_html(gi["matches"], list(sv.keys()), (gi["mode"]=="고정페어"), gi.get("player_with_number",{})), unsafe_allow_html=True)

# 관리자 탭
elif M == "admin":
    st.markdown(f"<div class='pg-title {title_cls['admin']}'>⚙️ 관리자 설정</div>", unsafe_allow_html=True)
    if st.text_input("🔑 관리자 비밀번호", type="password") == ADMIN_PW:
        t1, t2 = st.tabs(["🏆 명단 편집", "📅 대회 개최"])
        with t1:
            m_list = load_members()
            txt = st.text_area("회원 이름 (쉼표 구분)", value=",".join(m_list), height=150)
            if st.button("👥 명단 저장", type="primary", use_container_width=True):
                save_members([x.strip() for x in txt.split(",") if x.strip()])
                st.success("✅ 저장 완료")
        with t2:
            title = st.text_input("대회명", f"{date.today().month}월 두류 테니스 대회")
            all_m = load_members()
            sel_m = [n for n in all_m if st.checkbox(name, key=f"p_{n}")] if all_m else []
            g_m = st.selectbox("대진 방식", ["KDK (1인 3게임)", "고정페어"])
            if st.button("🚀 대회 시작", type="primary", use_container_width=True) and sel_m:
                tours = load_tours()
                ms, p2n = make_fixed(sel_m) if g_m == "고정페어" else make_kdk(sel_m, 3)
                tours[f"tour_{int(random.random()*100000)}"] = {"title": title, "status": "진행중", "groups": {"A": {"matches": ms, "mode": g_m, "player_with_number": p2n}}}
                save_tours(tours); st.success("🎉 생성 완료"); st.rerun()
