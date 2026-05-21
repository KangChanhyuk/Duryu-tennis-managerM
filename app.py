import streamlit as st
import pandas as pd
import random, os, json
from datetime import date
from io import BytesIO

st.set_page_config(page_title="두류 테니스", page_icon="🎾",
                   layout="centered", initial_sidebar_state="collapsed")

# ══════════════════════════════════════
# CSS (아이콘 및 탭 깨짐 현상 완벽 방지 보강)
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
  --r1:10px;--r2:16px;
  --sh:0 2px 10px rgba(0,0,0,.08);--sh2:0 4px 20px rgba(0,0,0,.13);
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent;}

/* 일반 요소에만 Noto Sans KR을 적용하고 Streamlit 아이콘 계열은 제외 */
html, body, [data-testid="stAppViewContainer"] :not(i):not(svg):not([class*="material-icons"]) {
    font-family: 'Noto Sans KR', sans-serif;
}

/* [arrow_right, chevron_down 해결] Streamlit 내장 아이콘 클래스의 폰트 패밀리를 절대 보호 */
[data-testid="stExpander"] [data-testid="stIconVisibility"],
[data-testid="stExpander"] svg,
[data-testid="stExpander"] span[class*="st-"],
span[data-testid="stIconVisibility"],
.st-emotion-cache-1f3w060,
.st-emotion-cache-p5msec,
i {
    font-family: 'Material Icons' !important;
    font-weight: normal !important;
    font-style: normal !important;
    text-transform: none !important;
    line-height: 1 !important;
}

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

/* 관리자 탭 한글/영어 자간 겹침 오류 수정 보강 */
button[data-baseweb="tab"]{
    font-size:.65rem!important;
    font-weight:700!important;
    padding:7px 6px!important;
    border-radius:var(--r1) var(--r1) 0 0!important;
    min-height:38px!important;
    white-space:nowrap!important;
    letter-spacing: 0px !important;
}
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

/* 그룹 개별 구분 카드 디자인 추가 */
.grp-card {
    background-color: #ffffff;
    border: 2px solid #388E3C;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# 데이터 구조 및 파일 입출력 정의
# ══════════════════════════════════════
RANK_FILE   = "ranking_master.csv"
MEMBER_FILE = "member_roster.json"
TOUR_FILE   = "tournaments.json"
CONFIG_FILE = "config.json"
COLS_RANK   = ["랭킹","이름","현재포인트","3월 포인트","결과","부과점","그룹","비고"]

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE,"r") as f: return json.load(f)
    return {"admin_pw":"0502"}

def save_config(cfg):
    with open(CONFIG_FILE,"w") as f: json.dump(cfg,f,ensure_ascii=False,indent=2)

def get_admin_pw():
    return load_config().get("admin_pw","0502")

GCLS  = ["mc0","mc1","mc2","mc3","mc4","mc5","mc6","mc7"]
TBCLS = ["tb0","tb1","tb2","tb3","tb4","tb5","tb6","tb7"]
GLBL  = ["🟢","🔵","🟠","🟣","🩵","🔴","🟡","⚪"]

# 1게임부터 유연하게 작동하도록 KDK 기본 룰 구조 연동 보장
KDK_1G = { 4: [(1,4,2,3)], 8: [(1,2,3,4),(5,6,7,8)] }
KDK_2G = { 4: [(1,4,2,3),(1,3,2,4)], 8: [(1,2,3,4),(5,6,7,8),(1,8,2,7),(3,6,4,5)] }
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
KDK_5G = KDK_4G # 5게임 선택 시 유연한 연동을 위한 대치

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
    if name.endswith(("xlsx","xls")): return pd.read_excel(up)
    return pd.read_csv(up,encoding_errors="replace")

def df_to_html(df):
    cols=df.columns.tolist()
    h="".join(f"<th>{c}</th>" for c in cols)
    body=""
    for _,row in df.iterrows():
        cells=""
        for val in row:
            if isinstance(val,float) and not pd.isna(val) and val==int(val): val=int(val)
            cells+=f"<td>{val}</td>"
        body+=f"<tr>{cells}</tr>"
    return f'<div class="mx-wrap"><table class="mx"><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table></div>'

# ══════════════════════════════════════
# 대진 및 전적 관리 로직
# ══════════════════════════════════════
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
    return 7 if rank<=2 else (5 if rank<=4 else (3 if rank<=6 else 1))

def grade(rank):
    return "🥇 우승" if rank<=2 else ("🥈 준우승" if rank<=4 else ("🥉 3위" if rank<=6 else "참가"))

def make_kdk(players,gperson):
    n=len(players)
    if gperson == 1: bp = KDK_1G.get(n) if KDK_1G.get(n) else KDK_3G.get(n)
    elif gperson == 2: bp = KDK_2G.get(n) if KDK_2G.get(n) else KDK_3G.get(n)
    elif gperson == 3: bp = KDK_3G.get(n)
    elif gperson == 5: bp = KDK_5G.get(n)
    else: bp = KDK_4G.get(n)
    
    if not bp: return [], {}
    sh=random.sample(players,n)
    n2p={i+1:sh[i] for i in range(n)}; p2n={sh[i]:i+1 for i in range(n)}
    ms=[{"t1":[n2p[a],n2p[b]],"t2":[n2p[c],n2p[d]],"s1":0,"s2":0} for a,b,c,d in bp]
    return ms,p2n

def make_fixed(players):
    n=len(players); pairs=[(players[i],players[n-1-i]) for i in range(n//2)]
    ms=[{"t1":list(pairs[i]),"t2":list(pairs[j]),"s1":0,"s2":0} for i in range(len(pairs)) for j in range(i+1,len(pairs))]
    random.shuffle(ms); return ms,{}

def make_singles(players):
    pl=players[:]; random.shuffle(pl)
    ms=[{"t1":[pl[i]],"t2":[pl[j]],"s1":0,"s2":0} for i in range(len(pl)) for j in range(i+1,len(pl))]
    random.shuffle(ms); return ms,{}

def build_matches(players,mode,gc):
    if not players or len(players) < 2: return [], {}
    if mode=="고정페어": return make_fixed(players)
    if mode=="KDK": return make_kdk(players,gc)
    return make_singles(players)

def kdk_html(n,gperson,p2n):
    if gperson == 1: bp = KDK_1G.get(n) if KDK_1G.get(n) else KDK_3G.get(n)
    elif gperson == 2: bp = KDK_2G.get(n) if KDK_2G.get(n) else KDK_3G.get(n)
    elif gperson == 3: bp = KDK_3G.get(n)
    elif gperson == 5: bp = KDK_5G.get(n)
    else: bp = KDK_4G.get(n)
    if not bp: return ""
    n2p={v:k for k,v in p2n.items()}; rows=""
    for i,(a,b,c,d) in enumerate(bp):
        t1=f"{n2p.get(a,a)}({a}) &amp; {n2p.get(b,b)}({b})"
        t2=f"{n2p.get(c,c)}({c}) &amp; {n2p.get(d,d)}({d})"
        rows+=f"<tr><td style='text-align:center'><span style='background:#1B5E20;color:#fff;border-radius:20px;padding:2px 8px;font-size:.58rem;font-weight:700'>{i+1}</span></td><td style='text-align:left'>{t1} vs {t2}</td></tr>"
    return f'<div class="kdk"><div style="font-size:.72rem;font-weight:800;color:#1B5E20;margin-bottom:5px">📋 KDK 1인 {gperson}게임 — {n}명</div><table><thead><tr><th>순서</th><th>대진</th></tr></thead><tbody>{rows}</tbody></table></div>'

def matrix_html(matches,rank_items,is_fixed,p2n):
    if not matches or not rank_items: return ""
    lab={t:" &amp; ".join(list(t)) for t in rank_items} if is_fixed else {p:f"{p}({p2n.get(p,'?')})" for p in rank_items}
    mat={lab[t]:{lab[o]:("■" if t==o else "—") for o in lab} for t in lab}
    for m in matches:
        a,b=int(m["s1"]),int(m["s2"])
        if a>0 or b>0:
            if is_fixed:
                k1,k2=tuple(m["t1"]),tuple(m["t2"])
                mat[lab[k1]][lab[k2]]=f"{a}:{b}";mat[lab[k2]][lab[k1]]=f"{b}:{a}"
            else:
                for x in m["t1"]:
                    for y in m["t2"]: mat[lab[x]][lab[y]]=f"{a}:{b}";mat[lab[y]][lab[x]]=f"{b}:{a}"
    keys=list(lab.values())
    header="".join(f"<th>{k}</th>" for k in keys)
    body=""
    for r in keys:
        cells="".join(f"<td class='mx-sc'>{mat[r][c]}</td>" if ":" in mat[r][c] else (f"<td class='mx-grey'>{mat[r][c]}</td>" if "■" in mat[r][c] else f"<td class='mx-dash'>{mat[r][c]}</td>") for c in keys)
        body+=f"<tr><td style='font-weight:700;background:#E8F5E9'>{r}</td>{cells}</tr>"
    return f'<div class="mx-wrap"><table class="mx"><thead><tr><th>구분</th>{header}</tr></thead><tbody>{body}</tbody></table></div>'

# ══════════════════════════════════════
# 세션 상태 변수 초기화
# ══════════════════════════════════════
ss=st.session_state
if "menu" not in ss: ss.menu="ranking"
if "is_admin" not in ss: ss.is_admin=False

# 헤더 렌더링
st.markdown("<div class='hdr'><div class='hdr-title'>두류 테니스 클럽</div><div class='hdr-sub'>DURYU TENNIS CLUB SYSTEM</div></div><div style='height:18px'></div>",unsafe_allow_html=True)

# 상단 모바일 최적화 메뉴바
m_cols=st.columns(5)
m_items=[("ranking","🏆 랭킹"),("schedule","📅 대진"),("result","🎾 결과"),("config","🛠️ 설정"),("admin","⚙️ 관리")]
for idx,(m_id,m_lb) in enumerate(m_items):
    with m_cols[idx]:
        if st.button(m_lb,key=f"m_btn_{m_id}",use_container_width=True,type="primary" if ss.menu==m_id else "secondary"):
            ss.menu=m_id; st.rerun()

# ══════════════════════════════════════════════════════
# 메뉴 1. 마스터 랭킹 보드
# ══════════════════════════════════════════════════════
if ss.menu=="ranking":
    st.markdown("<div class='pg-title c0'>🏆 마스터 랭킹 보드</div>",unsafe_allow_html=True)
    df=load_rank()
    if df.empty: st.markdown("<div class='ic'>📋 등록된 랭킹 데이터 파일이 비어 있습니다.</div>",unsafe_allow_html=True)
    else: st.markdown(df_to_html(df),unsafe_allow_html=True); st.download_button("Excel 다운로드",data=to_excel(df),file_name=f"랭킹_{date.today()}.xlsx",use_container_width=True)

# ══════════════════════════════════════════════════════
# 메뉴 2. 실시간 대진표 및 스코어 보드
# ══════════════════════════════════════════════════════
elif ss.menu=="schedule":
    tours=load_tours(); active=[k for k,v in tours.items() if v.get("status")=="진행중"]
    if not active: st.markdown("<div class='pg-title c1'>📅 대진표</div><div class='ic ic-b'>⚠️ 진행 중인 대회가 없습니다.</div>",unsafe_allow_html=True); st.stop()
    tid=active[-1]; tour=tours[tid]; gnames=list(tour.get("groups",{}).keys())
    st.markdown(f"<div class='pg-title c1'>📅 {tour['title']}</div>",unsafe_allow_html=True)
    st.markdown(f"<div class='ic ic-b'>📍 {tour.get('date','')} &nbsp;|&nbsp; {tour.get('place','')} &nbsp;|&nbsp; 코트 {tour.get('courts',2)}면</div>",unsafe_allow_html=True)
    if not gnames: st.markdown("<div class='ic ic-b'>ℹ️ 편성된 대진 그룹이 없습니다.</div>",unsafe_allow_html=True); st.stop()
    tabs=st.tabs([f"{GLBL[i%len(GLBL)]} {g}" for i,g in enumerate(gnames)])
    for ti,g in enumerate(gnames):
        with tabs[ti]:
            gi=tour["groups"][g]; ms=gi["matches"]; mode=gi["mode"]; p2n=gi.get("player_with_number",{})
            fx=(mode=="고정페어"); sv=stats_fixed(ms) if fx else stats_kdk(ms); rit=list(sv.keys())
            st.markdown("<div class='sec sec-b'>📋 전적 매트릭스</div>",unsafe_allow_html=True)
            st.markdown(matrix_html(ms,rit,fx,p2n),unsafe_allow_html=True)
            if not fx and p2n: st.markdown(kdk_html(len(p2n),gi.get("games",4),p2n),unsafe_allow_html=True)
            st.markdown("<div class='sec sec-b'>🏅 현재 그룹 순위</div>",unsafe_allow_html=True)
            if rit:
                ranked=sorted(rit,key=lambda x:(-sv[x]["승"],-sv[x]["득실"])); rows=[]
                for i,item in enumerate(ranked):
                    if fx: rows.append({"순위":i+1,"팀":" & ".join(list(item)),"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}'})
                    else: rows.append({"순위":i+1,"선수":item,"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"비고":grade(i+1)})
                st.markdown(df_to_html(pd.DataFrame(rows)),unsafe_allow_html=True)
            st.markdown("<div class='sec sec-b'>🎾 경기 스코어 입력</div>",unsafe_allow_html=True)
            for mi,m in enumerate(ms):
                t1s=" & ".join(m["t1"]); t2s=" & ".join(m["t2"])
                mc=GCLS[mi%len(GCLS)]; tbc=TBCLS[mi%len(TBCLS)]; s1v=int(m["s1"]); s2v=int(m["s2"])
                st.markdown(f'<div class="match-card"><span class="match-no {mc}">MATCH {mi+1}</span>',unsafe_allow_html=True)
                nA,nVS,nB=st.columns([5,1,5])
                with nA:
                    st.markdown(f'<div class="team-nm {tbc}">{t1s}</div>',unsafe_allow_html=True)
                with nVS:
                    st.markdown('<div style="height:40px;display:flex;align-items:center;justify-content:center;"><div class="vs-badge">VS</div></div>',unsafe_allow_html=True)
                with nB:
                    st.markdown(f'<div class="team-nm {tbc}">{t2s}</div>',unsafe_allow_html=True)
                st.markdown("<div style='height:8px'></div>",unsafe_allow_html=True)
                sc1,sc2=st.columns(2)
                with sc1:
                    c_id1,c_id2=f"ctrl_{g}_{mi}_1_dn",f"ctrl_{g}_{mi}_1_up"
                    st.markdown(f'<div class="ctrl-row" style="display:flex;gap:4px;align-items:center;">',unsafe_allow_html=True)
                    col_d,col_n,col_u = st.columns([1,2,1])
                    with col_d:
                        if st.button("➖",key=c_id1,use_container_width=True):
                            if s1v>0: ms[mi]["s1"]=s1v-1; save_tours(tours); st.rerun()
                    with col_n: st.markdown(f'<div class="ctrl-num">{s1v}</div>',unsafe_allow_html=True)
                    with col_u:
                        if st.button("➕",key=c_id2,use_container_width=True):
                            ms[mi]["s1"]=s1v+1; save_tours(tours); st.rerun()
                    st.markdown('</div>',unsafe_allow_html=True)
                with sc2:
                    c_id3,c_id4=f"ctrl_{g}_{mi}_2_dn",f"ctrl_{g}_{mi}_2_up"
                    st.markdown(f'<div class="ctrl-row" style="display:flex;gap:4px;align-items:center;">',unsafe_allow_html=True)
                    col_d,col_n,col_u = st.columns([1,2,1])
                    with col_d:
                        if st.button("➖",key=c_id3,use_container_width=True):
                            if s2v>0: ms[mi]["s2"]=s2v-1; save_tours(tours); st.rerun()
                    with col_n: st.markdown(f'<div class="ctrl-num">{s2v}</div>',unsafe_allow_html=True)
                    with col_u:
                        if st.button("➕",key=c_id4,use_container_width=True):
                            ms[mi]["s2"]=s2v+1; save_tours(tours); st.rerun()
                    st.markdown('</div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 메뉴 3. 최종 대회 결과 보고서
# ══════════════════════════════════════════════════════
elif ss.menu=="result":
    st.markdown("<div class='pg-title c2'>🎾 대회 종합 결과</div>",unsafe_allow_html=True)
    tours=load_tours(); t_done=[k for k,v in tours.items() if v.get("status")=="완료"]
    if not t_done: st.markdown("<div class='ic ic-o'>ℹ️ 마감 완료된 대회가 아직 존재하지 않습니다.</div>",unsafe_allow_html=True); st.stop()
    sel_tid=st.selectbox("🏆 지난 대회 아카이브 선택",t_done[::-1],format_func=lambda x: tours[x]["title"])
    tour=tours[sel_tid]
    st.markdown(f"<div class='ic ic-o'><b>🏆 {tour['title']} 공식 결과 보고서</b><br>📍 일자: {tour.get('date','')} | 장소: {tour.get('place','')}</div>",unsafe_allow_html=True)
    for g,gi in tour.get("groups",{}).items():
        ms=gi["matches"]; mode=gi["mode"]; fx=(mode=="고정페어"); sv=stats_fixed(ms) if fx else stats_kdk(ms); rit=list(sv.keys())
        if rit:
            ranked=sorted(rit,key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))
            st.markdown(f'<div class="sec sec-p">Group {g} ({mode})</div>',unsafe_allow_html=True)
            rows=[]
            for i,item in enumerate(ranked):
                pt=rank_pts(i+1,mode)
                if fx: rows.append({"순위":i+1,"팀":" & ".join(list(item)),"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"비고":grade(i+1)})
                else: rows.append({"순위":i+1,"선수":item,"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"비고":grade(i+1)})
            st.markdown(df_to_html(pd.DataFrame(rows)),unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 메뉴 4. 시스템 환경 설정 (비밀번호 가이드 설명 완벽히 숨김)
# ══════════════════════════════════════════════════════
elif ss.menu=="config":
    st.markdown("<div class='pg-title c3'>🛠️ 시스템 설정 및 관리</div>",unsafe_allow_html=True)
    st.markdown("<div class='sec sec-p'>🔒 관리자 비밀번호 변경</div>",unsafe_allow_html=True)
    old_pw=st.text_input("현재 비밀번호",type="password",key="cfg_old_pw")
    new_pw=st.text_input("새로운 비밀번호",type="password",key="cfg_new_pw")
    if st.button("💾 비밀번호 변경 적용",type="primary",use_container_width=True):
        if old_pw==get_admin_pw():
            if len(new_pw.strip())>=4: cfg=load_config(); cfg["admin_pw"]=new_pw.strip(); save_config(cfg); st.success("✅ 비밀번호가 수정되었습니다."); st.rerun()
            else: st.error("❌ 비밀번호는 공백 제외 최소 4자리 이상이어야 합니다.")
        else: st.error("❌ 현재 패스워드가 올바르지 않습니다.")
    st.divider()
    
    # 상단 설명 안내 문구 완전히 삭제 처리 (기능은 완벽 유지)
    init_pw=st.text_input("비밀번호 강제 초기화 (마스터 키)",type="password",key="cfg_init_pw")
    if st.button("🔄 시스템 암호 0502 초기화 실행",use_container_width=True):
        if init_pw=="duryu0502": cfg=load_config(); cfg["admin_pw"]="0502"; save_config(cfg); st.success("✅ 비밀번호가 '0502'로 완전히 초기화되었습니다."); st.rerun()
        else: st.error("❌ 마스터 암호키가 일치하지 않습니다.")

# ══════════════════════════════════════════════════════
# 메뉴 5. 관리자 제어 타워
# ══════════════════════════════════════════════════════
elif ss.menu=="admin":
    st.markdown("<div class='pg-title c4'>⚙️ 관리자 관제 센터</div>",unsafe_allow_html=True)
    pw=st.text_input("🔒 패스워드 인증",type="password",placeholder="암호코드 입력")
    if pw==get_admin_pw(): ss.is_admin=True
    if not ss.is_admin:
        if pw: st.error("❌ 패스워드가 올바르지 않습니다.")
        st.stop()
    adm=st.tabs(["📋 회원 명단","🏆 대회 관리","👥 참가자·그룹 자유 수정","💾 포인트 정산"])
    
    # 탭 [0] : 마스터 랭킹 및 텍스트 기반 명단 구성
    with adm[0]:
        st.markdown('<div class="sec sec-t">📝 전체 회원 명단 관리 (텍스트 등록)</div>',unsafe_allow_html=True)
        cur_m=load_members()
        txt_area=st.text_area("클럽 전체 회원 명단 (이름을 쉼표 또는 줄바꿈으로 구분해 적어주세요)", value=", ".join(cur_m), height=150)
        if st.button("💾 회원 명단 갱신 및 저장", type="primary", use_container_width=True):
            parsed=[n.strip() for n in txt_area.replace("\n",",").split(",") if n.strip()]
            save_members(parsed)
            rk_df=load_rank()
            for p in parsed:
                if rk_df.empty or p not in rk_df["이름"].values:
                    nr={c:"" for c in COLS_RANK}; nr["이름"]=p; nr["현재포인트"]=0
                    rk_df=pd.concat([rk_df,pd.DataFrame([nr])],ignore_index=True)
            save_rank(rk_df)
            st.success("✅ 회원 데이터 셋이 성공적으로 갱신되었습니다."); st.rerun()
        st.divider()
        st.markdown('<div class="sec sec-t">📥 엑셀(XLSX/CSV) 파일로 일괄 업로드 및 덮어쓰기</div>',unsafe_allow_html=True)
        up=st.file_uploader("랭킹 마스터 데이터 파일 선택",type=["csv","xlsx"])
        if up and st.button("🚀 마스터 랭킹 강제 파일 빌드 실행",use_container_width=True):
            try:
                ndf=read_file(up)
                for c in COLS_RANK:
                    if c not in ndf.columns: ndf[c]=""
                save_rank(ndf); st.success("✅ 마스터 파일 빌드 완료"); st.rerun()
            except Exception as e: st.error(f"오류: {e}")

    # 탭 [1] : 대회 생성 및 라이프 사이클 관리 (삭제 시 패스워드 재확인 컴포넌트 탑재)
    with adm[1]:
        st.markdown('<div class="sec sec-t">✨ 새로운 신규 대회 개설</div>',unsafe_allow_html=True)
        tn=st.text_input("🏆 대회 명칭 명명",value=f"{date.today().strftime('%m월 %d일')} 두류 정기전")
        td=st.date_input("📅 개최 일정 확정",date.today())
        tp=st.text_input("📍 경기 장소 지정",value="두류 테니스장")
        co=st.number_input("🎾 할당 코트 면적 수",1,20,value=3)
        g_count=st.selectbox("👥 최초 대진 구성 그룹 총 수",["1","2","3","4","5","6","7","8"],index=1)
        if st.button("🚀 새 대회 신설 공식 개막",use_container_width=True,type="primary"):
            if tn.strip():
                ts=load_tours(); t_key=f"{td}_{tn.strip()}"
                ng={f"{chr(65+i)}그룹":{"players":[],"mode":"KDK","games":4,"matches":[],"player_with_number":{},"size":8} for i in range(int(g_count))}
                ts[t_key]={"title":tn.strip(),"date":str(td),"place":tp,"courts":co,"status":"진행중","groups":ng,"players":[]}
                save_tours(ts); st.success(f"✅ 대회 '{tn.strip()}'가 생성되었습니다."); st.rerun()
            else: st.warning("대회 이름을 명확히 입력하십시오.")
        st.divider()
        ts=load_tours()
        if ts:
            st.markdown('<div class="sec sec-t">🔧 진행 상황 변경 및 대회 삭제</div>',unsafe_allow_html=True)
            sel_t=st.selectbox("제어 대상 대회 선별",list(ts.keys()),format_func=lambda k:f"[{ts[k].get('status',' 진행중')}] {ts[k]['title']}")
            curr_t=ts[sel_t]
            c5,c6=st.columns(2)
            with c5:
                s_opts=["진행중","완료","예정"]
                chg_s=st.selectbox("상태 변경",s_opts,index=s_opts.index(curr_t.get("status","진행중")))
                if st.button("💾 상태 저장",use_container_width=True):
                    curr_t["status"]=chg_s; save_tours(ts); st.success("변경 완료"); st.rerun()
            with c6:
                # 대회 삭제 전 비밀번호 검증 필드 필수 추가
                del_pw = st.text_input("⚠️ 삭제 확인 비밀번호", type="password", key="del_tour_pw_input", placeholder="관리자 패스워드 입력")
                if st.button("🗑️ 해당 대회 데이터 영구 삭제",type="primary",use_container_width=True):
                    if del_pw == get_admin_pw():
                        del ts[sel_t]; save_tours(ts); st.warning("대회가 삭제되었습니다."); st.rerun()
                    else:
                        st.error("❌ 삭제 비밀번호가 일치하지 않습니다.")

    # 탭 [2] : 당일 참가자 텍스트 등록 및 그룹 자유 편집 시스템 (카드형 테두리 분할 + 1게임부터 선택)
    with adm[2]:
        ts=load_tours(); act_tids=[k for k,v in ts.items() if v.get("status")=="진행중"]
        if not act_tids: st.info("현재 진행 중인 대회가 존재하지 않습니다."); st.stop()
        sel_tid=act_tids[-1]; tour=ts[sel_tid]; cg=tour["groups"]
        st.markdown(f"### 👥 {tour['title']} 당일 출전 명단 조율 파트")
        all_m=load_members()
        if not all_m: st.warning("회원 명단이 비어 있습니다. 1탭에서 회원 명단을 먼저 등록하세요."); st.stop()
        st.markdown("#### 1 단계: 당일 출전하는 전체 회원 체크")
        saved_p=tour.get("players", [])
        chosen_p=st.multiselect("오늘 경기 참가자 선택", options=all_m, default=[p for p in saved_p if p in all_m])
        if st.button("💾 당일 참가 명단 확정 보관", use_container_width=True, type="primary"):
            tour["players"]=chosen_p; save_tours(ts); st.success(f"당일 명단 {len(chosen_p)}명 저장 완료! 아래에서 그룹을 조율하세요.")
            st.divider()
            
        # 2 단계: 카드 테두리로 그룹을 가독성 있게 구분 및 인당 1게임부터 설정 가능 적용
        st.markdown("### 🔀 [2단계] 그룹 배정 현황 및 자유 수정")
        for gname, gdata in list(tour["groups"].items()):
            # HTML 구조를 사용해 깔끔한 컴포넌트 박스(테두리) 생성 시작
            st.markdown(f'<div class="grp-card">', unsafe_allow_html=True)
            st.markdown(f"#### 🏷️ **{gname} 설정**")
            c_m, c_g, c_z = st.columns(3)
            with c_m:
                m_opts=["KDK","고정페어","단식"]
                gdata["mode"] = st.selectbox(f"방식 ({gname})", m_opts, index=m_opts.index(gdata.get("mode","KDK")), key=f"md_edit_{gname}")
            with c_g: 
                # 인당 게임 수를 1게임부터 설정 가능하도록 배열 변경 완료
                gdata["games"] = st.selectbox(f"인당 게임 수 ({gname})", [1,2,3,4,5], index=[1,2,3,4,5].index(gdata.get("games",4)), key=f"gm_edit_{gname}")
            with c_z: 
                gdata["size"] = st.number_input(f"배정 정원 ({gname})", 2, 24, value=gdata.get("size",8), key=f"sz_edit_{gname}")
            cur_grp_players = gdata.get("players", [])
            grp_text_input = st.text_input(f"✍️ {gname} 소속 선수 명단 직접 편집 (쉼표로 구분)", value=", ".join(cur_grp_players), key=f"grp_txt_{gname}")
            updated_grp_p = [n.strip() for n in grp_text_input.split(",") if n.strip()]
            gdata["players"] = updated_grp_p
            st.markdown('</div>', unsafe_allow_html=True) # HTML 테두리 닫기
            
        if st.button("💾 모든 그룹 셋팅값 & 소속 선수 영구 백업", key="save_grp_configs_btn", type="primary", use_container_width=True):
            save_tours(ts); st.success("⚙️ 모든 그룹 설정과 배정 인원 데이터가 정상 보관되었습니다."); st.rerun()
        st.divider()
        st.markdown("### 🎲 [3단계] 최종 라운드 대진표 자동 빌드 트래커")
        if st.button("🔥 각 그룹별 설정에 맞춰 대진표 최종 자동 매칭 실행", use_container_width=True, type="primary"):
            for gn, gd in tour["groups"].items():
                pl = gd.get("players", [])
                m = gd.get("mode", "KDK")
                gp = gd.get("games", 4)
                if not pl: continue
                if m == "KDK":
                    ms, p2n = make_kdk(pl, gp)
                    if not ms:
                        st.error(f"❌ {gn}: KDK 인원 매칭 포맷 결크 ({len(pl)}명 에러) — {gp}게임 매칭 불가")
                        st.stop()
                    gd["matches"] = ms; gd["player_with_number"] = p2n
                elif m == "고정페어":
                    ms, p2n = make_fixed(pl)
                    gd["matches"] = ms; gd["player_with_number"] = p2n
                else:
                    ms, p2n = make_singles(pl)
                    gd["matches"] = ms; gd["player_with_number"] = p2n
            save_tours(ts); st.success("🎉 모든 그룹의 대진표가 완벽하게 빌드되었습니다! 대진 메뉴를 확인하세요.")

    # 탭 [3] : 당일 최종 스코어 기반 랭킹 포인트 결산 및 마감 처리
    with adm[3]:
        ts=load_tours(); act_tids=[k for k,v in ts.items() if v.get("status")=="진행중"]
        if not act_tids: st.warning("정산 대상 대회가 활성화되어 있지 않습니다."); st.stop()
        t_key=act_tids[-1]; t_obj=ts[t_key]
        earn={}
        for gname, gdata in t_obj.get("groups",{}).items():
            mode, ms = gdata["mode"], gdata["matches"]
            fx = (mode == "고정페어")
            sv = stats_fixed(ms) if fx else stats_kdk(ms)
            rit = list(sv.keys())
            if not rit: continue
            ranked = sorted(rit, key=lambda x: (-sv[x]["승"], -sv[x]["득실"]))
            for idx, p_item in enumerate(ranked):
                pts = rank_pts(idx+1, mode)
                if fx:
                    for individual in list(p_item): earn[individual] = earn.get(individual,0) + pts
                else: earn[p_item] = earn.get(p_item,0) + pts
        if earn:
            st.markdown('<div class="sec sec-t">🏆 금일 누적 획득 예정 포인트</div>',unsafe_allow_html=True)
            res_df = pd.DataFrame(sorted(earn.items(),key=lambda x:-x[1]),columns=["선수명","지급포인트"])
            st.markdown(df_to_html(res_df),unsafe_allow_html=True)
        c_fin, c_rst = st.columns(2)
        with c_fin:
            if st.button("🏆 계산된 포인트 마스터 랭킹에 영구 반영",type="primary",use_container_width=True):
                r_master = load_rank()
                for p, p_val in earn.items():
                    if p in r_master["이름"].values: r_master.loc[r_master["이름"]==p, "현재포인트"] += p_val
                    else:
                        new_r = {c:"" for c in COLS_RANK}; new_r["이름"]=p; new_r["현재포인트"]=p_val
                        r_master = pd.concat([r_master, pd.DataFrame([new_r])],ignore_index=True)
                save_rank(r_master); t_obj["status"]="완료"; save_tours(ts)
                st.success("🎉 금일 포인트 마스터 보드 반영 완료 및 대회 공식 종료 처리!"); st.rerun()
