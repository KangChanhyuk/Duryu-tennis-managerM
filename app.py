import streamlit as st
import pandas as pd
import random, os, json
from datetime import date
from io import BytesIO

st.set_page_config(page_title="두류 테니스", page_icon="🎾",
                   layout="centered", initial_sidebar_state="collapsed")

# ══════════════════════════════════════
# CSS (아이콘 깨짐 현상 완벽 방지 및 스타일 보강)
# ══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght=400;500;700;900&display=swap');
:root{
  --g0:#1B5E20;--g2:#388E3C;--g3:#66BB6A;--g5:#E8F5E9;
  --nav0:#2E7D32;--nav1:#1565C0;--nav2:#E65100;--nav3:#4A148C;--nav4:#00695C;
  --bg:#F4F6F9;--card:#fff;--bd:#E0E4EA;
  --r1:10px;--r2:16px;
  --sh:0 2px 10px rgba(0,0,0,.08);--sh2:0 4px 20px rgba(0,0,0,.13);
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent;}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Noto Sans KR', sans-serif !important;
}

[data-testid="stIconVisibility"], 
svg, 
i, 
[class*="material-icons"],
[class*="st-key-"] span {
    font-family: inherit !important;
}

.block-container{padding:0 0.6rem 5rem!important;max-width:520px!important;margin:0 auto!important;background:var(--bg)!important;}
.stApp{background:var(--bg)!important;}

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

.hdr{background:linear-gradient(135deg,#1B5E20 0%,#2E7D32 60%,#388E3C 100%);margin:0 -0.6rem 0;padding:13px 16px 0;position:relative;overflow:hidden;box-shadow:var(--sh2);}
.hdr::after{content:'🎾';position:absolute;right:12px;top:8px;font-size:2.4rem;opacity:.12;}
.hdr-title{color:#fff;font-size:1rem;font-weight:900;margin:0 0 2px;}
.hdr-sub{color:rgba(255,255,255,.5);font-size:.55rem;letter-spacing:2px;}

.pg-title{color:#fff;padding:11px 14px;border-radius:var(--r2);margin:0 0 12px;font-size:.95rem;font-weight:900;text-align:center;box-shadow:var(--sh2);}
.c0{background:linear-gradient(135deg,var(--nav0),#43A047);}
.c1{background:linear-gradient(135deg,var(--nav1),#1976D2);}
.c2{background:linear-gradient(135deg,var(--nav2),#F4511E);}
.c3{background:linear-gradient(135deg,var(--nav3),#7B1FA2);}
.c4{background:linear-gradient(135deg,var(--nav4),#00897B);}

.sec{font-size:.82rem;font-weight:800;color:var(--g0);border-left:4px solid var(--g3);padding-left:8px;margin:14px 0 7px;}
.sec-b{color:var(--nav1);border-left-color:var(--nav1);}
.sec-o{color:var(--nav2);border-left-color:var(--nav2);}
.sec-p{color:var(--nav3);border-left-color:var(--nav3);}
.sec-t{color:var(--nav4);border-left-color:var(--nav4);}

.ic{background:var(--card);border-left:4px solid var(--g3);border-radius:var(--r1);padding:9px 12px;margin:6px 0;box-shadow:var(--sh);font-size:.78rem;color:#3a3a5c;}
.ic-b{border-left-color:var(--nav1);}
.ic-o{border-left-color:var(--nav2);}
.ic-p{border-left-color:var(--nav3);}
.ic-t{border-left-color:var(--nav4);}

button[data-baseweb="tab"]{font-size:.65rem!important;font-weight:700!important;padding:7px 4px!important;border-radius:var(--r1) var(--r1) 0 0!important;min-height:38px!important;white-space:nowrap!important;}
button[data-baseweb="tab"][aria-selected="true"]{background:linear-gradient(135deg,var(--g0),var(--g2))!important;color:#fff!important;}
[data-baseweb="tab-list"]{background:#DDD!important;border-radius:var(--r1) var(--r1) 0 0!important;padding:3px 3px 0!important;gap:2px!important;flex-wrap:nowrap!important;overflow-x:auto!important;}

.mx-wrap{background:var(--card);border-radius:var(--r1);padding:8px;box-shadow:var(--sh);overflow-x:auto;margin:7px 0;border:1px solid var(--bd);}
.mx{border-collapse:collapse;white-space:nowrap;font-size:.7rem;width:100%;}
.mx th,.mx td{padding:7px 6px;border:1px solid var(--bd);text-align:center!important;vertical-align:middle!important;}
.mx thead th{background:var(--g0);color:#fff;font-weight:700;}
.mx tbody tr:nth-child(even) td{background:var(--g5);}
.mx-grey{background:#D0D0D0!important;color:#D0D0D0!important;}
.mx-dash{color:#CCC;}
.mx-sc{font-weight:800;color:var(--g0);}

.kdk{background:var(--card);border-radius:var(--r1);padding:8px;box-shadow:var(--sh);overflow-x:auto;margin:7px 0;border:1px solid var(--bd);}
.kdk table{border-collapse:collapse;white-space:nowrap;font-size:.64rem;width:100%;}
.kdk th,.kdk td{padding:5px 5px;border:1px solid var(--bd);text-align:center;vertical-align:middle;}
.kdk thead th{background:var(--g0);color:#fff;font-weight:700;}
.kdk td:first-child{width:50px;text-align:center;}
.kdk td:last-child{text-align:left;}

.match-card{background:var(--card);border-radius:var(--r2);padding:12px 10px;margin:12px 0;box-shadow:var(--sh2);border:1px solid var(--bd);}
.m-color-0 { border-top: 5px solid #2E7D32; }
.m-color-1 { border-top: 5px solid #1565C0; }
.m-color-2 { border-top: 5px solid #E65100; }
.m-color-3 { border-top: 5px solid #4A148C; }
.m-color-4 { border-top: 5px solid #00695C; }
.m-color-5 { border-top: 5px solid #C62828; }
.m-color-6 { border-top: 5px solid #0277BD; }
.m-color-7 { border-top: 5px solid #EF6C00; }

.match-no{display:inline-block;border-radius:20px;padding:3px 12px;font-size:.6rem;font-weight:900;margin-bottom:8px;color:#fff;}
.mc0{background:#2E7D32;}.mc1{background:#1565C0;}.mc2{background:#E65100;}
.mc3{background:#4A148C;}.mc4{background:#00695C;}.mc5{background:#C62828;}
.mc6{background:#0277BD;}.mc7{background:#EF6C00;}

.team-nm{border-radius:8px;padding:7px 3px;font-weight:900;font-size:clamp(.6rem,2.8vw,.85rem);text-align:center;color:#fff;box-shadow:var(--sh);min-height:40px;display:flex;align-items:center;justify-content:center;word-break:keep-all;line-height:1.2;}
.tb0{background:linear-gradient(135deg, #2E7D32, #4CAF50);}
.tb1{background:linear-gradient(135deg, #1565C0, #2196F3);}
.tb2{background:linear-gradient(135deg, #E65100, #FF8F00);}
.tb3{background:linear-gradient(135deg, #4A148C, #9C27B0);}
.tb4{background:linear-gradient(135deg, #00695C, #009688);}
.tb5{background:linear-gradient(135deg, #C62828, #E53935);}
.tb6{background:linear-gradient(135deg, #0277BD, #039BE5);}
.tb7{background:linear-gradient(135deg, #EF6C00, #F57C00);}

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
# 데이터 구조 및 파일 입출력 정의
# ══════════════════════════════════════
RANK_FILE   = "ranking_master.csv"
MEMBER_FILE = "member_roster.json"
TOUR_FILE   = "tournaments.json"
ADMIN_PW    = "0502"
COLS_RANK   = ["랭킹","이름","현재포인트","3월 포인트","결과","부과점","그룹","비고"]

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

def safe_parse_team(team_data):
    if isinstance(team_data, list):
        return [str(p) for p in team_data if p]
    if isinstance(team_data, (str, int, float)):
        if pd.isna(team_data) or team_data == "": return []
        return [str(team_data)]
    return []

def stats_fixed(matches):
    s={}
    for m in matches:
        t1 = tuple(safe_parse_team(m.get("t1", [])))
        t2 = tuple(safe_parse_team(m.get("t2", [])))
        if not t1 or not t2: continue
        for t in (t1,t2):
            if t not in s: s[t]={"승":0,"패":0,"득실":0}
        a,b=int(m.get("s1", 0)),int(m.get("s2", 0))
        if a>b:   s[t1]["승"]+=1;s[t2]["패"]+=1
        elif b>a: s[t2]["승"]+=1;s[t1]["패"]+=1
        s[t1]["득실"]+=a-b;s[t2]["득실"]+=b-a
    return s

def stats_kdk(matches):
    s={}
    for m in matches:
        p1 = safe_parse_team(m.get("t1", []))
        p2 = safe_parse_team(m.get("t2", []))
        for p in p1+p2:
            if p not in s: s[p]={"승":0,"패":0,"득실":0}
        a,b=int(m.get("s1", 0)),int(m.get("s2", 0))
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
    if mode in ["고정페어", "단식"]: return {1:7,2:5,3:3}.get(rank,1)
    return 7 if rank<=2 else (5 if rank<=4 else (3 if rank<=6 else 1))

def grade(rank):
    return "🥇 우승" if rank<=2 else ("🥈 준우승" if rank<=4 else ("🥉 3위" if rank<=6 else "참가"))

def make_kdk(players,gperson):
    n=len(players); bp=KDK_3G.get(n) if gperson==3 else KDK_4G.get(n)
    if not bp: return [], {}
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
    ms=[{"t1":[pl[i]],"t2":[pl[j]],"s1":0,"s2":0} for i in range(len(pl)) for j in range(i+1,len(pl))]
    random.shuffle(ms); return ms,{}

def build_matches(players,mode,gc):
    if not players or len(players) < 2: return [], {}
    if mode=="고정페어": return make_fixed(players)
    if mode in ["단식", "싱글"]: return make_singles(players)
    return make_kdk(players,gc)

def kdk_html(n,gperson,p2n):
    if not p2n or not isinstance(p2n, dict): return ""
    bp=KDK_3G.get(n) if gperson==3 else KDK_4G.get(n)
    if not bp: return ""
    n2p={v:k for k,v in p2n.items()}; rows=""
    for i,(a,b,c,d) in enumerate(bp):
        t1=f"{n2p.get(a,a)}({a}) &amp; {n2p.get(b,b)}({b})"
        t2=f"{n2p.get(c,c)}({c}) &amp; {n2p.get(d,d)}({d})"
        rows+=f"<tr><td style='text-align:center'><span style='background:#1B5E20;color:#fff;border-radius:20px;padding:2px 8px;font-size:.58rem;font-weight:700'>{i+1}</span></td><td style='text-align:left'>{t1} vs {t2}</td></tr>"
    return f'<div class="kdk"><div style="font-size:.72rem;font-weight:800;color:#1B5E20;margin-bottom:5px">📋 KDK 1인 {gperson}게임 — {n}명</div><table><thead><tr><th>순서</th><th>대진</th></tr></thead><tbody>{rows}</tbody></table></div>'

def matrix_html(matches,rank_items,mode,p2n):
    if not matches or not rank_items: return ""
    p2n_dict = p2n if (p2n and isinstance(p2n, dict)) else {}
    is_fixed = (mode == "고정페어")
    is_singles = (mode in ["단식", "싱글"])
    
    if is_fixed:
        lab = {t: " &amp; ".join(list(t)) for t in rank_items}
    elif is_singles:
        lab = {p: str(p) for p in rank_items}
    else:
        lab = {p: f"{p}({p2n_dict.get(p,'?')})" if p2n_dict else str(p) for p in rank_items}
        
    keys = list(lab.values())
    mat = {rk: {ck: "■" if rk == ck else "—" for ck in keys} for rk in keys}
    
    for m in matches:
        a, b = int(m.get("s1", 0)), int(m.get("s2", 0))
        if a > 0 or b > 0:
            t1_players = safe_parse_team(m.get("t1", []))
            t2_players = safe_parse_team(m.get("t2", []))
            
            if is_fixed:
                k1, k2 = tuple(t1_players), tuple(t2_players)
                rk, ck = lab.get(k1), lab.get(k2)
                if rk in mat and ck in mat[rk]: mat[rk][ck] = f"{a}:{b}"
                if ck in mat and rk in mat[ck]: mat[ck][rk] = f"{b}:{a}"
            elif is_singles:
                if t1_players and t2_players:
                    x, y = t1_players[0], t2_players[0]
                    rk, ck = lab.get(x), lab.get(y)
                    if rk in mat and ck in mat[rk]: mat[rk][ck] = f"{a}:{b}"
                    if ck in mat and rk in mat[ck]: mat[ck][rk] = f"{b}:{a}"
            else:
                for x in t1_players:
                    for y in t2_players:
                        rk, ck = lab.get(x), lab.get(y)
                        if rk in mat and ck in mat[rk]: mat[rk][ck] = f"{a}:{b}"
                        if ck in mat and rk in mat[ck]: mat[ck][rk] = f"{b}:{a}"
                        
    header = "".join(f"<th>{k}</th>" for k in keys)
    body = ""
    for rk in keys:
        body += f"<tr><th>{rk}</th>"
        for ck in keys:
            v = mat[rk][ck]
            if v == "■":   body += '<td class="mx-grey">■</td>'
            elif v == "—": body += '<td class="mx-dash">—</td>'
            else:        body += f'<td class="mx-sc">{v}</td>'
        body += "</tr>"
    return f'<div class="mx-wrap"><table class="mx"><thead><tr><th></th>{header}</tr></thead><tbody>{body}</tbody></table></div>'

def adj_score(tid,grp,mi,side,delta):
    tours = load_tours()
    if tid in tours and "groups" in tours[tid] and grp in tours[tid]["groups"]:
        m = tours[tid]["groups"][grp]["matches"][mi]
        key = "s1" if side=="A" else "s2"
        m[key] = max(0, int(m.get(key, 0)) + delta)
        save_tours(tours)

# ══════════════════════════════════════
# 세션 관리 및 기본값 구성
# ══════════════════════════════════════
ss=st.session_state
if "is_admin" not in ss: ss.is_admin=False
if "menu"     not in ss: ss.menu="ranking"

# ══════════════════════════════════════
# 상단 레이아웃 및 내비게이션 바
# ══════════════════════════════════════
MENUS=[("ranking","🏆","랭킹"),("schedule","📅","대진"),("result","📊","결과"),("archive","📂","기록"),("admin","⚙️","관리")]
MENU_COLOR={"ranking":"#2E7D32","schedule":"#1565C0","result":"#E65100","archive":"#4A148C","admin":"#00695C"}

st.markdown('<div class="hdr"><div class="hdr-title">🎾 두류 테니스 클럽</div><div class="hdr-sub">DURYU TENNIS CLUB</div></div>',unsafe_allow_html=True)
nav_cols=st.columns(len(MENUS))
for col,(key,icon,label) in zip(nav_cols,MENUS):
    with col:
        if st.button(f"{icon}\n{label}",key=f"nav_{key}",use_container_width=True,type="primary" if ss.menu==key else "secondary"):
            ss.menu=key; st.rerun()
cc=MENU_COLOR.get(ss.menu,"#2E7D32")
st.markdown(f'<div style="height:4px;background:{cc};margin:0 -0.6rem 12px;box-shadow:0 2px 6px rgba(0,0,0,.18)"></div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 메뉴 1. 랭킹 뷰어
# ══════════════════════════════════════════════════════
if ss.menu=="ranking":
    st.markdown(f"<div class='pg-title c0'>🏆 두류 랭킹</div>",unsafe_allow_html=True)
    df=load_rank()
    if df.empty:
        st.markdown("<div class='ic'>📭 등록된 랭킹이 없습니다.<br>관리실 메뉴에서 회원을 업로드해 주세요.</div>",unsafe_allow_html=True)
    else:
        medal=["🥇","🥈","🥉"]; d=df.copy()
        d.insert(0,"순위",[medal[i] if i<3 else str(i+1) for i in range(len(d))])
        st.markdown(df_to_html(d),unsafe_allow_html=True)
        st.download_button("📥 엑셀 다운로드",data=to_excel(df),file_name=f"랭킹_{date.today()}.xlsx",use_container_width=True)

# ══════════════════════════════════════════════════════
# 메뉴 2. 실시간 대진표 및 스코어 보드
# ══════════════════════════════════════════════════════
elif ss.menu=="schedule":
    tours=load_tours(); active=[k for k,v in tours.items() if v.get("status")=="진행중"]
    if not active:
        st.markdown("<div class='pg-title c1'>📅 대진표</div><div class='ic ic-b'>⚠️ 진행 중인 대회가 없습니다.</div>",unsafe_allow_html=True); st.stop()
    tid=active[-1]; tour=tours[tid]; gnames=list(tour.get("groups",{}).keys())
    st.markdown(f"<div class='pg-title c1'>📅 {tour['title']}</div>",unsafe_allow_html=True)
    st.markdown(f"<div class='ic ic-b'>📍 {tour.get('date','')} &nbsp;|&nbsp; {tour.get('place','')} &nbsp;|&nbsp; 코트 {tour.get('courts',2)}면</div>",unsafe_allow_html=True)
    if not gnames:
        st.markdown("<div class='ic ic-b'>ℹ️ 편성된 대진 그룹이 없습니다.</div>",unsafe_allow_html=True); st.stop()
        
    tabs=st.tabs([f"{GLBL[i%len(GLBL)]} {g}" for i,g in enumerate(gnames)])
    for ti,g in enumerate(gnames):
        with tabs[ti]:
            gi=tour["groups"][g]; ms=gi.get("matches",[]); mode=gi.get("mode","KDK")
            p2n=gi.get("player_with_number",{})
            fx=(mode=="고정페어"); sv=stats_fixed(ms) if (fx or mode=="단식") else stats_kdk(ms); rit=list(sv.keys())
            
            st.markdown("<div class='sec sec-b'>📋 전적 매트릭스</div>",unsafe_allow_html=True)
            st.markdown(matrix_html(ms,rit,mode,p2n),unsafe_allow_html=True)
            if mode=="KDK" and p2n: st.markdown(kdk_html(len(p2n),gi.get("games",4),p2n),unsafe_allow_html=True)
            
            st.markdown("<div class='sec sec-b'>🏆 현재 그룹 순위</div>",unsafe_allow_html=True)
            if rit:
                ranked=sorted(rit,key=lambda x:(-sv[x]["승"],-sv[x]["득실"])); rows=[]
                for i,item in enumerate(ranked):
                    if fx: rows.append({"순위":i+1,"팀":" & ".join(list(item)),"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}'})
                    elif mode=="단식": rows.append({"순위":i+1,"선수":list(item)[0] if isinstance(item, tuple) else item,"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"비고":grade(i+1)})
                    else:  rows.append({"순위":i+1,"선수":item,"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"비고":grade(i+1)})
                st.markdown(df_to_html(pd.DataFrame(rows)),unsafe_allow_html=True)
                
            st.markdown("<div class='sec sec-b'>🎾 경기 스코어 입력</div>",unsafe_allow_html=True)
            for mi,m in enumerate(ms):
                t1_list = safe_parse_team(m.get("t1", []))
                t2_list = safe_parse_team(m.get("t2", []))
                t1s=" & ".join(t1_list) if t1_list else "미정"
                t2s=" & ".join(t2_list) if t2_list else "미정"
                
                color_idx = mi % 8
                mc = f"mc{color_idx}"
                tbc = f"tb{color_idx}"
                
                s1v=int(m.get("s1", 0)); s2v=int(m.get("s2", 0))
                st.markdown(f'<div class="match-card m-color-{color_idx}"><span class="match-no {mc}">MATCH {mi+1}</span>',unsafe_allow_html=True)
                nA,nVS,nB=st.columns([5,1,5])
                with nA: st.markdown(f'<div class="team-nm {tbc}">{t1s}</div>',unsafe_allow_html=True)
                with nVS: st.markdown('<div style="height:40px;display:flex;align-items:center;justify-content:center"><div class="vs-badge">VS</div></div>',unsafe_allow_html=True)
                with nB: st.markdown(f'<div class="team-nm {tbc}">{t2s}</div>',unsafe_allow_html=True)
                cAm,cAn,cAp,cG,cBm,cBn,cBp=st.columns([1.1,1.6,1.1,0.4,1.1,1.6,1.1])
                with cAm: st.markdown('<div class="ctrl-row">',unsafe_allow_html=True); st.button("－",key=f"dm_{tid}_{g}_{mi}_A",on_click=adj_score,args=(tid,g,mi,"A",-1),use_container_width=True); st.markdown('</div>',unsafe_allow_html=True)
                with cAn: st.markdown(f'<div class="ctrl-num">{s1v}</div>',unsafe_allow_html=True)
                with cAp: st.markdown('<div class="ctrl-row">',unsafe_allow_html=True); st.button("＋",key=f"ip_{tid}_{g}_{mi}_A",on_click=adj_score,args=(tid,g,mi,"A",1),use_container_width=True); st.markdown('</div>',unsafe_allow_html=True)
                with cG: st.markdown('<div style="height:42px"></div>',unsafe_allow_html=True)
                with cBm: st.markdown('<div class="ctrl-row">',unsafe_allow_html=True); st.button("－",key=f"dm_{tid}_{g}_{mi}_B",on_click=adj_score,args=(tid,g,mi,"B",-1),use_container_width=True); st.markdown('</div>',unsafe_allow_html=True)
                with cBn: st.markdown(f'<div class="ctrl-num">{s2v}</div>',unsafe_allow_html=True)
                with cBp: st.markdown('<div class="ctrl-row">',unsafe_allow_html=True); st.button("＋",key=f"ip_{tid}_{g}_{mi}_B",on_click=adj_score,args=(tid,g,mi,"B",1),use_container_width=True); st.markdown('</div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════
# 메뉴 3. 최종 결과 현황
# ═══════════════════════════════════════
elif ss.menu=="result":
    tours=load_tours(); active=[k for k,v in tours.items() if v.get("status")=="진행중"]
    if not active:
        st.markdown("<div class='pg-title c2'>📊 경기 결과</div><div class='ic ic-o'>⚠️ 진행 중인 대회가 없습니다.</div>",unsafe_allow_html=True); st.stop()
    tid=active[-1]; tour=tours[tid]
    st.markdown(f"<div class='pg-title c2'>📊 {tour['title']} 최종 현황</div>",unsafe_allow_html=True)
    for g,gi in tour.get("groups", {}).items():
        mode,ms=gi.get("mode","KDK"),gi.get("matches",[])
        p2n=gi.get("player_with_number",{})
        fx=(mode=="고정페어"); sv=stats_fixed(ms) if (fx or mode=="단식") else stats_kdk(ms)
        ranked=sorted(sv.keys(),key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))
        st.markdown(f'<div class="sec sec-o">{g} ({mode})</div>',unsafe_allow_html=True)
        rows=[]
        for i,item in enumerate(ranked):
            pt=rank_pts(i+1,mode)
            if fx: rows.append({"순위":i+1,"팀":" & ".join(list(item)),"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"비고":grade(i+1)})
            elif mode=="단식": rows.append({"순위":i+1,"선수":list(item)[0] if isinstance(item, tuple) else item,"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"비고":grade(i+1)})
            else:  rows.append({"순위":i+1,"선수":item,"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"비고":grade(i+1)})
        st.markdown(df_to_html(pd.DataFrame(rows)),unsafe_allow_html=True)
        
        with st.expander("📋 세부 매치 기록 보기"):
            mr=[]
            for m in ms:
                t1_list = safe_parse_team(m.get("t1", []))
                t2_list = safe_parse_team(m.get("t2", []))
                t1s = " & ".join(t1_list) if t1_list else "미정"
                t2s = " & ".join(t2_list) if t2_list else "미정"
                mr.append({"경기": f"{t1s} vs {t2s}", "결과": f"{m.get('s1', 0)} : {m.get('s2', 0)}"})
            if mr:
                st.markdown(df_to_html(pd.DataFrame(mr)),unsafe_allow_html=True)
            else:
                st.caption("기록된 경기가 없습니다.")

# ══════════════════════════════════════════════════════
# 메뉴 4. 히스토리 기록실
# ══════════════════════════════════════
elif ss.menu=="archive":
    st.markdown("<div class='pg-title c3'>📂 대회 기록실</div>",unsafe_allow_html=True)
    tours=load_tours(); past={k:v for k,v in tours.items() if v.get("status")!="진행중"}
    if not past:
        st.markdown("<div class='ic ic-p'>📭 아카이브된 과거 대회가 없습니다.</div>",unsafe_allow_html=True); st.stop()
    sel=st.selectbox("조회할 대회 선택",list(past.keys()),format_func=lambda k:f"{past[k]['title']} ({past[k].get('date','')})")
    tour=past[sel]
    st.markdown(f"<div class='ic ic-p'>🏆 <strong>{tour['title']}</strong> &nbsp;|&nbsp; {tour.get('date','')} &nbsp;|&nbsp; {tour.get('place','')}</div>",unsafe_allow_html=True)
    for g,gi in tour.get("groups",{}).items():
        mode,ms=gi.get("mode","KDK"),gi.get("matches",[]); fx=(mode=="고정페어"); sv=stats_fixed(ms) if (fx or mode=="단식") else stats_kdk(ms)
        ranked=sorted(sv.keys(),key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))
        st.markdown(f'<div class="sec sec-p">{g} ({mode})</div>',unsafe_allow_html=True)
        rows=[]
        for i,item in enumerate(ranked):
            pt=rank_pts(i+1,mode)
            if fx: rows.append({"순위":i+1,"팀":" & ".join(list(item)),"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"비고":grade(i+1)})
            elif mode=="단식": rows.append({"순위":i+1,"선수":list(item)[0] if isinstance(item, tuple) else item,"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"비고":grade(i+1)})
            else:  rows.append({"순위":i+1,"선수":item,"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"포인트":pt,"비고":grade(i+1)})
        st.markdown(df_to_html(pd.DataFrame(rows)),unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 메뉴 5. 관리자 제어 타워
# ══════════════════════════════════════════════════════
elif ss.menu=="admin":
    st.markdown("<div class='pg-title c4'>⚙️ 관리자 관제 센터</div>",unsafe_allow_html=True)
    pw=st.text_input("🔒 패스워드 인증",type="password",placeholder="암호코드 입력")
    if pw==ADMIN_PW: ss.is_admin=True
    if not ss.is_admin:
        if pw: st.error("❌ 패스워드가 올바르지 않습니다.")
        st.stop()
        
    adm=st.tabs(["📋 회원 명단","🏆 대회 생성/관리","👥 참가자·그룹 자유 수정","💾 포인트 정산"])

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
        st.markdown('<div class="sec sec-t">📂 엑셀(CSV) 파일로 일괄 업로드</div>',unsafe_allow_html=True)
        up=st.file_uploader("업로드",type=["xlsx","xls","csv"],key="rank_up_file",label_visibility="collapsed")
        if up:
            try:
                du=read_file(up)
                if "현재포인트" in du.columns:
                    du["현재포인트"]=pd.to_numeric(du["현재포인트"],errors="coerce").fillna(0)
                st.markdown(df_to_html(du),unsafe_allow_html=True)
                if st.button("💾 업로드 데이터로 랭킹 덮어쓰기",key="save_up_rk",use_container_width=True):
                    save_rank(du)
                    if "이름" in du.columns: save_members(du["이름"].tolist())
                    st.success("✅ 저장 성공!"); st.rerun()
            except Exception as e: st.error(f"오류가 발생했습니다: {e}")

    # 탭 [1] : 새 대회 생성 및 그룹별 개별 옵션 커스텀 설정
    with adm[1]:
        st.markdown('<div class="sec sec-t">📅 신규 대회 개최 설정</div>',unsafe_allow_html=True)
        tn=st.text_input("대회명칭",placeholder="예: 두류 테니스 클럽 6월 정기대회")
        c1,c2=st.columns(2)
        with c1: td=st.date_input("개최일자",value=date.today())
        with c2: tp=st.text_input("장소",value="두류 테니스장")
        c3,c4=st.columns(2)
        with c3: co=st.selectbox("할당 코트", [1,2,3,4,5], index=1)
        with c4: g_count=st.number_input("설정할 그룹 수",1,6,value=4)
        
        st.markdown('<div style="font-size:0.75rem; color:#555; font-weight:bold; margin-top:5px;">⚙️ 각 그룹 초기 스펙 정의</div>', unsafe_allow_html=True)
        init_g_setup = {}
        for i in range(int(g_count)):
            g_char = chr(64 + 1 + i)  # A, B, C, D...
            g_full_name = f"{g_char}그룹"
            st.markdown(f"**[{g_full_name} 옵션]**")
            cols_init = st.columns(3)
            with cols_init[0]:
                m_init = st.selectbox(f"방식 ({g_char})", ["KDK", "고정페어", "단식"], key=f"init_m_{g_char}")
            with cols_init[1]:
                g_init = st.selectbox(f"게임 수 ({g_char})", [3, 4, 5], index=1, key=f"init_g_{g_char}")
            with cols_init[2]:
                sz_init = st.number_input(f"배정 정원 ({g_char})", 2, 24, value=8, key=f"init_sz_{g_char}")
            init_g_setup[g_full_name] = {"mode": m_init, "games": g_init, "size": int(sz_init)}
            
        if st.button("🚀 대회 공식 개막", type="primary", use_container_width=True):
            if tn.strip():
                ts=load_tours(); t_key=f"{td}_{tn.strip()}"
                ng={}
                for gname, spec in init_g_setup.items():
                    ng[gname] = {
                        "players": [],
                        "mode": spec["mode"],
                        "games": spec["games"],
                        "size": spec["size"],
                        "matches": [],
                        "player_with_number": {}
                    }
                ts[t_key]={"title":tn.strip(),"date":str(td),"place":tp,"courts":co,"status":"진행중","groups":ng,"players":[]}
                save_tours(ts); st.success(f"✅ 대회 '{tn.strip()}'가 맞춤 설정 구조로 대진 그룹이 생성되었습니다."); st.rerun()
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
                st.markdown("<div style='height:28px'></div>",unsafe_allow_html=True)
                if st.button("🗑️ 해당 대회 데이터 영구 삭제",type="primary",use_container_width=True):
                    del ts[sel_t]; save_tours(ts); st.warning("대회가 삭제되었습니다."); st.rerun()

    # 탭 [2] : 당일 참가자 명단 조정 및 그룹별 실시간 자유 조율 컴포넌트
    with adm[2]:
        ts=load_tours(); act_tids=[k for k,v in ts.items() if v.get("status")=="진행중"]
        if not act_tids:
            st.info("현재 진행 중인 대회가 존재하지 않습니다."); st.stop()
        sel_tid=act_tids[-1]; tour=ts[sel_tid]; cg=tour.get("groups",{})
        
        st.markdown(f"### 👥 {tour['title']} 당일 출전 명단 관리")
        
        with st.expander("📝 [1단계] 당일 참가자 명단 텍스트 일괄 등록", expanded=False):
            st.markdown("오늘 출전한 모든 선수의 이름을 쉼표(,) 또는 엔터로 구분하여 아래에 적어주세요.")
            joined_p = []
            for g_info in cg.values(): joined_p.extend(g_info.get("players", []))
            
            raw_input_p = st.text_area("참가자 명단 입력", value=", ".join(joined_p), height=100, key="day_p_input")
            
            c_auto, c_direct = st.columns(2)
            with c_auto:
                if st.button("⚡ 랭킹순으로 그룹 자동 배정 및 대진 생성", type="primary", use_container_width=True):
                    parsed_p = [n.strip() for n in raw_input_p.replace("\n",",").split(",") if n.strip()]
                    if parsed_p:
                        parsed_p = list(dict.fromkeys(parsed_p))
                        rk_df = load_rank()
                        if not rk_df.empty and "이름" in rk_df.columns:
                            rk_map = {row["이름"]: i for i, row in rk_df.iterrows()}
                            parsed_p.sort(key=lambda x: rk_map.get(x, 999))
                        
                        g_names = list(cg.keys())
                        ptr = 0
                        for gname in g_names:
                            if gname not in cg: continue
                            g_sz = cg[gname].get("size", 8)
                            assigned = parsed_p[ptr:ptr+g_sz]
                            cg[gname]["players"] = assigned
                            ptr += g_sz
                            
                            ms2, pwn2 = build_matches(assigned, cg[gname].get("mode","KDK"), cg[gname].get("games",4))
                            cg[gname]["matches"] = ms2
                            cg[gname]["player_with_number"] = pwn2
                        tour["players"] = parsed_p
                        save_tours(ts)
                        st.success("✅ 설정된 그룹 크기에 의거해 자동 배정 및 매치 테이블 편성이 완료되었습니다."); st.rerun()
            with c_direct:
                if st.button("💾 명단만 일단 저장 (대진 미생성)", use_container_width=True):
                    parsed_p = [n.strip() for n in raw_input_p.replace("\n",",").split(",") if n.strip()]
                    tour["players"] = list(dict.fromkeys(parsed_p))
                    save_tours(ts); st.success("✅ 출전 인원 기본 저장이 완료되었습니다. 하단에서 수동 조율하세요.")

        st.divider()
        
        st.markdown("### 🔀 각 그룹 명단 추가, 수정, 삭제")
        for gname, gdata in list(tour.get("groups",{}).items()):
            st.markdown(f"#### 🏷️ **{gname}** 세부 설정 변경")
            c_m, c_g, c_z = st.columns(3)
            with c_m: 
                m_opts=["KDK","고정페어","단식"]
                gdata["mode"] = st.selectbox(f"방식 ({gname})", m_opts, index=m_opts.index(gdata.get("mode","KDK")), key=f"md_edit_{gname}")
            with c_g: 
                gdata["games"] = st.selectbox(f"인당 게임 수 ({gname})", [3,4,5], index=[3,4,5].index(gdata.get("games",4)), key=f"gm_edit_{gname}")
            with c_z: 
                gdata["size"] = st.number_input(f"배정 정원 ({gname})", 2, 24, value=gdata.get("size",8), key=f"sz_edit_{gname}")
                
            cur_grp_players = gdata.get("players", [])
            
            st.markdown(f"**📌 현재 소속 선수 ({len(cur_grp_players)}명)**")
            if cur_grp_players:
                st.info(f"👉 {', '.join(cur_grp_players)}")
            else:
                st.caption("현재 소속된 선수가 없습니다.")
                
            grp_text_input = st.text_input(f"✍️ {gname} 명단 편집 (이름을 쉼표로 구분)", value=", ".join(cur_grp_players), key=f"grp_txt_{gname}")
            
            updated_grp_p = [n.strip() for n in grp_text_input.split(",") if n.strip()]
            if updated_grp_p != cur_grp_players:
                gdata["players"] = updated_grp_p
                ms3, pwn3 = build_matches(updated_grp_p, gdata["mode"], gdata["games"])
                gdata["matches"] = ms3
                gdata["player_with_number"] = pwn3
                save_tours(ts)
                st.rerun()
                
            st.markdown("<div style='height:1px; background:#ddd; margin:15px 0;'></div>", unsafe_allow_html=True)
            
        if st.button("🏁 모든 그룹 최종 변동사항 저장 및 대진 전면 확정", type="primary", use_container_width=True):
            save_tours(ts); st.success("✅ 전체 대진 매트릭스가 완벽하게 세이브되었습니다. 대진 메뉴를 확인하세요.")

    # 탭 [3] : 당일 최종 스코어 기반 랭킹 포인트 결산 및 마감 처리
    with adm[3]:
        ts=load_tours(); act_tids=[k for k,v in ts.items() if v.get("status")=="진행중"]
        if not act_tids: st.warning("정산 대상 대회가 활성화되어 있지 않습니다."); st.stop()
        t_key=act_tids[-1]; t_obj=ts[t_key]
        
        earn={}
        for gname, gdata in t_obj.get("groups",{}).items():
            mode = gdata.get("mode","KDK")
            ms = gdata.get("matches",[])
            
            fx=(mode=="고정페어")
            score_map = stats_fixed(ms) if (fx or mode=="단식") else stats_kdk(ms)
            if not score_map: continue
                
            rk_list = sorted(score_map.keys(), key=lambda x:(-score_map[x]["승"], -score_map[x]["득실"]))
            for i, p_item in enumerate(rk_list):
                pts = rank_pts(i+1, mode)
                if fx:
                    for individual in list(p_item): earn[individual] = earn.get(individual,0) + pts
                elif mode=="단식":
                    individual = list(p_item)[0] if isinstance(p_item, tuple) else p_item
                    earn[individual] = earn.get(individual,0) + pts
                else:
                    earn[p_item] = earn.get(p_item,0) + pts
                
        if earn:
            st.markdown('<div class="ic ic-t">🏆 금일 누적 획득 예정 포인트</div>',unsafe_allow_html=True)
            res_df = pd.DataFrame(sorted(earn.items(),key=lambda x:-x[1]),columns=["선수명","지급포인트"])
            st.markdown(df_to_html(res_df),unsafe_allow_html=True)
        else:
            st.info("ℹ️ 현재 스코어가 입력되었거나 진행된 경기가 없어 정산할 포인트 데이터가 없습니다.")
            
        c_fin, c_rst = st.columns(2)
        with c_fin:
            if st.button("🏆 계산된 포인트 마스터 랭킹에 영구 반영",type="primary",use_container_width=True):
                if not earn:
                    st.error("❌ 정산할 포인트 내역이 없어 마감할 수 없습니다. 최소 1경기 이상의 결과를 입력해주세요.")
                else:
                    r_master = load_rank()
                    for p, p_val in earn.items():
                        if p in r_master["이름"].values:
                            r_master.loc[r_master["이름"]==p, "현재포인트"] += p_val
                        else:
                            new_r = {c:"" for c in COLS_RANK}; new_r["이름"]=p; new_r["현재포인트"]=p_val
                            r_master = pd.concat([r_master, pd.DataFrame([new_r])],ignore_index=True)
                    save_rank(r_master); t_obj["status"]="완료"; save_tours(ts)
                    st.success("✅ 정상 마감 처리되어 역대 기록실로 이관되었습니다."); st.rerun()
        with c_rst:
            if st.button("🚨 입력된 경기 점수 전부 강제 초기화",use_container_width=True):
                for gname, gdata in t_obj.get("groups",{}).items():
                    for m in gdata.get("matches",[]): m["s1"]=0; m["s2"]=0
                save_tours(ts); st.success("✅ 모든 경기 스코어가 0:0으로 초기화되었습니다."); st.rerun()

}
