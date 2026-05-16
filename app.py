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
# CSS (색상 확장)
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

/* ── 변수 ── */
:root {
  --g0:#1B5E20; --g1:#2E7D32; --g2:#388E3C;
  --g3:#66BB6A; --g4:#C8E6C9; --g5:#E8F5E9;
  --yel:#FFD600; --ora:#FB8C00;
  --bg:#F0F7F0; --card:#fff; --bd:#DCEDC8;
  --tx:#1A1A1A; --tx2:#555;
  --r1:10px; --r2:16px; --r3:24px;
  --sh:0 2px 10px rgba(0,0,0,.08);
  --sh2:0 4px 20px rgba(0,0,0,.13);

  /* 10가지 경기 색 */
  --mc0:#2E7D32; --mc1:#1565C0; --mc2:#E65100; --mc3:#6A1B9A; --mc4:#00695C;
  --mc5:#AD1457; --mc6:#004D40; --mc7:#BF360C; --mc8:#1A237E; --mc9:#4A148C;
}

/* ── 글로벌 ── */
*,*::before,*::after{
  font-family:'Noto Sans KR',sans-serif!important;
  box-sizing:border-box;
}

.block-container{
  padding:0 0.9rem 5rem!important;
  max-width:540px!important;
  margin:0 auto!important;
  background:var(--bg)!important;
}
.stApp{background:var(--bg)!important;}

/* 헤더 */
.hdr{
  background:linear-gradient(135deg,var(--g0) 0%,var(--g2) 70%,#43A047 100%);
  margin:0 -0.9rem 0;
  padding:16px 22px 0;
  position:relative;overflow:hidden;
  box-shadow:var(--sh2);
}
.hdr::after{
  content:'🎾';position:absolute;right:16px;top:10px;
  font-size:2.8rem;opacity:.12;pointer-events:none;
}
.hdr-title{color:#fff;font-size:1.1rem;font-weight:900;margin:0 0 2px;}
.hdr-sub{color:rgba(255,255,255,.5);font-size:.6rem;letter-spacing:2px;
         text-transform:uppercase;margin-bottom:10px;}

/* 네비게이션 */
.nav-bar{
  background:linear-gradient(135deg,var(--g0),var(--g2));
  height:4px;margin:0 -0.9rem 14px;
}
section.main [data-testid="stHorizontalBlock"]:first-of-type .stButton>button{
  background:transparent!important;
  color:rgba(255,255,255,.7)!important;
  border:none!important;border-radius:0!important;
  font-size:.7rem!important;font-weight:700!important;
  padding:10px 2px!important;line-height:1.4!important;
  white-space:pre-line!important;box-shadow:none!important;
  min-height:54px!important;border-bottom:3px solid transparent!important;
}
section.main [data-testid="stHorizontalBlock"]:first-of-type .stButton>button:hover{
  color:#fff!important;background:rgba(255,255,255,.08)!important;
}
section.main [data-testid="stHorizontalBlock"]:first-of-type .stButton>button[kind="primary"]{
  color:#fff!important;
  border-bottom:3px solid var(--yel)!important;
  background:rgba(255,255,255,.1)!important;
}

/* 페이지 타이틀 */
.pg-title{
  background:linear-gradient(135deg,var(--g0),var(--g2));
  color:#fff;padding:13px 18px;border-radius:var(--r2);
  margin:0 0 14px;font-size:1.05rem;font-weight:900;
  text-align:center;box-shadow:var(--sh2);
}

/* 섹션 라벨 */
.sec{
  font-size:.88rem;font-weight:800;color:var(--g0);
  border-left:4px solid var(--g3);padding-left:9px;
  margin:18px 0 8px;
}

/* 정보 카드 */
.ic{
  background:var(--card);border-left:4px solid var(--g3);
  border-radius:var(--r1);padding:11px 14px;margin:7px 0;
  box-shadow:var(--sh);font-size:.82rem;color:var(--tx2);line-height:1.55;
}

/* 데이터프레임 가운데 정렬 */
div[data-testid="stDataFrame"]{
  border-radius:var(--r1)!important;
  overflow:hidden!important;
  box-shadow:var(--sh)!important;
  border:1px solid var(--bd)!important;
  width:100%!important;
}
div[data-testid="stDataFrame"] table{
  width:100%!important;
  font-size:.76rem!important;
  border-collapse:collapse!important;
  table-layout:fixed!important;
}
div[data-testid="stDataFrame"] table th,
div[data-testid="stDataFrame"] table td{
  text-align:center!important;
  vertical-align:middle!important;
  padding:9px 4px!important;
  white-space:nowrap;
}
div[data-testid="stDataFrame"] thead tr th{
  background:var(--g0)!important;
  color:#fff!important;
  font-weight:700!important;
  font-size:.72rem!important;
}

/* 경기 카드 */
.match-card{
  background:var(--card);
  border-radius:var(--r3);
  padding:14px 12px 18px;
  margin:14px 0;
  box-shadow:var(--sh2);
  border:1px solid var(--bd);
}
.match-no{
  display:inline-block;
  border-radius:20px;
  padding:4px 16px;
  font-size:.65rem;font-weight:900;letter-spacing:1px;
  margin-bottom:12px;color:#fff;
}
/* 10가지 색 */
.mc0{background:var(--mc0);} .mc1{background:var(--mc1);} .mc2{background:var(--mc2);}
.mc3{background:var(--mc3);} .mc4{background:var(--mc4);} .mc5{background:var(--mc5);}
.mc6{background:var(--mc6);} .mc7{background:var(--mc7);} .mc8{background:var(--mc8);}
.mc9{background:var(--mc9);}

.team-box{
  border-radius:var(--r2);
  padding:12px 8px;
  font-weight:900;font-size:.95rem;
  text-align:center;
  min-height:58px;
  display:flex;align-items:center;justify-content:center;
  word-break:keep-all;line-height:1.35;
  color:#fff;
  margin-bottom:10px;
  box-shadow:var(--sh);
}
.tb0{background:var(--mc0);} .tb1{background:var(--mc1);} .tb2{background:var(--mc2);}
.tb3{background:var(--mc3);} .tb4{background:var(--mc4);} .tb5{background:var(--mc5);}
.tb6{background:var(--mc6);} .tb7{background:var(--mc7);} .tb8{background:var(--mc8);}
.tb9{background:var(--mc9);}

/* 점수 컨트롤 (버튼 + 숫자 inline) */
.score-inline{
  display:flex;
  align-items:center;
  justify-content:center;
  gap:4px;
  margin-top:5px;
}
.score-num{
  font-size:2rem;
  font-weight:900;
  text-align:center;
  min-width:70px;
}

/* VS 원 */
.vs{
  width:46px;height:46px;
  background:linear-gradient(135deg,#FFB74D,var(--ora));
  border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-weight:900;font-size:.78rem;color:#fff;
  margin:0 auto;box-shadow:var(--sh);
}

/* 일반 버튼 */
.stButton>button{
  border-radius:var(--r2)!important;
  font-weight:700!important;font-size:.85rem!important;
  min-height:52px!important;padding:10px 14px!important;
  transition:all .15s!important;
}
.stButton>button[kind="primary"]{
  background:linear-gradient(135deg,var(--g0),var(--g2))!important;
  color:#fff!important;border:none!important;
  box-shadow:0 4px 14px rgba(46,125,50,.35)!important;
}
.stButton>button[kind="secondary"]{
  background:var(--card)!important;color:var(--g0)!important;
  border:2px solid var(--g4)!important;
}

/* 기타 */
.kdk{
  background:var(--card);border-radius:var(--r1);
  padding:12px 14px;margin:8px 0;box-shadow:var(--sh);
  overflow-x:auto;border:1px solid var(--bd);
}
.kdk table{border-collapse:collapse;white-space:nowrap;}
.kdk th,.kdk td{padding:8px 10px;font-size:.72rem;border:1px solid var(--bd);text-align:center;}
.kdk thead th{background:var(--g0);color:#fff;font-weight:700;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 상수 (확장된 색상 리스트)
# ══════════════════════════════════════════════════════════════
RANK_FILE   = "ranking_master.csv"
MEMBER_FILE = "member_roster.json"
TOUR_FILE   = "tournaments.json"
ADMIN_PW    = "0502"
COLS_RANK   = ["랭킹","이름","현재포인트","3월 포인트","결과","부과점","그룹","비고"]

GCLS = ["mc0","mc1","mc2","mc3","mc4","mc5","mc6","mc7","mc8","mc9"]
TBCLS = ["tb0","tb1","tb2","tb3","tb4","tb5","tb6","tb7","tb8","tb9"]
GLBL = ["🟢","🔵","🟠","🟣","🩵","🔴","🟤","⚫","🟡","🟢"]

KDK_3G = {4:[(1,4,2,3),(1,3,2,4),(1,2,3,4)],8:[(1,2,3,4),(5,6,7,8),(1,8,2,7),(3,6,4,5),(1,4,5,8),(2,3,6,7)],12:[(1,2,3,4),(5,6,7,8),(9,10,11,12),(1,3,5,7),(2,4,6,8),(9,11,1,5),(4,8,9,12),(6,7,10,11),(10,12,2,3)]}
KDK_4G = {5:[(1,2,3,4),(1,3,2,5),(1,4,3,5),(1,5,2,4),(2,3,4,5)],6:[(1,3,2,4),(1,5,4,6),(2,3,5,6),(1,4,3,5),(2,6,3,4),(1,6,2,5)],7:[(1,2,3,4),(5,6,1,7),(2,3,5,7),(1,4,6,7),(3,5,2,4),(1,6,2,5),(4,6,3,7)],8:[(1,2,3,4),(5,6,7,8),(1,3,5,7),(2,4,6,8),(1,5,2,6),(3,7,4,8),(1,6,3,8),(2,5,4,7)],9:[(1,2,3,4),(5,6,7,8),(1,9,5,7),(2,3,6,8),(4,9,3,8),(1,5,2,6),(3,6,4,5),(1,7,8,9),(2,4,7,9)],10:[(1,2,3,5),(6,7,8,10),(2,3,4,6),(7,8,1,9),(3,4,5,7),(8,9,2,10),(4,5,6,8),(1,3,9,10),(5,6,7,9),(1,10,2,4)],11:[(1,2,3,5),(6,7,8,10),(4,9,1,11),(2,3,6,8),(4,5,7,10),(9,11,2,6),(1,3,7,11),(4,8,5,9),(1,10,2,8),(4,7,6,11),(3,9,5,10)]}

# ══════════════════════════════════════════════════════════════
# 데이터 헬퍼 (동일)
# ══════════════════════════════════════════════════════════════
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
        with open(MEMBER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    df = load_rank()
    return df["이름"].tolist() if not df.empty else []

def save_members(names):
    with open(MEMBER_FILE, "w", encoding="utf-8") as f:
        json.dump(names, f, ensure_ascii=False, indent=2)

def load_tours():
    if os.path.exists(TOUR_FILE):
        with open(TOUR_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_tours(d):
    with open(TOUR_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def to_excel(df):
    buf = BytesIO(); df.to_excel(buf, index=False); return buf.getvalue()

def stats_fixed(matches):
    s = {}
    for m in matches:
        t1,t2 = tuple(m["t1"]),tuple(m["t2"])
        for t in (t1,t2):
            if t not in s: s[t]={"승":0,"패":0,"득실":0}
        a,b = int(m["s1"]),int(m["s2"])
        if a>b:   s[t1]["승"]+=1;s[t2]["패"]+=1
        elif b>a: s[t2]["승"]+=1;s[t1]["패"]+=1
        s[t1]["득실"]+=a-b; s[t2]["득실"]+=b-a
    return s

def stats_kdk(matches):
    s = {}
    for m in matches:
        p1,p2 = m["t1"],m["t2"]
        for p in p1+p2:
            if p not in s: s[p]={"승":0,"패":0,"득실":0}
        a,b = int(m["s1"]),int(m["s2"])
        if a>b:
            for p in p1: s[p]["승"]+=1
            for p in p2: s[p]["패"]+=1
        elif b>a:
            for p in p2: s[p]["승"]+=1
            for p in p1: s[p]["패"]+=1
        for p in p1: s[p]["득실"]+=a-b
        for p in p2: s[p]["득실"]+=b-a
    return s

def rank_pts(rank, mode):
    if mode=="고정페어": return {1:7,2:5,3:3}.get(rank,1)
    if rank<=2: return 7
    if rank<=4: return 5
    if rank<=6: return 3
    return 1

def grade(rank):
    if rank<=2: return "🥇 우승"
    if rank<=4: return "🥈 준우승"
    if rank<=6: return "🥉 3위"
    return "참가"

def make_kdk(players, gperson):
    n = len(players)
    bp = KDK_3G.get(n) if gperson==3 else KDK_4G.get(n)
    if not bp: return None, {}
    sh = random.sample(players, n)
    p2n = {sh[i]:i+1 for i in range(n)}
    n2p = {i+1:sh[i] for i in range(n)}
    ms  = [{"t1":[n2p[a],n2p[b]],"t2":[n2p[c],n2p[d]],"s1":0,"s2":0} for a,b,c,d in bp]
    return ms, p2n

def make_fixed(players):
    n = len(players)
    pairs = [(players[i],players[n-1-i]) for i in range(n//2)]
    ms = [{"t1":list(pairs[i]),"t2":list(pairs[j]),"s1":0,"s2":0}
          for i in range(len(pairs)) for j in range(i+1,len(pairs))]
    random.shuffle(ms); return ms, {}

def make_singles(players):
    pl = players[:]
    random.shuffle(pl)
    ms = [{"t1":[pl[i]],"t2":[pl[j]],"s1":0,"s2":0}
          for i in range(len(pl)) for j in range(i+1,len(pl))]
    random.shuffle(ms); return ms, {}

def kdk_html(n, gperson, p2n):
    bp  = KDK_3G.get(n) if gperson==3 else KDK_4G.get(n)
    if not bp: return ""
    n2p = {v:k for k,v in p2n.items()}
    title = f"KDK 1인 {gperson}게임 — {n}명"
    rows  = ""
    for i,(a,b,c,d) in enumerate(bp):
        t1 = f"{n2p.get(a,a)}({a}) &amp; {n2p.get(b,b)}({b})"
        t2 = f"{n2p.get(c,c)}({c}) &amp; {n2p.get(d,d)}({d})"
        rows += f"<tr><td><span style='background:#1B5E20;color:#fff;border-radius:20px;padding:2px 9px;font-size:.62rem;font-weight:700'>{i+1}</span></td><td style='text-align:left;padding-left:10px;white-space:nowrap'>{t1} vs {t2}</td></tr>"
    return (f'<div class="kdk"><div class="kdk-title">📋 {title}</div>'
            f'<table><thead><tr><th style="width:38px">순서</th><th>대진</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')

def show_kdk(n, gperson, p2n):
    st.markdown(kdk_html(n, gperson, p2n), unsafe_allow_html=True)

def matrix_html(matches, rank_items, is_fixed, p2n):
    if not matches or not rank_items: return ""
    if is_fixed:
        lab = {t:" & ".join(list(t)) for t in rank_items}
    else:
        lab = {p:f"{p}({p2n.get(p,'?')})" for p in rank_items}
    mat = {lab[t]:{lab[o]:("■" if t==o else "—") for o in lab} for t in lab}
    for m in matches:
        a,b = int(m["s1"]),int(m["s2"])
        if a>0 or b>0:
            if is_fixed:
                k1,k2 = tuple(m["t1"]),tuple(m["t2"])
                mat[lab[k1]][lab[k2]] = f"{a}:{b}"
                mat[lab[k2]][lab[k1]] = f"{b}:{a}"
            else:
                for x in m["t1"]:
                    for y in m["t2"]:
                        mat[lab[x]][lab[y]] = f"{a}:{b}"
                        mat[lab[y]][lab[x]] = f"{b}:{a}"
    keys   = list(lab.values())
    header = "".join(f"<th style='white-space:nowrap'>{k}</th>" for k in keys)
    body   = ""
    for rk in keys:
        body += f"<tr><th style='white-space:nowrap'>{rk}</th>"
        for ck in keys:
            v = mat[rk][ck]
            if v=="■":   body += '<td class="mx-grey">■</td>'
            elif v=="—": body += '<td class="mx-dash">—</td>'
            else:        body += f'<td class="mx-sc">{v}</td>'
        body += "</tr>"
    return (f'<div class="mx-wrap">'
            f'<table class="mx"><thead><tr><th></th>{header}</tr></thead>'
            f'<tbody>{body}</tbody></table></div>')

def adj_score(tid, grp, mi, side, delta):
    tours = load_tours()
    m = tours[tid]["groups"][grp]["matches"][mi]
    key = "s1" if side=="A" else "s2"
    nv  = max(0, int(m[key]) + delta)
    m[key] = nv
    save_tours(tours)

# ══════════════════════════════════════════════════════════════
# 세션
# ══════════════════════════════════════════════════════════════
ss = st.session_state
if "is_admin" not in ss: ss.is_admin = False
if "menu" not in ss: ss.menu = "ranking"
if "participants" not in ss: ss.participants = []

# ══════════════════════════════════════════════════════════════
# 헤더 + 네비
# ══════════════════════════════════════════════════════════════
MENUS = [
    ("ranking",  "🏆\n랭킹"),
    ("schedule", "📅\n대진"),
    ("result",   "📊\n결과"),
    ("archive",  "📂\n기록"),
    ("admin",    "⚙️\n관리"),
]
st.markdown(
    '<div class="hdr">'
    '<div class="hdr-title">🎾 두류 테니스 클럽</div>'
    '<div class="hdr-sub">Duryu Tennis Club</div>'
    '</div>',
    unsafe_allow_html=True
)
nav_cols = st.columns(len(MENUS))
for col,(key,label) in zip(nav_cols, MENUS):
    with col:
        t = "primary" if ss.menu==key else "secondary"
        if st.button(label, key=f"nav_{key}", use_container_width=True, type=t):
            ss.menu = key; st.rerun()
st.markdown('<div class="nav-bar"></div>', unsafe_allow_html=True)
M = ss.menu

# ══════════════════════════════════════════════════════════════
# 1. 랭킹
# ══════════════════════════════════════════════════════════════
if M == "ranking":
    st.markdown("<div class='pg-title'>🏆 두류 랭킹</div>", unsafe_allow_html=True)
    with st.expander("📤 엑셀/CSV 바로 업로드"):
        up = st.file_uploader("파일 선택 (xlsx / csv)", type=["xlsx","csv"], key="rank_up_main")
        if up:
            try:
                du = (pd.read_excel(up) if up.name.endswith("xlsx")
                      else pd.read_csv(up, encoding_errors="replace"))
                if "현재포인트" in du.columns:
                    du["현재포인트"] = pd.to_numeric(du["현재포인트"], errors="coerce").fillna(0)
                    du = du.sort_values("현재포인트", ascending=False).reset_index(drop=True)
                    du["랭킹"] = du.index + 1
                st.dataframe(du, use_container_width=True)
                if st.button("💾 랭킹 저장", type="primary", use_container_width=True, key="rank_save_main"):
                    save_rank(du)
                    if "이름" in du.columns: save_members(du["이름"].tolist())
                    st.success("✅ 랭킹 저장 완료!"); st.rerun()
            except Exception as e:
                st.error(f"오류: {e}")
    df = load_rank()
    if df.empty:
        st.markdown("<div class='ic'>📭 등록된 랭킹이 없습니다.<br>위 업로드 버튼으로 엑셀을 올려주세요.</div>", unsafe_allow_html=True)
    else:
        medal = ["🥇","🥈","🥉"]
        d = df.copy()
        d.insert(0,"순위",[medal[i] if i<3 else str(i+1) for i in range(len(d))])
        cfg = {c: st.column_config.TextColumn(c, width="small") for c in d.columns}
        st.dataframe(d, use_container_width=True, hide_index=True, column_config=cfg)
        st.download_button("📥 엑셀 다운로드", data=to_excel(df),
                           file_name=f"랭킹_{date.today()}.xlsx", use_container_width=True)

# ══════════════════════════════════════════════════════════════
# 2. 대진 / 경기 입력 (개선된 점수 UI + 카드별 색상)
# ══════════════════════════════════════════════════════════════
elif M == "schedule":
    tours  = load_tours()
    active = [k for k,v in tours.items() if v.get("status")=="진행중"]
    if not active:
        st.markdown("<div class='pg-title'>📅 대진표</div>", unsafe_allow_html=True)
        st.markdown("<div class='ic'>⚠️ 진행 중인 대회가 없습니다.</div>", unsafe_allow_html=True)
        st.stop()

    tid  = active[-1]; tour = tours[tid]
    st.markdown(f"<div class='pg-title'>📅 {tour['title']}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='ic'>📍 {tour.get('date','')} &nbsp;|&nbsp; "
        f"{tour.get('place','')} &nbsp;|&nbsp; 코트 {tour.get('courts',2)}면</div>",
        unsafe_allow_html=True)

    gnames = list(tour["groups"].keys())
    if not gnames:
        st.markdown("<div class='ic'>ℹ️ 대진이 없습니다.</div>", unsafe_allow_html=True)
        st.stop()

    tabs = st.tabs([f"{GLBL[i%len(GLBL)]} {g}" for i,g in enumerate(gnames)])
    for ti, g in enumerate(gnames):
        with tabs[ti]:
            gi   = tour["groups"][g]
            ms   = gi["matches"]
            mode = gi["mode"]
            p2n  = gi.get("player_with_number", {})
            fx   = (mode=="고정페어")
            sv   = stats_fixed(ms) if fx else stats_kdk(ms)
            rit  = list(sv.keys())

            # 전적 매트릭스
            st.markdown("<div class='sec'>📋 전적 매트릭스</div>", unsafe_allow_html=True)
            st.markdown(matrix_html(ms, rit, fx, p2n), unsafe_allow_html=True)

            # KDK 대진표
            if not fx and p2n:
                st.divider()
                show_kdk(len(p2n), gi.get("games",3), p2n)

            st.divider()

            # 현재 순위
            st.markdown("<div class='sec'>🏅 현재 순위</div>", unsafe_allow_html=True)
            if rit:
                ranked = sorted(rit, key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))
                rows = []
                for i,item in enumerate(ranked):
                    if fx:
                        rows.append({"순위":i+1,"팀":" & ".join(list(item)),
                                     "승":sv[item]["승"],"패":sv[item]["패"],
                                     "득실":f'{sv[item]["득실"]:+d}'})
                    else:
                        rows.append({"순위":i+1,"선수":item,
                                     "승":sv[item]["승"],"패":sv[item]["패"],
                                     "득실":f'{sv[item]["득실"]:+d}',"비고":grade(i+1)})
                rdf  = pd.DataFrame(rows)
                rcfg = {c: st.column_config.TextColumn(c, width="small") for c in rdf.columns}
                st.dataframe(rdf, use_container_width=True, hide_index=True, column_config=rcfg)

            st.divider()
            st.markdown("<div class='sec'>🎾 경기 입력</div>", unsafe_allow_html=True)

            # ── 경기 카드 (색상 매치별 고유하게) ──
            for mi, m in enumerate(ms):
                t1s = " & ".join(m["t1"]); t2s = " & ".join(m["t2"])
                color_idx = mi % len(GCLS)   # 각 match마다 다른 색상 순환
                mc  = GCLS[color_idx]
                tbc = TBCLS[color_idx]
                s1v = int(m["s1"]); s2v = int(m["s2"])

                st.markdown(
                    f'<div class="match-card">'
                    f'<div class="match-no {mc}">MATCH {mi+1}</div>',
                    unsafe_allow_html=True)

                left, mid, right = st.columns([5,2,5])

                # 왼쪽 팀 (A)
                with left:
                    st.markdown(f'<div class="team-box {tbc}">{t1s}</div>', unsafe_allow_html=True)
                    # 점수 조정 버튼 + 숫자 (가운데 정렬)
                    col_a1, col_a2, col_a3 = st.columns([1,2,1])
                    with col_a1:
                        st.button("−", key=f"d_{tid}_{g}_{mi}_A",
                                  on_click=adj_score, args=(tid,g,mi,"A",-1),
                                  use_container_width=True)
                    with col_a2:
                        st.markdown(f'<div class="score-num">{s1v}</div>', unsafe_allow_html=True)
                    with col_a3:
                        st.button("+", key=f"i_{tid}_{g}_{mi}_A",
                                  on_click=adj_score, args=(tid,g,mi,"A",1),
                                  use_container_width=True)

                # 가운데 VS
                with mid:
                    st.markdown(
                        '<div style="height:58px;display:flex;align-items:center;'
                        'justify-content:center;"><div class="vs">VS</div></div>',
                        unsafe_allow_html=True)

                # 오른쪽 팀 (B)
                with right:
                    st.markdown(f'<div class="team-box {tbc}">{t2s}</div>', unsafe_allow_html=True)
                    col_b1, col_b2, col_b3 = st.columns([1,2,1])
                    with col_b1:
                        st.button("−", key=f"d_{tid}_{g}_{mi}_B",
                                  on_click=adj_score, args=(tid,g,mi,"B",-1),
                                  use_container_width=True)
                    with col_b2:
                        st.markdown(f'<div class="score-num">{s2v}</div>', unsafe_allow_html=True)
                    with col_b3:
                        st.button("+", key=f"i_{tid}_{g}_{mi}_B",
                                  on_click=adj_score, args=(tid,g,mi,"B",1),
                                  use_container_width=True)

                st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 3. 경기 결과 (변경 없음)
# ══════════════════════════════════════════════════════════════
elif M == "result":
    tours  = load_tours()
    active = [k for k,v in tours.items() if v.get("status")=="진행중"]
    if not active:
        st.markdown("<div class='pg-title'>📊 경기 결과</div>", unsafe_allow_html=True)
        st.markdown("<div class='ic'>⚠️ 진행 중인 대회가 없습니다.</div>", unsafe_allow_html=True)
        st.stop()
    tid = active[-1]; tour = tours[tid]
    st.markdown(f"<div class='pg-title'>📊 {tour['title']}</div>", unsafe_allow_html=True)

    for g, gi in tour["groups"].items():
        mode, ms = gi["mode"], gi["matches"]
        p2n = gi.get("player_with_number", {})
        fx  = (mode=="고정페어")
        sv  = stats_fixed(ms) if fx else stats_kdk(ms)
        ranked = sorted(sv.keys(), key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))

        st.markdown(f'<div class="sec">{g} ({mode})</div>', unsafe_allow_html=True)
        if not fx and p2n:
            show_kdk(len(p2n), gi.get("games",3), p2n); st.divider()

        rows = []
        for i,item in enumerate(ranked):
            pt = rank_pts(i+1, mode)
            if fx:
                rows.append({"순위":i+1,"팀":" & ".join(list(item)),
                             "승":sv[item]["승"],"패":sv[item]["패"],
                             "득실":f'{sv[item]["득실"]:+d}',"포인트":pt,
                             "등급":["🥇 우승","🥈 준우승","🥉 3위"][i] if i<3 else "참가"})
            else:
                rows.append({"순위":i+1,"선수":item,
                             "승":sv[item]["승"],"패":sv[item]["패"],
                             "득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"비고":grade(i+1)})
        rdf  = pd.DataFrame(rows)
        rcfg = {c: st.column_config.TextColumn(c, width="small") for c in rdf.columns}
        st.dataframe(rdf, use_container_width=True, hide_index=True, column_config=rcfg)

        with st.expander("📋 전체 경기 결과 보기"):
            mr = [{"경기":f"{' & '.join(m['t1'])} vs {' & '.join(m['t2'])}",
                   "결과":f"{m['s1']} : {m['s2']}"} for m in ms]
            st.dataframe(pd.DataFrame(mr), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# 4. 지난 대회 (변경 없음)
# ══════════════════════════════════════════════════════════════
elif M == "archive":
    st.markdown("<div class='pg-title'>📂 지난 대회</div>", unsafe_allow_html=True)
    tours = load_tours()
    past  = {k:v for k,v in tours.items() if v.get("status")!="진행중"}
    if not past:
        st.markdown("<div class='ic'>📭 완료된 대회가 없습니다.</div>", unsafe_allow_html=True)
        st.stop()

    sel  = st.selectbox("대회 선택", list(past.keys()),
                        format_func=lambda k:f"{past[k]['title']} ({past[k].get('date','')})")
    tour = past[sel]
    st.markdown(
        f"<div class='ic'>🏆 <strong>{tour['title']}</strong> &nbsp;|&nbsp; "
        f"{tour.get('date','')} &nbsp;|&nbsp; {tour.get('place','')}</div>",
        unsafe_allow_html=True)
    if not tour.get("groups"):
        st.markdown("<div class='ic'>ℹ️ 대진 정보 없음</div>", unsafe_allow_html=True)
        st.stop()

    for g, gi in tour["groups"].items():
        mode, ms = gi["mode"], gi["matches"]
        p2n = gi.get("player_with_number", {})
        fx  = (mode=="고정페어")
        sv  = stats_fixed(ms) if fx else stats_kdk(ms)
        ranked = sorted(sv.keys(), key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))

        st.markdown(f'<div class="sec">{g} ({mode})</div>', unsafe_allow_html=True)
        if not fx and p2n:
            show_kdk(len(p2n), gi.get("games",3), p2n); st.divider()

        rows = []
        for i,item in enumerate(ranked):
            pt = rank_pts(i+1, mode)
            if fx:
                rows.append({"순위":i+1,"팀/선수":" & ".join(list(item)),
                             "승":sv[item]["승"],"패":sv[item]["패"],
                             "득실":f'{sv[item]["득실"]:+d}',"포인트":pt,
                             "등급":["🥇 우승","🥈 준우승","🥉 3위"][i] if i<3 else "참가"})
            else:
                rows.append({"순위":i+1,"선수":item,
                             "승":sv[item]["승"],"패":sv[item]["패"],
                             "득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"비고":grade(i+1)})
        adf  = pd.DataFrame(rows)
        acfg = {c: st.column_config.TextColumn(c, width="small") for c in adf.columns}
        st.dataframe(adf, use_container_width=True, hide_index=True, column_config=acfg)

# ══════════════════════════════════════════════════════════════
# 5. 관리자 (변경 없음)
# ══════════════════════════════════════════════════════════════
elif M == "admin":
    st.markdown("<div class='pg-title'>⚙️ 관리자</div>", unsafe_allow_html=True)
    pw = st.text_input("🔒 비밀번호", type="password", placeholder="비밀번호 입력")
    if pw == ADMIN_PW: ss.is_admin = True
    if not ss.is_admin:
        if pw and pw != ADMIN_PW: st.error("❌ 비밀번호 오류")
        st.stop()

    st.markdown("<div class='ic'>✅ 관리자 모드</div>", unsafe_allow_html=True)
    adm = st.tabs(["🏆 대회","👥 참가자","📋 랭킹","💾 반영"])

    # ── 대회 관리 ──────────────────────────────────────────────
    with adm[0]:
        st.markdown('<div class="sec">새 대회 생성</div>', unsafe_allow_html=True)
        with st.form("f_new"):
            tn = st.text_input("대회명")
            td = st.date_input("날짜", value=date.today())
            tp = st.text_input("장소")
            co = st.selectbox("코트 수",[1,2,3],index=1)
            if st.form_submit_button("✅ 생성", use_container_width=True, type="primary"):
                if tn.strip():
                    ts = load_tours(); tid2 = f"{td}_{tn.strip()}"
                    if tid2 not in ts:
                        ts[tid2] = {"title":tn.strip(),"date":str(td),"place":tp,
                                    "courts":co,"status":"진행중","groups":{}}
                        save_tours(ts); st.success("🎉 생성됨!"); st.rerun()
                    else: st.warning("이미 존재")

        st.divider()
        st.markdown('<div class="sec">대회 목록</div>', unsafe_allow_html=True)
        ts = load_tours()
        for tid2,tv in list(ts.items()):
            st.markdown(f"<div class='ic'><strong>{tv['title']}</strong> ({tv.get('date','')})</div>",
                        unsafe_allow_html=True)
            c1,c2,c3 = st.columns([2,1.5,1.5])
            with c1:
                so=["진행중","완료","예정"]; cs2=tv.get("status","진행중")
                ns=st.selectbox("상태",so,index=so.index(cs2) if cs2 in so else 0,
                                key=f"ss_{tid2}",label_visibility="collapsed")
            with c2:
                if st.button("💾 수정",key=f"es_{tid2}",use_container_width=True):
                    ts[tid2]["status"]=ns; save_tours(ts); st.success("수정됨!"); st.rerun()
            with c3:
                if st.button("🗑 삭제",key=f"dl_{tid2}",use_container_width=True):
                    del ts[tid2]; save_tours(ts); st.rerun()
            if st.button("✏️ 상세 수정",key=f"de_{tid2}",use_container_width=True):
                ss.edit_tour_id=tid2; st.rerun()
            st.divider()

        eid = ss.get("edit_tour_id")
        if eid and eid in ts:
            et = ts[eid]
            st.markdown(f'<div class="sec">✏️ "{et["title"]}" 수정</div>', unsafe_allow_html=True)
            nt=st.text_input("대회명",value=et["title"],key="edt")
            try: dd=pd.to_datetime(et.get("date",str(date.today()))).date()
            except: dd=date.today()
            nd=st.date_input("날짜",value=dd,key="edd")
            np2=st.text_input("장소",value=et.get("place",""),key="edp")
            nc=st.selectbox("코트 수",[1,2,3],index=max(0,et.get("courts",2)-1),key="edc")
            cs,cc=st.columns(2)
            with cs:
                if st.button("💾 저장",type="primary",use_container_width=True,key="sbi"):
                    et.update({"title":nt,"date":str(nd),"place":np2,"courts":nc})
                    save_tours(ts); st.success("저장!"); ss.edit_tour_id=None; st.rerun()
            with cc:
                if st.button("취소",use_container_width=True,key="cce"):
                    ss.edit_tour_id=None; st.rerun()
            st.divider()

            st.markdown('<div class="sec">🎲 그룹 설정</div>', unsafe_allow_html=True)
            st.caption("※ 변경 시 기존 대진 초기화")
            cg=et.get("groups",{})
            ci1,ci2=st.columns(2)
            with ci1: gcnt=st.number_input("그룹 수",1,6,value=max(1,len(cg)),key="egc")
            with ci2: st.write(f"현재 {len(cg)}개")
            gcfg={}
            gnms=[f"{chr(65+i)}그룹" for i in range(int(gcnt))]
            for i,gn in enumerate(gnms):
                ex=cg.get(gn,{})
                st.markdown(f"**{gn}**")
                ca,cb,cc2,cdx=st.columns(4)
                with ca:
                    dsz=len(ex.get("players",[])) if ex else 8
                    sz=st.number_input("인원",2,30,value=dsz,key=f"esz_{eid}_{i}")
                with cb:
                    dmd=ex.get("mode","고정페어"); mdo=["고정페어","KDK","단식"]
                    md=st.selectbox("방식",mdo,
                                    index=mdo.index(dmd) if dmd in mdo else 0,
                                    key=f"emd_{eid}_{i}")
                with cc2:
                    dgc=ex.get("games",4); gco=[3,4,5]
                    gc=st.selectbox("게임수",gco,
                                    index=gco.index(dgc) if dgc in gco else 1,
                                    key=f"egc2_{eid}_{i}")
                with cdx: st.write(f"{len(ex.get('players',[]))}명")
                gcfg[gn]=(sz,md,gc)
            tot=sum(v[0] for v in gcfg.values())
            apl=et.get("players",[])
            if tot==len(apl): st.success(f"✅ {len(apl)}명 / 배정 {tot}명")
            else: st.warning(f"⚠️ {len(apl)}명 / 배정 {tot}명 (차이 {len(apl)-tot:+d}명)")
            if st.button("🎲 대진 재생성",type="primary",use_container_width=True,key="agc"):
                ptr=0; ng={}
                for gn,(sz,md,gc) in gcfg.items():
                    gp=apl[ptr:ptr+sz]; ptr+=sz
                    if md=="고정페어": ms2,pwn=make_fixed(gp)
                    elif md=="KDK":
                        ms2,pwn=make_kdk(gp,gc)
                        if not ms2: ms2,pwn=make_singles(gp)
                    else: ms2,pwn=make_singles(gp)
                    ng[gn]={"players":gp,"mode":md,"games":gc,
                            "matches":ms2,"player_with_number":pwn}
                et["groups"]=ng; save_tours(ts); st.success("완료!"); st.rerun()

    # ── 참가자 ──────────────────────────────────────────────────
    with adm[1]:
        ts=load_tours()
        act2=[k for k,v in ts.items() if v.get("status")=="진행중"]
        if not act2: st.warning("진행 중인 대회 없음"); st.stop()
        stid=st.selectbox("대회 선택",act2,format_func=lambda k:ts[k]['title'],key="a1st")
        tour=ts[stid]
        if tour.get("groups"):
            for gn,gi in tour["groups"].items():
                st.markdown(f"<div class='ic'>✅ <strong>{gn}</strong>: "
                            f"{gi['mode']} / {len(gi['players'])}명</div>",
                            unsafe_allow_html=True)
        st.markdown('<div class="sec">📝 참가자 명단</div>', unsafe_allow_html=True)
        mr2=load_members()
        dtext=", ".join(tour.get("players",ss.participants))
        pinp=st.text_area("명단 (쉼표 구분)",value=dtext,height=90)
        if st.button("✅ 명단 저장",use_container_width=True,type="primary",key="sr"):
            raw=pinp.replace("\n",",").split(",")
            prs=[n.strip() for n in raw if n.strip()]
            ro={nm:i for i,nm in enumerate(mr2)}
            pso=sorted(set(prs),key=lambda x:ro.get(x,len(mr2)+1))
            ss.participants=pso; tour["players"]=pso
            ts[stid]=tour; save_tours(ts); st.success(f"✅ {len(pso)}명 저장"); st.rerun()
        st.markdown('<div class="sec">✏️ 개별 수정</div>', unsafe_allow_html=True)
        if tour.get("groups"):
            grps=list(tour["groups"].keys())
            if grps:
                sg=st.selectbox("그룹",grps,key="a1eg")
                cpl=tour["groups"][sg]["players"].copy()
                st.markdown(f"<div class='ic'>현재 <b>{sg}</b>: "
                            f"{', '.join(cpl) if cpl else '없음'}</div>",
                            unsafe_allow_html=True)
                if cpl:
                    sp=st.selectbox("삭제할 참가자",cpl,key="a1dp")
                    if st.button("🗑 삭제",use_container_width=True,key="a1db"):
                        tour["groups"][sg]["players"].remove(sp)
                        tour["groups"][sg]["matches"]=[
                            m for m in tour["groups"][sg]["matches"]
                            if sp not in m["t1"] and sp not in m["t2"]]
                        agp=[p for gg in grps for p in tour["groups"][gg]["players"]]
                        if sp not in agp and sp in tour.get("players",[]):
                            tour["players"].remove(sp)
                        ts[stid]=tour; save_tours(ts); st.success(f"'{sp}' 삭제"); st.rerun()
                st.divider()
                nn=st.text_input("새 참가자",placeholder="예: 홍길동",key="a1ap")
                if st.button("➕ 추가",use_container_width=True,key="a1ab"):
                    if nn and nn.strip():
                        nn=nn.strip()
                        if nn not in tour["groups"][sg]["players"]:
                            tour["groups"][sg]["players"].append(nn)
                            if nn not in tour.get("players",[]): tour.setdefault("players",[]).append(nn)
                            md2=tour["groups"][sg]["mode"]; gc2=tour["groups"][sg].get("games",3)
                            if md2=="고정페어": nm2,_=make_fixed(tour["groups"][sg]["players"])
                            elif md2=="KDK":
                                nm2,np3=make_kdk(tour["groups"][sg]["players"],gc2)
                                if nm2: tour["groups"][sg]["player_with_number"]=np3
                                else: nm2,_=make_singles(tour["groups"][sg]["players"])
                            else: nm2,_=make_singles(tour["groups"][sg]["players"])
                            tour["groups"][sg]["matches"]=nm2
                            ts[stid]=tour; save_tours(ts); st.success(f"'{nn}' 추가"); st.rerun()
                        else: st.warning("이미 있는 참가자")
                st.divider()
                awg=[(p,gg) for gg in grps for p in tour["groups"][gg]["players"]]
                if awg:
                    mp=st.selectbox("이동할 참가자",[p for p,_ in awg],key="a1mp")
                    cgrp=next((gg for p,gg in awg if p==mp),grps[0])
                    og=[gg for gg in grps if gg!=cgrp]
                    if og:
                        tg=st.selectbox("이동할 그룹",og,key="a1tg")
                        if st.button("🔄 이동",use_container_width=True,key="a1mb"):
                            tour["groups"][cgrp]["players"].remove(mp)
                            tour["groups"][tg]["players"].append(mp)
                            for grp in [cgrp,tg]:
                                md3=tour["groups"][grp]["mode"]; gc3=tour["groups"][grp].get("games",3)
                                if md3=="고정페어": nm3,_=make_fixed(tour["groups"][grp]["players"])
                                elif md3=="KDK":
                                    nm3,np4=make_kdk(tour["groups"][grp]["players"],gc3)
                                    if nm3: tour["groups"][grp]["player_with_number"]=np4
                                    else: nm3,_=make_singles(tour["groups"][grp]["players"])
                                else: nm3,_=make_singles(tour["groups"][grp]["players"])
                                tour["groups"][grp]["matches"]=nm3
                            ts[stid]=tour; save_tours(ts); st.success(f"'{mp}'→{tg}"); st.rerun()
                    else: st.info("이동할 다른 그룹 없음")
        else:
            st.markdown("<div class='ic'>ℹ️ 그룹 없음. 대회 탭에서 먼저 설정하세요.</div>",
                        unsafe_allow_html=True)

    # ── 랭킹 관리 ──────────────────────────────────────────────
    with adm[2]:
        st.markdown('<div class="sec">📁 엑셀/CSV 업로드</div>', unsafe_allow_html=True)
        up=st.file_uploader("파일 선택",type=["xlsx","csv"],key="adm_rank_up")
        if up:
            try:
                du=(pd.read_excel(up) if up.name.endswith("xlsx")
                    else pd.read_csv(up,encoding_errors="replace"))
                if "현재포인트" in du.columns:
                    du["현재포인트"]=pd.to_numeric(du["현재포인트"],errors="coerce").fillna(0)
                    du=du.sort_values("현재포인트",ascending=False).reset_index(drop=True)
                    du["랭킹"]=du.index+1
                st.dataframe(du,use_container_width=True)
                if st.button("💾 저장",type="primary",key="a2su"):
                    save_rank(du)
                    if "이름" in du.columns: save_members(du["이름"].tolist())
                    st.success("✅ 저장!"); st.rerun()
            except Exception as e: st.error(f"오류: {e}")
        st.divider()
        st.markdown('<div class="sec">📊 현재 랭킹</div>', unsafe_allow_html=True)
        dc=load_rank()
        if not dc.empty:
            st.dataframe(dc,use_container_width=True)
            st.download_button("📥 다운로드",data=to_excel(dc),
                               file_name=f"랭킹_{date.today()}.xlsx",key="a2dl")
        st.divider()
        st.markdown('<div class="sec">✏️ 직접 수정</div>', unsafe_allow_html=True)
        de=load_rank()
        if not de.empty:
            edited=st.data_editor(de,use_container_width=True,hide_index=True,num_rows="dynamic")
            if st.button("💾 저장",type="primary",key="a2se"):
                save_rank(edited); save_members(edited["이름"].tolist())
                st.success("✅ 저장!"); st.rerun()

    # ── 결과 반영 ──────────────────────────────────────────────
    with adm[3]:
        ts=load_tours()
        act3=[k for k,v in ts.items() if v.get("status")=="진행중"]
        if not act3: st.warning("진행 중인 대회 없음"); st.stop()
        stid2=st.selectbox("대회 선택",act3,format_func=lambda k:ts[k]['title'],key="a3st")
        t3=ts[stid2]
        if not t3.get("groups"): st.warning("대진 없음"); st.stop()
        earn={}
        for g,gi in t3["groups"].items():
            mode2,ms2=gi["mode"],gi["matches"]
            fx2=(mode2=="고정페어")
            sv2=stats_fixed(ms2) if fx2 else stats_kdk(ms2)
            rk2=sorted(sv2.keys(),key=lambda x:(-sv2[x]["승"],-sv2[x]["득실"]))
            for i,item in enumerate(rk2):
                pt=rank_pts(i+1,mode2)
                if fx2:
                    for p in list(item): earn[p]=earn.get(p,0)+pt
                else: earn[item]=earn.get(item,0)+pt
        if earn:
            ef=pd.DataFrame(earn.items(),columns=["선수","획득포인트"])
            ec={c:st.column_config.TextColumn(c,width="small") for c in ef.columns}
            st.dataframe(ef,use_container_width=True,column_config=ec)
        c1,c2=st.columns(2)
        with c1:
            if st.button("🏆 랭킹 반영",type="primary",use_container_width=True,key="a3ap"):
                dr=load_rank()
                if dr.empty: dr=pd.DataFrame(columns=COLS_RANK)
                for p,pt in earn.items():
                    if p in dr["이름"].values:
                        cur=dr.loc[dr["이름"]==p,"현재포인트"].values[0]
                        dr.loc[dr["이름"]==p,"현재포인트"]=cur+pt
                    else:
                        nr={c:"" for c in COLS_RANK}; nr["이름"]=p; nr["현재포인트"]=pt
                        dr=pd.concat([dr,pd.DataFrame([nr])],ignore_index=True)
                save_rank(dr); ts[stid2]["status"]="완료"
                save_tours(ts); st.success("✅ 반영 완료!"); st.rerun()
        with c2:
            if st.button("🗑 점수 초기화",use_container_width=True,key="a3rs"):
                for g in t3["groups"]:
                    for m in t3["groups"][g]["matches"]: m["s1"]=0; m["s2"]=0
                save_tours(ts); st.success("✅ 초기화!"); st.rerun()
