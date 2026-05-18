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

/* ── 데이터프레임 무조건 가운데 정렬 (랭킹/순위 전용) ── */
div[data-testid="stDataFrame"]{
  border-radius:var(--r1)!important; overflow:hidden!important;
  box-shadow:var(--sh)!important; border:1px solid var(--bd)!important;
  width:100%!important;
}
div[data-testid="stDataFrame"] .data-table, 
div[data-testid="stDataFrame"] table,
div[data-testid="stDataFrame"] div[role="grid"] div[role="row"] div[role="gridcell"],
div[data-testid="stDataFrame"] div[role="columnheader"] span {
  text-align: center !important;
  justify-content: center !important;
  align-items: center !important;
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
   경기 카드 — 핵심 레이아웃 및 모바일 가로 유지 설정
══════════════════════════════════════════════════════════════ */
.match-card{
  background:var(--card); border-radius:var(--r2); padding:12px 10px 14px;
  margin:12px 0; box-shadow:var(--sh2); border:1px solid var(--bd);
}
.match-no{
  display:inline-block; border-radius:20px; padding:3px 14px;
  font-size:.6rem; font-weight:900; margin-bottom:10px; color:#fff;
}
/* 카드 색상 배리에이션 */
.mc0{background:var(--mc0);} .mc1{background:var(--mc1);} .mc2{background:var(--mc2);}
.mc3{background:var(--mc3);} .mc4{background:var(--mc4);} .mc5{background:var(--mc5);}
.mc6{background:var(--mc6);} .mc7{background:var(--mc7);}

/* 경기 메인 행: [팀A] [VS] [팀B] */
.match-row{
  display:flex; align-items:stretch; gap:6px; width:100%;
}
/* 팀 사이드 (이름 + 점수컨트롤) */
.team-side{
  flex:1; display:flex; flex-direction:column; gap:6px;
}
/* 팀 이름 박스 */
.team-name{
  border-radius:var(--r1); padding:8px 4px; font-weight:900; font-size:.82rem;
  text-align:center; color:#fff; box-shadow:var(--sh); min-height:46px;
  display:flex; align-items:center; justify-content:center; word-break:keep-all; line-height:1.2;
}
.tb0{background:var(--tb0);} .tb1{background:var(--tb1);} .tb2{background:var(--tb2);}
.tb3{background:var(--tb3);} .tb4{background:var(--tb4);} .tb5{background:var(--tb5);}
.tb6{background:var(--tb6);} .tb7{background:var(--tb7);}

/* 📱 모바일에서 점수입력 [-][점수][+] 컬럼 가로 한 줄 강제 고정 */
.score-btn-wrap div[data-testid="stHorizontalBlock"] {
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 4px !important;
}
.score-btn-wrap div[data-testid="stHorizontalBlock"] > div {
  width: auto !important;
  min-width: 0 !important;
  flex: 1 !important;
}
/* 숫자 표시칸은 조금 더 여유있게 비율 조정 */
.score-btn-wrap div[data-testid="stHorizontalBlock"] > div:nth-child(2) {
  flex: 1.2 !important;
}

/* 점수 증감 버튼 커스텀 스타일 */
div.score-btn-wrap button {
  min-height: 40px !important;
  height: 40px !important;
  font-size: 1.1rem !important;
  font-weight: 900 !important;
  background: #E8F5E9 !important;
  border: 2px solid #C8E6C9 !important;
  color: #1B5E20 !important;
  border-radius: 10px !important;
  padding: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}
div.score-btn-wrap button:active {
  background: #A5D6A7 !important;
}

.score-num-display {
  display: flex; align-items: center; justify-content: center;
  background: #fff; border: 2.5px solid #C8E6C9; border-radius: 10px;
  font-size: 1.3rem; font-weight: 900; color: #1B5E20; height: 40px;
}

/* VS 구분자 */
.vs-col{
  width:36px; display:flex; align-items:center; justify-content:center; flex-shrink:0;
}
.vs-badge{
  width:34px; height:34px; border-radius:50%;
  background:linear-gradient(135deg,#FFB74D,var(--ora));
  display:flex; align-items:center; justify-content:center;
  font-weight:900; font-size:.65rem; color:#fff; box-shadow:var(--sh);
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
        
        # 전원 가운데 정렬을 위한 설정 적용
        cfg = {c: st.column_config.TextColumn(c, width="small") for c in d.columns}
        st.dataframe(d, use_container_width=True, hide_index=True, column_config=cfg)
        st.download_button(
            "📥 엑셀 다운로드",
            data=to_excel(df),
            file_name=f"랭킹_{date.today()}.xlsx",
            use_container_width=True
        )

# ══════════════════════════════════════════════════════════════
# 2. 대진/경기 입력
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
            gi = tour["groups"][g]
            ms = gi["matches"]
            mode = gi["mode"]
            p2n = gi.get("player_with_number", {})
            fx = (mode == "고정페어")
            sv = stats_fixed(ms) if fx else stats_kdk(ms)
            rit = list(sv.keys())

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
                        rows.append({"순위":i+1, "팀":" & ".join(list(item)), "승":sv[item]["승"], "패":sv[item]["패"], "득실":f'{sv[item]["득실"]:+d}'})
                    else:
                        rows.append({"순위":i+1, "선수":item, "승":sv[item]["승"], "패":sv[item]["패"], "득실":f'{sv[item]["득실"]:+d}', "비고":grade(i+1)})
                rdf = pd.DataFrame(rows)
                rcfg = {c: st.column_config.TextColumn(c, width="small") for c in rdf.columns}
                st.dataframe(rdf, use_container_width=True, hide_index=True, column_config=rcfg)
            st.divider()

            st.markdown("<div class='sec'>🎾 경기 입력</div>", unsafe_allow_html=True)
            for mi, m in enumerate(ms):
                t1s = " & ".join(m["t1"])
                t2s = " & ".join(m["t2"])
                mc = GCLS[mi % len(GCLS)]
                tbc = TBCLS[mi % len(TBCLS)]
                s1v = int(m["s1"])
                s2v = int(m["s2"])

                st.markdown(f'<div class="match-card"><span class="match-no {mc}">MATCH {mi+1}</span>', unsafe_allow_html=True)
                
                m_col1, m_vs, m_col2 = st.columns([10, 3, 10])
                
                with m_col1:
                    st.markdown(f'<div class="team-side"><div class="team-name {tbc}">{t1s}</div></div>', unsafe_allow_html=True)
                    st.markdown('<div class="score-btn-wrap">', unsafe_allow_html=True)
                    ctrl_cols = st.columns([1, 1.2, 1])
                    if ctrl_cols[0].button("－", key=f"btn_m_A_{g}_{mi}"):
                        adj_score(tid, g, mi, "A", -1)
                        st.rerun()
                    ctrl_cols[1].markdown(f'<div class="score-num-display">{s1v}</div>', unsafe_allow_html=True)
                    if ctrl_cols[2].button("＋", key=f"btn_p_A_{g}_{mi}"):
                        adj_score(tid, g, mi, "A", 1)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

                with m_vs:
                    st.markdown('<div style="height:25px;"></div>', unsafe_allow_html=True)
                    st.markdown('<div class="vs-col" style="width:100%;"><div class="vs-badge">VS</div></div>', unsafe_allow_html=True)

                with m_col2:
                    st.markdown(f'<div class="team-side"><div class="team-name {tbc}">{t2s}</div></div>', unsafe_allow_html=True)
                    st.markdown('<div class="score-btn-wrap">', unsafe_allow_html=True)
                    ctrl_cols = st.columns([1, 1.2, 1])
                    if ctrl_cols[0].button("－", key=f"btn_m_B_{g}_{mi}"):
                        adj_score(tid, g, mi, "B", -1)
                        st.rerun()
                    ctrl_cols[1].markdown(f'<div class="score-num-display">{s2v}</div>', unsafe_allow_html=True)
                    if ctrl_cols[2].button("＋", key=f"btn_p_B_{g}_{mi}"):
                        adj_score(tid, g, mi, "B", 1)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 3. 결과 마감
# ══════════════════════════════════════════════════════════════
elif M == "result":
    tc = title_cls["result"]
    tours = load_tours()
    active = [k for k, v in tours.items() if v.get("status") == "진행중"]
    if not active:
        st.markdown(f"<div class='pg-title {tc}'>📊 대회 마감</div>", unsafe_allow_html=True)
        st.markdown("<div class='ic'>⚠️ 진행 중인 대회가 없습니다.</div>", unsafe_allow_html=True)
        st.stop()

    stid2 = active[-1]
    t2    = tours[stid2]
    st.markdown(f"<div class='pg-title {tc}'>📊 {t2['title']} 마감</div>", unsafe_allow_html=True)

    earn = {}
    for gn, gi in t2["groups"].items():
        ms = gi["matches"]
        md = gi["mode"]
        fx = (md == "고정페어")
        sv = stats_fixed(ms) if fx else stats_kdk(ms)
        rit = list(sv.keys())
        if not rit: continue

        ranked = sorted(rit, key=lambda x: (-sv[x]["승"], -sv[x]["득실"]))
        st.markdown(f"<div class='sec'> Grp. {gn} 최종 획득 포인트</div>", unsafe_allow_html=True)

        for i, item in enumerate(ranked):
            pt = rank_pts(i+1, md)
            if fx:
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
            tours[stid2]["status"] = "완료"
            save_tours(tours)
            st.success("✅ 랭킹 반영 완료!")
            st.rerun()

# ══════════════════════════════════════════════════════════════
# 4. 기록 아카이브
# ══════════════════════════════════════════════════════════════
elif M == "archive":
    tc = title_cls["archive"]
    st.markdown(f"<div class='pg-title {tc}'>📂 대회 기록실</div>", unsafe_allow_html=True)
    ts = load_tours()
    done = {k: v for k, v in ts.items() if v.get("status") == "완료"}
    if not done:
        st.markdown("<div class='ic'>📭 완료된 대회 기록이 없습니다.</div>", unsafe_allow_html=True)
    else:
        sel = st.selectbox("🏆 대회 선택", list(done.keys()), format_func=lambda x: done[x]["title"])
        if sel:
            t = done[sel]
            st.markdown(f"<div class='ic'>📅 일시: {t.get('date','')} | 장소: {t.get('place','')}</div>", unsafe_allow_html=True)
            for gn, gi in t["groups"].items():
                st.markdown(f"<div class='sec'>🔷 그룹: {gn} ({gi['mode']})</div>", unsafe_allow_html=True)
                ms = gi["matches"]
                fx = (gi["mode"] == "고정페어")
                p2n = gi.get("player_with_number", {})
                sv = stats_fixed(ms) if fx else stats_kdk(ms)
                rit = list(sv.keys())
                st.markdown(matrix_html(ms, rit, fx, p2n), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 5. 관리자 페이지
# ══════════════════════════════════════════════════════════════
elif M == "admin":
    tc = title_cls["admin"]
    st.markdown(f"<div class='pg-title {tc}'>⚙️ 관리자 설정</div>", unsafe_allow_html=True)

    pw = st.text_input("🔑 관리자 비밀번호", type="password")
    if pw != ADMIN_PW:
        if pw: st.error("❌ 비밀번호가 올바르지 않습니다.")
        st.stop()

    st.success("🔓 관리자 인증 성공")
    t1, t2, t3 = st.tabs(["🏆 랭킹/회원 관리", "📅 새 대회 생성", "💥 데이터 초기화"])

    with t1:
        st.markdown("<div class='sec'>📥 랭킹 마스터 업로드 (.csv)</div>", unsafe_allow_html=True)
        f = st.file_uploader("파일 선택", type=["csv"], key="csv_up")
        if f:
            try:
                tdf = pd.read_csv(f)
                save_rank(tdf)
                st.success("✅ 랭킹 마스터가 성공적으로 업데이트되었습니다!")
            except Exception as e:
                st.error(f"오류 발생: {e}")

        st.divider()
        st.markdown("<div class='sec'>👥 회원 명단 직접 편집</div>", unsafe_allow_html=True)
        m_list = load_members()
        txt = st.text_area("회원 이름들을 쉼표(,)로 구분하여 입력", value=",".join(m_list), height=150)
        if st.button("👥 명단 저장", type="primary", use_container_width=True):
            nl = [x.strip() for x in txt.split(",") if x.strip()]
            save_members(nl)
            st.success(f"✅ 총 {len(nl)}명의 명단이 저장되었습니다.")

    with t2:
        st.markdown("<div class='sec'>📅 새로운 대회 개최</div>", unsafe_allow_html=True)
        title = st.text_input("대회명", f"{date.today().month}월 두류 테니스 대회")
        dt    = st.date_input("대회 일자", date.today())
        loc   = st.text_input("장소", "두류 테니스장")
        ct    = st.number_input("사용 코트 수", 1, 10, 2)

        st.divider()
        st.markdown("<div class='sec'>👥 참가자 선택</div>", unsafe_allow_html=True)
        all_m = load_members()
        if not all_m:
            st.warning("⚠️ 등록된 회원이 없습니다. 명단을 먼저 작성해주세요.")
        else:
            sel_m = []
            cols = st.columns(3)
            for idx, name in enumerate(all_m):
                with cols[idx % 3]:
                    if st.checkbox(name, key=f"p_{name}"):
                        sel_m.append(name)

            st.write(f"선택된 참가자: {len(sel_m)}명")

            st.divider()
            st.markdown("<div class='sec'>🌿 그룹 및 대진 방식 설정</div>", unsafe_allow_html=True)
            g_cnt = st.number_input("분할할 그룹 수", 1, 4, 1)

            groups_config = {}
            for gi in range(int(g_cnt)):
                gn = chr(65 + gi)
                st.markdown(f"**🟢 그룹 {gn} 설정**")
                g_p = st.multiselect(f"그룹 {gn} 참가자 선택", sel_m, key=f"g_p_{gn}")
                g_m = st.selectbox(f"그룹 {gn} 방식", ["KDK (1인 3게임)", "KDK (1인 4게임)", "고정페어", "단식 풀리그"], key=f"g_m_{gn}")

                groups_config[gn] = {"players": g_p, "mode": g_m}

            if st.button("🚀 대회 시작 & 대진표 생성", type="primary", use_container_width=True):
                if not groups_config:
                    st.error("그룹 설정이 잘못되었습니다.")
                else:
                    tours = load_tours()
                    tid = f"tour_{int(random.random()*100000)}"

                    g_data = {}
                    for gn, conf in groups_config.items():
                        pl = conf["players"]
                        m  = conf["mode"]
                        if not pl: continue

                        if "KDK" in m:
                            gp = 3 if "3게임" in m else 4
                            ms, p2n = make_kdk(pl, gp)
                            if ms is None:
                                st.error(f"❌ 그룹 {gn}: 인원수({len(pl)}명)에 맞는 KDK 대진을 지원하지 않습니다.")
                                st.stop()
                            g_data[gn] = {"matches": ms, "mode": "KDK", "games": gp, "player_with_number": p2n}
                        elif m == "고정페어":
                            ms, p2n = make_fixed(pl)
                            g_data[gn] = {"matches": ms, "mode": "고정페어", "player_with_number": p2n}
                        else:
                            ms, p2n = make_singles(pl)
                            g_data[gn] = {"matches": ms, "mode": "단식", "player_with_number": p2n}

                    tours[tid] = {
                        "title": title,
                        "date": str(dt),
                        "place": loc,
                        "courts": ct,
                        "status": "진행중",
                        "groups": g_data
                    }
                    save_tours(tours)
                    st.success("🎉 대회가 성공적으로 개설되었습니다! '대진' 메뉴로 이동하세요.")
                    st.rerun()

    with t3:
        st.markdown("<div class='sec'>💥 데이터 초기화</div>", unsafe_allow_html=True)
        st.warning("⚠️ 초기화된 데이터는 복구할 수 없습니다.")
        if st.button("🚨 모든 대회 및 파일 초기화", use_container_width=True):
            for f in [RANK_FILE, MEMBER_FILE, TOUR_FILE]:
                if os.path.exists(f): os.remove(f)
            st.success("💥 시스템 초기화가 완료되었습니다.")
            st.rerun()
