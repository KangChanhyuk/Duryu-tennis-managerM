import streamlit as st
import pandas as pd
import random, os, json
from datetime import date
from io import BytesIO

st.set_page_config(page_title="두류 테니스", page_icon="🎾",
                   layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');
:root{
  --g0:#1B5E20;--g2:#388E3C;--g3:#66BB6A;--g5:#E8F5E9;
  --nav0:#2E7D32;--nav1:#1565C0;--nav2:#E65100;--nav3:#4A148C;--nav4:#00695C;
  --mc0:#1B5E20;--mc1:#0D47A1;--mc2:#BF360C;--mc3:#4A148C;
  --mc4:#006064;--mc5:#1A237E;--mc6:#880E4F;--mc7:#33691E;
  --tb0:#2E7D32;--tb1:#1565C0;--tb2:#D84315;--tb3:#6A1B9A;
  --tb4:#00695C;--tb5:#283593;--tb6:#AD1457;--tb7:#558B2F;
  --yel:#FFD600;--ora:#FB8C00;
  --bg:#F4F6F9;--card:#fff;--bd:#E0E4EA;
  --r1:10px;--r2:16px;
  --sh:0 2px 10px rgba(0,0,0,.08);--sh2:0 4px 20px rgba(0,0,0,.13);
}
*{font-family:'Noto Sans KR',sans-serif!important;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
.block-container{padding:0 0.6rem 5rem!important;max-width:520px!important;margin:0 auto!important;background:var(--bg)!important;}
.stApp{background:var(--bg)!important;}

/* 모바일 메뉴 여러 줄 배치 */
@media (max-width: 640px) {
  [data-testid="stHorizontalBlock"] {
    flex-wrap: wrap !important;
    gap: 6px !important;
  }
  [data-testid="stHorizontalBlock"] .stButton {
    flex: 1 0 auto !important;
    min-width: 70px !important;
  }
  .stButton button {
    font-size: 0.65rem !important;
    padding: 6px 4px !important;
    white-space: normal !important;
    word-break: keep-all !important;
  }
}

/* 헤더 */
.hdr{background:linear-gradient(135deg,#1B5E20 0%,#2E7D32 60%,#388E3C 100%);margin:0 -0.6rem 0;padding:13px 16px 0;position:relative;overflow:hidden;box-shadow:var(--sh2);}
.hdr::after{content:'🎾';position:absolute;right:12px;top:8px;font-size:2.4rem;opacity:.12;}
.hdr-title{color:#fff;font-size:1rem;font-weight:900;margin:0 0 2px;}
.hdr-sub{color:rgba(255,255,255,.5);font-size:.55rem;letter-spacing:2px;}

/* 페이지 타이틀 */
.pg-title{color:#fff;padding:11px 14px;border-radius:var(--r2);margin:0 0 12px;font-size:.95rem;font-weight:900;text-align:center;box-shadow:var(--sh2);}
.c0{background:linear-gradient(135deg,var(--nav0),#43A047);}
.c1{background:linear-gradient(135deg,var(--nav1),#1976D2);}
.c2{background:linear-gradient(135deg,var(--nav2),#F4511E);}
.c3{background:linear-gradient(135deg,var(--nav3),#7B1FA2);}
.c4{background:linear-gradient(135deg,var(--nav4),#00897B);}

/* 섹션 헤더 */
.sec{font-size:.82rem;font-weight:800;color:var(--g0);border-left:4px solid var(--g3);padding-left:8px;margin:14px 0 7px;}
.sec-b{color:var(--nav1);border-left-color:var(--nav1);}
.sec-o{color:var(--nav2);border-left-color:var(--nav2);}
.sec-p{color:var(--nav3);border-left-color:var(--nav3);}
.sec-t{color:var(--nav4);border-left-color:var(--nav4);}

/* 인포 카드 */
.ic{background:var(--card);border-left:4px solid var(--g3);border-radius:var(--r1);padding:9px 12px;margin:6px 0;box-shadow:var(--sh);font-size:.78rem;color:#3a3a5c;}
.ic-b{border-left-color:var(--nav1);}
.ic-o{border-left-color:var(--nav2);}
.ic-p{border-left-color:var(--nav3);}
.ic-t{border-left-color:var(--nav4);}

/* 탭 */
button[data-baseweb="tab"]{font-size:.65rem!important;font-weight:700!important;padding:7px 4px!important;border-radius:var(--r1) var(--r1) 0 0!important;min-height:38px!important;white-space:nowrap!important;}
button[data-baseweb="tab"][aria-selected="true"]{background:linear-gradient(135deg,var(--g0),var(--g2))!important;color:#fff!important;}
[data-baseweb="tab-list"]{background:#DDD!important;border-radius:var(--r1) var(--r1) 0 0!important;padding:3px 3px 0!important;gap:2px!important;flex-wrap:nowrap!important;overflow-x:auto!important;}

/* HTML 표 */
.mx-wrap{background:var(--card);border-radius:var(--r1);padding:8px;box-shadow:var(--sh);overflow-x:auto;margin:7px 0;border:1px solid var(--bd);}
.mx{border-collapse:collapse;white-space:nowrap;font-size:.7rem;width:100%;}
.mx th,.mx td{padding:7px 6px;border:1px solid var(--bd);text-align:center!important;vertical-align:middle!important;}
.mx thead th{background:var(--g0);color:#fff;font-weight:700;}
.mx tbody tr:nth-child(even) td{background:var(--g5);}
.mx-grey{background:#D0D0D0!important;color:#D0D0D0!important;}
.mx-dash{color:#CCC;}
.mx-sc{font-weight:800;color:var(--g0);}

/* KDK 표 */
.kdk{background:var(--card);border-radius:var(--r1);padding:8px;box-shadow:var(--sh);overflow-x:auto;margin:7px 0;border:1px solid var(--bd);}
.kdk table{border-collapse:collapse;white-space:nowrap;font-size:.64rem;width:100%;}
.kdk th,.kdk td{padding:5px 5px;border:1px solid var(--bd);text-align:center;vertical-align:middle;}
.kdk thead th{background:var(--g0);color:#fff;font-weight:700;}
.kdk td:first-child{width:50px;text-align:center;}
.kdk td:last-child{text-align:left;}

/* Streamlit 데이터프레임 */
div[data-testid="stDataFrame"]{border-radius:var(--r1)!important;overflow:hidden!important;box-shadow:var(--sh)!important;border:1px solid var(--bd)!important;}
div[data-testid="stDataFrame"] table{width:100%!important;font-size:.7rem!important;border-collapse:collapse!important;}
div[data-testid="stDataFrame"] table th,
div[data-testid="stDataFrame"] table td{text-align:center!important;vertical-align:middle!important;padding:7px 4px!important;white-space:nowrap;}
div[data-testid="stDataFrame"] thead tr th{background:var(--g0)!important;color:#fff!important;font-weight:700!important;}
div[data-testid="stDataFrame"] tbody tr:nth-child(even) td{background:var(--g5)!important;}

/* 경기 카드 */
.match-card{background:var(--card);border-radius:var(--r2);padding:10px 8px 12px;margin:10px 0;box-shadow:var(--sh2);border:1px solid var(--bd);}
.match-no{display:inline-block;border-radius:20px;padding:3px 12px;font-size:.58rem;font-weight:900;margin-bottom:8px;color:#fff;}
.mc0{background:var(--mc0);}.mc1{background:var(--mc1);}.mc2{background:var(--mc2);}
.mc3{background:var(--mc3);}.mc4{background:var(--mc4);}.mc5{background:var(--mc5);}
.mc6{background:var(--mc6);}.mc7{background:var(--mc7);}

.team-nm{border-radius:8px;padding:7px 3px;font-weight:900;font-size:clamp(.6rem,2.8vw,.85rem);text-align:center;color:#fff;box-shadow:var(--sh);min-height:40px;display:flex;align-items:center;justify-content:center;word-break:keep-all;line-height:1.2;}
.tb0{background:var(--tb0);}.tb1{background:var(--tb1);}.tb2{background:var(--tb2);}
.tb3{background:var(--tb3);}.tb4{background:var(--tb4);}.tb5{background:var(--tb5);}
.tb6{background:var(--tb6);}.tb7{background:var(--tb7);}

.vs-badge{width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,#FFB74D,#FB8C00);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:.52rem;color:#fff;box-shadow:var(--sh);margin:0 auto;}

.ctrl-num{display:flex;align-items:center;justify-content:center;background:#fff;border:2px solid #A5D6A7;border-radius:8px;font-size:clamp(1rem,5.5vw,1.5rem);font-weight:900;color:#1B5E20;height:42px;width:100%;}
.ctrl-row .stButton>button{height:42px!important;min-height:42px!important;max-height:42px!important;font-size:clamp(.9rem,4.5vw,1.3rem)!important;font-weight:900!important;padding:0!important;border-radius:8px!important;background:#E8F5E9!important;color:#1B5E20!important;border:2px solid #A5D6A7!important;box-shadow:none!important;width:100%!important;line-height:1!important;}
.ctrl-row .stButton>button:hover{background:#C8E6C9!important;}
.ctrl-row .stButton>button:active{background:#81C784!important;transform:scale(.93)!important;}

.stButton>button{border-radius:var(--r2)!important;font-weight:700!important;font-size:.8rem!important;min-height:48px!important;padding:9px 12px!important;}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,var(--g0),var(--g2))!important;color:#fff!important;border:none!important;box-shadow:0 4px 14px rgba(46,125,50,.35)!important;}

.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stSelectbox>div>div{min-height:46px!important;border-radius:var(--r1)!important;}

[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInstructions"]>div>span,
[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInstructions"]>div>small{display:none!important;}
[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"]::after{content:'📂 파일 선택 (xlsx/csv)';}
[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"] span{display:none!important;}
[data-testid="stFileUploaderDropzone"]{border:2px dashed var(--g3)!important;background:var(--g5)!important;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# 상수
# ══════════════════════════════════════
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

# ══════════════════════════════════════
# 헬퍼 함수
# ══════════════════════════════════════
def load_rank():
    if not os.path.exists(RANK_FILE): return pd.DataFrame(columns=COLS_RANK)
    df = pd.read_csv(RANK_FILE)
    for c in ["현재포인트","3월 포인트","부과점"]:
        if c in df.columns: df[c]=pd.to_numeric(df[c],errors="coerce").fillna(0)
    if "현재포인트" in df.columns:
        df=df.sort_values("현재포인트",ascending=False).reset_index(drop=True)
        df["랭킹"]=df.index+1
    return df.fillna("")

def save_rank(df):
    if "현재포인트" in df.columns:
        df=df.sort_values("현재포인트",ascending=False).reset_index(drop=True)
        df["랭킹"]=df.index+1
    df.to_csv(RANK_FILE,index=False)

def load_members():
    if os.path.exists(MEMBER_FILE):
        with open(MEMBER_FILE,"r") as f: return json.load(f)
    df=load_rank(); return df["이름"].tolist() if not df.empty else []

def save_members(names):
    with open(MEMBER_FILE,"w") as f: json.dump(names,f,ensure_ascii=False,indent=2)

def load_tours():
    if os.path.exists(TOUR_FILE):
        with open(TOUR_FILE,"r") as f: return json.load(f)
    return {}

def save_tours(d):
    with open(TOUR_FILE,"w") as f: json.dump(d,f,ensure_ascii=False,indent=2)

def to_excel(df):
    buf=BytesIO(); df.to_excel(buf,index=False); return buf.getvalue()

def read_file(up):
    name=up.name.lower()
    if name.endswith(("xlsx","xls")):
        return pd.read_excel(up)
    return pd.read_csv(up,encoding_errors="replace")

def df_to_html(df, medal_col=None):
    cols=df.columns.tolist()
    h="".join(f"<th>{c}</th>" for c in cols)
    body=""
    for i,(_,row) in enumerate(df.iterrows()):
        cells=""
        for j,val in enumerate(row):
            if isinstance(val,float) and not pd.isna(val) and val==int(val): val=int(val)
            cells+=f"<td>{val}</td>"
        body+=f"<tr>{cells}</tr>"
    return (f'<div class="mx-wrap"><table class="mx">'
            f'<thead><tr>{h}</tr></thead>'
            f'<tbody>{body}</tbody></table></div>')

def stats_fixed(matches):
    s={}
    for m in matches:
        t1,t2=tuple(m["t1"]),tuple(m["t2"])
        for t in (t1,t2):
            if t not in s: s[t]={"승":0,"패":0,"득실":0}
        a,b=int(m["s1"]),int(m["s2"])
        if a>b:   s[t1]["승"]+=1;s[t2]["패"]+=1
        elif b>a: s[t2]["승"]+=1;s[t1]["패"]+=1
        s[t1]["득실"]+=a-b;s[t2]["득실"]+=b-a
    return s

def stats_kdk(matches):
    s={}
    for m in matches:
        p1,p2=m["t1"],m["t2"]
        for p in p1+p2:
            if p not in s: s[p]={"승":0,"패":0,"득실":0}
        a,b=int(m["s1"]),int(m["s2"])
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
    n2p={i+1:sh[i] for i in range(n)}; p2n={sh[i]:i+1 for i in range(n)}
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

def build_matches(players,mode,gc):
    if mode=="고정페어": return make_fixed(players)
    if mode=="KDK":
        ms,pwn=make_kdk(players,gc)
        if ms: return ms,pwn
    return make_singles(players)

def kdk_html(n,gperson,p2n):
    bp=KDK_3G.get(n) if gperson==3 else KDK_4G.get(n)
    if not bp: return ""
    n2p={v:k for k,v in p2n.items()}; rows=""
    for i,(a,b,c,d) in enumerate(bp):
        t1=f"{n2p.get(a,a)}({a}) &amp; {n2p.get(b,b)}({b})"
        t2=f"{n2p.get(c,c)}({c}) &amp; {n2p.get(d,d)}({d})"
        rows+=f"<tr><td style='text-align:center'><span style='background:#1B5E20;color:#fff;border-radius:20px;padding:2px 8px;font-size:.58rem;font-weight:700'>{i+1}</span></td><td style='text-align:left'>{t1} vs {t2}</td></tr>"
    return (f'<div class="kdk"><div style="font-size:.72rem;font-weight:800;color:#1B5E20;margin-bottom:5px">'
            f'📋 KDK 1인 {gperson}게임 — {n}명</div>'
            f'<table><thead><tr><th>순서</th><th>대진</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')

def show_kdk(n,gperson,p2n): st.markdown(kdk_html(n,gperson,p2n),unsafe_allow_html=True)

def matrix_html(matches,rank_items,is_fixed,p2n):
    if not matches or not rank_items: return ""
    if is_fixed: lab={t:" &amp; ".join(list(t)) for t in rank_items}
    else:        lab={p:f"{p}({p2n.get(p,'?')})" for p in rank_items}
    mat={lab[t]:{lab[o]:("■" if t==o else "—") for o in lab} for t in lab}
    for m in matches:
        a,b=int(m["s1"]),int(m["s2"])
        if a>0 or b>0:
            if is_fixed:
                k1,k2=tuple(m["t1"]),tuple(m["t2"])
                mat[lab[k1]][lab[k2]]=f"{a}:{b}";mat[lab[k2]][lab[k1]]=f"{b}:{a}"
            else:
                for x in m["t1"]:
                    for y in m["t2"]:
                        mat[lab[x]][lab[y]]=f"{a}:{b}";mat[lab[y]][lab[x]]=f"{b}:{a}"
    keys=list(lab.values())
    header="".join(f"<th style='white-space:nowrap'>{k}</th>" for k in keys)
    body=""
    for rk in keys:
        body+=f"<tr><th style='white-space:nowrap'>{rk}</th>"
        for ck in keys:
            v=mat[rk][ck]
            if v=="■":   body+='<td class="mx-grey">■</td>'
            elif v=="—": body+='<td class="mx-dash">—</td>'
            else:        body+=f'<td class="mx-sc">{v}<tr>'
        body+="</tr>"
    return (f'<div class="mx-wrap"><table class="mx">'
            f'<thead><tr><th></th>{header}</tr></thead>'
            f'<tbody>{body}</tbody></table></div>')

def adj_score(tid,grp,mi,side,delta):
    tours=load_tours(); m=tours[tid]["groups"][grp]["matches"][mi]
    key="s1" if side=="A" else "s2"
    m[key]=max(0,int(m[key])+delta); save_tours(tours)

# ══════════════════════════════════════
# 세션
# ══════════════════════════════════════
ss=st.session_state
if "is_admin" not in ss: ss.is_admin=False
if "menu"     not in ss: ss.menu="ranking"
if "group_selections" not in ss: ss.group_selections = {}

# ══════════════════════════════════════
# 헤더 + 네비게이션
# ══════════════════════════════════════
MENUS=[("ranking","🏆","랭킹"),("schedule","📅","대진"),
       ("result","📊","결과"),("archive","📂","기록"),("admin","⚙️","관리")]
MENU_COLOR={"ranking":"#2E7D32","schedule":"#1565C0","result":"#E65100",
            "archive":"#4A148C","admin":"#00695C"}

st.markdown('<div class="hdr"><div class="hdr-title">🎾 두류 테니스 클럽</div>'
            '<div class="hdr-sub">DURYU TENNIS CLUB</div></div>',unsafe_allow_html=True)
nav_cols=st.columns(len(MENUS))
for col,(key,icon,label) in zip(nav_cols,MENUS):
    with col:
        if st.button(f"{icon}\n{label}",key=f"nav_{key}",use_container_width=True,
                     type="primary" if ss.menu==key else "secondary"):
            ss.menu=key; st.rerun()
cc=MENU_COLOR.get(ss.menu,"#2E7D32")
st.markdown(f'<div style="height:4px;background:{cc};margin:0 -0.6rem 12px;'
            f'box-shadow:0 2px 6px rgba(0,0,0,.18)"></div>',unsafe_allow_html=True)
M=ss.menu

# ══════════════════════════════════════════════════════
# 1. 랭킹
# ══════════════════════════════════════════════════════
if M=="ranking":
    st.markdown(f"<div class='pg-title c0'>🏆 두류 랭킹</div>",unsafe_allow_html=True)
    df=load_rank()
    if df.empty:
        st.markdown("<div class='ic'>📭 등록된 랭킹이 없습니다.<br>관리자 메뉴에서 엑셀을 업로드해 주세요.</div>",
                    unsafe_allow_html=True)
    else:
        medal=["🥇","🥈","🥉"]; d=df.copy()
        d.insert(0,"순위",[medal[i] if i<3 else str(i+1) for i in range(len(d))])
        st.markdown(df_to_html(d),unsafe_allow_html=True)
        st.download_button("📥 엑셀 다운로드",data=to_excel(df),
                           file_name=f"랭킹_{date.today()}.xlsx",use_container_width=True)

# ══════════════════════════════════════════════════════
# 2. 대진
# ══════════════════════════════════════════════════════
elif M=="schedule":
    tours=load_tours(); active=[k for k,v in tours.items() if v.get("status")=="진행중"]
    if not active:
        st.markdown("<div class='pg-title c1'>📅 대진표</div>",unsafe_allow_html=True)
        st.markdown("<div class='ic ic-b'>⚠️ 진행 중인 대회가 없습니다.</div>",unsafe_allow_html=True)
        st.stop()
    tid=active[-1]; tour=tours[tid]
    st.markdown(f"<div class='pg-title c1'>📅 {tour['title']}</div>",unsafe_allow_html=True)
    st.markdown(f"<div class='ic ic-b'>📍 {tour.get('date','')} &nbsp;|&nbsp; "
                f"{tour.get('place','')} &nbsp;|&nbsp; 코트 {tour.get('courts',2)}면</div>",
                unsafe_allow_html=True)
    gnames=list(tour["groups"].keys())
    if not gnames:
        st.markdown("<div class='ic ic-b'>ℹ️ 대진이 없습니다.</div>",unsafe_allow_html=True); st.stop()
    tabs=st.tabs([f"{GLBL[i%len(GLBL)]} {g}" for i,g in enumerate(gnames)])
    for ti,g in enumerate(gnames):
        with tabs[ti]:
            gi=tour["groups"][g]; ms=gi["matches"]
            mode=gi["mode"]; p2n=gi.get("player_with_number",{})
            fx=(mode=="고정페어")
            sv=stats_fixed(ms) if fx else stats_kdk(ms); rit=list(sv.keys())

            st.markdown("<div class='sec sec-b'>📋 전적 매트릭스</div>",unsafe_allow_html=True)
            st.markdown(matrix_html(ms,rit,fx,p2n),unsafe_allow_html=True)
            if not fx and p2n: st.divider();show_kdk(len(p2n),gi.get("games",3),p2n)
            st.divider()

            st.markdown("<div class='sec sec-b'>🏅 현재 순위</div>",unsafe_allow_html=True)
            if rit:
                ranked=sorted(rit,key=lambda x:(-sv[x]["승"],-sv[x]["득실"])); rows=[]
                for i,item in enumerate(ranked):
                    if fx: rows.append({"순위":i+1,"팀":" & ".join(list(item)),
                                        "승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}'})
                    else:  rows.append({"순위":i+1,"선수":item,"승":sv[item]["승"],"패":sv[item]["패"],
                                        "득실":f'{sv[item]["득실"]:+d}',"비고":grade(i+1)})
                st.markdown(df_to_html(pd.DataFrame(rows)),unsafe_allow_html=True)
            st.divider()

            st.markdown("<div class='sec sec-b'>🎾 경기 입력</div>",unsafe_allow_html=True)
            for mi,m in enumerate(ms):
                t1s=" & ".join(m["t1"]); t2s=" & ".join(m["t2"])
                mc=GCLS[mi%len(GCLS)]; tbc=TBCLS[mi%len(TBCLS)]
                s1v=int(m["s1"]); s2v=int(m["s2"])
                st.markdown(f'<div class="match-card"><span class="match-no {mc}">MATCH {mi+1}</span>',
                            unsafe_allow_html=True)
                nA,nVS,nB=st.columns([5,1,5])
                with nA: st.markdown(f'<div class="team-nm {tbc}">{t1s}</div>',unsafe_allow_html=True)
                with nVS: st.markdown('<div style="height:40px;display:flex;align-items:center;'
                                      'justify-content:center"><div class="vs-badge">VS</div></div>',
                                      unsafe_allow_html=True)
                with nB: st.markdown(f'<div class="team-nm {tbc}">{t2s}</div>',unsafe_allow_html=True)
                cAm,cAn,cAp,cG,cBm,cBn,cBp=st.columns([1.1,1.6,1.1,0.4,1.1,1.6,1.1])
                with cAm:
                    st.markdown('<div class="ctrl-row">',unsafe_allow_html=True)
                    st.button("－",key=f"dm_{tid}_{g}_{mi}_A",on_click=adj_score,args=(tid,g,mi,"A",-1),use_container_width=True)
                    st.markdown('</div>',unsafe_allow_html=True)
                with cAn: st.markdown(f'<div class="ctrl-num">{s1v}</div>',unsafe_allow_html=True)
                with cAp:
                    st.markdown('<div class="ctrl-row">',unsafe_allow_html=True)
                    st.button("＋",key=f"ip_{tid}_{g}_{mi}_A",on_click=adj_score,args=(tid,g,mi,"A",1),use_container_width=True)
                    st.markdown('</div>',unsafe_allow_html=True)
                with cG: st.markdown('<div style="height:42px"></div>',unsafe_allow_html=True)
                with cBm:
                    st.markdown('<div class="ctrl-row">',unsafe_allow_html=True)
                    st.button("－",key=f"dm_{tid}_{g}_{mi}_B",on_click=adj_score,args=(tid,g,mi,"B",-1),use_container_width=True)
                    st.markdown('</div>',unsafe_allow_html=True)
                with cBn: st.markdown(f'<div class="ctrl-num">{s2v}</div>',unsafe_allow_html=True)
                with cBp:
                    st.markdown('<div class="ctrl-row">',unsafe_allow_html=True)
                    st.button("＋",key=f"ip_{tid}_{g}_{mi}_B",on_click=adj_score,args=(tid,g,mi,"B",1),use_container_width=True)
                    st.markdown('</div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 3. 결과
# ══════════════════════════════════════════════════════
elif M=="result":
    tours=load_tours(); active=[k for k,v in tours.items() if v.get("status")=="진행중"]
    if not active:
        st.markdown("<div class='pg-title c2'>📊 경기 결과</div>",unsafe_allow_html=True)
        st.markdown("<div class='ic ic-o'>⚠️ 진행 중인 대회가 없습니다.</div>",unsafe_allow_html=True)
        st.stop()
    tid=active[-1]; tour=tours[tid]
    st.markdown(f"<div class='pg-title c2'>📊 {tour['title']}</div>",unsafe_allow_html=True)
    for g,gi in tour["groups"].items():
        mode,ms=gi["mode"],gi["matches"]; p2n=gi.get("player_with_number",{})
        fx=(mode=="고정페어"); sv=stats_fixed(ms) if fx else stats_kdk(ms)
        ranked=sorted(sv.keys(),key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))
        st.markdown(f'<div class="sec sec-o">Grp. {g} 최종 결과 ({mode})</div>',unsafe_allow_html=True)
        if not fx and p2n: show_kdk(len(p2n),gi.get("games",3),p2n);st.divider()
        rows=[]
        for i,item in enumerate(ranked):
            pt=rank_pts(i+1,mode)
            if fx: rows.append({"순위":i+1,"팀":" & ".join(list(item)),
                                 "승":sv[item]["승"],"패":sv[item]["패"],
                                 "득실":f'{sv[item]["득실"]:+d}',"포인트":pt,
                                 "등급":["🥇 우승","🥈 준우승","🥉 3위"][i] if i<3 else "참가"})
            else:  rows.append({"순위":i+1,"선수":item,"승":sv[item]["승"],"패":sv[item]["패"],
                                 "득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"비고":grade(i+1)})
        st.markdown(df_to_html(pd.DataFrame(rows)),unsafe_allow_html=True)
        with st.expander("📋 전체 경기 결과 보기"):
            mr=[{"경기":f"{' & '.join(m['t1'])} vs {' & '.join(m['t2'])}",
                 "결과":f"{m['s1']} : {m['s2']}"} for m in ms]
            st.markdown(df_to_html(pd.DataFrame(mr)),unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 4. 기록
# ══════════════════════════════════════════════════════
elif M=="archive":
    st.markdown("<div class='pg-title c3'>📂 대회 기록실</div>",unsafe_allow_html=True)
    tours=load_tours(); past={k:v for k,v in tours.items() if v.get("status")!="진행중"}
    if not past:
        st.markdown("<div class='ic ic-p'>📭 완료된 대회가 없습니다.</div>",unsafe_allow_html=True); st.stop()
    sel=st.selectbox("대회 선택",list(past.keys()),
                     format_func=lambda k:f"{past[k]['title']} ({past[k].get('date','')})")
    tour=past[sel]
    st.markdown(f"<div class='ic ic-p'>🏆 <strong>{tour['title']}</strong> &nbsp;|&nbsp; "
                f"{tour.get('date','')} &nbsp;|&nbsp; {tour.get('place','')}</div>",
                unsafe_allow_html=True)
    if not tour.get("groups"):
        st.markdown("<div class='ic ic-p'>ℹ️ 대진 정보가 없습니다.</div>",unsafe_allow_html=True); st.stop()
    for g,gi in tour["groups"].items():
        mode,ms=gi["mode"],gi["matches"]; p2n=gi.get("player_with_number",{})
        fx=(mode=="고정페어"); sv=stats_fixed(ms) if fx else stats_kdk(ms)
        ranked=sorted(sv.keys(),key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))
        st.markdown(f'<div class="sec sec-p">Grp. {g} ({mode})</div>',unsafe_allow_html=True)
        if not fx and p2n: show_kdk(len(p2n),gi.get("games",3),p2n);st.divider()
        rows=[]
        for i,item in enumerate(ranked):
            pt=rank_pts(i+1,mode)
            if fx: rows.append({"순위":i+1,"팀":" & ".join(list(item)),
                                 "승":sv[item]["승"],"패":sv[item]["패"],
                                 "득실":f'{sv[item]["득실"]:+d}',"포인트":pt,
                                 "등급":["🥇 우승","🥈 준우승","🥉 3위"][i] if i<3 else "참가"})
            else:  rows.append({"순위":i+1,"선수":item,"승":sv[item]["승"],"패":sv[item]["패"],
                                 "득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"비고":grade(i+1)})
        st.markdown(df_to_html(pd.DataFrame(rows)),unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 5. 관리자
# ══════════════════════════════════════════════════════
elif M=="admin":
    st.markdown("<div class='pg-title c4'>⚙️ 관리자 설정</div>",unsafe_allow_html=True)
    pw=st.text_input("🔒 관리자 비밀번호",type="password",placeholder="비밀번호 입력")
    if pw==ADMIN_PW: ss.is_admin=True
    if not ss.is_admin:
        if pw: st.error("❌ 비밀번호 오류")
        st.stop()
    st.markdown("<div class='ic ic-t'>🔓 관리자 인증 성공</div>",unsafe_allow_html=True)

    adm=st.tabs(["📋 랭킹·회원","🏆 대회 관리","👥 참가자·대진","💾 결과 반영"])

    # ── 탭 0: 랭킹·회원 ──
    with adm[0]:
        st.markdown('<div class="sec sec-t">📁 랭킹 마스터 업로드 (.xlsx / .xls / .csv)</div>',
                    unsafe_allow_html=True)
        up=st.file_uploader("파일 선택",type=["xlsx","xls","csv"],
                             key="adm_rank_up",label_visibility="collapsed")
        if up:
            try:
                du=read_file(up)
                if "현재포인트" in du.columns:
                    du["현재포인트"]=pd.to_numeric(du["현재포인트"],errors="coerce").fillna(0)
                    du=du.sort_values("현재포인트",ascending=False).reset_index(drop=True)
                    du["랭킹"]=du.index+1
                st.markdown(df_to_html(du),unsafe_allow_html=True)
                if st.button("💾 랭킹 저장",type="primary",key="a0_su",use_container_width=True):
                    save_rank(du)
                    if "이름" in du.columns: save_members(du["이름"].tolist())
                    st.success("✅ 저장 완료!"); st.rerun()
            except Exception as e: st.error(f"오류: {e}")
        st.divider()
        st.markdown('<div class="sec sec-t">📊 현재 랭킹</div>',unsafe_allow_html=True)
        dc=load_rank()
        if not dc.empty:
            medal=["🥇","🥈","🥉"]; dc2=dc.copy()
            dc2.insert(0,"순위",[medal[i] if i<3 else str(i+1) for i in range(len(dc2))])
            st.markdown(df_to_html(dc2),unsafe_allow_html=True)
            st.download_button("📥 엑셀 다운로드",data=to_excel(dc),
                               file_name=f"랭킹_{date.today()}.xlsx",key="a0_dl",use_container_width=True)
        st.divider()
        st.markdown('<div class="sec sec-t">✏️ 회원 명단 직접 편집</div>',unsafe_allow_html=True)
        de=load_rank()
        if not de.empty:
            edited=st.data_editor(de,use_container_width=True,hide_index=True,num_rows="dynamic")
            if st.button("💾 저장",type="primary",key="a0_se",use_container_width=True):
                save_rank(edited); save_members(edited["이름"].tolist())
                st.success("✅ 저장 완료!"); st.rerun()
        else:
            st.info("랭킹 데이터가 없습니다. 위에서 파일을 업로드하세요.")

    # ── 탭 1: 대회 관리 ──
    with adm[1]:
        st.markdown('<div class="sec sec-t">📅 새 대회 생성</div>',unsafe_allow_html=True)
        with st.form("f_new_tour"):
            tn=st.text_input("대회명",placeholder="예: 두류 6월 월례대회")
            c1,c2=st.columns(2)
            with c1: td=st.date_input("날짜",value=date.today())
            with c2: tp=st.text_input("장소",placeholder="예: 두류공원")
            c3,c4=st.columns(2)
            with c3: co=st.selectbox("코트 수",[1,2,3,4],index=1)
            with c4: gcnt_new=st.number_input("그룹 수",1,6,value=3)
            if st.form_submit_button("✅ 대회 생성",use_container_width=True,type="primary"):
                if tn.strip():
                    ts=load_tours(); tid2=f"{td}_{tn.strip()}"
                    if tid2 not in ts:
                        ng={}
                        for i in range(int(gcnt_new)):
                            gn=f"{chr(65+i)}그룹"
                            ng[gn]={"players":[],"mode":"KDK","games":4,"matches":[],"player_with_number":{},"size":8}
                        ts[tid2]={"title":tn.strip(),"date":str(td),"place":tp,
                                  "courts":co,"status":"진행중","groups":ng,"players":[]}
                        save_tours(ts); st.success(f"✅ '{tn.strip()}' 생성됨!"); st.rerun()
                    else: st.warning("이미 존재하는 대회입니다.")
                else: st.warning("대회명을 입력하세요.")

        st.divider()
        ts=load_tours()
        if not ts:
            st.info("생성된 대회가 없습니다."); st.stop()

        st.markdown('<div class="sec sec-t">🔧 대회 상세 설정</div>',unsafe_allow_html=True)
        all_tids=list(ts.keys())
        sel_t=st.selectbox("편집할 대회",all_tids,
                           format_func=lambda k:f"[{ts[k].get('status','')}] {ts[k]['title']} ({ts[k].get('date','')})",
                           key="adm1_sel")
        et=ts[sel_t]

        inner=st.tabs(["ℹ️ 기본정보","🎲 그룹·방식","📋 대진 미리보기"])
        with inner[0]:
            nt=st.text_input("대회명",value=et["title"],key="ei_t")
            c1,c2=st.columns(2)
            with c1:
                try:    dd=pd.to_datetime(et.get("date",str(date.today()))).date()
                except: dd=date.today()
                nd=st.date_input("날짜",value=dd,key="ei_d")
            with c2: np2=st.text_input("장소",value=et.get("place",""),key="ei_p")
            c3,c4=st.columns(2)
            with c3: nc=st.selectbox("코트 수",[1,2,3,4],index=max(0,et.get("courts",2)-1),key="ei_c")
            with c4:
                so=["진행중","완료","예정"]; cur=et.get("status","진행중")
                ns=st.selectbox("상태",so,index=so.index(cur) if cur in so else 0,key="ei_s")
            c5,c6=st.columns(2)
            with c5:
                if st.button("💾 기본정보 저장",type="primary",use_container_width=True,key="ei_save"):
                    et.update({"title":nt,"date":str(nd),"place":np2,"courts":nc,"status":ns})
                    save_tours(ts); st.success("저장됨!"); st.rerun()
            with c6:
                if st.button("🗑 대회 삭제",use_container_width=True,key="ei_del"):
                    del ts[sel_t]; save_tours(ts); st.warning("삭제됨!"); st.rerun()
        with inner[1]:
            cg=et.get("groups",{})
            st.caption("그룹 수를 변경하면 기존 대진이 초기화됩니다.")
            gcnt2=st.number_input("그룹 수",1,6,value=max(1,len(cg)),key="ei_gc")
            gnms=[f"{chr(65+i)}그룹" for i in range(int(gcnt2))]
            gcfg={}
            for i,gn in enumerate(gnms):
                ex=cg.get(gn,{})
                st.markdown(f"**{gn}**")
                g1,g2,g3,g4=st.columns(4)
                with g1:
                    default_sz=ex.get("size",8) if ex.get("size") else 8
                    sz=st.number_input("인원",2,30,value=default_sz,key=f"ei_sz_{sel_t}_{i}")
                with g2:
                    mdo=["KDK","고정페어","단식"]
                    default_md=ex.get("mode","KDK")
                    if default_md not in mdo: default_md="KDK"
                    md=st.selectbox("방식",mdo,index=mdo.index(default_md),key=f"ei_md_{sel_t}_{i}")
                with g3:
                    gco=[3,4,5]
                    default_gc=ex.get("games",4)
                    if default_gc not in gco: default_gc=4
                    gc=st.selectbox("게임수",gco,index=gco.index(default_gc),key=f"ei_gco_{sel_t}_{i}")
                with g4:
                    st.markdown(f"<div style='padding-top:28px;font-size:.75rem;color:#888'>"
                                f"{len(ex.get('players',[]))}명 배정됨</div>",unsafe_allow_html=True)
                gcfg[gn]=(sz,md,gc)
            tot=sum(v[0] for v in gcfg.values()); apl=et.get("players",[])
            if apl:
                if tot==len(apl): st.success(f"✅ 참가자 {len(apl)}명 ↔ 배정 {tot}명 일치")
                else:             st.warning(f"⚠️ 참가자 {len(apl)}명 / 필요 {tot}명 (차이 {len(apl)-tot:+d}명)")
            c_s,c_r=st.columns(2)
            with c_s:
                if st.button("💾 그룹 구성 저장",use_container_width=True,key="ei_gs"):
                    ng={}
                    for gn,(sz,md,gc) in gcfg.items():
                        old=cg.get(gn,{})
                        ng[gn]={"players":old.get("players",[]),
                                "mode":md,"games":gc,
                                "matches":old.get("matches",[]),
                                "player_with_number":old.get("player_with_number",{}),
                                "size":sz}
                    et["groups"]=ng; save_tours(ts); st.success("그룹 구성 저장됨!"); st.rerun()
            with c_r:
                if st.button("🎲 대진 재생성",type="primary",use_container_width=True,key="ei_regen"):
                    ptr=0; ng={}
                    for gn,(sz,md,gc) in gcfg.items():
                        gp=apl[ptr:ptr+sz]; ptr+=sz
                        if len(gp)<2: gp=gp+(apl[:max(0,sz-len(gp))])
                        ms2,pwn=build_matches(gp,md,gc)
                        ng[gn]={"players":gp,"mode":md,"games":gc,"matches":ms2,"player_with_number":pwn,"size":sz}
                    et["groups"]=ng; save_tours(ts)
                    st.success("✅ 대진 재생성 완료!"); st.rerun()
        with inner[2]:
            for g,gi in et.get("groups",{}).items():
                st.markdown(f"**{g}** ({gi['mode']}) — {len(gi['players'])}명")
                if gi.get("player_with_number"):
                    show_kdk(len(gi["player_with_number"]),gi.get("games",4),gi["player_with_number"])
                elif gi.get("matches"):
                    rows=[{"경기":f"MATCH {i+1}",
                           "팀A":" & ".join(m["t1"]),
                           "팀B":" & ".join(m["t2"])} for i,m in enumerate(gi["matches"])]
                    st.markdown(df_to_html(pd.DataFrame(rows)),unsafe_allow_html=True)
                else: st.caption("대진이 아직 없습니다.")

    # ── 탭 2: 참가자·대진 배정 ──
    with adm[2]:
        ts=load_tours(); act2=[k for k,v in ts.items() if v.get("status")=="진행중"]
        completed=[k for k,v in ts.items() if v.get("status")!="진행중"]
        all_editable=act2+completed
        if not all_editable: st.warning("대회가 없습니다."); st.stop()

        sel_tid=st.selectbox("대회 선택",all_editable,
                             format_func=lambda k:f"[{ts[k].get('status','')}] {ts[k]['title']}",
                             key="a2_sel")
        tour=ts[sel_tid]; cg=tour.get("groups",{})

        if not cg:
            st.warning("먼저 '대회 관리' 탭에서 그룹을 설정하세요."); st.stop()

        all_members=load_members()
        if not all_members:
            st.warning("회원 명단이 없습니다. '랭킹·회원' 탭에서 업로드하세요."); st.stop()

        # ── 전체 참가자 랭킹순 자동 배정 ──
        with st.expander("🏆 전체 참가자 랭킹순 자동 배정 (상위 랭커부터 A그룹 순)", expanded=False):
            st.markdown("아래에 쉼표로 구분된 전체 참가자 목록을 입력하면 **현재 랭킹 순서**로 각 그룹의 정해진 인원수만큼 자동 배정합니다.")
            default_text = ", ".join(all_members) if all_members else ""
            full_text = st.text_area("참가자 이름 (쉼표 구분)", value=default_text, height=100, key="full_assign_text")
            if st.button("랭킹순으로 그룹 자동 배정", use_container_width=True):
                names = [n.strip() for n in full_text.split(",") if n.strip()]
                if not names:
                    st.warning("참가자 목록을 입력하세요.")
                else:
                    seen = set()
                    unique_names = []
                    for n in names:
                        if n not in seen:
                            seen.add(n)
                            unique_names.append(n)
                    rank_df = load_rank()
                    rank_map = {row["이름"]: idx for idx, row in rank_df.iterrows()}
                    def sort_key(name):
                        if name in rank_map:
                            return (0, rank_map[name])
                        else:
                            return (1, name)
                    sorted_names = sorted(unique_names, key=sort_key)
                    group_sizes = []
                    group_names = list(cg.keys())
                    for gn in group_names:
                        size = cg[gn].get("size", 8)
                        group_sizes.append(size)
                    total_needed = sum(group_sizes)
                    if len(sorted_names) < total_needed:
                        st.warning(f"참가자 수({len(sorted_names)})가 필요한 총 인원({total_needed})보다 적습니다. 부족한 인원은 기존 멤버에서 채우지 않습니다.")
                    idx = 0
                    new_group_players = {}
                    for i, gn in enumerate(group_names):
                        needed = group_sizes[i]
                        assigned = sorted_names[idx:idx+needed]
                        new_group_players[gn] = assigned
                        idx += needed
                    for gn, players in new_group_players.items():
                        if players:
                            tour["groups"][gn]["players"] = players
                            mode = tour["groups"][gn]["mode"]
                            games = tour["groups"][gn].get("games", 4)
                            new_matches, pwn = build_matches(players, mode, games)
                            tour["groups"][gn]["matches"] = new_matches
                            tour["groups"][gn]["player_with_number"] = pwn
                    all_players = []
                    for gn in tour["groups"]:
                        all_players.extend(tour["groups"][gn]["players"])
                    tour["players"] = all_players
                    save_tours(ts)
                    st.success("✅ 랭킹순 자동 배정 완료! 아래에서 그룹별로 세부 조정할 수 있습니다.")
                    st.rerun()
        st.divider()

        # ── 그룹별 수동 배정 (전체선택/해제, 텍스트 일괄 입력) ──
        st.markdown('<div class="sec sec-t">👥 그룹별 참가자 배정 (수동 조정)</div>', unsafe_allow_html=True)

        for gn, gi in cg.items():
            cur_in = tour["groups"][gn].get("players", [])
            other_players = set()
            for og in cg.keys():
                if og != gn:
                    other_players.update(tour["groups"][og].get("players", []))
            selectable = [m for m in all_members if m not in other_players or m in cur_in]

            key = f"sel_{sel_tid}_{gn}"
            if key not in ss:
                ss[key] = cur_in

            selected = st.multiselect(
                f"{gn} 참가자",
                options=selectable,
                default=ss[key],
                key=f"ms_{sel_tid}_{gn}"
            )
            if selected != ss[key]:
                ss[key] = selected
                st.rerun()

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"전체선택", key=f"select_all_{sel_tid}_{gn}", use_container_width=True):
                    ss[key] = selectable.copy()
                    st.rerun()
            with col2:
                if st.button(f"전체해제", key=f"clear_all_{sel_tid}_{gn}", use_container_width=True):
                    ss[key] = []
                    st.rerun()

            with st.expander(f"텍스트로 일괄 설정 (쉼표 구분)"):
                text_input = st.text_area("참가자 이름 (쉼표로 구분)", key=f"batch_text_{sel_tid}_{gn}")
                if st.button(f"설정", key=f"batch_set_{sel_tid}_{gn}"):
                    names = [n.strip() for n in text_input.split(",") if n.strip()]
                    if not names:
                        st.warning("이름을 입력하세요.")
                    elif len(names) != len(set(names)):
                        st.error("같은 그룹 내 중복된 이름이 있습니다.")
                    else:
                        other_players = []
                        for other_gn, other_gi in tour["groups"].items():
                            if other_gn != gn:
                                other_players.extend(other_gi.get("players", []))
                        duplicates = [n for n in names if n in other_players]
                        if duplicates:
                            st.warning(f"다른 그룹에 이미 있는 이름: {', '.join(duplicates)}")
                        else:
                            tour["groups"][gn]["players"] = names
                            mode = tour["groups"][gn]["mode"]
                            games = tour["groups"][gn].get("games", 4)
                            new_matches, pwn = build_matches(names, mode, games)
                            tour["groups"][gn]["matches"] = new_matches
                            tour["groups"][gn]["player_with_number"] = pwn
                            all_players = []
                            for g in tour["groups"]:
                                all_players.extend(tour["groups"][g]["players"])
                            tour["players"] = all_players
                            save_tours(ts)
                            st.success(f"{gn} 참가자 설정 및 대진 재생성 완료!")
                            st.rerun()

        total = sum(len(tour["groups"][gn].get("players", [])) for gn in cg.keys())
        st.markdown(f"<div class='ic ic-t'>총 배정: {total}명</div>", unsafe_allow_html=True)

        col_save, col_gen = st.columns(2)
        with col_save:
            if st.button("배정만 저장", use_container_width=True, key="a2_save"):
                for gn in cg.keys():
                    key = f"sel_{sel_tid}_{gn}"
                    if key in ss:
                        tour["groups"][gn]["players"] = ss[key]
                all_sel = [p for gn in cg.keys() for p in tour["groups"][gn]["players"]]
                tour["players"] = all_sel
                save_tours(ts)
                st.success("✅ 참가자 배정 저장됨!")
                st.rerun()
        with col_gen:
            if st.button("배정+대진 생성", type="primary", use_container_width=True, key="a2_gen"):
                all_sel = []
                for gn in cg.keys():
                    key = f"sel_{sel_tid}_{gn}"
                    if key in ss:
                        players = ss[key]
                        all_sel.extend(players)
                    else:
                        players = tour["groups"][gn].get("players", [])
                        all_sel.extend(players)
                if len(set(all_sel)) != len(all_sel):
                    st.error("중복 선수 있음!")
                    st.stop()
                ng = {}
                for gn in cg.keys():
                    key = f"sel_{sel_tid}_{gn}"
                    if key in ss:
                        players = ss[key]
                    else:
                        players = tour["groups"][gn].get("players", [])
                    gi = cg[gn]
                    md = gi["mode"]
                    gc = gi.get("games", 4)
                    if len(players) < 2:
                        st.warning(f"{gn}: 인원 부족 ({len(players)}명)")
                        continue
                    ms2, pwn = build_matches(players, md, gc)
                    ng[gn] = {"players": players, "mode": md, "games": gc, "matches": ms2, "player_with_number": pwn, "size": gi.get("size", 8)}
                tour["groups"] = ng
                tour["players"] = all_sel
                save_tours(ts)
                st.success("✅ 대진 생성 완료! '대진' 메뉴에서 확인하세요.")
                st.rerun()

        st.divider()
        st.markdown('<div class="sec sec-t">✏️ 개별 참가자 수정 (대진 유지)</div>', unsafe_allow_html=True)
        groups = list(cg.keys())
        if groups:
            sel_g = st.selectbox("그룹 선택", groups, key="a2_eg")
            cur_players = tour["groups"][sel_g]["players"].copy()
            st.markdown(f"**현재 {sel_g}:** {', '.join(cur_players) if cur_players else '없음'}")
            if cur_players:
                sel_p = st.selectbox("삭제할 참가자", cur_players, key="a2_dp")
                if st.button("삭제", use_container_width=True, key="a2_db"):
                    tour["groups"][sel_g]["players"].remove(sel_p)
                    tour["groups"][sel_g]["matches"] = [m for m in tour["groups"][sel_g]["matches"]
                                                         if sel_p not in m["t1"] and sel_p not in m["t2"]]
                    if sel_p not in [p for g in groups for p in tour["groups"][g]["players"]]:
                        if sel_p in tour.get("players", []):
                            tour["players"].remove(sel_p)
                    save_tours(ts)
                    st.success(f"'{sel_p}' 삭제됨")
                    st.rerun()
            st.markdown("---")
            nn = st.text_input("새 참가자", placeholder="예: 홍길동", key="a2_an")
            if st.button("추가", use_container_width=True, key="a2_ab"):
                if nn and nn.strip():
                    n2 = nn.strip()
                    if n2 not in tour["groups"][sel_g]["players"]:
                        tour["groups"][sel_g]["players"].append(n2)
                        if n2 not in tour.get("players", []):
                            tour.setdefault("players", []).append(n2)
                        md2 = tour["groups"][sel_g]["mode"]
                        gc2 = tour["groups"][sel_g].get("games", 4)
                        ms2, pwn2 = build_matches(tour["groups"][sel_g]["players"], md2, gc2)
                        tour["groups"][sel_g]["matches"] = ms2
                        if pwn2:
                            tour["groups"][sel_g]["player_with_number"] = pwn2
                        save_tours(ts)
                        st.success(f"'{n2}' 추가됨")
                        st.rerun()
                    else:
                        st.warning("이미 있는 참가자입니다.")
            st.markdown("---")
            all_pairs = [(p, g) for g in groups for p in tour["groups"][g]["players"]]
            if all_pairs:
                move_p = st.selectbox("이동할 참가자", [p for p, _ in all_pairs], key="a2_mp")
                cur_g2 = next((g for p, g in all_pairs if p == move_p), groups[0])
                other_g = [g for g in groups if g != cur_g2]
                if other_g:
                    tgt = st.selectbox("이동할 그룹", other_g, key="a2_tg")
                    if st.button("이동", use_container_width=True, key="a2_mb"):
                        tour["groups"][cur_g2]["players"].remove(move_p)
                        tour["groups"][tgt]["players"].append(move_p)
                        for grp in [cur_g2, tgt]:
                            md3 = tour["groups"][grp]["mode"]
                            gc3 = tour["groups"][grp].get("games", 4)
                            ms3, pwn3 = build_matches(tour["groups"][grp]["players"], md3, gc3)
                            tour["groups"][grp]["matches"] = ms3
                            if pwn3:
                                tour["groups"][grp]["player_with_number"] = pwn3
                        save_tours(ts)
                        st.success(f"'{move_p}' → {tgt} 이동됨")
                        st.rerun()

    # ── 탭 3: 결과 반영 ──
    with adm[3]:
        ts=load_tours(); act3=[k for k,v in ts.items() if v.get("status")=="진행중"]
        if not act3: st.warning("진행 중인 대회가 없습니다."); st.stop()
        stid2=st.selectbox("대회 선택",act3,format_func=lambda k:ts[k]['title'],key="a3_sel")
        t3=ts[stid2]
        if not t3.get("groups"): st.warning("대진 정보가 없습니다."); st.stop()

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
            st.markdown('<div class="sec sec-t">🏅 획득 포인트 미리보기</div>',unsafe_allow_html=True)
            ef=pd.DataFrame(sorted(earn.items(),key=lambda x:-x[1]),columns=["선수","획득포인트"])
            st.markdown(df_to_html(ef),unsafe_allow_html=True)

        c1,c2=st.columns(2)
        with c1:
            if st.button("🏆 랭킹 반영",type="primary",use_container_width=True,key="a3_ap"):
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
                st.success("✅ 랭킹 반영 완료!"); st.rerun()
        with c2:
            if st.button("🗑 점수 초기화",use_container_width=True,key="a3_rs"):
                for g in t3["groups"]:
                    for m in t3["groups"][g]["matches"]: m["s1"]=0; m["s2"]=0
                save_tours(ts); st.success("✅ 점수 초기화 완료!"); st.rerun()
