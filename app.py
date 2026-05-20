import streamlit as st
import pandas as pd
import random, os, json
from datetime import date
from io import BytesIO

st.set_page_config(page_title="두류 테니스", page_icon="🎾",
                   layout="centered", initial_sidebar_state="collapsed")

# ══════════════════════════════════════
# CSS (UI 스타일 및 모바일 최적화)
# ══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght=400;500;700;900&display=swap');
:root{
  --g0:#1B5E20;--g2:#388E3C;--g3:#66BB6A;--g5:#E8F5E9;
  --nav0:#2E7D32;--nav1:#1565C0;--nav2:#E65100;--nav3:#4A148C;--nav4:#00695C;
  --mc0:#1B5E20;--mc1:#0D47A1;--mc2:#BF360C;--mc3:#4A148C;
  --bg:#F4F6F9;--card:#fff;--bd:#E0E4EA;
  --r1:10px;--r2:16px;
  --sh:0 2px 10px rgba(0,0,0,.08);--sh2:0 4px 20px rgba(0,0,0,.13);
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent;}

html, body, [data-testid="stAppViewContainer"] :not(i):not(svg):not([class*="material-icons"]) {
    font-family: 'Noto Sans KR', sans-serif;
}

.block-container{padding:0 0.6rem 5rem!important;max-width:520px!important;margin:0 auto!important;background:var(--bg)!important;}
.stApp{background:var(--bg)!important;}

@media (max-width: 640px) {
  [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; gap: 6px !important; }
  [data-testid="stHorizontalBlock"] .stButton { flex: 1 0 auto !important; min-width: 70px !important; }
  .stButton button { font-size: 0.65rem !important; padding: 6px 4px !important; white-space: normal !important; word-break: keep-all !important; }
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

.match-card{background:var(--card);border-radius:var(--r2);padding:10px 8px 12px;margin:10px 0;box-shadow:var(--sh2);border:1px solid var(--bd);}
.match-no{display:inline-block;border-radius:20px;padding:3px 12px;font-size:.58rem;font-weight:900;margin-bottom:8px;color:#fff;}
.mc0{background:var(--mc0);}.mc1{background:var(--mc1);}.mc2{background:var(--mc2);}.mc3{background:var(--mc3);}

.team-nm{border-radius:8px;padding:7px 3px;font-weight:900;font-size:clamp(.6rem,2.8vw,.85rem);text-align:center;color:#fff;box-shadow:var(--sh);min-height:40px;display:flex;align-items:center;justify-content:center;word-break:keep-all;line-height:1.2;}
.tb0{background:var(--g0);}.tb1{background:var(--nav1);}

.vs-badge{width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,#FFB74D,#FB8C00);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:.52rem;color:#fff;box-shadow:var(--sh);margin:0 auto;}

.ctrl-num{display:flex;align-items:center;justify-content:center;background:#fff;border:2px solid #A5D6A7;border-radius:8px;font-size:clamp(1rem,5.5vw,1.5rem);font-weight:900;color:#1B5E20;height:42px;width:100%;}
.ctrl-row .stButton>button{height:42px!important;min-height:42px!important;font-size:clamp(.9rem,4.5vw,1.3rem)!important;font-weight:900!important;padding:0!important;border-radius:8px!important;background:#E8F5E9!important;color:#1B5E20!important;border:2px solid #A5D6A7!important;box-shadow:none!important;width:100%!important;}

.stButton>button{border-radius:var(--r2)!important;font-weight:700!important;font-size:.8rem!important;min-height:44px!important;}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,var(--g0),var(--g2))!important;color:#fff!important;border:none!important;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# 데이터 정의 및 파일 입출력
# ══════════════════════════════════════
RANK_FILE   = "ranking_master.csv"
MEMBER_FILE = "member_roster.json"
TOUR_FILE   = "tournaments.json"
COLS_RANK   = ["랭킹","이름","현재포인트","3월 포인트","결과","부과점","그룹","비고"]
GLBL        = ["🟢","🔵","🟠","🟣","🩵","🔴","🟡","⚪"]

KDK_3G = {
    4:  [(1,4,2,3),(1,3,2,4),(1,2,3,4)],
    8:  [(1,2,3,4),(5,6,7,8),(1,8,2,7),(3,6,4,5),(1,4,5,8),(2,3,6,7)],
    12: [(1,2,3,4),(5,6,7,8),(9,10,11,12),(1,3,5,7),(2,4,6,8),(9,11,1,5),(4,8,9,12),(6,7,10,11),(10,12,2,3)],
}
KDK_4G = {
    5:  [(1,2,3,4),(1,3,2,5),(1,4,3,5),(1,5,2,4),(2,3,4,5)],
    6:  [(1,3,2,4),(1,5,4,6),(2,3,5,6),(1,4,3,5),(2,6,3,4),(1,6,2,5)],
    7:  [(1,2,3,4),(5,6,1,7),(2,3,5,7),(1,4,6,7),(3,5,2,4),(1,6,2,5),(4,6,3,7)],
    8:  [(1,2,3,4),(5,6,7,8),(1,3,5,7),(2,4,6,8),(1,5,2,6),(3,7,4,8),(1,6,3,8),(2,5,4,7)],
    9:  [(1,2,3,4),(5,6,7,8),(1,9,5,7),(2,3,6,8),(4,9,3,8),(1,5,2,6),(3,6,4,5),(1,7,8,9),(2,4,7,9)],
    10: [(1,2,3,5),(6,7,8,10),(2,3,4,6),(7,8,1,9),(3,4,5,7),(8,9,2,10),(4,5,6,8),(1,3,9,10),(5,6,7,9),(1,10,2,4)],
    11: [(1,2,3,5),(6,7,8,10),(4,9,1,11),(2,3,6,8),(4,5,7,10),(9,11,2,6),(1,3,7,11),(4,8,5,9),(1,10,2,8),(4,7,6,11),(3,9,5,10)],
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
        with open(MEMBER_FILE,"r",encoding="utf-8") as f: return json.load(f)
    df=load_rank(); return df["이름"].tolist() if not df.empty else []

def save_members(names):
    with open(MEMBER_FILE,"w",encoding="utf-8") as f: json.dump(names,f,ensure_ascii=False,indent=2)

def load_tours():
    if os.path.exists(TOUR_FILE):
        with open(TOUR_FILE,"r",encoding="utf-8") as f: return json.load(f)
    return {}

def save_tours(d):
    with open(TOUR_FILE,"w",encoding="utf-8") as f: json.dump(d,f,ensure_ascii=False,indent=2)

def to_excel(df):
    buf=BytesIO(); df.to_excel(buf,index=False); return buf.getvalue()

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
# 대진 편성 핵심 엔진 알고리즘
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

def make_fixed_balance(players):
    """ 랭킹순 정렬된 명단을 기반으로 (1위+최하위), (2위+차하위) 순으로 묶어 리그전 편성 """
    n = len(players)
    if n < 4: return [], {}
    
    # 페어링 빌드 (짝수 안 맞으면 남는 한 명은 이전 직전조에 유연 편성하거나 대기)
    pairs = []
    for i in range(n // 2):
        pairs.append((players[i], players[n - 1 - i]))
        
    ms = [{"t1": list(pairs[i]), "t2": list(pairs[j]), "s1": 0, "s2": 0}
          for i in range(len(pairs)) for j in range(i+1,len(pairs))]
    random.shuffle(ms)
    return ms, {}

def make_kdk_random(players, gperson):
    """ 임의의 번호(1~N)를 부여한 뒤 KDK 표준 대진 매핑 구현 """
    n=len(players); bp=KDK_3G.get(n) if gperson==3 else KDK_4G.get(n)
    if not bp: return [], {}
    sh=random.sample(players,n)
    n2p={i+1:sh[i] for i in range(n)}; p2n={sh[i]:i+1 for i in range(n)}
    ms=[{"t1":[n2p[a],n2p[b]],"t2":[n2p[c],n2p[d]],"s1":0,"s2":0} for a,b,c,d in bp]
    return ms,p2n

def make_singles_random(players):
    """ 단식 대진 무작위 셔플 후 풀리그 편성 """
    pl=players[:]; random.shuffle(pl)
    ms=[{"t1":[pl[i]],"t2":[pl[j]],"s1":0,"s2":0} for i in range(len(pl)) for j in range(i+1,len(pl))]
    random.shuffle(ms)
    return ms,{}

def build_matches(players,mode,gc):
    if not players or len(players) < 2: return [], {}
    if mode=="고정페어": return make_fixed_balance(players)
    if mode=="KDK": return make_kdk_random(players,gc)
    return make_singles_random(players)

def matrix_html(matches,rank_items,is_fixed,p2n):
    if not matches or not rank_items: return ""
    lab={t:" & ".join(list(t)) if is_fixed else f"{t}({p2n.get(t,'?')})" for t in rank_items}
    mat={lab[t]:{lab[o]:("■" if t==o else "—") for o in lab} for t in lab}
    for m in matches:
        a,b=int(m["s1"]),int(m["s2"])
        if a>0 or b>0:
            if is_fixed:
                k1,k2=tuple(m["t1"]),tuple(m["t2"])
                if lab.get(k1) in mat and lab.get(k2) in mat:
                    mat[lab[k1]][lab[k2]]=f"{a}:{b}";mat[lab[k2]][lab[k1]]=f"{b}:{a}"
            else:
                for x in m["t1"]:
                    for y in m["t2"]:
                        if lab.get(x) in mat and lab.get(y) in mat:
                            mat[lab[x]][lab[y]]=f"{a}:{b}";mat[lab[y]][lab[x]]=f"{b}:{a}"
    keys=list(lab.values())
    header="".join(f"<th>{k}</th>" for k in keys)
    body=""
    for rk in keys:
        body+=f"<tr><th>{rk}</th>"
        for ck in keys:
            v=mat[rk][ck]
            if v=="■":   body+='<td class="mx-grey">■</td>'
            elif v=="—": body+='<td class="mx-dash">—</td>'
            else:        body+=f'<td class="mx-sc">{v}</td>'
        body+="</tr>"
    return f'<div class="mx-wrap"><table class="mx"><thead><tr><th></th>{header}</tr></thead><tbody>{body}</tbody></table></div>'

def adj_score(tid,grp,mi,side,delta):
    tours=load_tours(); m=tours[tid]["groups"][grp]["matches"][mi]
    key="s1" if side=="A" else "s2"
    m[key]=max(0,int(m[key])+delta); save_tours(tours)

# ══════════════════════════════════════
# 세션초기화 및 통합 비밀번호 관리
# ══════════════════════════════════════
ss=st.session_state
if "is_admin" not in ss: ss.is_admin=False
if "menu"     not in ss: ss.menu="ranking"

# 세션 내 동적 관리자 비밀번호 세팅 인프라 구축
if not os.path.exists("admin_config.json"):
    with open("admin_config.json","w") as f: json.dump({"pwd":"0502"},f)
with open("admin_config.json","r") as f: ADMIN_PW = json.load(f)["pwd"]

# ══════════════════════════════════════
# 공통 상단 네비게이션
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
st.markdown(f'<div style="height:4px;background:{cc};margin:0 -0.6rem 12px;"></div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 메뉴 1. 마스터 랭킹 뷰어
# ══════════════════════════════════════════════════════
if ss.menu=="ranking":
    st.markdown(f"<div class='pg-title c0'>🏆 두류 실시간 랭킹</div>",unsafe_allow_html=True)
    df=load_rank()
    if df.empty:
         st.markdown("<div class='ic'>📭 등록된 랭킹 데이터 필드가 없습니다.<br>관리 탭에서 마스터 명단을 업로드해 주세요.</div>",unsafe_allow_html=True)
    else:
        medal=["🥇","🥈","🥉"]; d=df.copy()
        d.insert(0,"순위",[medal[i] if i<3 else str(i+1) for i in range(len(d))])
        st.markdown(df_to_html(d),unsafe_allow_html=True)
        st.download_button("📥 엑셀(XLSX) 다운로드",data=to_excel(df),file_name=f"Duryu_Ranking_{date.today()}.xlsx",use_container_width=True)

# ══════════════════════════════════════════════════════
# 메뉴 2. 경기 대진표 및 스코어 입력 보드
# ══════════════════════════════════════════════════════
elif ss.menu=="schedule":
    tours=load_tours(); active=[k for k,v in tours.items() if v.get("status")=="진행중"]
    if not active:
        st.markdown("<div class='pg-title c1'>📅 라이브 대진표</div><div class='ic ic-b'>⚠️ 현재 활성화된(진행중) 대회가 없습니다.</div>",unsafe_allow_html=True); st.stop()
    tid=active[-1]; tour=tours[tid]; gnames=list(tour.get("groups",{}).keys())
    st.markdown(f"<div class='pg-title c1'>📅 {tour['title']}</div>",unsafe_allow_html=True)
    st.markdown(f"<div class='ic ic-b'>📍 {tour.get('date','')} &nbsp;|&nbsp; {tour.get('place','')} &nbsp;|&nbsp; 최적화 할당 코트: {tour.get('courts',2)}면</div>",unsafe_allow_html=True)
    if not gnames:
        st.markdown("<div class='ic ic-b'>ℹ️ 편성 완료된 그룹이 없습니다. 관리자 제어 탭에서 생성해 주세요.</div>",unsafe_allow_html=True); st.stop()
        
    tabs=st.tabs([f"{GLBL[i%len(GLBL)]} {g}" for i,g in enumerate(gnames)])
    for ti,g in enumerate(gnames):
        with tabs[ti]:
            gi=tour["groups"][g]; ms=gi["matches"]; mode=gi["mode"]; p2n=gi.get("player_with_number",{})
            fx=(mode=="고정페어"); sv=stats_fixed(ms) if fx else stats_kdk(ms); rit=list(sv.keys())
            
            st.markdown("<div class='sec sec-b'>📋 전적 결과 스코어 보드</div>",unsafe_allow_html=True)
            st.markdown(matrix_html(ms,rit,fx,p2n),unsafe_allow_html=True)
            
            st.markdown("<div class='sec sec-b'>🏅 실시간 그룹 내부 순위</div>",unsafe_allow_html=True)
            if rit:
                ranked=sorted(rit,key=lambda x:(-sv[x]["승"],-sv[x]["득실"])); rows=[]
                for i,item in enumerate(ranked):
                    if fx: rows.append({"순위":i+1,"팀 조합":" & ".join(list(item)),"승리":sv[item]["승"],"패전":sv[item]["패"],"득실점":f'{sv[item]["득실"]:+d}'})
                    else:  rows.append({"순위":i+1,"선수명":item,"승리":sv[item]["승"],"패전":sv[item]["패"],"득실점":f'{sv[item]["득실"]:+d}',"등급":grade(i+1)})
                st.markdown(df_to_html(pd.DataFrame(rows)),unsafe_allow_html=True)
                
            st.markdown("<div class='sec sec-b'>🎾 실시간 매치 스코어 기록조정</div>",unsafe_allow_html=True)
            for mi,m in enumerate(ms):
                t1s=" & ".join(m["t1"]); t2s=" & ".join(m["t2"])
                s1v,s2v=int(m["s1"]),int(m["s2"])
                st.markdown(f'<div class="match-card"><span class="match-no mc1">MATCH {mi+1}</span>',unsafe_allow_html=True)
                nA,nVS,nB=st.columns([5,1,5])
                with nA: st.markdown(f'<div class="team-nm tb1">{t1s}</div>',unsafe_allow_html=True)
                with nVS: st.markdown('<div style="height:40px;display:flex;align-items:center;justify-content:center"><div class="vs-badge">VS</div></div>',unsafe_allow_html=True)
                with nB: st.markdown(f'<div class="team-nm tb1">{t2s}</div>',unsafe_allow_html=True)
                cAm,cAn,cAp,cG,cBm,cBn,cBp=st.columns([1.1,1.6,1.1,0.4,1.1,1.6,1.1])
                with cAm: st.markdown('<div class="ctrl-row">',unsafe_allow_html=True); st.button("－",key=f"dm_{tid}_{g}_{mi}_A",on_click=adj_score,args=(tid,g,mi,"A",-1),use_container_width=True); st.markdown('</div>',unsafe_allow_html=True)
                with cAn: st.markdown(f'<div class="ctrl-num">{s1v}</div>',unsafe_allow_html=True)
                with cAp: st.markdown('<div class="ctrl-row">',unsafe_allow_html=True); st.button("＋",key=f"ip_{tid}_{g}_{mi}_A",on_click=adj_score,args=(tid,g,mi,"A",1),use_container_width=True); st.markdown('</div>',unsafe_allow_html=True)
                with cG: st.markdown('<div style="height:42px"></div>',unsafe_allow_html=True)
                with cBm: st.markdown('<div class="ctrl-row">',unsafe_allow_html=True); st.button("－",key=f"dm_{tid}_{g}_{mi}_B",on_click=adj_score,args=(tid,g,mi,"B",-1),use_container_width=True); st.markdown('</div>',unsafe_allow_html=True)
                with cBn: st.markdown(f'<div class="ctrl-num">{s2v}</div>',unsafe_allow_html=True)
                with cBp: st.markdown('<div class="ctrl-row">',unsafe_allow_html=True); st.button("＋",key=f"ip_{tid}_{g}_{mi}_B",on_click=adj_score,args=(tid,g,mi,"B",1),use_container_width=True); st.markdown('</div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 메뉴 3. 최종 결과 현황 분석 뷰어
# ══════════════════════════════════════════════════════
elif ss.menu=="result":
    tours=load_tours(); active=[k for k,v in tours.items() if v.get("status")=="진행중"]
    if not active:
        st.markdown("<div class='pg-title c2'>📊 경기 최종 결과 결과 통계</div><div class='ic ic-o'>⚠️ 진행 중인 대회가 존재하지 않습니다.</div>",unsafe_allow_html=True); st.stop()
    tid=active[-1]; tour=tours[tid]
    st.markdown(f"<div class='pg-title c2'>📊 {tour['title']} 최종 성적표</div>",unsafe_allow_html=True)
    for g,gi in tour["groups"].items():
        mode,ms=gi["mode"],gi["matches"]; p2n=gi.get("player_with_number",{})
        fx=(mode=="고정페어"); sv=stats_fixed(ms) if fx else stats_kdk(ms)
        ranked=sorted(sv.keys(),key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))
        st.markdown(f'<div class="sec sec-o">그룹 명칭: {g} ({mode})</div>',unsafe_allow_html=True)
        rows=[]
        for i,item in enumerate(ranked):
            pt=rank_pts(i+1,mode)
            if fx: rows.append({"순위":i+1,"팀명 조합":" & ".join(list(item)),"승점":sv[item]["승"],"패전":sv[item]["패"],"득실차":f'{sv[item]["득실"]:+d}',"정산포인트":pt,"결과비고":grade(i+1)})
            else:  rows.append({"순위":i+1,"선수명":item,"승점":sv[item]["승"],"패전":sv[item]["패"],"득실차":f'{sv[item]["득실"]:+d}',"정산포인트":pt,"결과비고":grade(i+1)})
        st.markdown(df_to_html(pd.DataFrame(rows)),unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 메뉴 4. 히스토리 기록실
# ══════════════════════════════════════════════════════
elif ss.menu=="archive":
    st.markdown("<div class='pg-title c3'>📂 대회 아카이브 기록실</div>",unsafe_allow_html=True)
    tours=load_tours(); past={k:v for k,v in tours.items() if v.get("status")=="완료"}
    if not past:
         st.markdown("<div class='ic ic-p'>📭 이관 완료된 과거 정기대회 기록 아카이브가 비어있습니다.</div>",unsafe_allow_html=True); st.stop()
    sel=st.selectbox("과거 아카이브 검색 및 조회",list(past.keys()),format_func=lambda k:f"🏆 {past[k]['title']} ({past[k].get('date','')})")
    tour=past[sel]
    st.markdown(f"<div class='ic ic-p'>📅 <strong>{tour['title']}</strong> | 일자: {tour.get('date','')} | 장소: {tour.get('place','')}</div>",unsafe_allow_html=True)
    for g,gi in tour.get("groups",{}).items():
        mode,ms=gi["mode"],gi["matches"]; fx=(mode=="고정페어"); sv=stats_fixed(ms) if fx else stats_kdk(ms)
        ranked=sorted(sv.keys(),key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))
        st.markdown(f'<div class="sec sec-p">그룹: {g} ({mode})</div>',unsafe_allow_html=True)
        rows=[]
        for i,item in enumerate(ranked):
            pt=rank_pts(i+1,mode)
            if fx: rows.append({"순위":i+1,"팀":" & ".join(list(item)),"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"부여포인트":pt})
            else:  rows.append({"순위":i+1,"선수":item,"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"부여포인트":pt})
        st.markdown(df_to_html(pd.DataFrame(rows)),unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 메뉴 5. 통합 관리자 통제 센터
# ══════════════════════════════════════════════════════
elif ss.menu=="admin":
    st.markdown("<div class='pg-title c4'>⚙️ 두류 테니스 통제 제어센터</div>",unsafe_allow_html=True)
    pw=st.text_input("🔒 관리자 보안 키 입력",type="password")
    if pw==ADMIN_PW: ss.is_admin=True
    if not ss.is_admin:
        if pw: st.error("❌ 등록되지 않은 보안인증 마스터 키 코드입니다.")
        st.stop()
        
    adm=st.tabs(["📋 회원/보안 설정","🏆 대회 빌더 & 지난대회 수정","👥 당일 출전 수동/자동 매칭 타워","💾 포인트 정산"])

    # 탭 0 : 전체 마스터 명단 및 비밀번호 자체 변경 세션
    with adm[0]:
        st.markdown('<div class="sec sec-t">📝 클럽 마스터 랭킹 회원 명단 등록</div>',unsafe_allow_html=True)
        cur_m=load_members()
        txt_area=st.text_area("구분 기호(줄바꿈 또는 쉼표)로 회원 이름을 기입", value=", ".join(cur_m), height=120)
        if st.button("💾 클럽 회원 데이터베이스 총괄 동기화", type="primary", use_container_width=True):
            parsed=[n.strip() for n in txt_area.replace("\n",",").split(",") if n.strip()]
            save_members(parsed)
            rk_df=load_rank()
            for p in parsed:
                if rk_df.empty or p not in rk_df["이름"].values:
                    nr={c:"" for c in COLS_RANK}; nr["이름"]=p; nr["현재포인트"]=0
                    rk_df=pd.concat([rk_df,pd.DataFrame([nr])],ignore_index=True)
            save_rank(rk_df); st.success("⚙️ 마스터 로스터 풀 리셋 완료."); st.rerun()
            
        st.divider()
        st.markdown('<div class="sec sec-t">🔒 관리자 인증 패스워드 직접 변경</div>',unsafe_allow_html=True)
        new_pwd = st.text_input("새로운 관리자 패스워드 설정", type="password", placeholder="변경할 암호 코드 입력")
        if st.button("🔑 패스워드 변경 승인", use_container_width=True):
            if new_pwd.strip():
                with open("admin_config.json","w") as f: json.dump({"pwd":new_pwd.strip()},f)
                st.success("✅ 암호 코드가 즉시 재설정되었습니다. 다음 로그인부터 적용됩니다."); st.rerun()

    # 탭 1 : 신규 대회 구성 (기본 4그룹 / 각8명 / 고정페어 / 4게임 디폴트 구조 설정) + 지난 대회 수정/삭제
    with adm[1]:
        st.markdown('<div class="sec sec-t">🚀 신규 공식 대회 자동 빌더 개최</div>',unsafe_allow_html=True)
        with st.form("f_create_tour_advanced"):
            tn=st.text_input("대회 공식 명칭 명명",placeholder="예: 두류 테니스 클럽 6월 마스터즈 정기전")
            td=st.date_input("개최 일자 지정",value=date.today())
            tp=st.text_input("테니스 코트 장소",value="두류 테니스장")
            
            st.markdown("⚠️ **대회 포맷 기본 세팅 프로필 (자유 하단 커스텀 가능)**")
            c_ct = st.selectbox("최적화 코트 수 배정 범위 선택", [1, 2, 3, 4, 5], index=1)
            g_count=st.number_input("조정할 총 그룹 개수",1,10,value=4)
            p_count=st.number_input("그룹별 할당 기본 인원",2,30,value=8)
            g_mode = st.selectbox("그룹별 기본 기본 경기방식 대진 포맷", ["고정페어","KDK","단식"], index=0)
            g_game = st.selectbox("그룹별 기본 인당 보장 게임 스코어 수", [3,4,5], index=1)
            
            if st.form_submit_button("🏁 대진 템플릿 기본 활성화 및 개막",use_container_width=True,type="primary"):
                if tn.strip():
                    ts=load_tours(); t_key=f"{td}_{tn.strip()}"
                    ng={}
                    for i in range(int(g_count)):
                        g_label = f"{chr(65+i)}그룹"
                        ng[g_label] = {"players":[],"mode":g_mode,"games":g_game,"matches":[],"player_with_number":{},"size":int(p_count)}
                    ts[t_key]={"title":tn.strip(),"date":str(td),"place":tp,"courts":c_ct,"status":"진행중","groups":ng,"players":[]}
                    save_tours(ts); st.success("✅ 디폴트 설정이 적용된 새 대회가 생성되었습니다."); st.rerun()
                    
        st.divider()
        st.markdown('<div class="sec sec-t">📂 역대 모든 대회 데이터 강제 편집 및 영구 삭제 축</div>',unsafe_allow_html=True)
        ts=load_tours()
        if ts:
            sel_t=st.selectbox("수정/삭제를 진행할 대상 대회 선택",list(ts.keys()),format_func=lambda k:f"[{ts[k].get('status','진행중')}] {ts[k]['title']}")
            curr_t=ts[sel_t]
            c5,c6=st.columns(2)
            with c5:
                s_opts=["진행중","완료","예정"]
                chg_s=st.selectbox("대회 진행 상태값 변경 연동",s_opts,index=s_opts.index(curr_t.get("status","진행중")), key=f"status_chg_{sel_t}")
                if st.button("💾 상태 변경사항 저장 반영",key=f"save_status_btn_{sel_t}",use_container_width=True):
                    curr_t["status"]=chg_s; save_tours(ts); st.success("대회 상태 변경 성공!"); st.rerun()
            with c6:
                st.markdown("<div style='height:28px'></div>",unsafe_allow_html=True)
                if st.button("🗑️ 해당 대회 데이터 영구 파기",type="primary",key=f"del_tour_btn_{sel_t}",use_container_width=True):
                    del ts[sel_t]; save_tours(ts); st.warning("선택된 대회 데이터가 완전히 소멸되었습니다."); st.rerun()

    # 탭 2 : 출전 명단 관리 (체크박스/이름 실시간 팝오버 변경/랭킹 자동 분배 수동 커스텀 인터페이스 총 집합)
    with adm[2]:
        ts=load_tours(); act_tids=[k for k,v in ts.items() if v.get("status")=="진행중"]
        if not act_tids:
            st.info("현재 편집 통제 가능한 '진행중' 상태의 대회가 존재하지 않습니다."); st.stop()
        sel_tid=act_tids[-1]; tour=ts[sel_tid]; cg=tour["groups"]
        
        st.markdown(f"### 👥 {tour['title']} 실시간 참가자 명단 관리 제어 스택")
        
        # 1단계 출석 통제소 (체크박스 구현)
        with st.expander("📝 [1단계] 클럽 전체 로스터 당일 참가 체크박스 필터링", expanded=True):
            all_club = load_members()
            st.markdown("체크 시 오늘 정기전 출전 대기 명단 풀에 즉시 추가됩니다.")
            
            # 저장된 참여자 리스트 기반으로 기본 체크 여부 파싱
            current_day_players = tour.get("players", [])
            checked_players = []
            
            chk_cols = st.columns(3)
            for idx, p_name in enumerate(all_club):
                with chk_cols[idx % 3]:
                    is_present = st.checkbox(p_name, value=(p_name in current_day_players), key=f"chk_pres_{p_name}")
                    if is_present: checked_players.append(p_name)
            
            if st.button("⚡ 체크된 인원 기반 랭킹순(A->B->C->D) 자동 조 편정 실행", type="primary", use_container_width=True):
                if checked_players:
                    rk_df = load_rank()
                    rk_map = {row["이름"]: i for i, row in rk_df.iterrows()}
                    # 마스터 랭킹 가중치 정렬 순차 정밀 처리
                    checked_players.sort(key=lambda x: rk_map.get(x, 999))
                    
                    g_names = list(cg.keys())
                    ptr = 0
                    for gname in g_names:
                        g_sz = cg[gname].get("size", 8)
                        assigned = checked_players[ptr:ptr+g_sz]
                        cg[gname]["players"] = assigned
                        ptr += g_sz
                        
                        # 대진 편성 자동 동기화 
                        ms2, pwn2 = build_matches(assigned, cg[gname]["mode"], cg[gname]["games"])
                        cg[gname]["matches"] = ms2
                        cg[gname]["player_with_number"] = pwn2
                    tour["players"] = checked_players
                    save_tours(ts); st.success("✅ 완벽하게 랭킹 분배 밸런싱 조 편성이 수립되었습니다."); st.rerun()

        st.divider()
        
        # 2단계: 실시간 동적 그룹 파라미터 스케줄링 변조 및 이름 원터치 팝오버 변경 모듈화
        st.markdown("### 🔀 [2단계] 그룹 세부설정 커스텀 및 이름 즉시 교체 런타임")
        
        for gname in list(cg.keys()):
            gdata = cg[gname]
            st.markdown(f"#### 🏷️ **{gname} 설정 구성 변경**")
            
            # 조 이름 동적 변경 모듈
            new_gname = st.text_input(f"조 명칭 수정 (현재: {gname})", value=gname, key=f"rename_input_{gname}")
            if new_gname != gname and new_gname.strip():
                cg[new_gname.strip()] = cg.pop(gname)
                save_tours(ts); st.rerun()
                
            c_m, c_g, c_z = st.columns(3)
            with c_m:
                m_opts=["고정페어","KDK","단식"]
                gdata["mode"] = st.selectbox(f"대진 방식", m_opts, index=m_opts.index(gdata.get("mode","고정페어")), key=f"md_edit_{gname}")
            with c_g:
                gdata["games"] = st.selectbox(f"인당 경기수", [3,4,5], index=[3,4,5].index(gdata.get("games",4)), key=f"gm_edit_{gname}")
            with c_z:
                gdata["size"] = st.number_input(f"조 정원 상한선", 2, 24, value=gdata.get("size",8), key=f"sz_edit_{gname}")
                
            # 텍스트 플로우 인라인 가시화 및 팝오버 명단 교체 아키텍처
            st.markdown("👇 **현재 소속 선수 (이름 클릭 시 실시간 타인으로 수정 가능)**")
            cur_p_list = gdata.get("players", [])
            
            if cur_p_list:
                p_btns = st.columns(4)
                for pi, p_name in enumerate(cur_p_list):
                    with p_btns[pi % 4]:
                        with st.popover(f"👤 {p_name}", use_container_width=True):
                            st.write(f"현재 선수: {p_name}")
                            alt_member_pool = load_members()
                            swap_target = st.selectbox("교체해 넣을 클럽 회원 선택", alt_member_pool, index=alt_member_pool.index(p_name) if p_name in alt_member_pool else 0, key=f"swap_sel_{gname}_{pi}_{p_name}")
                            if st.button("🔄 즉각 대치 변경 승인", key=f"swap_btn_{gname}_{pi}_{p_name}", use_container_width=True):
                                gdata["players"][pi] = swap_target
                                # 조 내 인원 속성 변경 감지로 대진 자동 동기화 트리거
                                ms_sw, pwn_sw = build_matches(gdata["players"], gdata["mode"], gdata["games"])
                                gdata["matches"] = ms_sw; gdata["player_with_number"] = pwn_sw
                                save_tours(ts); st.success("선수 명단 교체 성공"); st.rerun()
                                
            # 텍스트 기반 수동 추가/삭제 보조 서브 도구 상자
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            cc1, cc2 = st.columns(2)
            with cc1:
                cur_club_pool = load_members()
                target_add = st.selectbox(f"➕ {gname}에 보강 수동 투입", [m for m in cur_club_pool if m not in cur_p_list], key=f"quick_add_sel_{gname}")
                if st.button(f"조 선수 추가 실행", key=f"quick_add_btn_{gname}", use_container_width=True):
                    gdata["players"].append(target_add)
                    ms_add, pwn_add = build_matches(gdata["players"], gdata["mode"], gdata["games"])
                    gdata["matches"] = ms_add; gdata["player_with_number"] = pwn_add
                    save_tours(ts); st.rerun()
            with cc2:
                if cur_p_list:
                    target_del = st.selectbox(f"❌ {gname}에서 퇴출 제어", cur_p_list, key=f"quick_del_sel_{gname}")
                    if st.button(f"조 선수 영구 제외", key=f"quick_del_btn_{gname}", use_container_width=True):
                        gdata["players"].remove(target_del)
                        ms_del, pwn_del = build_matches(gdata["players"], gdata["mode"], gdata["games"])
                        gdata["matches"] = ms_del; gdata["player_with_number"] = pwn_del
                        save_tours(ts); st.rerun()
                        
            st.markdown("<div style='height:1px; background:#ddd; margin:15px 0;'></div>", unsafe_allow_html=True)
            
        if st.button("🏁 수동/자동 변동 내역 최종 저장 및 대진 확정", type="primary", use_container_width=True):
            save_tours(ts); st.success("✅ 모든 스케줄러 세션이 마스터 스토리지에 세이브되었습니다."); st.rerun()

    # 탭 3 : 마감 정산 보드
    with adm[3]:
        ts=load_tours(); act_tids=[k for k,v in ts.items() if v.get("status")=="진행중"]
        if not act_tids: st.warning("정산 마감 처리 대상 대회가 존재하지 않습니다."); st.stop()
        t_key=act_tids[-1]; t_obj=ts[t_key]
        
        earn={}
        for gname, gdata in t_obj.get("groups",{}).items():
            mode, ms = gdata["mode"], gdata["matches"]
            fx=(mode=="고정페어"); score_map = stats_fixed(ms) if fx else stats_kdk(ms)
            rk_list = sorted(score_map.keys(), key=lambda x:(-score_map[x]["승"], -score_map[x]["득실"]))
            for i, p_item in enumerate(rk_list):
                pts = rank_pts(i+1, mode)
                if fx:
                    for individual in list(p_item): earn[individual] = earn.get(individual,0) + pts
                else: earn[p_item] = earn.get(p_item,0) + pts
                
        if earn:
            st.markdown('<div class="sec sec-t">🏆 오늘 정기전 누적 정산 예정 포인트 테이블</div>',unsafe_allow_html=True)
            res_df = pd.DataFrame(sorted(earn.items(),key=lambda x:-x[1]),columns=["선수명","지급포인트"])
            st.markdown(df_to_html(res_df),unsafe_allow_html=True)
            
        c_fin, c_rst = st.columns(2)
        with c_fin:
            if st.button("🏆 계산된 점수 마스터 랭킹에 영구 반영 마감",type="primary",use_container_width=True):
                r_master = load_rank()
                for p, p_val in earn.items():
                    if p in r_master["이름"].values:
                        r_master.loc[r_master["이름"]==p, "현재포인트"] += p_val
                    else:
                        new_r = {c:"" for c in COLS_RANK}; new_r["이름"]=p; new_r["현재포인트"]=p_val
                        r_master = pd.concat([r_master, pd.DataFrame([new_r])],ignore_index=True)
                save_rank(r_master); t_obj["status"]="완료"; save_tours(ts)
                st.success("✅ 완벽하게 최종 포인트가 이관 및 정산 마감 완료 처리되었습니다."); st.rerun()
        with c_rst:
            if st.button("🚨 입력된 경기 라이브 스코어 전부 0:0 초기화",use_container_width=True):
                for gname in t_obj.get("groups",{}):
                    for m in t_obj["groups"][gname]["matches"]: m["s1"]=0; m["s2"]=0
                save_tours(ts); st.success("✅ 경기 점수판 리셋 완료."); st.rerun()
