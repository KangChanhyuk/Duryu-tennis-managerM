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
# CSS (모바일 최적화 + 다양한 색상 + 정사각 점수 버튼)
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
/* ── 인포 카드 ── */
.ic{
  background:var(--card); border-left:4px solid var(--g3); border-radius:var(--r1);
  padding:10px 14px; margin:7px 0; box-shadow:var(--sh); font-size:.8rem; color:var(--tx2);
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

/* ── 데이터프레임 가운데 정렬 ── */
div[data-testid="stDataFrame"]{
  border-radius:var(--r1)!important; overflow:hidden!important;
  box-shadow:var(--sh)!important; border:1px solid var(--bd)!important;
  width:100%!important;
}
div[data-testid="stDataFrame"] table{
  width:100%!important; font-size:.74rem!important; border-collapse:collapse!important;
}
div[data-testid="stDataFrame"] table th,
div[data-testid="stDataFrame"] table td{
  text-align:center!important; vertical-align:middle!important;
  padding:8px 4px!important; white-space:nowrap;
}
div[data-testid="stDataFrame"] thead tr th{
  background:var(--g0)!important; color:#fff!important; font-weight:700!important;
}
div[data-testid="stDataFrame"] tbody tr:nth-child(even) td{ background:var(--g5)!important; }

/* ══════════════════════════════════════════════════════════════
   경기 카드 — 레이아웃 및 완벽 오버레이 투명 버튼화
══════════════════════════════════════════════════════════════ */
.match-card{
  background:var(--card); border-radius:var(--r2); padding:12px 10px 14px;
  margin:12px 0; box-shadow:var(--sh2); border:1px solid var(--bd);
  position:relative;
}
.match-no{
  display:inline-block; border-radius:20px; padding:3px 14px;
  font-size:.6rem; font-weight:900; margin-bottom:10px; color:#fff;
}
.mc0{background:var(--mc0);} .mc1{background:var(--mc1);} .mc2{background:var(--mc2);}
.mc3{background:var(--mc3);} .mc4{background:var(--mc4);} .mc5{background:var(--mc5);}
.mc6{background:var(--mc6);} .mc7{background:var(--mc7);}

.match-row{
  display:flex; align-items:stretch; gap:6px; width:100%; position:relative;
}
.team-side{
  flex:1; display:flex; flex-direction:column; gap:6px; position:relative;
}
.team-name{
  border-radius:var(--r1); padding:8px 4px; font-weight:900; font-size:.82rem;
  text-align:center; color:#fff; box-shadow:var(--sh); min-height:46px;
  display:flex; align-items:center; justify-content:center; word-break:keep-all; line-height:1.2;
}
.tb0{background:var(--tb0);} .tb1{background:var(--tb1);} .tb2{background:var(--tb2);}
.tb3{background:var(--tb3);} .tb4{background:var(--tb4);} .tb5{background:var(--tb5);}
.tb6{background:var(--tb6);} .tb7{background:var(--tb7);}

/* 점수 디자인 뼈대 */
.score-ctrl{
  display:flex; align-items:stretch; gap:3px; height:48px; position:relative;
}
.score-ctrl .score-minus,
.score-ctrl .score-plus{
  flex:1; display:flex; align-items:center; justify-content:center;
  background:#E8F5E9; border:2px solid #C8E6C9; border-radius:var(--r1);
  font-size:1.3rem; font-weight:900; color:#1B5E20;
}
.score-ctrl .score-num{
  flex:1.4; display:flex; align-items:center; justify-content:center;
  background:#fff; border:2.5px solid #C8E6C9; border-radius:var(--r1);
  font-size:1.5rem; font-weight:900; color:#1B5E20;
}

.vs-col{ width:36px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.vs-badge{
  width:34px; height:34px; border-radius:50%;
  background:linear-gradient(135deg,#FFB74D,var(--ora));
  display:flex; align-items:center; justify-content:center;
  font-weight:900; font-size:.65rem; color:#fff; box-shadow:var(--sh);
}

/* ── 일반 Streamlit 버튼 스타일 ── */
.stButton>button{
  border-radius:var(--r2)!important; font-weight:700!important; font-size:.82rem!important;
  min-height:50px!important; padding:10px 14px!important;
}
.stButton>button[kind="primary"]{
  background:linear-gradient(135deg,var(--g0),var(--g2))!important; color:#fff!important;
  border:none!important; box-shadow:0 4px 14px rgba(46,125,50,.35)!important;
}

/* ★ 초강력 오버레이 투명화 규칙 (순정 버튼 외형 완전 소멸) ★ */
.stepper-overlay-container {
    display: flex !important; width: 100% !important; gap: 6px !important; 
    margin-top: -60px !important; margin-bottom: 12px !important; position: relative !important; z-index: 9999 !important;
}
.stepper-overlay-side {
    flex: 1 !important; display: flex !important; gap: 3px !important; height: 48px !important;
}
.st-btn-hidden-wrapper {
    flex: 1 !important; height: 48px !important; background: transparent !important;
}
/* 대진 탭 내 오버레이 껍데기 박스 및 내부 버튼 강제 투명화 처리 */
.stepper-overlay-container div[data-testid="stButton"],
.stepper-overlay-container button {
    height: 48px !important; min-height: 48px !important; margin: 0 !important; padding: 0 !important; width: 100% !important;
    background: transparent !important; background-color: transparent !important;
    border: none !important; border-color: transparent !important;
    color: transparent !important; text-color: transparent !important;
    box-shadow: none !important; outline: none !important;
}
.stepper-overlay-container button p {
    display: none !important; /* 내부 글자 원천 차단 */
}
.stepper-overlay-container button:active, .stepper-overlay-container button:focus {
    background: rgba(46, 125, 50, 0.15) !important; /* 클릭 피드백만 살짝 제공 */
    border: none !important; box-shadow: none !important;
}
.stepper-overlay-spacer { width: 36px !important; flex-shrink: 0 !important; }

/* ── 입력 필드 ── */
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div{
  min-height:48px!important; border-radius:var(--r1)!important;
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

/* ── 파일 업로더 ── */
[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInstructions"]>div>span,
[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInstructions"]>div>small{ display:none!important; }
[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"]::after{ content:'📂 파일 선택'; }
[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"] span{ display:none!important; }
[data-testid="stFileUploaderDropzone"]{ border:2px dashed var(--g3)!important; background:var(--g5)!important; }

/* ── 랭킹 뱃지 ── */
.rank-badge{
  display:inline-flex; align-items:center; justify-content:center;
  background:var(--g0); color:#fff; border-radius:8px;
  font-size:.7rem; font-weight:700; padding:4px 10px; margin-bottom:6px;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 상수 및 헬퍼
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
    if not os.path.exists(RANK_FILE):
        return pd.DataFrame(columns=COLS_RANK)
    df = pd.read_csv(RANK_FILE)
    for c in ["현재포인트","3월 포인트","부과점"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
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
        with open(MEMBER_FILE, "r") as f:
            return json.load(f)
    df = load_rank()
    return df["이름"].tolist() if not df.empty else []

def save_members(names):
    with open(MEMBER_FILE, "w") as f:
        json.dump(names, f, ensure_ascii=False, indent=2)

def load_tours():
    if os.path.exists(TOUR_FILE):
        with open(TOUR_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tours(d):
    with open(TOUR_FILE, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

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
    if mode == "고정페어":
        return {1:7, 2:5, 3:3}.get(rank, 1)
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
    if is_fixed:
        lab = {t: " &amp; ".join(list(t)) for t in rank_items}
    else:
        lab = {p: f"{p}({p2n.get(p,'?')})" for p in rank_items}
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
# 세션 초기화
# ══════════════════════════════════════════════════════════════
ss = st.session_state
if "is_admin"    not in ss: ss.is_admin    = False
if "menu"        not in ss: ss.menu        = "ranking"
if "participants" not in ss: ss.participants = []

# ══════════════════════════════════════════════════════════════
# 네비게이션
# ══════════════════════════════════════════════════════════════
MENUS = [
    ("ranking", "🏆", "랭킹",  "n0"),
    ("schedule","📅", "대진",  "n1"),
    ("result",  "📊", "결과",  "n2"),
    ("archive", "📂", "기록",  "n3"),
    ("admin",   "⚙️", "관리",  "n4"),
]

st.markdown('<div class="hdr"><div class="hdr-title">🎾 두류 테니스 클럽</div>'
            '<div class="hdr-sub">DURYU TENNIS CLUB</div></div>', unsafe_allow_html=True)

nav_cols = st.columns(len(MENUS))
for col, (key, icon, label, nc) in zip(nav_cols, MENUS):
    with col:
        is_active = (ss.menu == key)
        btn_type = "primary" if is_active else "secondary"
        btn_label = f"{icon}\n{label}"
        if st.button(btn_label, key=f"nav_{key}", use_container_width=True, type=btn_type):
            ss.menu = key
            st.rerun()

menu_colors = {"ranking":"#2E7D32","schedule":"#1565C0","result":"#E65100","archive":"#4A148C","admin":"#00695C"}
cur_color = menu_colors.get(ss.menu, "#2E7D32")
st.markdown(f'<div style="height:4px;background:{cur_color};margin:0 -0.7rem 14px;'
            f'box-shadow:0 2px 8px rgba(0,0,0,.2)"></div>', unsafe_allow_html=True)

title_cls = {"ranking":"c0","schedule":"c1","result":"c2","archive":"c3","admin":"c4"}
M = ss.menu

# ══════════════════════════════════════════════════════════════
# 1. 랭킹
# ══════════════════════════════════════════════════════════════
if M == "ranking":
    tc = title_cls["ranking"]
    st.markdown(f"<div class='pg-title {tc}'>🏆 두류 랭킹</div>", unsafe_allow_html=True)

    df = load_rank()
    if df.empty:
        st.markdown("<div class='ic'>📭 등록된 랭킹이 없습니다.<br>"
                    "관리자 메뉴에서 엑셀을 업로드해 주세요.</div>", unsafe_allow_html=True)
    else:
        medal = ["🥇","🥈","🥉"]
        d = df.copy()
        d.insert(0, "순위", [medal[i] if i < 3 else str(i+1) for i in range(len(d))])
        cfg = {c: st.column_config.TextColumn(c, width="small") for c in d.columns}
        st.dataframe(d, use_container_width=True, hide_index=True, column_config=cfg)
        st.download_button(
            "📥 엑셀 다운로드",
            data=to_excel(df),
            file_name=f"랭킹_{date.today()}.xlsx",
            use_container_width=True
        )

# ══════════════════════════════════════════════════════════════
# 2. 대진 (완벽 통합 실시간 오버레이 스태퍼)
# ══════════════════════════════════════════════════════════════
elif M == "schedule":
    tc = title_cls["schedule"]
    tours = load_tours()
    active = [k for k, v in tours.items() if v.get("status") == "진행중"]
    if not active:
        st.markdown(f"<div class='pg-title {tc}'>📅 대진표</div>", unsafe_allow_html=True)
        st.markdown("<div class='ic'>⚠️ 진행 중인 대회가 없습니다.</div>", unsafe_allow_html=True)
        st.stop()

    tid  = active[-1]
    tour = tours[tid]
    st.markdown(f"<div class='pg-title {tc}'>📅 {tour['title']}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='ic'>📍 {tour.get('date','')} &nbsp;|&nbsp; "
        f"{tour.get('place','')} &nbsp;|&nbsp; 코트 {tour.get('courts',2)}면</div>",
        unsafe_allow_html=True
    )

    gnames = list(tour["groups"].keys())
    if not gnames:
        st.markdown("<div class='ic'>ℹ️ 대진이 없습니다.</div>", unsafe_allow_html=True)
        st.stop()

    tabs = st.tabs([f"{GLBL[i%len(GLBL)]} {g}" for i, g in enumerate(gnames)])
    for ti, g in enumerate(gnames):
        with tabs[ti]:
            gi   = tour["groups"][g]
            ms   = gi["matches"]
            mode = gi["mode"]
            p2n  = gi.get("player_with_number", {})
            fx   = (mode == "고정페어")
            sv   = stats_fixed(ms) if fx else stats_kdk(ms)
            rit  = list(sv.keys())

            st.markdown("<div class='sec'>📋 전적 매트릭스</div>", unsafe_allow_html=True)
            st.markdown(matrix_html(ms, rit, fx, p2n), unsafe_allow_html=True)
            if not fx and p2n:
                st.divider()
                show_kdk(len(p2n), gi.get("games", 3), p2n)
            st.divider()

            st.markdown("<div class='sec'>🏅 현재 순위</div>", unsafe_allow_html=True)
            if rit:
                ranked = sorted(rit, key=lambda x: (-sv[x]["승"], -sv[x]["득실"]))
                rows = []
                for i, item in enumerate(ranked):
                    if fx:
                        rows.append({"순위":i+1, "팀":" & ".join(list(item)),
                                     "승":sv[item]["승"], "패":sv[item]["패"],
                                     "득실":f'{sv[item]["득실"]:+d}'})
                    else:
                        rows.append({"순위":i+1, "선수":item,
                                     "승":sv[item]["승"], "패":sv[item]["패"],
                                     "득실":f'{sv[item]["득실"]:+d}', "비고":grade(i+1)})
                rdf  = pd.DataFrame(rows)
                rcfg = {c: st.column_config.TextColumn(c, width="small") for c in rdf.columns}
                st.dataframe(rdf, use_container_width=True, hide_index=True, column_config=rcfg)
            st.divider()

            # 경기 카드 섹션
            st.markdown("<div class='sec'>🎾 경기 입력</div>", unsafe_allow_html=True)

            for mi, m in enumerate(ms):
                t1s  = " & ".join(m["t1"])
                t2s  = " & ".join(m["t2"])
                mc   = GCLS[mi % len(GCLS)]
                tbc  = TBCLS[mi % len(TBCLS)]
                s1v  = int(m["s1"])
                s2v  = int(m["s2"])

                # 디자인 레이아웃 렌더링
                st.markdown(
                    f'<div class="match-card">'
                    f'<span class="match-no {mc}">MATCH {mi+1}</span>'
                    f'<div class="match-row">'
                    f'<div class="team-side">'
                    f'<div class="team-name {tbc}">{t1s}</div>'
                    f'<div class="score-ctrl">'
                    f'<div class="score-minus">－</div>'
                    f'<div class="score-num">{s1v}</div>'
                    f'<div class="score-plus">＋</div>'
                    f'</div></div>'
                    f'<div class="vs-col"><div class="vs-badge">VS</div></div>'
                    f'<div class="team-side">'
                    f'<div class="team-name {tbc}">{t2s}</div>'
                    f'<div class="score-ctrl">'
                    f'<div class="score-minus">－</div>'
                    f'<div class="score-num">{s2v}</div>'
                    f'<div class="score-plus">＋</div>'
                    f'</div></div>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )

                # 투명 오버레이 버튼 레이어 (정확한 절대 좌표 및 완전 투명화 스타일 적용)
                st.markdown('<div class="stepper-overlay-container">', unsafe_allow_html=True)
                
                # 팀 A 스태퍼
                st.markdown('<div class="stepper-overlay-side">', unsafe_allow_html=True)
                st.markdown('<div class="st-btn-hidden-wrapper">', unsafe_allow_html=True)
                st.button(" ", key=f"d_{tid}_{g}_{mi}_A", on_click=adj_score, args=(tid,g,mi,"A",-1))
                st.markdown('</div><div style="flex:1.4;"></div><div class="st-btn-hidden-wrapper">', unsafe_allow_html=True)
                st.button(" ", key=f"i_{tid}_{g}_{mi}_A", on_click=adj_score, args=(tid,g,mi,"A",1))
                st.markdown('</div></div>', unsafe_allow_html=True)
                
                # 중앙 스페이서
                st.markdown('<div class="stepper-overlay-spacer"></div>', unsafe_allow_html=True)
                
                # 팀 B 스태퍼
                st.markdown('<div class="stepper-overlay-side">', unsafe_allow_html=True)
                st.markdown('<div class="st-btn-hidden-wrapper">', unsafe_allow_html=True)
                st.button(" ", key=f"d_{tid}_{g}_{mi}_B", on_click=adj_score, args=(tid,g,mi,"B",-1))
                st.markdown('</div><div style="flex:1.4;"></div><div class="st-btn-hidden-wrapper">', unsafe_allow_html=True)
                st.button(" ", key=f"i_{tid}_{g}_{mi}_B", on_click=adj_score, args=(tid,g,mi,"B",1))
                st.markdown('</div></div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 3. 결과
# ══════════════════════════════════════════════════════════════
elif M == "result":
    tc = title_cls["result"]
    tours  = load_tours()
    active = [k for k, v in tours.items() if v.get("status") == "진행중"]
    if not active:
        st.markdown(f"<div class='pg-title {tc}'>📊 경기 결과</div>", unsafe_allow_html=True)
        st.markdown("<div class='ic'>⚠️ 진행 중인 대회가 없습니다.</div>", unsafe_allow_html=True)
        st.stop()

    tid  = active[-1]
    tour = tours[tid]
    st.markdown(f"<div class='pg-title {tc}'>📊 {tour['title']}</div>", unsafe_allow_html=True)

    for g, gi in tour["groups"].items():
        mode, ms = gi["mode"], gi["matches"]
        p2n = gi.get("player_with_number", {})
        fx  = (mode == "고정페어")
        sv  = stats_fixed(ms) if fx else stats_kdk(ms)
        ranked = sorted(sv.keys(), key=lambda x: (-sv[x]["승"], -sv[x]["득실"]))

        st.markdown(f'<div class="sec">{g} ({mode})</div>', unsafe_allow_html=True)
        if not fx and p2n:
            show_kdk(len(p2n), gi.get("games", 3), p2n)
            st.divider()

        rows = []
        for i, item in enumerate(ranked):
            pt = rank_pts(i+1, mode)
            if fx:
                rows.append({
                    "순위":i+1, "팀":" & ".join(list(item)),
                    "승":sv[item]["승"], "패":sv[item]["패"],
                    "득실":f'{sv[item]["득실"]:+d}', "포인트":pt,
                    "등급":["🥇 우승","🥈 준우승","🥉 3위"][i] if i<3 else "참가"
                })
            else:
                rows.append({
                    "순위":i+1, "선수":item,
                    "승":sv[item]["승"], "패":sv[item]["패"],
                    "득실":f'{sv[item]["득실"]:+d}', "포인트":pt, "비고":grade(i+1)
                })
        rdf  = pd.DataFrame(rows)
        rcfg = {c: st.column_config.TextColumn(c, width="small") for c in rdf.columns}
        st.dataframe(rdf, use_container_width=True, hide_index=True, column_config=rcfg)

        with st.expander("📋 전체 경기 결과 보기"):
            mr = [{"경기":f"{' & '.join(m['t1'])} vs {' & '.join(m['t2'])}",
                   "결과":f"{m['s1']} : {m['s2']}"} for m in ms]
            st.dataframe(pd.DataFrame(mr), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# 4. 기록
# ══════════════════════════════════════════════════════════════
elif M == "archive":
    tc = title_cls["archive"]
    st.markdown(f"<div class='pg-title {tc}'>📂 지난 대회</div>", unsafe_allow_html=True)
    tours = load_tours()
    past  = {k: v for k, v in tours.items() if v.get("status") != "진행중"}
    if not past:
        st.markdown("<div class='ic'>📭 완료된 대회가 없습니다.</div>", unsafe_allow_html=True)
        st.stop()

    sel  = st.selectbox("대회 선택", list(past.keys()),
                        format_func=lambda k: f"{past[k]['title']} ({past[k].get('date','')})")
    tour = past[sel]
    st.markdown(
        f"<div class='ic'>🏆 <strong>{tour['title']}</strong> &nbsp;|&nbsp; "
        f"{tour.get('date','')} &nbsp;|&nbsp; {tour.get('place','')}</div>",
        unsafe_allow_html=True
    )
    if not tour.get("groups"):
        st.markdown("<div class='ic'>ℹ️ 대진 정보가 없습니다.</div>", unsafe_allow_html=True)
        st.stop()

    for g, gi in tour["groups"].items():
        mode, ms = gi["mode"], gi["matches"]
        p2n = gi.get("player_with_number", {})
        fx  = (mode == "고정페어")
        sv  = stats_fixed(ms) if fx else stats_kdk(ms)
        ranked = sorted(sv.keys(), key=lambda x: (-sv[x]["승"], -sv[x]["득실"]))

        st.markdown(f'<div class="sec">{g} ({mode})</div>', unsafe_allow_html=True)
        if not fx and p2n:
            show_kdk(len(p2n), gi.get("games", 3), p2n)
            st.divider()

        rows = []
        for i, item in enumerate(ranked):
            pt = rank_pts(i+1, mode)
            if fx:
                rows.append({
                    "순위":i+1, "팀":" & ".join(list(item)),
                    "승":sv[item]["승"], "패":sv[item]["패"],
                    "득실":f'{sv[item]["득실"]:+d}', "포인트":pt,
                    "등급":["🥇 우승","🥈 준우승","🥉 3위"][i] if i<3 else "참가"
                })
            else:
                rows.append({
                    "순위":i+1, "선수":item,
                    "승":sv[item]["승"], "패":sv[item]["패"],
                    "득실":f'{sv[item]["득실"]:+d}', "포인트":pt, "비고":grade(i+1)
                })
        adf  = pd.DataFrame(rows)
        acfg = {c: st.column_config.TextColumn(c, width="small") for c in adf.columns}
        st.dataframe(adf, use_container_width=True, hide_index=True, column_config=acfg)

# ══════════════════════════════════════════════════════════════
# 5. 관리자
# ══════════════════════════════════════════════════════════════
elif M == "admin":
    tc = title_cls["admin"]
    st.markdown(f"<div class='pg-title {tc}'>⚙️ 관리자</div>", unsafe_allow_html=True)
    pw = st.text_input("🔒 비밀번호", type="password", placeholder="비밀번호 입력")
    if pw == ADMIN_PW: ss.is_admin = True
    if not ss.is_admin:
        if pw: st.error("❌ 비밀번호 오류")
        st.stop()
    st.markdown("<div class='ic'>✅ 관리자 모드 활성화</div>", unsafe_allow_html=True)

    adm = st.tabs(["🏆 대회", "👥 참가자·대진", "📋 랭킹", "💾 반영"])

    # ── 탭0: 대회 관리 ──
    with adm[0]:
        st.markdown('<div class="sec">새 대회 생성</div>', unsafe_allow_html=True)
        with st.form("f_new"):
            tn = st.text_input("대회명")
            td = st.date_input("날짜", value=date.today())
            tp = st.text_input("장소")
            co = st.selectbox("코트 수", [1,2,3], index=1)
            if st.form_submit_button("✅ 생성", use_container_width=True, type="primary"):
                if tn.strip():
                    ts    = load_tours()
                    tid2  = f"{td}_{tn.strip()}"
                    if tid2 not in ts:
                        ts[tid2] = {"title":tn.strip(), "date":str(td), "place":tp,
                                    "courts":co, "status":"진행중", "groups":{}}
                        save_tours(ts); st.success("생성됨!"); st.rerun()
                    else: st.warning("이미 존재하는 대회입니다.")

        st.divider()
        st.markdown('<div class="sec">대회 목록</div>', unsafe_allow_html=True)
        ts = load_tours()
        for tid2, tv in list(ts.items()):
            st.markdown(
                f"<div class='ic'><strong>{tv['title']}</strong> ({tv.get('date','')})</div>",
                unsafe_allow_html=True
            )
            c1, c2, c3 = st.columns([2,1.5,1.5])
            with c1:
                so  = ["진행중","완료","예정"]
                cur = tv.get("status","진행중")
                ns  = st.selectbox("상태", so,
                                   index=so.index(cur) if cur in so else 0,
                                   key=f"ss_{tid2}", label_visibility="collapsed")
            with c2:
                if st.button("💾 수정", key=f"es_{tid2}", use_container_width=True):
                    ts[tid2]["status"] = ns; save_tours(ts); st.success("수정됨!"); st.rerun()
            with c3:
                if st.button("🗑 삭제", key=f"dl_{tid2}", use_container_width=True):
                    del ts[tid2]; save_tours(ts); st.rerun()

            if st.button("✏️ 상세 수정", key=f"de_{tid2}", use_container_width=True):
                ss.edit_tour_id = tid2; st.rerun()
            st.divider()

        if eid := ss.get("edit_tour_id"):
            if eid in ts:
                et = ts[eid]
                st.markdown(f'<div class="sec">✏️ "{et["title"]}" 수정</div>', unsafe_allow_html=True)
                nt  = st.text_input("대회명", value=et["title"], key="edt")
                try:    dd = pd.to_datetime(et.get("date", str(date.today()))).date()
                except: dd = date.today()
                nd  = st.date_input("날짜", value=dd, key="edd")
                np2 = st.text_input("장소", value=et.get("place",""), key="edp")
                nc  = st.selectbox("코트 수", [1,2,3], index=max(0, et.get("courts",2)-1), key="edc")
                cs1, cs2 = st.columns(2)
                with cs1:
                    if st.button("💾 저장", type="primary", use_container_width=True, key="sbi"):
                        et.update({"title":nt, "date":str(nd), "place":np2, "courts":nc})
                        save_tours(ts); st.success("저장됨!"); ss.edit_tour_id = None; st.rerun()
                with cs2:
                    if st.button("취소", use_container_width=True, key="cce"):
                        ss.edit_tour_id = None; st.rerun()

                st.divider()
                st.markdown('<div class="sec">🎲 그룹 설정</div>', unsafe_allow_html=True)
                st.caption("※ 변경 시 기존 대진 초기화")
                cg   = et.get("groups", {})
                ci1, ci2 = st.columns(2)
                with ci1: gcnt = st.number_input("그룹 수", 1, 6, value=max(1,len(cg)), key="egc")
                with ci2: st.write(f"현재 {len(cg)}개")
                gcfg = {}
                gnms = [f"{chr(65+i)}그룹" for i in range(int(gcnt))]
                for i, gn in enumerate(gnms):
                    ex = cg.get(gn, {})
                    st.markdown(f"**{gn}**")
                    a1,a2,a3,a4 = st.columns(4)
                    with a1:
                        default_sz = len(ex.get("players",[])) if ex else 8
                        sz = st.number_input("인원", 2, 30, value=default_sz, key=f"esz_{eid}_{i}")
                    with a2:
                        default_md = ex.get("mode","고정페어")
                        mdo = ["고정페어","KDK","단식"]
                        md  = st.selectbox("방식", mdo, index=mdo.index(default_md), key=f"emd_{eid}_{i}")
                    with a3:
                        default_gc = ex.get("games",4)
                        gco = [3,4,5]
                        gc  = st.selectbox("게임수", gco, index=gco.index(default_gc), key=f"egc2_{eid}_{i}")
                    with a4:
                        st.write(f"{len(ex.get('players',[]))}명")
                    gcfg[gn] = (sz, md, gc)
                tot = sum(v[0] for v in gcfg.values())
                apl = et.get("players", [])
                if tot == len(apl): st.success(f"✅ 참가자 {len(apl)}명 / 배정 {tot}명")
                else:               st.warning(f"⚠️ 참가자 {len(apl)}명 / 배정 {tot}명 (차이 {len(apl)-tot:+d}명)")

                if st.button("🎲 대진 재생성", type="primary", use_container_width=True, key="agc"):
                    ptr=0; ng={}
                    for gn, (sz,md,gc) in gcfg.items():
                        gp = apl[ptr:ptr+sz]; ptr += sz
                        if md == "고정페어": ms2, pwn = make_fixed(gp)
                        elif md == "KDK":
                            ms2, pwn = make_kdk(gp, gc)
                            if not ms2: ms2, pwn = make_singles(gp)
                        else: ms2, pwn = make_singles(gp)
                        ng[gn] = {"players":gp, "mode":md, "games":gc,
                                  "matches":ms2, "player_with_number":pwn}
                    et["groups"] = ng; save_tours(ts)
                    st.success("대진 재생성 완료!"); st.rerun()

    # ── 탭1: 참가자·대진 ──
    with adm[1]:
        ts   = load_tours()
        act2 = [k for k, v in ts.items() if v.get("status") == "진행중"]
        if not act2:
            st.warning("진행 중인 대회가 없습니다."); st.stop()

        sel_tid = st.selectbox("대회 선택", act2,
                               format_func=lambda k: ts[k]['title'], key="a1st")
        tour = ts[sel_tid]

        st.markdown('<div class="sec">🎲 1. 그룹 구성 설정</div>', unsafe_allow_html=True)
        current_groups = tour.get("groups", {})
        default_gcnt   = len(current_groups) if current_groups else 4
        gcnt           = st.number_input("그룹 수", 1, 6, value=default_gcnt, key="temp_gcnt")
        group_names    = [f"{chr(65+i)}그룹" for i in range(gcnt)]
        temp_gcfg      = {}
        for i, gn in enumerate(group_names):
            existing = current_groups.get(gn, {})
            st.markdown(f"**{gn}**")
            c1,c2,c3,c4 = st.columns(4)
            with c1:
                sz = st.number_input("인원", 2, 30,
                                     value=len(existing.get("players",[])) or 8,
                                     key=f"tmp_sz_{i}")
            with c2:
                md = st.selectbox("방식", ["고정페어","KDK","단식"],
                                  index=["고정페어","KDK","단식"].index(existing.get("mode","고정페어")),
                                  key=f"tmp_md_{i}")
            with c3:
                gc = st.selectbox("게임수", [3,4,5],
                                  index=[3,4,5].index(existing.get("games",4)),
                                  key=f"tmp_gc_{i}")
            with c4:
                st.write(f"현재 {len(existing.get('players',[]))}명")
            temp_gcfg[gn] = (sz, md, gc)

        if st.button("💾 그룹 구성 저장 (임시)", use_container_width=True, key="save_temp_config"):
            ss.temp_group_config = temp_gcfg
            ss.temp_tour_id      = sel_tid
            st.success("그룹 구성 저장됨! 아래에서 참가자를 배정하세요.")
            st.rerun()

        st.divider()
        st.markdown('<div class="sec">👥 2. 참가자 배정</div>', unsafe_allow_html=True)

        if ss.get("temp_group_config") and ss.get("temp_tour_id") == sel_tid:
            gcfg = ss.temp_group_config
        else:
            gcfg = {}
            for gn, gi in current_groups.items():
                gcfg[gn] = (len(gi["players"]), gi["mode"], gi.get("games",4))

        if not gcfg:
            st.info("먼저 '그룹 구성 저장' 버튼을 눌러 그룹을 설정하세요.")
            st.stop()

        all_members = load_members()
        if not all_members:
            st.warning("회원 명단이 없습니다. '랭킹 관리'에서 엑셀을 업로드하세요.")
            st.stop()

        assigned = {}
        for gn in gcfg.keys():
            if gn in current_groups:
                assigned[gn] = current_groups[gn].get("players", []).copy()
            else:
                assigned[gn] = []

        new_assigned = {}
        for gn, (sz, md, gc) in gcfg.items():
            st.markdown(f"#### {gn} (최대 {sz}명)")
            current_in_this = assigned.get(gn, [])
            other_assigned  = set()
            for other_gn, lst in assigned.items():
                if other_gn != gn: other_assigned.update(lst)
            selectable = [m for m in all_members if m not in other_assigned or m in current_in_this]
            selected = st.multiselect(
                f"{gn} 참가자 선택",
                options=selectable,
                default=current_in_this,
                key=f"assign_{gn}"
            )
            if len(selected) > sz:
                st.warning(f"{gn}의 최대 인원은 {sz}명입니다. 현재 {len(selected)}명 선택됨")
            new_assigned[gn] = selected[:sz]

            col_sel, col_des = st.columns(2)
            with col_sel:
                if st.button(f"✅ {gn} 전체선택", key=f"sel_all_{gn}", use_container_width=True):
                    ss[f"temp_sel_{gn}"] = selectable[:sz]; st.rerun()
            with col_des:
                if st.button(f"❌ {gn} 전체해제", key=f"des_all_{gn}", use_container_width=True):
                    ss[f"temp_sel_{gn}"] = []; st.rerun()
            if f"temp_sel_{gn}" in ss:
                new_assigned[gn] = ss[f"temp_sel_{gn}"]
                del ss[f"temp_sel_{gn}"]

        total_assigned = sum(len(lst) for lst in new_assigned.values())
        total_needed   = sum(sz for sz,_,_ in gcfg.values())
        if total_assigned != total_needed:
            st.warning(f"⚠️ 배정 인원: {total_assigned}명 / 필요 인원: {total_needed}명")
        else:
            st.success(f"✅ 배정 완료! 총 {total_assigned}명")

        if st.button("🎲 3. 대진 생성 (배정 완료 후)", type="primary",
                     use_container_width=True, key="generate_final"):
            all_selected = []
            for lst in new_assigned.values(): all_selected.extend(lst)
            if len(set(all_selected)) != len(all_selected):
                st.error("같은 선수가 여러 그룹에 배정되었습니다! 중복을 제거하세요."); st.stop()
            if total_assigned != total_needed:
                st.error(f"인원 수가 맞지 않습니다. (필요 {total_needed}, 배정 {total_assigned})"); st.stop()
            new_groups = {}
            for gn, players in new_assigned.items():
                sz, md, gc = gcfg[gn]
                if len(players) != sz:
                    st.error(f"{gn}의 인원이 {sz}명이 아닙니다. (현재 {len(players)}명)"); st.stop()
                if md == "고정페어":   ms, pwn = make_fixed(players)
                elif md == "KDK":
                    ms, pwn = make_kdk(players, gc)
                    if not ms:
                        st.warning(f"{gn}: {gc}게임 기준 {len(players)}명 미지원 → 단식 리그로 대체")
                        ms, pwn = make_singles(players)
                else: ms, pwn = make_singles(players)
                new_groups[gn] = {"players":players, "mode":md, "games":gc,
                                  "matches":ms, "player_with_number":pwn}
            tour["groups"]  = new_groups
            tour["players"] = all_selected
            save_tours(ts)
            if "temp_group_config" in ss: del ss.temp_group_config
            if "temp_tour_id"      in ss: del ss.temp_tour_id
            st.success("✅ 대진 생성 완료! '대진' 메뉴에서 확인하세요.")
            st.rerun()

        st.divider()
        st.markdown('<div class="sec">✏️ 개별 참가자 수정 (대진 유지)</div>', unsafe_allow_html=True)
        if tour.get("groups"):
            groups = list(tour["groups"].keys())
            if groups:
                sel_g      = st.selectbox("그룹 선택", groups, key="edit_group")
                cur_players = tour["groups"][sel_g]["players"].copy()
                st.markdown(f"**현재 {sel_g} 참가자:** {', '.join(cur_players) if cur_players else '없음'}")

                if cur_players:
                    sel_p = st.selectbox("삭제할 참가자", cur_players, key="del_player")
                    if st.button("🗑 삭제", use_container_width=True, key="del_btn"):
                        tour["groups"][sel_g]["players"].remove(sel_p)
                        tour["groups"][sel_g]["matches"] = [
                            m for m in tour["groups"][sel_g]["matches"]
                            if sel_p not in m["t1"] and sel_p not in m["t2"]
                        ]
                        if sel_p not in [p for g in groups for p in tour["groups"][g]["players"]]:
                            if sel_p in tour.get("players",[]): tour["players"].remove(sel_p)
                        save_tours(ts); st.success(f"'{sel_p}' 삭제됨"); st.rerun()

                st.markdown("---")
                new_name = st.text_input("새 참가자", placeholder="예: 홍길동", key="add_name")
                if st.button("➕ 추가", use_container_width=True, key="add_btn"):
                    if new_name and new_name.strip():
                        new_name = new_name.strip()
                        if new_name not in tour["groups"][sel_g]["players"]:
                            tour["groups"][sel_g]["players"].append(new_name)
                            if new_name not in tour.get("players",[]): tour.setdefault("players",[]).append(new_name)
                            md2 = tour["groups"][sel_g]["mode"]
                            gc2 = tour["groups"][sel_g].get("games",3)
                            if md2 == "고정페어": nm2, _ = make_fixed(tour["groups"][sel_g]["players"])
                            elif md2 == "KDK":
                                nm2, np3 = make_kdk(tour["groups"][sel_g]["players"], gc2)
                                if nm2: tour["groups"][sel_g]["player_with_number"] = np3
                                else: nm2, _ = make_singles(tour["groups"][sel_g]["players"])
                            else: nm2, _ = make_singles(tour["groups"][sel_g]["players"])
                            tour["groups"][sel_g]["matches"] = nm2
                            save_tours(ts); st.success(f"'{new_name}' 추가됨"); st.rerun()
                        else: st.warning("이미 있는 참가자입니다.")

                st.markdown("---")
                all_pairs = [(p, g) for g in groups for p in tour["groups"][g]["players"]]
                if all_pairs:
                    move_p = st.selectbox("이동할 참가자", [p for p,_ in all_pairs], key="move_player")
                    cur_g  = next((g for p,g in all_pairs if p==move_p), groups[0])
                    other_g = [g for g in groups if g != cur_g]
                    if other_g:
                        target_g = st.selectbox("이동할 그룹", other_g, key="target_group")
                        if st.button("🔄 이동", use_container_width=True, key="move_btn"):
                            tour["groups"][cur_g]["players"].remove(move_p)
                            tour["groups"][target_g]["players"].append(move_p)
                            for grp in [cur_g, target_g]:
                                md3 = tour["groups"][grp]["mode"]
                                gc3 = tour["groups"][grp].get("games",3)
                                if md3 == "고정페어": nm3, _ = make_fixed(tour["groups"][grp]["players"])
                                elif md3 == "KDK":
                                    nm3, np4 = make_kdk(tour["groups"][grp]["players"], gc3)
                                    if nm3: tour["groups"][grp]["player_with_number"] = np4
                                    else: nm3, _ = make_singles(tour["groups"][grp]["players"])
                                else: nm3, _ = make_singles(tour["groups"][grp]["players"])
                                tour["groups"][grp]["matches"] = nm3
                            save_tours(ts); st.success(f"'{move_p}' → {target_g} 이동됨"); st.rerun()
        else:
            st.info("아직 그룹이 없습니다. 위에서 대진을 먼저 생성하세요.")

    # ── 탭2: 랭킹 관리 ──
    with adm[2]:
        st.markdown('<div class="sec">📁 엑셀/CSV 업로드</div>', unsafe_allow_html=True)
        up = st.file_uploader("파일 선택", type=["xlsx","csv"],
                              key="adm_rank_up", label_visibility="collapsed")
        if up:
            try:
                du = pd.read_excel(up) if up.name.endswith("xlsx") else pd.read_csv(up, encoding_errors="replace")
                if "현재포인트" in du.columns:
                    du["현재포인트"] = pd.to_numeric(du["현재포인트"], errors="coerce").fillna(0)
                    du = du.sort_values("현재포인트", ascending=False).reset_index(drop=True)
                    du["랭킹"] = du.index + 1
                st.dataframe(du, use_container_width=True)
                if st.button("💾 저장", type="primary", key="a2su"):
                    save_rank(du)
                    if "이름" in du.columns: save_members(du["이름"].tolist())
                    st.success("저장 완료!"); st.rerun()
            except Exception as e:
                st.error(f"오류: {e}")

        st.divider()
        st.markdown('<div class="sec">📊 현재 랭킹</div>', unsafe_allow_html=True)
        dc = load_rank()
        if not dc.empty:
            st.dataframe(dc, use_container_width=True)
            st.download_button("📥 다운로드", data=to_excel(dc),
                               file_name=f"랭킹_{date.today()}.xlsx", key="a2dl")

        st.divider()
        st.markdown('<div class="sec">✏️ 직접 수정</div>', unsafe_allow_html=True)
        de = load_rank()
        if not de.empty:
            edited = st.data_editor(de, use_container_width=True, hide_index=True, num_rows="dynamic")
            if st.button("💾 저장", type="primary", key="a2se"):
                save_rank(edited); save_members(edited["이름"].tolist())
                st.success("저장 완료!"); st.rerun()

    # ── 탭3: 결과 반영 ──
    with adm[3]:
        ts   = load_tours()
        act3 = [k for k, v in ts.items() if v.get("status") == "진행중"]
        if not act3:
            st.warning("진행 중인 대회가 없습니다."); st.stop()

        stid2 = st.selectbox("대회 선택", act3,
                             format_func=lambda k: ts[k]['title'], key="a3st")
        t3 = ts[stid2]
        if not t3.get("groups"):
            st.warning("대진 정보가 없습니다."); st.stop()

        earn = {}
        for g, gi in t3["groups"].items():
            mode2, ms2 = gi["mode"], gi["matches"]
            fx2  = (mode2 == "고정페어")
            sv2  = stats_fixed(ms2) if fx2 else stats_kdk(ms2)
            rk2  = sorted(sv2.keys(), key=lambda x: (-sv2[x]["승"], -sv2[x]["득실"]))
            for i, item in enumerate(rk2):
                pt = rank_pts(i+1, mode2)
                if fx2:
                    for p in list(item): earn[p] = earn.get(p, 0) + pt
                else:
                    earn[item] = earn.get(item, 0) + pt

        if earn:
            ef  = pd.DataFrame(earn.items(), columns=["선수","획득포인트"])
            ec  = {c: st.column_config.TextColumn(c, width="small") for c in ef.columns}
            st.dataframe(ef, use_container_width=True, column_config=ec)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🏆 랭킹 반영", type="primary", use_container_width=True, key="a3ap"):
                dr = load_rank()
                if dr.empty: dr = pd.DataFrame(columns=COLS_RANK)
                for p, pt in earn.items():
                    if p in dr["이름"].values:
                        cur = dr.loc[dr["이름"]==p, "현재포인트"].values[0]
                        dr.loc[dr["이름"]==p, "현재포인트"] = cur + pt
                    else:
                        nr = {c:"" for c in COLS_RANK}; nr["이름"]=p; nr["현재포인트"]=pt
                        dr = pd.concat([dr, pd.DataFrame([nr])], ignore_index=True)
                save_rank(dr)
                ts[stid2]["status"] = "완료"
                save_tours(ts)
                st.success("✅ 랭킹 반영 완료!"); st.rerun()
        with c2:
            if st.button("🗑 점수 초기화", use_container_width=True, key="a3rs"):
                for g in t3["groups"]:
                    for m in t3["groups"][g]["matches"]:
                        m["s1"] = 0; m["s2"] = 0
                save_tours(ts); st.success("✅ 점수 초기화 완료!"); st.rerun()
