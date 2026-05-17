import streamlit as st
import pandas as pd
import random, os, json
from datetime import date
from io import BytesIO

st.set_page_config(page_title="두류 테니스", page_icon="🎾",
                   layout="centered", initial_sidebar_state="collapsed")

# ══════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

:root {
  --g0:#1B5E20; --g2:#388E3C; --g3:#66BB6A; --g4:#C8E6C9; --g5:#E8F5E9;
  --yel:#FFD600; --ora:#FB8C00;
  --bg:#F0F7F0; --card:#fff; --bd:#DCEDC8;
  --r1:10px; --r2:16px; --r3:22px;
  --sh:0 2px 10px rgba(0,0,0,.08); --sh2:0 4px 20px rgba(0,0,0,.13);
  --mc0:#2E7D32; --mc1:#1565C0; --mc2:#C62828; --mc3:#6A1B9A; --mc4:#00695C;
  /* 네비 5색 */
  --nav0:#2E7D32; --nav1:#1565C0; --nav2:#E65100; --nav3:#6A1B9A; --nav4:#00695C;
}

*{ font-family:'Noto Sans KR',sans-serif!important; box-sizing:border-box; -webkit-tap-highlight-color:transparent; }

/* ── 레이아웃 ── */
.block-container{ padding:0 0.8rem 5rem!important; max-width:520px!important; margin:0 auto!important; background:var(--bg)!important; }
.stApp{ background:var(--bg)!important; }

/* ── 가운데 정렬 전역 ── */
.stApp [data-testid="stVerticalBlock"] > div,
.stApp [data-testid="stVerticalBlockBorderWrapper"] { text-align:center; }
/* 섹션 라벨, 정보카드는 왼쪽 유지 */
.sec, .ic { text-align:left!important; }
/* 데이터프레임 가운데 */
div[data-testid="stDataFrame"] table th,
div[data-testid="stDataFrame"] table td { text-align:center!important; vertical-align:middle!important; }

/* ── 헤더 ── */
.hdr{
  background:linear-gradient(135deg,var(--g0) 0%,var(--g2) 70%,#43A047 100%);
  margin:0 -0.8rem 0; padding:16px 20px 0; position:relative; overflow:hidden; box-shadow:var(--sh2);
}
.hdr::after{ content:'🎾'; position:absolute; right:14px; top:8px; font-size:2.8rem; opacity:.12; }
.hdr-title{ color:#fff; font-size:1.1rem; font-weight:900; margin:0 0 2px; text-align:center; }
.hdr-sub{ color:rgba(255,255,255,.5); font-size:.6rem; letter-spacing:2px; text-transform:uppercase; margin-bottom:0; text-align:center; }

/* ── 네비게이션 버튼 5색 ── */
/* 버튼을 감싸는 헤더 행 */
.nav-wrap{
  display:flex; margin:0 -0.8rem; overflow:hidden;
}
/* 각 네비 버튼 공통 */
section.main [data-testid="stHorizontalBlock"]:first-of-type .stButton>button{
  background:rgba(255,255,255,.08)!important;
  color:rgba(255,255,255,.75)!important;
  border:none!important; border-radius:0!important;
  font-size:.68rem!important; font-weight:700!important;
  padding:10px 2px!important; line-height:1.4!important;
  white-space:pre-line!important; min-height:52px!important;
  border-bottom:3px solid transparent!important;
  transition:all .15s!important;
}
/* 활성 탭 — 버튼 인덱스별 색 (JS 없이 nth-child 활용) */
section.main [data-testid="stHorizontalBlock"]:first-of-type
  > div:nth-child(1) .stButton>button[kind="primary"]{
  background:var(--nav0)!important; color:#fff!important; border-bottom:3px solid var(--yel)!important;
}
section.main [data-testid="stHorizontalBlock"]:first-of-type
  > div:nth-child(2) .stButton>button[kind="primary"]{
  background:var(--nav1)!important; color:#fff!important; border-bottom:3px solid #90CAF9!important;
}
section.main [data-testid="stHorizontalBlock"]:first-of-type
  > div:nth-child(3) .stButton>button[kind="primary"]{
  background:var(--nav2)!important; color:#fff!important; border-bottom:3px solid #FFAB91!important;
}
section.main [data-testid="stHorizontalBlock"]:first-of-type
  > div:nth-child(4) .stButton>button[kind="primary"]{
  background:var(--nav3)!important; color:#fff!important; border-bottom:3px solid #CE93D8!important;
}
section.main [data-testid="stHorizontalBlock"]:first-of-type
  > div:nth-child(5) .stButton>button[kind="primary"]{
  background:var(--nav4)!important; color:#fff!important; border-bottom:3px solid #80CBC4!important;
}
/* 호버 */
section.main [data-testid="stHorizontalBlock"]:first-of-type .stButton>button:hover{
  color:#fff!important; background:rgba(255,255,255,.18)!important;
}
/* 네비 아래 구분선 */
.nav-bar{ height:4px; background:linear-gradient(90deg,var(--nav0),var(--nav1),var(--nav2),var(--nav3),var(--nav4)); margin:0 -0.8rem 14px; }

/* ── UI 요소 ── */
.pg-title{
  background:linear-gradient(135deg,var(--g0),var(--g2)); color:#fff;
  padding:13px 18px; border-radius:var(--r2); margin:0 0 14px;
  font-size:1.05rem; font-weight:900; text-align:center; box-shadow:var(--sh2);
}
.sec{ font-size:.88rem; font-weight:800; color:var(--g0); border-left:4px solid var(--g3); padding-left:9px; margin:18px 0 8px; }
.ic{ background:var(--card); border-left:4px solid var(--g3); border-radius:var(--r1); padding:11px 14px; margin:7px 0; box-shadow:var(--sh); font-size:.82rem; color:#555; }

/* ── 탭 ── */
button[data-baseweb="tab"]{ font-size:.72rem!important; font-weight:700!important; padding:10px 8px!important; border-radius:var(--r1) var(--r1) 0 0!important; min-height:44px!important; }
button[data-baseweb="tab"][aria-selected="true"]{ background:linear-gradient(135deg,var(--g0),var(--g2))!important; color:#fff!important; }
[data-baseweb="tab-list"]{ background:#DDD!important; border-radius:var(--r1) var(--r1) 0 0!important; padding:4px 4px 0!important; gap:2px!important; }

/* ── 데이터프레임 ── */
div[data-testid="stDataFrame"]{ border-radius:var(--r1)!important; overflow:hidden!important; box-shadow:var(--sh)!important; border:1px solid var(--bd)!important; }
div[data-testid="stDataFrame"] table{ width:100%!important; font-size:.75rem!important; border-collapse:collapse!important; }
div[data-testid="stDataFrame"] table th,
div[data-testid="stDataFrame"] table td{ padding:8px 4px!important; white-space:nowrap; }
div[data-testid="stDataFrame"] thead tr th{ background:var(--g0)!important; color:#fff!important; font-weight:700!important; }
div[data-testid="stDataFrame"] tbody tr:nth-child(even) td{ background:var(--g5)!important; }

/* ════════════════════════════════════════
   경기 카드 & 점수 입력
   [ 팀A ] [ VS ] [ 팀B ]
   [ -  점수  + ] [ -  점수  + ]
   ⬆ 한 행에 가로 배치, 모바일/PC 동일
════════════════════════════════════════ */
.match-card{
  background:var(--card); border-radius:var(--r3);
  padding:14px 10px 16px; margin:14px 0;
  box-shadow:var(--sh2); border:1px solid var(--bd);
}
.match-no{
  display:inline-block; border-radius:20px; padding:3px 14px;
  font-size:.63rem; font-weight:900; letter-spacing:1px; color:#fff; margin-bottom:10px;
}
.mc0{background:var(--mc0);} .mc1{background:var(--mc1);} .mc2{background:var(--mc2);}
.mc3{background:var(--mc3);} .mc4{background:var(--mc4);}

/* 팀 이름 박스 */
.team-box{
  border-radius:var(--r2); padding:10px 6px; font-weight:900; font-size:.88rem;
  min-height:54px; display:flex; align-items:center; justify-content:center;
  word-break:keep-all; line-height:1.3; color:#fff; box-shadow:var(--sh); width:100%;
}
.tb0{background:var(--mc0);} .tb1{background:var(--mc1);} .tb2{background:var(--mc2);}
.tb3{background:var(--mc3);} .tb4{background:var(--mc4);}

/* ───────────────────────────────
   점수 행: − [숫자] +  완전 가로
   핵심: Streamlit column 안의 버튼을
   강제로 height 고정 + 정사각형에 가깝게
─────────────────────────────── */
/* 점수 숫자 표시 div */
.snum{
  width:100%; height:64px;
  display:flex; align-items:center; justify-content:center;
  font-size:2.2rem; font-weight:900; color:var(--g0);
  background:#fff; border:2.5px solid var(--g4);
  border-radius:var(--r1); box-shadow:var(--sh);
  font-variant-numeric:tabular-nums;
}

/* − / + 버튼: 모든 .stButton 버튼 중
   특정 래퍼(.sbtn) 안의 버튼만 타겟 */
.sbtn .stButton>button{
  height:64px!important; min-height:64px!important; width:100%!important;
  font-size:2rem!important; font-weight:900!important; line-height:1!important;
  padding:0!important; margin:0!important;
  border-radius:var(--r1)!important;
  background:var(--g4)!important; color:var(--g0)!important;
  border:2px solid var(--g3)!important;
  box-shadow:var(--sh)!important;
  transition:background .08s, transform .06s!important;
}
.sbtn .stButton>button:hover{ background:var(--g3)!important; color:#fff!important; }
.sbtn .stButton>button:active{ background:var(--g2)!important; color:#fff!important; transform:scale(.93)!important; }

/* VS 원 */
.vs-wrap{ display:flex; align-items:center; justify-content:center; height:54px; }
.vs{
  width:44px; height:44px; background:linear-gradient(135deg,#FFB74D,var(--ora));
  border-radius:50%; display:flex; align-items:center; justify-content:center;
  font-weight:900; font-size:.75rem; color:#fff; box-shadow:var(--sh);
}

/* 매트릭스 / KDK */
.mx-wrap,.kdk{ background:var(--card); border-radius:var(--r1); padding:10px; box-shadow:var(--sh); overflow-x:auto; margin:8px 0; border:1px solid var(--bd); -webkit-overflow-scrolling:touch; }
.mx,.kdk table{ border-collapse:collapse; white-space:nowrap; font-size:.7rem; width:100%; }
.mx th,.mx td,.kdk th,.kdk td{ padding:7px 8px; border:1px solid var(--bd); text-align:center; }
.mx thead th,.kdk thead th{ background:var(--g0); color:#fff; font-weight:700; }
.mx tbody tr:nth-child(even),.kdk tbody tr:nth-child(even){ background:var(--g5); }
.mx-grey{ background:#D0D0D0!important; color:#D0D0D0!important; }
.mx-dash{ color:#CCC; }
.mx-sc{ font-weight:800; color:var(--g0); }

/* 일반 버튼 */
.stButton>button{ border-radius:var(--r2)!important; font-weight:700!important; font-size:.85rem!important; min-height:52px!important; padding:10px 14px!important; }
.stButton>button[kind="primary"]{ background:linear-gradient(135deg,var(--g0),var(--g2))!important; color:#fff!important; border:none!important; box-shadow:0 4px 14px rgba(46,125,50,.35)!important; }
.stButton>button[kind="secondary"]{ background:var(--card)!important; color:var(--g0)!important; border:2px solid var(--g4)!important; }

/* 인풋 */
.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stSelectbox>div>div{ min-height:50px!important; border-radius:var(--r1)!important; }

/* 파일 업로더 한국어화 */
[data-testid="stFileUploaderDropzoneInstructions"]>div>span,
[data-testid="stFileUploaderDropzoneInstructions"]>div>small{ display:none!important; }
[data-testid="stBaseButton-secondary"] span{ display:none!important; }
[data-testid="stBaseButton-secondary"]::after{ content:'📂 파일 선택'; font-size:.85rem; font-weight:700; }
[data-testid="stFileUploaderDropzone"]{ border:2px dashed var(--g3)!important; background:var(--g5)!important; border-radius:var(--r2)!important; }

/* 기타 */
hr{ margin:14px 0; border-color:var(--bd); }
div[data-testid="stDataEditor"] table{ font-size:.75rem!important; text-align:center!important; }
::-webkit-scrollbar{ width:4px; height:4px; }
::-webkit-scrollbar-thumb{ background:var(--g4); border-radius:4px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 상수
# ══════════════════════════════════════════════════════════════
RANK_FILE   = "ranking_master.csv"
MEMBER_FILE = "member_roster.json"
TOUR_FILE   = "tournaments.json"
ADMIN_PW    = "0502"
COLS_RANK   = ["랭킹","이름","현재포인트","3월 포인트","결과","부과점","그룹","비고"]

GCLS  = ["mc0","mc1","mc2","mc3","mc4"]
TBCLS = ["tb0","tb1","tb2","tb3","tb4"]
GLBL  = ["🟢","🔵","🔴","🟣","🩵"]

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

# ══════════════════════════════════════════════════════════════
# 데이터 함수
# ══════════════════════════════════════════════════════════════
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
        with open(MEMBER_FILE,"r",encoding="utf-8") as f: return json.load(f)
    df = load_rank()
    return df["이름"].tolist() if not df.empty else []

def save_members(names):
    with open(MEMBER_FILE,"w",encoding="utf-8") as f: json.dump(names,f,ensure_ascii=False,indent=2)

def load_tours():
    if os.path.exists(TOUR_FILE):
        with open(TOUR_FILE,"r",encoding="utf-8") as f: return json.load(f)
    return {}

def save_tours(d):
    with open(TOUR_FILE,"w",encoding="utf-8") as f: json.dump(d,f,ensure_ascii=False,indent=2)

def to_excel(df):
    buf = BytesIO(); df.to_excel(buf,index=False); return buf.getvalue()

def stats_fixed(matches):
    s = {}
    for m in matches:
        t1,t2 = tuple(m["t1"]),tuple(m["t2"])
        for t in (t1,t2):
            if t not in s: s[t]={"승":0,"패":0,"득실":0}
        a,b = int(m["s1"]),int(m["s2"])
        if a>b:   s[t1]["승"]+=1; s[t2]["패"]+=1
        elif b>a: s[t2]["승"]+=1; s[t1]["패"]+=1
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

def rank_pts(rank,mode):
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

def make_kdk(players,gperson):
    n=len(players); bp=KDK_3G.get(n) if gperson==3 else KDK_4G.get(n)
    if not bp: return None,{}
    sh=random.sample(players,n)
    p2n={sh[i]:i+1 for i in range(n)}; n2p={i+1:sh[i] for i in range(n)}
    ms=[{"t1":[n2p[a],n2p[b]],"t2":[n2p[c],n2p[d]],"s1":0,"s2":0} for a,b,c,d in bp]
    return ms,p2n

def make_fixed(players):
    n=len(players); pairs=[(players[i],players[n-1-i]) for i in range(n//2)]
    ms=[{"t1":list(pairs[i]),"t2":list(pairs[j]),"s1":0,"s2":0}
        for i in range(len(pairs)) for j in range(i+1,len(pairs))]
    random.shuffle(ms); return ms,{}

def make_singles(players):
    pl=players[:]; random.shuffle(pl)
    ms=[{"t1":[pl[i]],"t2":[pl[j]],"s1":0,"s2":0}
        for i in range(len(pl)) for j in range(i+1,len(pl))]
    random.shuffle(ms); return ms,{}

def kdk_html(n,gperson,p2n):
    bp=KDK_3G.get(n) if gperson==3 else KDK_4G.get(n)
    if not bp: return ""
    n2p={v:k for k,v in p2n.items()}
    title=f"KDK 1인 {gperson}게임 — {n}명"
    rows=""
    for i,(a,b,c,d) in enumerate(bp):
        t1=f"{n2p.get(a,a)}({a}) &amp; {n2p.get(b,b)}({b})"
        t2=f"{n2p.get(c,c)}({c}) &amp; {n2p.get(d,d)}({d})"
        rows+=(f"<tr><td><span style='background:#1B5E20;color:#fff;border-radius:20px;"
               f"padding:2px 9px;font-size:.62rem;font-weight:700'>{i+1}</span></td>"
               f"<td style='text-align:left;white-space:nowrap'>{t1} vs {t2}</td></tr>")
    return (f'<div class="kdk"><div style="font-weight:800;color:#1B5E20;font-size:.85rem;margin-bottom:8px">📋 {title}</div>'
            f'<table><thead><tr><th style="width:38px">순서</th><th>대진</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')

def show_kdk(n,gperson,p2n): st.markdown(kdk_html(n,gperson,p2n),unsafe_allow_html=True)

def matrix_html(matches,rank_items,is_fixed,p2n):
    if not matches or not rank_items: return ""
    lab={t:" &amp; ".join(list(t)) for t in rank_items} if is_fixed else {p:f"{p}({p2n.get(p,'?')})" for p in rank_items}
    mat={lab[t]:{lab[o]:("■" if t==o else "—") for o in lab} for t in lab}
    for m in matches:
        a,b=int(m["s1"]),int(m["s2"])
        if a>0 or b>0:
            if is_fixed:
                k1,k2=tuple(m["t1"]),tuple(m["t2"])
                mat[lab[k1]][lab[k2]]=f"{a}:{b}"; mat[lab[k2]][lab[k1]]=f"{b}:{a}"
            else:
                for x in m["t1"]:
                    for y in m["t2"]:
                        mat[lab[x]][lab[y]]=f"{a}:{b}"; mat[lab[y]][lab[x]]=f"{b}:{a}"
    keys=list(lab.values())
    hdr="".join(f"<th style='white-space:nowrap'>{k}</th>" for k in keys)
    body=""
    for rk in keys:
        body+=f"<tr><th style='white-space:nowrap'>{rk}</th>"
        for ck in keys:
            v=mat[rk][ck]
            if v=="■": body+='<td class="mx-grey">■</td>'
            elif v=="—": body+='<td class="mx-dash">—</td>'
            else: body+=f'<td class="mx-sc">{v}</td>'
        body+="</tr>"
    return (f'<div class="mx-wrap"><table class="mx"><thead><tr><th></th>{hdr}</tr></thead>'
            f'<tbody>{body}</tbody></table></div>')

def adj_score(tid,grp,mi,side,delta):
    ts=load_tours(); m=ts[tid]["groups"][grp]["matches"][mi]
    k="s1" if side=="A" else "s2"
    m[k]=max(0,int(m[k])+delta); save_tours(ts)

# ══════════════════════════════════════════════════════════════
# 세션
# ══════════════════════════════════════════════════════════════
ss=st.session_state
if "is_admin" not in ss: ss.is_admin=False
if "menu" not in ss: ss.menu="ranking"
if "participants" not in ss: ss.participants=[]

# ══════════════════════════════════════════════════════════════
# 헤더 + 네비
# ══════════════════════════════════════════════════════════════
MENUS=[("ranking","🏆\n랭킹"),("schedule","📅\n대진"),("result","📊\n결과"),("archive","📂\n기록"),("admin","⚙️\n관리")]

st.markdown('<div class="hdr"><div class="hdr-title">🎾 두류 테니스 클럽</div><div class="hdr-sub">Duryu Tennis Club</div></div>',unsafe_allow_html=True)

cols=st.columns(len(MENUS))
for col,(key,label) in zip(cols,MENUS):
    with col:
        t="primary" if ss.menu==key else "secondary"
        if st.button(label,key=f"nav_{key}",use_container_width=True,type=t):
            ss.menu=key; st.rerun()

st.markdown('<div class="nav-bar"></div>',unsafe_allow_html=True)
M=ss.menu

# ══════════════════════════════════════════════════════════════
# 1. 랭킹
# ══════════════════════════════════════════════════════════════
if M=="ranking":
    st.markdown("<div class='pg-title'>🏆 두류 랭킹</div>",unsafe_allow_html=True)
    with st.expander("📤 엑셀/CSV 바로 업로드"):
        up=st.file_uploader("파일",type=["xlsx","csv"],key="rank_up_main",label_visibility="collapsed")
        st.caption("xlsx / csv 파일 지원")
        if up:
            try:
                du=pd.read_excel(up) if up.name.endswith("xlsx") else pd.read_csv(up,encoding_errors="replace")
                if "현재포인트" in du.columns:
                    du["현재포인트"]=pd.to_numeric(du["현재포인트"],errors="coerce").fillna(0)
                    du=du.sort_values("현재포인트",ascending=False).reset_index(drop=True)
                    du["랭킹"]=du.index+1
                st.dataframe(du,use_container_width=True)
                if st.button("💾 랭킹 저장",type="primary",use_container_width=True,key="rank_save_main"):
                    save_rank(du)
                    if "이름" in du.columns: save_members(du["이름"].tolist())
                    st.success("저장 완료!"); st.rerun()
            except Exception as e: st.error(f"오류: {e}")
    df=load_rank()
    if df.empty:
        st.markdown("<div class='ic'>📭 등록된 랭킹이 없습니다.<br>위 업로드 버튼으로 엑셀을 올려주세요.</div>",unsafe_allow_html=True)
    else:
        medal=["🥇","🥈","🥉"]
        d=df.copy()
        d.insert(0,"순위",[medal[i] if i<3 else str(i+1) for i in range(len(d))])
        cfg={c:st.column_config.TextColumn(c,width="small") for c in d.columns}
        st.dataframe(d,use_container_width=True,hide_index=True,column_config=cfg)
        st.download_button("📥 엑셀 다운로드",data=to_excel(df),file_name=f"랭킹_{date.today()}.xlsx",use_container_width=True)

# ══════════════════════════════════════════════════════════════
# 2. 대진/경기 입력
# ══════════════════════════════════════════════════════════════
elif M=="schedule":
    tours=load_tours()
    active=[k for k,v in tours.items() if v.get("status")=="진행중"]
    if not active:
        st.markdown("<div class='pg-title'>📅 대진표</div>",unsafe_allow_html=True)
        st.markdown("<div class='ic'>⚠️ 진행 중인 대회가 없습니다.</div>",unsafe_allow_html=True)
        st.stop()
    tid=active[-1]; tour=tours[tid]
    st.markdown(f"<div class='pg-title'>📅 {tour['title']}</div>",unsafe_allow_html=True)
    st.markdown(f"<div class='ic'>📍 {tour.get('date','')} &nbsp;|&nbsp; {tour.get('place','')} &nbsp;|&nbsp; 코트 {tour.get('courts',2)}면</div>",unsafe_allow_html=True)

    gnames=list(tour["groups"].keys())
    if not gnames:
        st.markdown("<div class='ic'>ℹ️ 대진이 없습니다.</div>",unsafe_allow_html=True); st.stop()

    tabs=st.tabs([f"{GLBL[i%len(GLBL)]} {g}" for i,g in enumerate(gnames)])
    for ti,g in enumerate(gnames):
        with tabs[ti]:
            gi=tour["groups"][g]; ms=gi["matches"]; mode=gi["mode"]
            p2n=gi.get("player_with_number",{}); fx=(mode=="고정페어")
            sv=stats_fixed(ms) if fx else stats_kdk(ms); rit=list(sv.keys())

            st.markdown("<div class='sec'>📋 전적 매트릭스</div>",unsafe_allow_html=True)
            st.markdown(matrix_html(ms,rit,fx,p2n),unsafe_allow_html=True)
            if not fx and p2n: st.divider(); show_kdk(len(p2n),gi.get("games",3),p2n)
            st.divider()

            st.markdown("<div class='sec'>🏅 현재 순위</div>",unsafe_allow_html=True)
            if rit:
                ranked=sorted(rit,key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))
                rows=[]
                for i,item in enumerate(ranked):
                    if fx: rows.append({"순위":i+1,"팀":" & ".join(list(item)),"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}'})
                    else:  rows.append({"순위":i+1,"선수":item,"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"비고":grade(i+1)})
                rdf=pd.DataFrame(rows)
                rcfg={c:st.column_config.TextColumn(c,width="small") for c in rdf.columns}
                st.dataframe(rdf,use_container_width=True,hide_index=True,column_config=rcfg)
            st.divider()

            st.markdown("<div class='sec'>🎾 경기 입력</div>",unsafe_allow_html=True)

            for mi,m in enumerate(ms):
                t1s=" & ".join(m["t1"]); t2s=" & ".join(m["t2"])
                mc=GCLS[mi%len(GCLS)]; tbc=TBCLS[mi%len(TBCLS)]
                s1v=int(m["s1"]); s2v=int(m["s2"])

                st.markdown(f'<div class="match-card"><span class="match-no {mc}">MATCH {mi+1}</span>',unsafe_allow_html=True)

                # ── 윗 행: 팀A | VS | 팀B ──
                c1,c2,c3=st.columns([5,2,5])
                with c1: st.markdown(f'<div class="team-box {tbc}">{t1s}</div>',unsafe_allow_html=True)
                with c2: st.markdown('<div class="vs-wrap"><div class="vs">VS</div></div>',unsafe_allow_html=True)
                with c3: st.markdown(f'<div class="team-box {tbc}">{t2s}</div>',unsafe_allow_html=True)

                # ── 아랫 행: [−][숫자][+]  [−][숫자][+] ──
                # 6칸으로 분할: A−, A숫자, A+, B−, B숫자, B+
                ca,cb,cc,cd,ce,cf=st.columns([1,1.4,1,1,1.4,1])
                with ca:
                    st.markdown('<div class="sbtn">',unsafe_allow_html=True)
                    st.button("−",key=f"d_{tid}_{g}_{mi}_A",on_click=adj_score,args=(tid,g,mi,"A",-1),use_container_width=True)
                    st.markdown('</div>',unsafe_allow_html=True)
                with cb:
                    st.markdown(f'<div class="snum">{s1v}</div>',unsafe_allow_html=True)
                with cc:
                    st.markdown('<div class="sbtn">',unsafe_allow_html=True)
                    st.button("+",key=f"i_{tid}_{g}_{mi}_A",on_click=adj_score,args=(tid,g,mi,"A",1),use_container_width=True)
                    st.markdown('</div>',unsafe_allow_html=True)
                with cd:
                    st.markdown('<div class="sbtn">',unsafe_allow_html=True)
                    st.button("−",key=f"d_{tid}_{g}_{mi}_B",on_click=adj_score,args=(tid,g,mi,"B",-1),use_container_width=True)
                    st.markdown('</div>',unsafe_allow_html=True)
                with ce:
                    st.markdown(f'<div class="snum">{s2v}</div>',unsafe_allow_html=True)
                with cf:
                    st.markdown('<div class="sbtn">',unsafe_allow_html=True)
                    st.button("+",key=f"i_{tid}_{g}_{mi}_B",on_click=adj_score,args=(tid,g,mi,"B",1),use_container_width=True)
                    st.markdown('</div>',unsafe_allow_html=True)

                st.markdown('</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 3. 경기 결과
# ══════════════════════════════════════════════════════════════
elif M=="result":
    tours=load_tours()
    active=[k for k,v in tours.items() if v.get("status")=="진행중"]
    if not active:
        st.markdown("<div class='pg-title'>📊 경기 결과</div>",unsafe_allow_html=True)
        st.markdown("<div class='ic'>⚠️ 진행 중인 대회가 없습니다.</div>",unsafe_allow_html=True); st.stop()
    tid=active[-1]; tour=tours[tid]
    st.markdown(f"<div class='pg-title'>📊 {tour['title']}</div>",unsafe_allow_html=True)
    for g,gi in tour["groups"].items():
        mode,ms=gi["mode"],gi["matches"]; p2n=gi.get("player_with_number",{}); fx=(mode=="고정페어")
        sv=stats_fixed(ms) if fx else stats_kdk(ms)
        ranked=sorted(sv.keys(),key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))
        st.markdown(f'<div class="sec">{g} ({mode})</div>',unsafe_allow_html=True)
        if not fx and p2n: show_kdk(len(p2n),gi.get("games",3),p2n); st.divider()
        rows=[]
        for i,item in enumerate(ranked):
            pt=rank_pts(i+1,mode)
            if fx: rows.append({"순위":i+1,"팀":" & ".join(list(item)),"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"등급":["🥇 우승","🥈 준우승","🥉 3위"][i] if i<3 else "참가"})
            else:  rows.append({"순위":i+1,"선수":item,"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"비고":grade(i+1)})
        rdf=pd.DataFrame(rows); rcfg={c:st.column_config.TextColumn(c,width="small") for c in rdf.columns}
        st.dataframe(rdf,use_container_width=True,hide_index=True,column_config=rcfg)
        with st.expander("📋 전체 경기 결과 보기"):
            mr=[{"경기":f"{' & '.join(m['t1'])} vs {' & '.join(m['t2'])}","결과":f"{m['s1']} : {m['s2']}"} for m in ms]
            st.dataframe(pd.DataFrame(mr),use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════════════════
# 4. 지난 대회
# ══════════════════════════════════════════════════════════════
elif M=="archive":
    st.markdown("<div class='pg-title'>📂 지난 대회</div>",unsafe_allow_html=True)
    tours=load_tours(); past={k:v for k,v in tours.items() if v.get("status")!="진행중"}
    if not past: st.markdown("<div class='ic'>📭 완료된 대회가 없습니다.</div>",unsafe_allow_html=True); st.stop()
    sel=st.selectbox("대회 선택",list(past.keys()),format_func=lambda k:f"{past[k]['title']} ({past[k].get('date','')})")
    tour=past[sel]
    st.markdown(f"<div class='ic'>🏆 <strong>{tour['title']}</strong> &nbsp;|&nbsp; {tour.get('date','')} &nbsp;|&nbsp; {tour.get('place','')}</div>",unsafe_allow_html=True)
    if not tour.get("groups"): st.markdown("<div class='ic'>ℹ️ 대진 정보 없음</div>",unsafe_allow_html=True); st.stop()
    for g,gi in tour["groups"].items():
        mode,ms=gi["mode"],gi["matches"]; p2n=gi.get("player_with_number",{}); fx=(mode=="고정페어")
        sv=stats_fixed(ms) if fx else stats_kdk(ms)
        ranked=sorted(sv.keys(),key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))
        st.markdown(f'<div class="sec">{g} ({mode})</div>',unsafe_allow_html=True)
        if not fx and p2n: show_kdk(len(p2n),gi.get("games",3),p2n); st.divider()
        rows=[]
        for i,item in enumerate(ranked):
            pt=rank_pts(i+1,mode)
            if fx: rows.append({"순위":i+1,"팀/선수":" & ".join(list(item)),"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"등급":["🥇 우승","🥈 준우승","🥉 3위"][i] if i<3 else "참가"})
            else:  rows.append({"순위":i+1,"선수":item,"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"비고":grade(i+1)})
        adf=pd.DataFrame(rows); acfg={c:st.column_config.TextColumn(c,width="small") for c in adf.columns}
        st.dataframe(adf,use_container_width=True,hide_index=True,column_config=acfg)

# ══════════════════════════════════════════════════════════════
# 5. 관리자
# ══════════════════════════════════════════════════════════════
elif M=="admin":
    st.markdown("<div class='pg-title'>⚙️ 관리자</div>",unsafe_allow_html=True)
    pw=st.text_input("🔒 비밀번호",type="password",placeholder="비밀번호 입력")
    if pw==ADMIN_PW: ss.is_admin=True
    if not ss.is_admin:
        if pw: st.error("❌ 비밀번호 오류")
        st.stop()
    st.markdown("<div class='ic'>✅ 관리자 모드</div>",unsafe_allow_html=True)
    adm=st.tabs(["🏆 대회","👥 참가자·대진","📋 랭킹","💾 반영"])

    # ── 대회 관리 ──
    with adm[0]:
        st.markdown('<div class="sec">새 대회 생성</div>',unsafe_allow_html=True)
        with st.form("f_new"):
            tn=st.text_input("대회명"); td=st.date_input("날짜",value=date.today())
            tp=st.text_input("장소"); co=st.selectbox("코트 수",[1,2,3],index=1)
            if st.form_submit_button("✅ 생성",use_container_width=True,type="primary"):
                if tn.strip():
                    ts=load_tours(); tid2=f"{td}_{tn.strip()}"
                    if tid2 not in ts:
                        ts[tid2]={"title":tn.strip(),"date":str(td),"place":tp,"courts":co,"status":"진행중","groups":{}}
                        save_tours(ts); st.success("생성됨!"); st.rerun()
                    else: st.warning("이미 존재")
        st.divider()
        st.markdown('<div class="sec">대회 목록</div>',unsafe_allow_html=True)
        ts=load_tours()
        for tid2,tv in list(ts.items()):
            st.markdown(f"<div class='ic'><strong>{tv['title']}</strong> ({tv.get('date','')})</div>",unsafe_allow_html=True)
            c1,c2,c3=st.columns([2,1.5,1.5])
            with c1:
                so=["진행중","완료","예정"]; cur=tv.get("status","진행중")
                ns=st.selectbox("상태",so,index=so.index(cur) if cur in so else 0,key=f"ss_{tid2}",label_visibility="collapsed")
            with c2:
                if st.button("💾 수정",key=f"es_{tid2}",use_container_width=True):
                    ts[tid2]["status"]=ns; save_tours(ts); st.success("수정됨!"); st.rerun()
            with c3:
                if st.button("🗑 삭제",key=f"dl_{tid2}",use_container_width=True):
                    del ts[tid2]; save_tours(ts); st.rerun()
            if st.button("✏️ 상세 수정",key=f"de_{tid2}",use_container_width=True):
                ss.edit_tour_id=tid2; st.rerun()
            st.divider()
        if eid:=ss.get("edit_tour_id"):
            if eid in ts:
                et=ts[eid]
                st.markdown(f'<div class="sec">✏️ "{et["title"]}" 수정</div>',unsafe_allow_html=True)
                nt=st.text_input("대회명",value=et["title"],key="edt")
                try: dd=pd.to_datetime(et.get("date",str(date.today()))).date()
                except: dd=date.today()
                nd=st.date_input("날짜",value=dd,key="edd")
                np2=st.text_input("장소",value=et.get("place",""),key="edp")
                nc=st.selectbox("코트 수",[1,2,3],index=max(0,et.get("courts",2)-1),key="edc")
                cs1,cs2=st.columns(2)
                with cs1:
                    if st.button("💾 저장",type="primary",use_container_width=True,key="sbi"):
                        et.update({"title":nt,"date":str(nd),"place":np2,"courts":nc})
                        save_tours(ts); st.success("저장!"); ss.edit_tour_id=None; st.rerun()
                with cs2:
                    if st.button("취소",use_container_width=True,key="cce"):
                        ss.edit_tour_id=None; st.rerun()
                st.divider()
                st.markdown('<div class="sec">🎲 그룹 설정</div>',unsafe_allow_html=True)
                st.caption("※ 변경 시 기존 대진 초기화")
                cg=et.get("groups",{}); ci1,ci2=st.columns(2)
                with ci1: gcnt=st.number_input("그룹 수",1,6,value=max(1,len(cg)),key="egc")
                with ci2: st.write(f"현재 {len(cg)}개")
                gcfg={}; gnms=[f"{chr(65+i)}그룹" for i in range(int(gcnt))]
                for i,gn in enumerate(gnms):
                    ex=cg.get(gn,{}); st.markdown(f"**{gn}**")
                    a1,a2,a3,a4=st.columns(4)
                    with a1: sz=st.number_input("인원",2,30,value=len(ex.get("players",[])) or 8,key=f"esz_{eid}_{i}")
                    with a2: dmd=ex.get("mode","고정페어"); mdo=["고정페어","KDK","단식"]; md=st.selectbox("방식",mdo,index=mdo.index(dmd) if dmd in mdo else 0,key=f"emd_{eid}_{i}")
                    with a3: dgc=ex.get("games",4); gco=[3,4,5]; gc=st.selectbox("게임수",gco,index=gco.index(dgc) if dgc in gco else 1,key=f"egc2_{eid}_{i}")
                    with a4: st.write(f"{len(ex.get('players',[]))}명")
                    gcfg[gn]=(sz,md,gc)
                tot=sum(v[0] for v in gcfg.values()); apl=et.get("players",[])
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
                        ng[gn]={"players":gp,"mode":md,"games":gc,"matches":ms2,"player_with_number":pwn}
                    et["groups"]=ng; save_tours(ts); st.success("대진 재생성 완료!"); st.rerun()

    # ── 참가자·대진 ──
    with adm[1]:
        ts=load_tours()
        act2=[k for k,v in ts.items() if v.get("status")=="진행중"]
        if not act2: st.warning("진행 중인 대회 없음"); st.stop()
        sel_tid=st.selectbox("대회 선택",act2,format_func=lambda k:ts[k]['title'],key="a1st")
        tour=ts[sel_tid]
        st.markdown('<div class="sec">🎲 1. 그룹 구성 설정</div>',unsafe_allow_html=True)
        current_groups=tour.get("groups",{})
        gcnt=st.number_input("그룹 수",1,6,value=len(current_groups) or 4,key="temp_gcnt")
        group_names=[f"{chr(65+i)}그룹" for i in range(gcnt)]
        temp_gcfg={}
        for i,gn in enumerate(group_names):
            ex=current_groups.get(gn,{}); st.markdown(f"**{gn}**")
            c1,c2,c3,c4=st.columns(4)
            with c1: sz=st.number_input("인원",2,30,value=len(ex.get("players",[])) or 8,key=f"tmp_sz_{i}")
            with c2: md=st.selectbox("방식",["고정페어","KDK","단식"],index=["고정페어","KDK","단식"].index(ex.get("mode","고정페어")),key=f"tmp_md_{i}")
            with c3: gc=st.selectbox("게임수",[3,4,5],index=[3,4,5].index(ex.get("games",4)),key=f"tmp_gc_{i}")
            with c4: st.write(f"현재 {len(ex.get('players',[]))}명")
            temp_gcfg[gn]=(sz,md,gc)
        if st.button("💾 그룹 구성 저장",use_container_width=True,key="save_temp"):
            ss.temp_group_config=temp_gcfg; ss.temp_tour_id=sel_tid
            st.success("저장됨! 아래에서 참가자를 배정하세요."); st.rerun()
        st.divider()
        st.markdown('<div class="sec">👥 2. 참가자 배정</div>',unsafe_allow_html=True)
        gcfg=ss.get("temp_group_config") if ss.get("temp_tour_id")==sel_tid else {gn:(len(gi["players"]),gi["mode"],gi.get("games",4)) for gn,gi in current_groups.items()}
        if not gcfg: st.info("먼저 그룹 구성을 저장하세요."); st.stop()
        all_members=load_members()
        if not all_members: st.warning("회원 명단이 없습니다."); st.stop()
        assigned={gn:current_groups[gn].get("players",[]).copy() if gn in current_groups else [] for gn in gcfg}
        new_assigned={}
        for gn,(sz,md,gc) in gcfg.items():
            st.markdown(f"#### {gn} (최대 {sz}명)")
            other_assigned={p for og,lst in assigned.items() if og!=gn for p in lst}
            selectable=[m for m in all_members if m not in other_assigned or m in assigned.get(gn,[])]
            sel=st.multiselect(f"{gn} 참가자",options=selectable,default=assigned.get(gn,[]),key=f"assign_{gn}")
            if len(sel)>sz: st.warning(f"최대 {sz}명")
            new_assigned[gn]=sel[:sz]
        total_assigned=sum(len(v) for v in new_assigned.values())
        total_needed=sum(v[0] for v in gcfg.values())
        if total_assigned==total_needed: st.success(f"✅ 배정 완료! 총 {total_assigned}명")
        else: st.warning(f"⚠️ 배정 {total_assigned}명 / 필요 {total_needed}명")
        if st.button("🎲 3. 대진 생성",type="primary",use_container_width=True,key="gen_final"):
            all_sel=[p for lst in new_assigned.values() for p in lst]
            if len(set(all_sel))!=len(all_sel): st.error("중복 선수가 있습니다!"); st.stop()
            if total_assigned!=total_needed: st.error("인원 수가 맞지 않습니다."); st.stop()
            ng={}
            for gn,players in new_assigned.items():
                sz,md,gc=gcfg[gn]
                if md=="고정페어": ms2,pwn=make_fixed(players)
                elif md=="KDK":
                    ms2,pwn=make_kdk(players,gc)
                    if not ms2: ms2,pwn=make_singles(players)
                else: ms2,pwn=make_singles(players)
                ng[gn]={"players":players,"mode":md,"games":gc,"matches":ms2,"player_with_number":pwn}
            tour["groups"]=ng; tour["players"]=all_sel; save_tours(ts)
            for k in ["temp_group_config","temp_tour_id"]:
                if k in ss: del ss[k]
            st.success("✅ 대진 생성 완료!"); st.rerun()
        st.divider()
        st.markdown('<div class="sec">✏️ 개별 수정 (대진 유지)</div>',unsafe_allow_html=True)
        if tour.get("groups"):
            groups=list(tour["groups"].keys())
            if groups:
                sel_g=st.selectbox("그룹",groups,key="edit_g")
                cur_pl=tour["groups"][sel_g]["players"].copy()
                st.markdown(f"**현재 {sel_g}:** {', '.join(cur_pl) if cur_pl else '없음'}")
                if cur_pl:
                    sel_p=st.selectbox("삭제",cur_pl,key="del_p")
                    if st.button("🗑 삭제",use_container_width=True,key="del_b"):
                        tour["groups"][sel_g]["players"].remove(sel_p)
                        tour["groups"][sel_g]["matches"]=[m for m in tour["groups"][sel_g]["matches"] if sel_p not in m["t1"] and sel_p not in m["t2"]]
                        if sel_p not in [p for g in groups for p in tour["groups"][g]["players"]]:
                            if sel_p in tour.get("players",[]): tour["players"].remove(sel_p)
                        save_tours(ts); st.success(f"'{sel_p}' 삭제"); st.rerun()
                st.markdown("---")
                nn=st.text_input("새 참가자",placeholder="홍길동",key="add_n")
                if st.button("➕ 추가",use_container_width=True,key="add_b"):
                    if nn and nn.strip():
                        nn=nn.strip()
                        if nn not in tour["groups"][sel_g]["players"]:
                            tour["groups"][sel_g]["players"].append(nn)
                            if nn not in tour.get("players",[]): tour.setdefault("players",[]).append(nn)
                            md2=tour["groups"][sel_g]["mode"]; gc2=tour["groups"][sel_g].get("games",3)
                            if md2=="고정페어": nm2,_=make_fixed(tour["groups"][sel_g]["players"])
                            elif md2=="KDK":
                                nm2,np3=make_kdk(tour["groups"][sel_g]["players"],gc2)
                                if nm2: tour["groups"][sel_g]["player_with_number"]=np3
                                else: nm2,_=make_singles(tour["groups"][sel_g]["players"])
                            else: nm2,_=make_singles(tour["groups"][sel_g]["players"])
                            tour["groups"][sel_g]["matches"]=nm2
                            save_tours(ts); st.success(f"'{nn}' 추가"); st.rerun()
                        else: st.warning("이미 있는 참가자")
                st.markdown("---")
                all_pairs=[(p,g) for g in groups for p in tour["groups"][g]["players"]]
                if all_pairs:
                    move_p=st.selectbox("이동할 참가자",[p for p,_ in all_pairs],key="mov_p")
                    cur_g=next((g for p,g in all_pairs if p==move_p),groups[0])
                    other_g=[g for g in groups if g!=cur_g]
                    if other_g:
                        tg=st.selectbox("이동할 그룹",other_g,key="mov_tg")
                        if st.button("🔄 이동",use_container_width=True,key="mov_b"):
                            tour["groups"][cur_g]["players"].remove(move_p)
                            tour["groups"][tg]["players"].append(move_p)
                            for grp in [cur_g,tg]:
                                md3=tour["groups"][grp]["mode"]; gc3=tour["groups"][grp].get("games",3)
                                if md3=="고정페어": nm3,_=make_fixed(tour["groups"][grp]["players"])
                                elif md3=="KDK":
                                    nm3,np4=make_kdk(tour["groups"][grp]["players"],gc3)
                                    if nm3: tour["groups"][grp]["player_with_number"]=np4
                                    else: nm3,_=make_singles(tour["groups"][grp]["players"])
                                else: nm3,_=make_singles(tour["groups"][grp]["players"])
                                tour["groups"][grp]["matches"]=nm3
                            save_tours(ts); st.success(f"'{move_p}'→{tg}"); st.rerun()
                    else: st.info("이동할 다른 그룹 없음")

    # ── 랭킹 관리 ──
    with adm[2]:
        st.markdown('<div class="sec">📁 엑셀/CSV 업로드</div>',unsafe_allow_html=True)
        up=st.file_uploader("파일",type=["xlsx","csv"],key="adm_rank_up",label_visibility="collapsed")
        st.caption("xlsx / csv 파일 지원")
        if up:
            try:
                du=pd.read_excel(up) if up.name.endswith("xlsx") else pd.read_csv(up,encoding_errors="replace")
                if "현재포인트" in du.columns:
                    du["현재포인트"]=pd.to_numeric(du["현재포인트"],errors="coerce").fillna(0)
                    du=du.sort_values("현재포인트",ascending=False).reset_index(drop=True)
                    du["랭킹"]=du.index+1
                st.dataframe(du,use_container_width=True)
                if st.button("💾 저장",type="primary",key="a2su"):
                    save_rank(du)
                    if "이름" in du.columns: save_members(du["이름"].tolist())
                    st.success("저장 완료!"); st.rerun()
            except Exception as e: st.error(f"오류: {e}")
        st.divider()
        st.markdown('<div class="sec">📊 현재 랭킹</div>',unsafe_allow_html=True)
        dc=load_rank()
        if not dc.empty:
            st.dataframe(dc,use_container_width=True)
            st.download_button("📥 다운로드",data=to_excel(dc),file_name=f"랭킹_{date.today()}.xlsx",key="a2dl")
        st.divider()
        st.markdown('<div class="sec">✏️ 직접 수정</div>',unsafe_allow_html=True)
        de=load_rank()
        if not de.empty:
            edited=st.data_editor(de,use_container_width=True,hide_index=True,num_rows="dynamic")
            if st.button("💾 저장",type="primary",key="a2se"):
                save_rank(edited); save_members(edited["이름"].tolist()); st.success("저장 완료!"); st.rerun()

    # ── 결과 반영 ──
    with adm[3]:
        ts=load_tours()
        act3=[k for k,v in ts.items() if v.get("status")=="진행중"]
        if not act3: st.warning("진행 중인 대회 없음"); st.stop()
        stid2=st.selectbox("대회 선택",act3,format_func=lambda k:ts[k]['title'],key="a3st")
        t3=ts[stid2]
        if not t3.get("groups"): st.warning("대진 없음"); st.stop()
        earn={}
        for g,gi in t3["groups"].items():
            mode2,ms2=gi["mode"],gi["matches"]; fx2=(mode2=="고정페어")
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
                save_rank(dr); ts[stid2]["status"]="완료"; save_tours(ts)
                st.success("✅ 반영 완료!"); st.rerun()
        with c2:
            if st.button("🗑 점수 초기화",use_container_width=True,key="a3rs"):
                for g in t3["groups"]:
                    for m in t3["groups"][g]["matches"]: m["s1"]=0; m["s2"]=0
                save_tours(ts); st.success("✅ 초기화!"); st.rerun()
