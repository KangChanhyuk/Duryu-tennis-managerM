import streamlit as st
import pandas as pd
import random, os, json, requests, base64
from datetime import date, datetime
from io import BytesIO

st.set_page_config(page_title="두류 테니스", page_icon="🎾",
                   layout="centered", initial_sidebar_state="collapsed")

# 🎨 디자인 시스템 및 레이아웃 통합 스타일
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght=400;500;700;900&display=swap');
:root{
  --g0:#1B5E20;--g2:#2E7D32;--g3:#4CAF50;--g5:#F1F8E9;
  --nav0:#2E7D32;--nav1:#1565C0;--nav2:#E65100;--nav3:#4A148C;--nav4:#00695C;
  --mc0:#1B5E20;--mc1:#0D47A1;--mc2:#BF360C;--mc3:#4A148C;
  --mc4:#006064;--mc5:#1A237E;--mc6:#880E4F;--mc7:#33691E;
  --tb0:#2E7D32;--tb1:#1565C0;--tb2:#D84315;--tb3:#6A1B9A;
  --tb4:#00695C;--tb5:#283593;--tb6:#AD1457;--tb7:#558B2F;
  --yel:#FFD600;--ora:#FB8C00;
  --bg:#F4F6F8;--card:#ffffff;--bd:#E0E4E8;
  --r1:10px;--r2:14px;
  --sh:0 2px 8px rgba(0,0,0,.06);--sh2:0 4px 16px rgba(0,0,0,.1);
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent;}

html, body, [data-testid="stAppViewContainer"] :not(i):not(svg):not([class*="material-icons"]) {
    font-family: 'Noto Sans KR', sans-serif;
}

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
    font-size: 0.7rem !important;
    padding: 6px 4px !important;
    white-space: normal !important;
    word-break: keep-all !important;
  }
}

.hdr{background:linear-gradient(135deg,#1B5E20 0%,#2E7D32 60%,#388E3C 100%);margin:0 -0.6rem 0;padding:15px 16px;position:relative;overflow:hidden;box-shadow:var(--sh2);border-bottom-left-radius:8px;border-bottom-right-radius:8px;}
.hdr::after{content:'🎾';position:absolute;right:14px;top:10px;font-size:2.2rem;opacity:.15;}
.hdr-title{color:#fff;font-size:1.15rem;font-weight:900;margin:0 0 2px;}
.hdr-sub{color:rgba(255,255,255,.6);font-size:.58rem;letter-spacing:2px;}

.pg-title{color:#fff;padding:11px 14px;border-radius:var(--r2);margin:0 0 12px;font-size:.95rem;font-weight:900;text-align:center;box-shadow:var(--sh2);}
.c0{background:linear-gradient(135deg,var(--nav0),#43A047);}
.c1{background:linear-gradient(135deg,var(--nav1),#1976D2);}
.c2{background:linear-gradient(135deg,var(--nav2),#F4511E);}
.c3{background:linear-gradient(135deg,var(--nav3),#7B1FA2);}
.c4{background:linear-gradient(135deg,var(--nav4),#00897B);}

.sec{font-size:.85rem;font-weight:800;color:var(--g0);border-left:4px solid var(--g3);padding-left:8px;margin:18px 0 8px;}
.sec-b{color:var(--nav1);border-left-color:var(--nav1);}
.sec-o{color:var(--nav2);border-left-color:var(--nav2);}
.sec-p{color:var(--nav3);border-left-color:var(--nav3);}
.sec-t{color:var(--nav4);border-left-color:var(--nav4);}

.ic{background:var(--card);border-left:4px solid var(--g3);border-radius:var(--r1);padding:10px 14px;margin:8px 0;box-shadow:var(--sh);font-size:.8rem;color:#2C3E50;line-height:1.4;}
.ic-b{border-left-color:var(--nav1);}
.ic-o{border-left-color:var(--nav2);}
.ic-p{border-left-color:var(--nav3);}
.ic-t{border-left-color:var(--nav4);}

button[data-baseweb="tab"]{font-size:.7rem!important;font-weight:700!important;padding:8px 6px!important;border-radius:var(--r1) var(--r1) 0 0!important;min-height:38px!important;}
button[data-baseweb="tab"][aria-selected="true"]{background:linear-gradient(135deg,var(--g0),var(--g2))!important;color:#fff!important;}
[data-baseweb="tab-list"]{background:#E0E4E8!important;border-radius:var(--r1) var(--r1) 0 0!important;padding:4px 4px 0!important;gap:3px!important;}

.mx-wrap{background:var(--card);border-radius:var(--r1);padding:6px;box-shadow:var(--sh);overflow-x:auto;margin:8px 0;border:1px solid var(--bd);width:100%;}
.mx{border-collapse:collapse;white-space:nowrap;font-size:.75rem;width:100%;table-layout:auto;}
.mx th,.mx td{padding:9px 10px;border:1px solid var(--bd);text-align:center!important;vertical-align:middle!important;}
.mx thead th{background:var(--g0);color:#fff;font-weight:700;}
.mx tbody tr:nth-child(even) td{background:var(--g5);}
.mx-grey{background:#ECEFF1!important;color:#B0BEC5!important;font-weight:normal;}
.mx-dash{color:#CFD8DC;}
.mx-sc{font-weight:800;color:#2E7D32;background:#F1F8E9;}

.kdk{background:var(--card);border-radius:var(--r1);padding:8px;box-shadow:var(--sh);overflow-x:auto;margin:8px 0;border:1px solid var(--bd);}
.kdk table{border-collapse:collapse;white-space:nowrap;font-size:.68rem;width:100%;}
.kdk th,.kdk td{padding:6px;border:1px solid var(--bd);text-align:center;vertical-align:middle;}
.kdk thead th{background:var(--g2);color:#fff;font-weight:700;}

.match-card{background:var(--card);border-radius:var(--r2);padding:12px 10px;margin:12px 0;box-shadow:var(--sh2);border:1px solid var(--bd);}
.match-no{display:inline-block;border-radius:20px;padding:3px 12px;font-size:.6rem;font-weight:900;margin-bottom:10px;color:#fff;}
.mc0{background:var(--mc0);}.mc1{background:var(--mc1);}.mc2{background:var(--mc2);}
.mc3{background:var(--mc3);}.mc4{background:var(--mc4);}.mc5{background:var(--mc5);}
.mc6{background:var(--mc6);}.mc7{background:var(--mc7);}

.team-nm{border-radius:8px;padding:8px 4px;font-weight:900;font-size:clamp(.65rem,2.8vw,.85rem);text-align:center;color:#fff;box-shadow:var(--sh);min-height:42px;display:flex;align-items:center;justify-content:center;word-break:keep-all;line-height:1.2;}
.tb0{background:var(--tb0);}.tb1{background:var(--tb1);}.tb2{background:var(--tb2);}
.tb3{background:var(--tb3);}.tb4{background:var(--tb4);}.tb5{background:var(--tb5);}
.tb6{background:var(--tb6);}.tb7{background:var(--tb7);}

.vs-badge{width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,#FFB74D,#FB8C00);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:.55rem;color:#fff;box-shadow:var(--sh);margin:0 auto;}

.ctrl-num{display:flex;align-items:center;justify-content:center;background:#fff;border:2px solid #A5D6A7;border-radius:8px;font-size:clamp(1.1rem,5.5vw,1.5rem);font-weight:900;color:#1B5E20;height:42px;width:100%;}
.ctrl-row .stButton>button{height:42px!important;min-height:42px!important;max-height:42px!important;font-size:clamp(.9rem,4.5vw,1.3rem)!important;font-weight:900!important;padding:0!important;border-radius:8px!important;background:#E8F5E9!important;color:#1B5E20!important;border:2px solid #A5D6A7!important;box-shadow:none!important;width:100%;}

.stButton>button{border-radius:var(--r2)!important;font-weight:700!important;font-size:.8rem!important;min-height:46px!important;padding:9px 12px!important;}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,var(--g0),var(--g2))!important;color:#fff!important;border:none!important;box-shadow:0 4px 12px rgba(46,125,50,.3)!important;}

.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stSelectbox>div>div{min-height:44px!important;border-radius:var(--r1)!important;}
[data-testid="stFileUploaderDropzone"]{border:2px dashed var(--g3)!important;background:var(--g5)!important;}

.matrix-input-box div[data-baseweb="input"] {
    min-height: 28px !important;
    background: transparent !important;
}
.matrix-input-box input {
    min-height: 28px !important;
    padding: 2px 4px !important;
    font-size: 0.72rem !important;
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)

# 💾 데이터 및 동기화 설정
REPO = "자신의_깃허브_아이디/레포지토리_이름"
TOKEN = st.secrets.get("GITHUB_TOKEN", "")

def push_to_github(filepath, commit_msg="Update data"):
    if not TOKEN or "자신의_깃허브" in REPO: return False
    try:
        url = f"https://api.github.com/repos/{REPO}/contents/{filepath}"
        headers = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}
        res = requests.get(url, headers=headers)
        sha = res.json().get("sha") if res.status_code == 200 else None
        with open(filepath, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")
        payload = {"message": commit_msg, "content": content}
        if sha: payload["sha"] = sha
        requests.put(url, headers=headers, json=payload)
        return True
    except Exception:
        return False

RANK_FILE   = "ranking_master.csv"
TOUR_FILE   = "tournaments.json"
MEMBER_FILE = "member_roster_backup.json"
CONFIG_FILE = "config_backup.json"

COLS_RANK   = ["랭킹", "이름", "현재포인트", "부과점", "비고", "대회포인트"]

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE,"r") as f: return json.load(f)
    return {"admin_pw":"0502"}

def save_config(cfg):
    with open(CONFIG_FILE,"w") as f: json.dump(cfg,f,ensure_ascii=False,indent=2)
    push_to_github(CONFIG_FILE, "Backup config")

def get_admin_pw():
    return load_config().get("admin_pw","0502")

GCLS  = ["mc0","mc1","mc2","mc3","mc4","mc5","mc6","mc7"]
TBCLS = ["tb0","tb1","tb2","tb3","tb4","tb5","tb6","tb7"]
GLBL  = ["🟢","🔵","🟠","🟣","🩵","🔴","🟡","⚪"]

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
    if os.path.exists(RANK_FILE):
        df = pd.read_csv(RANK_FILE).dropna(subset=["이름"])
        if "대회포인트" not in df.columns: df["대회포인트"] = 0
        if "부과점" not in df.columns: df["부과점"] = 0
        if "비고" not in df.columns: df["비고"] = ""
        
        for c in ["현재포인트","부과점","대회포인트"]:
            if c in df.columns: df[c]=pd.to_numeric(df[c],errors="coerce").fillna(0)
        
        # 📈 부과점과 대회포인트를 합산한 현재포인트를 구한 뒤 내림차순 정렬
        df["현재포인트"] = df["대회포인트"] + df["부과점"]
        df = df.sort_values(by="현재포인트", ascending=False).reset_index(drop=True)
        df["랭킹"] = df.index + 1
        return df.fillna("")
    return pd.DataFrame(columns=COLS_RANK)

def save_rank(df):
    df["대회포인트"] = pd.to_numeric(df["대회포인트"], errors="coerce").fillna(0)
    df["부과점"] = pd.to_numeric(df["부과점"], errors="coerce").fillna(0)
    df["현재포인트"] = df["대회포인트"] + df["부과점"]
    
    # 📈 저장하기 전 다시 한 번 확실하게 현재포인트 기준 내림차순 정렬 후 순위 재생성
    df = df.sort_values(by="현재포인트", ascending=False).reset_index(drop=True)
    df["랭킹"] = df.index + 1
    
    for c in COLS_RANK:
        if c not in df.columns: df[c] = ""
    df = df[COLS_RANK]
    
    df.fillna("").to_csv(RANK_FILE, index=False, encoding="utf-8-sig")
    push_to_github(RANK_FILE, "Backup ranking master")

def load_members():
    if os.path.exists(MEMBER_FILE):
        with open(MEMBER_FILE,"r") as f: return json.load(f)
    df=load_rank(); return df["이름"].tolist() if not df.empty else []

def save_members(names):
    with open(MEMBER_FILE,"w") as f: json.dump(names,f,ensure_ascii=False,indent=2)
    push_to_github(MEMBER_FILE, "Backup member roster")

def load_tours():
    if os.path.exists(TOUR_FILE):
        with open(TOUR_FILE,"r") as f: return json.load(f)
    return {}

def save_tours(d):
    with open(TOUR_FILE,"w") as f: json.dump(d,f,ensure_ascii=False,indent=2)
    push_to_github(TOUR_FILE, "Backup tournament status")

def to_excel(df):
    buf=BytesIO(); df.to_excel(buf,index=False); return buf.getvalue()

def read_file(up):
    name=up.name.lower()
    if name.endswith(("xlsx","xls")): return pd.read_excel(up)
    return pd.read_csv(up,encoding_errors="replace")

def df_to_html(df, is_master=False):
    if df.empty: return "<div class='ic'>데이터가 없습니다.</div>"
    
    # 🛠️ 중요 고정: 메인 마스터 보드의 6개 항목 순서를 온전하게 강제 유지 및 설정
    if is_master:
        cols = ["랭킹", "이름", "현재포인트", "부과점", "비고", "대회포인트"]
    else:
        cols = [c for c in ["랭킹", "이름", "현재포인트", "부과점", "비고", "대회포인트"] if c in df.columns]
        if not cols: cols = df.columns.tolist()
    
    h = "".join(f"<th>{c}</th>" for c in cols)
    body = ""
    for _, row in df.iterrows():
        cells = ""
        for c in cols:
            val = row.get(c, "")
            if isinstance(val, float) and not pd.isna(val) and val == int(val): val = int(val)
            cells += f"<td>{val}</td>"
        body += f"<tr>{cells}</tr>"
    return f'<div class="mx-wrap"><table class="mx"><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table></div>'

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

def stats_team(matches):
    s = {}
    for m in matches:
        team1, team2 = m.get("team1", "A팀"), m.get("team2", "B팀")
        if team1 not in s: s[team1] = {"승":0, "패":0, "득실":0, "매치승":0, "매치패":0}
        if team2 not in s: s[team2] = {"승":0, "패":0, "득실":0, "매치승":0, "매치패":0}
        a, b = int(m["s1"]), int(m["s2"])
        if a > b:
            s[team1]["매치승"] += 1; s[team2]["매치패"] += 1
        elif b > a:
            s[team2]["매치승"] += 1; s[team1]["매치패"] += 1
        s[team1]["득실"] += a - b
        s[team2]["득실"] += b - a
    return s

def rank_pts(rank,mode):
    if mode in ["고정페어", "팀전"]: return {1:7,2:5,3:3}.get(rank,1)
    return 7 if rank<=2 else (5 if rank<=4 else (3 if rank<=6 else 1))

def grade_fixed(rank):
    if rank == 1: return "🥇 우승"
    elif rank == 2: return "🥈 준우승"
    elif rank == 3: return "🥉 3위"
    return "참가"

def grade_kdk(rank):
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
    ms=[{"t1":list(pairs[i]),"t2":list(pairs[j]),"s1":0,"s2":0} for i in range(len(pairs)) for j in range(i+1,len(pairs))]
    random.shuffle(ms); return ms,{}

def make_singles(players):
    pl=players[:]; random.shuffle(pl)
    ms=[{"t1":[pl[i]],"t2":[pl[j]],"s1":0,"s2":0} for i in range(len(pl)) for j in range(i+1,len(pl))]
    random.shuffle(ms); return ms,{}

def kdk_html(n,gperson,p2n):
    bp=KDK_3G.get(n) if gperson==3 else KDK_4G.get(n)
    if not bp: return ""
    n2p={v:k for k,v in p2n.items()}; rows=""
    for i,(a,b,c,d) in enumerate(bp):
        t1=f"{n2p.get(a,a)}({a}) & {n2p.get(b,b)}({b})"
        t2=f"{n2p.get(c,c)}({c}) & {n2p.get(d,d)}({d})"
        rows+=f"<tr><td><span style='background:#2E7D32;color:#fff;border-radius:12px;padding:2px 8px;font-size:.62rem;font-weight:700'>{i+1}</span></td><td style='text-align:left!important;'>{t1} <b>vs</b> {t2}</td></tr>"
    return f'<div class="kdk"><div style="font-size:.75rem;font-weight:800;color:#1B5E20;margin-bottom:6px">📋 KDK 대진 정보 (1인 {gperson}게임)</div><table><thead><tr><th style="width:50px;">순서</th><th>대진 매칭</th></tr></thead><tbody>{rows}</tbody></table></div>'

def matrix_html(matches,rank_items,mode,p2n):
    if not matches or not rank_items: return ""
    is_fixed = (mode == "고정페어")
    if mode == "팀전": return ""
    lab={t:"&".join(list(t)) for t in rank_items} if is_fixed else {p:f"{p}({p2n.get(p,'?')})" for p in rank_items}
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
        cells=""
        for c in keys:
            val = mat[r][c]
            if ":" in val: cells += f"<td class='mx-sc'>{val}</td>"
            elif "■" in val: cells += f"<td class='mx-grey'>{val}</td>"
            else: cells += f"<td class='mx-dash'>{val}</td>"
        body+=f"<tr><td style='font-weight:700;background:#F1F8E9;color:#1B5E20;'>{r}</td>{cells}</tr>"
    return f'<div class="mx-wrap"><table class="mx"><thead><tr><th style="background:#1B5E20;">구분</th>{header}</tr></thead><tbody>{body}</tbody></table></div>'

def redistribute_players_by_ranking(tour):
    r_df = load_rank()
    master_order = r_df["이름"].tolist() if not r_df.empty else []
    chosen_p = tour.get("players", [])
    chosen_p_sorted = [p for p in master_order if p in chosen_p]
    chosen_p_sorted += [p for p in chosen_p if p not in chosen_p_sorted]
    
    current_index = 0
    for gname, gdata in tour.get("groups", {}).items():
        size = gdata.get("size", 8)
        gdata["players"] = chosen_p_sorted[current_index : current_index + size]
        current_index += size

ss=st.session_state
if "menu" not in ss: ss.menu="ranking"
if "is_admin" not in ss: ss.is_admin=False

st.markdown("<div class='hdr'><div class='hdr-title'>두류 테니스 클럽</div><div class='hdr-sub'>DURYU TENNIS CLUB SYSTEM</div></div><div style='height:18px'></div>",unsafe_allow_html=True)

m_cols=st.columns(5)
m_items=[("ranking","🏆 랭킹"),("schedule","📅 대진"),("result","🎾 결과"),("admin","⚙️ 관리"),("config","🛠️ 설정")]
for idx,(m_id,m_lb) in enumerate(m_items):
    with m_cols[idx]:
        if st.button(m_lb,key=f"m_btn_{m_id}",use_container_width=True,type="primary" if ss.menu==m_id else "secondary"):
            ss.menu=m_id; st.rerun()

# ----------------- [1. 🏆 메인 마스터 랭킹 탭] -----------------
if ss.menu=="ranking":
    st.markdown("<div class='pg-title c0'>🏆 마스터 랭킹 보드</div>",unsafe_allow_html=True)
    df=load_rank()
    if df.empty: st.markdown("<div class='ic'>📋 등록된 랭킹 데이터 파일이 비어 있습니다.</div>",unsafe_allow_html=True)
    else: 
        # 🛠️ 중요 고정: is_master=True 를 사용하여 6개 항목이 온전하게 노출되도록 강제 보정
        st.markdown(df_to_html(df, is_master=True),unsafe_allow_html=True)
        st.download_button("Excel 다운로드",data=to_excel(df),file_name=f"랭킹_{date.today()}.xlsx",use_container_width=True)

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
            gi=tour["groups"][g]; ms=gi["matches"]; mode=gi.get("mode","KDK"); p2n=gi.get("player_with_number",{})
            fx=(mode=="고정페어"); tm=(mode=="팀전")
            
            if tm:
                st.markdown("<div class='sec sec-b'>📋 팀전 종합 스코어 보드</div>",unsafe_allow_html=True)
                tsv = stats_team(ms)
                t_ranked = sorted(list(tsv.keys()))
                t_rows = []
                for i, t_nm in enumerate(t_ranked):
                    t_rows.append({"팀명": t_nm, "매치 전적": f"{tsv[t_nm]['매치승']}승 / {tsv[t_nm]['매치패']}패", "게임 득실차": f"{tsv[t_nm]['득실']:+d}"})
                st.markdown(df_to_html(pd.DataFrame(t_rows)),unsafe_allow_html=True)
            else:
                sv=stats_fixed(ms) if fx else stats_kdk(ms); rit=list(sv.keys())
                st.markdown("<div class='sec sec-b'>📋 대진 매트릭스 전적 현황</div>",unsafe_allow_html=True)
                st.markdown(matrix_html(ms,rit,mode,p2n),unsafe_allow_html=True)
                if mode=="KDK" and p2n: st.markdown(kdk_html(len(p2n),gi.get("games",4),p2n),unsafe_allow_html=True)
                st.markdown("<div class='sec sec-b'>🏅 그룹 현재 실시간 순위</div>",unsafe_allow_html=True)
                if rit:
                    ranked=sorted(rit,key=lambda x:(-sv[x]["승"],-sv[x]["득실"])); rows=[]
                    for i,item in enumerate(ranked):
                        if fx: rows.append({"순위":i+1,"팀명":" & ".join(list(item)),"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"결과":grade_fixed(i+1)})
                        else: rows.append({"순위":i+1,"선수명":item,"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"결과":grade_kdk(i+1)})
                    st.markdown(df_to_html(pd.DataFrame(rows)),unsafe_allow_html=True)
            
            st.markdown("<div class='sec sec-b'>🎾 경기 결과 스코어 입력</div>",unsafe_allow_html=True)
            for mi,m in enumerate(ms):
                t1s=" & ".join(m["t1"]); t2s=" & ".join(m["t2"])
                if tm:
                    t1s = f"[{m.get('team1','A팀')}] {t1s}"
                    t2s = f"[{m.get('team2','B팀')}] {t2s}"
                mc=GCLS[mi%len(GCLS)]; tbc=TBCLS[mi%len(TBCLS)]; s1v=int(m["s1"]); s2v=int(m["s2"])
                st.markdown(f'<div class="match-card"><span class="match-no {mc}">MATCH {mi+1}</span>',unsafe_allow_html=True)
                nA,nVS,nB=st.columns([5,1,5])
                with nA: st.markdown(f'<div class="team-nm {tbc}">{t1s}</div>',unsafe_allow_html=True)
                with nVS: st.markdown('<div style="height:40px;display:flex;align-items:center;justify-content:center;"><div class="vs-badge">VS</div></div>',unsafe_allow_html=True)
                with nB: st.markdown(f'<div class="team-nm {tbc}">{t2s}</div>',unsafe_allow_html=True)
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

elif ss.menu=="result":
    st.markdown("<div class='pg-title c2'>🎾 대회 최종 결과 보고</div>",unsafe_allow_html=True)
    tours=load_tours(); t_done=[k for k,v in tours.items() if v.get("status")=="완료"]
    if not t_done: st.markdown("<div class='ic ic-o'>ℹ️ 마감 완료된 대회가 아직 존재하지 않습니다.</div>",unsafe_allow_html=True); st.stop()
    sel_tid=st.selectbox("🏆 지난 대회 아카이브 선택",t_done[::-1],format_func=lambda x: tours[x]["title"])
    tour=tours[sel_tid]
    st.markdown(f"<div class='ic ic-o'><b>🏆 {tour['title']} 공식 결과</b><br>📍 일자: {tour.get('date','')} | 장소: {tour.get('place','')}</div>",unsafe_allow_html=True)
    for g,gi in tour.get("groups",{}).items():
        ms=gi["matches"]; mode=gi.get("mode","KDK"); fx=(mode=="고정페어"); tm=(mode=="팀전")
        st.markdown(f'<div class="sec sec-p">Group {g} ({mode})</div>',unsafe_allow_html=True)
        if tm:
            tsv = stats_team(ms)
            t_ranked = sorted(list(tsv.keys()))
            t_rows = []
            for i, t_nm in enumerate(t_ranked):
                t_rows.append({"팀명": t_nm, "최종 매치 전적": f"{tsv[t_nm]['매치승']}승 / {tsv[t_nm]['매치패']}패", "총 게임 득실": f"{tsv[t_nm]['득실']:+d}"})
            st.markdown(df_to_html(pd.DataFrame(t_rows)),unsafe_allow_html=True)
        else:
            sv=stats_fixed(ms) if fx else stats_kdk(ms); rit=list(sv.keys())
            if rit:
                ranked=sorted(rit,key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))
                rows=[]
                for i,item in enumerate(ranked):
                    pt=rank_pts(i+1,mode)
                    if fx: rows.append({"순위":i+1,"팀명":" & ".join(list(item)),"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"획득포인트":pt,"비고":grade_fixed(i+1)})
                    else: rows.append({"순위":i+1,"선수명":item,"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"획득포인트":pt,"비고":grade_kdk(i+1)})
                st.markdown(df_to_html(pd.DataFrame(rows)),unsafe_allow_html=True)

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
    init_pw=st.text_input("비밀번호 강제 초기화 (마스터 키)",type="password",key="cfg_init_pw")
    if st.button("🔄 시스템 암호 0502 초기화 실행",use_container_width=True):
        if init_pw=="duryu0502": cfg=load_config(); cfg["admin_pw"]="0502"; save_config(cfg); st.success("✅ 비밀번호가 '0502'로 완전히 초기화되었습니다."); st.rerun()
        else: st.error("❌ 마스터 암호키가 일치하지 않습니다.")

# ----------------- [4. ⚙️ 관리자 탭 통합 관제] -----------------
elif ss.menu=="admin":
    st.markdown("<div class='pg-title c4'>⚙️ 관리자 관제 센터</div>",unsafe_allow_html=True)
    pw=st.text_input("🔒 패스워드 인증",type="password",placeholder="암호코드 입력")
    if pw==get_admin_pw(): ss.is_admin=True
    if not ss.is_admin:
        if pw: st.error("❌ 패스워드가 올바르지 않습니다.")
        st.stop()
        
    adm=st.tabs(["🏆 대회 관리","👥 참가자 명단 조율","💾 포인트 정산 & 명부 통합 수정"])

    with adm[0]:
        ts=load_tours()
        st.markdown('<div class="sec sec-t">✨ 새로운 신규 대회 개설 및 진행 대회 수정</div>',unsafe_allow_html=True)
        active_tids=[k for k,v in ts.items() if v.get("status")=="진행중"]
        is_edit_mode = len(active_tids) > 0
        
        if is_edit_mode:
            target_tid = active_tids[-1]
            edit_tour = ts[target_tid]
            st.info(f"🔄 현재 진행 중인 대회가 존재하여 **[대회 정보 수정 모드]**로 자동 전환되었습니다.")
            init_tn = edit_tour.get("title", "")
            try: init_td = datetime.strptime(edit_tour.get("date", str(date.today())), "%Y-%m-%d").date()
            except: init_td = date.today()
            init_tp = edit_tour.get("place", "두류 테니스장")
            init_co = int(edit_tour.get("courts", 3))
            init_gc = str(len(edit_tour.get("groups", {})))
        else:
            st.success(f"✨ 진행 중인 대회가 없습니다. **[신규 대회 개설 모드]**")
            init_tn = f"{date.today().strftime('%m월 %d일')} 두류 정기전"
            init_td = date.today()
            init_tp = "두류 테니스장"
            init_co = 3
            init_gc = "2"
            
        tn=st.text_input("🏆 대회 명칭 명명", value=init_tn)
        td=st.date_input("📅 개최 일정 확정", value=init_td)
        tp=st.text_input("📍 경기 장소 지정", value=init_tp)
        co=st.number_input("🎾 할당 코트 면적 수", 1, 20, value=init_co)
        g_count=st.selectbox("👥 대진 구성 그룹 총 수", ["1","2","3","4","5","6","7","8"], index=["1","2","3","4","5","6","7","8"].index(init_gc))
        
        if is_edit_mode:
            if st.button("💾 진행중인 대회 정보 수정 및 그룹 재편성 적용", type="primary", use_container_width=True):
                if tn.strip():
                    target_tid = active_tids[-1]
                    ts[target_tid]["title"] = tn.strip()
                    ts[target_tid]["date"] = str(td)
                    ts[target_tid]["place"] = tp
                    ts[target_tid]["courts"] = co
                    
                    new_g_count = int(g_count)
                    existing_groups = ts[target_tid].get("groups", {})
                    updated_groups = {}
                    
                    for i in range(new_g_count):
                        g_letter = chr(64 + (i+1)) + "그룹"
                        if g_letter in existing_groups:
                            updated_groups[g_letter] = existing_groups[g_letter]
                        else:
                            updated_groups[g_letter] = {"players":[], "mode":"KDK", "games":4, "matches":[], "player_with_number":{}, "size":8}
                    
                    ts[target_tid]["groups"] = updated_groups
                    redistribute_players_by_ranking(ts[target_tid])
                    save_tours(ts)
                    st.success("✅ 진행 중인 대회 정보 및 그룹 연동 체계가 실시간 업데이트되었습니다."); st.rerun()
                else: st.warning("대회 이름을 명확히 입력하십시오.")
        else:
            if st.button("🚀 새 대회 신설 공식 개막", use_container_width=True, type="primary"):
                if tn.strip():
                    t_key=f"{td}_{tn.strip()}"
                    ng={f"{chr(65+i)}그룹":{"players":[],"mode":"KDK","games":4,"matches":[],"player_with_number":{},"size":8} for i in range(int(g_count))}
                    ts[t_key]={"title":tn.strip(),"date":str(td),"place":tp,"courts":co,"status":"진행중","groups":ng,"players":[]}
                    save_tours(ts); st.success(f"✅ 대회 '{tn.strip()}'가 생성되었습니다."); st.rerun()
                else: st.warning("대회 이름을 명확히 입력하십시오.")
        st.divider()
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
                del_pw = st.text_input("⚠️ 삭제 확인 비밀번호", type="password", key="del_tour_pw_input", placeholder="관리자 패스워드 입력")
                if st.button("🗑️ 해당 대회 데이터 영구 삭제",type="primary",use_container_width=True):
                    if del_pw == get_admin_pw():
                        del ts[sel_t]; save_tours(ts); st.warning("대회가 삭제되었습니다."); st.rerun()
                    else: st.error("❌ 삭제 비밀번호가 일치하지 않습니다.")

    with adm[1]:
        ts=load_tours(); act_tids=[k for k,v in ts.items() if v.get("status")=="진행중"]
        if not act_tids: st.info("현재 진행 중인 대회가 존재하지 않습니다."); st.stop()
        sel_tid=act_tids[-1]; tour=ts[sel_tid]
        if "groups" not in tour:
            tour["groups"] = {"A그룹":{"players":[],"mode":"KDK","games":4,"matches":[],"player_with_number":{},"size":8}}
            save_tours(ts)
        cg=tour["groups"]
        st.markdown(f"### 👥 {tour['title']} 참가자 조율")
        all_m=load_members()
        if not all_m: st.warning("회원 명단이 비어 있습니다. 아래 탭에서 회원 명단을 먼저 등록하세요."); st.stop()
        st.markdown("#### [1단계] 당일 참가자 선택")
        saved_p=tour.get("players", [])
        if "sel_all_trigger" not in ss: ss.sel_all_trigger = None
        c_sel1, c_sel2 = st.columns(2)
        with c_sel1:
            if st.button("✅ 전체 회원 체크", use_container_width=True):
                ss.sel_all_trigger = True; st.rerun()
        with c_sel2:
            if st.button("❌ 전체 체크 해제", use_container_width=True):
                ss.sel_all_trigger = False; st.rerun()
        if ss.sel_all_trigger is True:
            def_players = all_m; ss.sel_all_trigger = None
        elif ss.sel_all_trigger is False:
            def_players = []; ss.sel_all_trigger = None
        else:
            def_players = [p for p in saved_p if p in all_m]
        chosen_p = st.multiselect("출전 선수 직접 선택", options=all_m, default=def_players, key="multiselect_players_act")

        text_p_input = st.text_area(
            "✍️ 출전 선수 텍스트 직접 추가/편집 (이름을 쉼표로 구분)",
            value=", ".join(chosen_p), height=80, key="text_area_players_act"
        )
        final_chosen_p = [n.strip() for n in text_p_input.replace("\n",",").split(",") if n.strip()]

        if st.button("💾 참가 명단 저장 및 랭킹정렬 분배", use_container_width=True, type="primary"):
            tour["players"] = final_chosen_p
            redistribute_players_by_ranking(tour)
            save_tours(ts); st.success(f"당일 명단 {len(final_chosen_p)}명 저장 및 그룹별 자동 정렬 분배 완료!")
            st.divider()
        
        st.markdown("#### [2단계] 그룹별 세부 배정")
        for gname, gdata in list(tour["groups"].items()):
            st.markdown(f"##### 🏷️ **{gname}** 설정")
            c_m, c_g, c_z = st.columns(3)
            with c_m:
                m_opts=["KDK","고정페어","단식","팀전"]
                gdata["mode"] = st.selectbox(f"방식 ({gname})", m_opts, index=m_opts.index(gdata.get("mode","KDK")), key=f"md_edit_{gname}")
            with c_g: gdata["games"] = st.selectbox(f"인당 게임 수 ({gname})", [3,4,5], index=[3,4,5].index(gdata.get("games",4)), key=f"gm_edit_{gname}")
            with c_z: 
                old_size = gdata.get("size", 8)
                new_size = st.number_input(f"정원 ({gname})", 2, 50, value=old_size, key=f"sz_edit_{gname}")
                if new_size != old_size:
                    gdata["size"] = new_size
                    redistribute_players_by_ranking(tour)
                    save_tours(ts)
                    st.rerun()

            cur_grp_players = gdata.get("players", [])
            if gdata["mode"] == "팀전":
                st.info("💡 **팀전 안내**: 아래 텍스트박스에 양 팀의 명단을 적고, [3단계]에서 대진을 상세 설정하세요.")
            
            grp_text_input = st.text_area(
                f"✍️ {gname} 명단 직접 편집 (쉼표 구분)",
                value=", ".join(cur_grp_players), height=80, key=f"grp_txt_{gname}"
            )
            gdata["players"] = [n.strip() for n in grp_text_input.replace("\n",",").split(",") if n.strip()]

        if st.button("💾 모든 그룹 셋팅값 & 소속 선수 백업", key="save_grp_configs_btn", type="primary", use_container_width=True):
            save_tours(ts); st.success("⚙️ 모든 설정이 저장되었습니다."); st.rerun()
        st.divider()
        
        st.markdown("#### [3단계] 대진표 최종 빌드")
        has_team_mode = any(gdata.get("mode") == "팀전" for gname, gdata in tour["groups"].items())
        if has_team_mode:
            st.markdown("<div class='sec sec-o'>📋 팀전(단체전) 대진 수동 상세 입력 세션</div>", unsafe_allow_html=True)
            for gname, gdata in tour["groups"].items():
                if gdata.get("mode") == "팀전":
                    st.markdown(f"**[{gname} - 리그전 대진 설정]**")
                    tm_num = st.number_input(f"{gname} 총 경기 매치 개수", 1, 30, value=len(gdata.get("matches", [])) if gdata.get("matches") else 3, key=f"tm_num_{gname}")
                    
                    custom_matches = []
                    for mi in range(tm_num):
                        st.markdown(f"**🔹 MATCH {mi+1}**")
                        ex_m = gdata.get("matches", [])[mi] if (gdata.get("matches") and mi < len(gdata["matches"])) else {}
                        
                        col_t1, col_t2 = st.columns(2)
                        with col_t1:
                            t1_name = st.text_input(f"M{mi+1} 1팀명", value=ex_m.get("team1",""), key=f"tm_t1_{gname}_{mi}")
                        with col_t2:
                            t2_name = st.text_input(f"M{mi+1} 2팀명", value=ex_m.get("team2",""), key=f"tm_t2_{gname}_{mi}")
                            
                        sc1, sc2 = st.columns(2)
                        with sc1:
                            s1_val = st.number_input(f"M{mi+1} 1팀 점수", 0, 99, value=int(ex_m.get("s1",0)), key=f"tm_s1_{gname}_{mi}")
                        with sc2:
                            s2_val = st.number_input(f"M{mi+1} 2팀 점수", 0, 99, value=int(ex_m.get("s2",0)), key=f"tm_s2_{gname}_{mi}")
                        
                        custom_matches.append({"t1":[], "t2":[], "s1":s1_val, "s2":s2_val, "team1":t1_name, "team2":t2_name})
                    
                    if st.button(f"💾 {gname} 팀전 대진 생성 및 확정", key=f"btn_tm_{gname}"):
                        gdata["matches"] = custom_matches
                        save_tours(ts)
                        st.success(f"✅ {gname} 팀전 대진표가 반영되었습니다.")
                        st.rerun()

        st.markdown("<div class='sec sec-t'>🎲 자동 대진표 일괄 생성기 (KDK/고정페어/단식 전용)</div>", unsafe_allow_html=True)
        if st.button("🔥 대진표 자동 빌드 및 매칭 확정 (팀전 제외)", type="primary", use_container_width=True):
            for gname, gdata in tour["groups"].items():
                if gdata.get("mode") == "팀전": continue
                pl = gdata.get("players", [])
                if not pl: continue
                mode = gdata.get("mode", "KDK")
                if mode == "KDK":
                    ms, p2n = make_kdk(pl, gdata.get("games", 4))
                    gdata["matches"] = ms; gdata["player_with_number"] = p2n
                elif mode == "고정페어":
                    ms, _ = make_fixed(pl)
                    gdata["matches"] = ms; gdata["player_with_number"] = {}
                elif mode == "단식":
                    ms, _ = make_singles(pl)
                    gdata["matches"] = ms; gdata["player_with_number"] = {}
            save_tours(ts)
            st.success("✅ 조건에 부합하는 모든 그룹의 대진표 빌드가 완료되었습니다!"); st.rerun()

    with adm[2]:
        # 📥 엑셀 파일 업로드 및 회원 덮어쓰기 최상단 유지
        st.markdown('<div class="sec sec-t">📥 엑셀(XLSX/CSV) 회원 명단 일괄 업로드 및 덮어쓰기</div>', unsafe_allow_html=True)
        up=st.file_uploader("랭킹 마스터 데이터 파일 선택",type=["csv","xlsx"])
        if up and st.button("🚀 마스터 랭킹 강제 파일 빌드 실행",use_container_width=True):
            try:
                ndf=read_file(up)
                for c in COLS_RANK:
                    if c not in ndf.columns: ndf[c]=""
                save_rank(ndf); st.success("✅ 데이터가 파일 시스템에 성공적으로 업로드 및 덮어쓰기 되었습니다."); st.rerun()
            except Exception as e: st.error(f"오류: {e}")
            
        st.divider()

        st.markdown('<div class="sec sec-t">🏆 금일 대회 자동 획득 포인트 현황</div>', unsafe_allow_html=True)
        tours=load_tours(); active=[k for k,v in tours.items() if v.get("status")=="진행중"]
        
        earn={}
        if active:
            tid=active[-1]; tour=tours[tid]
            for g,gi in tour.get("groups",{}).items():
                ms=gi["matches"]; mode=gi.get("mode","KDK"); fx=(mode=="고정페어")
                if mode == "팀전": continue
                sv=stats_fixed(ms) if fx else stats_kdk(ms); rit=list(sv.keys())
                if not rit: continue
                ranked=sorted(rit,key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))
                for idx,p_item in enumerate(ranked):
                    pts=rank_pts(idx+1,mode)
                    if fx:
                        for individual in list(p_item): earn[individual]=earn.get(individual,0)+pts
                    else: earn[p_item]=earn.get(p_item,0)+pts
            
            if earn:
                res_df = pd.DataFrame(sorted(earn.items(),key=lambda x:-x[1]),columns=["선수명","금일 획득포인트"])
                st.markdown(df_to_html(res_df),unsafe_allow_html=True)
                if st.button("☝️ 위 자동 계산된 당일 대화 점수를 하단 명부에 일괄 가산", use_container_width=True):
                    r_temp = load_rank()
                    for p, p_val in earn.items():
                        if p in r_temp["이름"].values:
                            r_temp.loc[r_temp["이름"]==p, "대회포인트"] += p_val
                    save_rank(r_temp)
                    st.success("✅ 오늘 경기 보너스 점수가 아래 명부의 [대회포인트] 칸에 가산되었습니다. 최종 확인 후 마감 저장해 주세요!")
                    st.rerun()
        else:
            st.info("현재 진행 중인 대진이 없어 당일 자동 정산 점수가 없습니다. 하단 명부 편집을 통해 직접 포인트 조율이 가능합니다.")

        # 📋 회원 통합 조율 보드 (대회포인트, 부과점수, 비고사유 입력 테이블 구조 유지)
        st.markdown('<div class="sec sec-t">⭐ 전체 회원 정보 및 스코어·부가점·비고 통합 조율 보드</div>', unsafe_allow_html=True)
        r_master = load_rank()
        
        if not r_master.empty:
            st.markdown("💡 점수나 사유를 수정한 뒤 하단의 **[💾 최종 데이터 마스터 보드에 반영 및 마감]** 단추를 반드시 누르셔야 첫 탭(랭킹 포인트 및 비고)에 영구 연동됩니다.")
            
            updated_rows = []
            
            st.markdown("""
            <div class="mx-wrap">
                <table class="mx">
                    <thead>
                        <tr>
                            <th style="width:10%;">랭킹</th>
                            <th style="width:15%;">이름</th>
                            <th style="width:18%;">대회포인트</th>
                            <th style="width:18%;">부과점</th>
                            <th>현재 총점 및 비고 사유 기재</th>
                        </tr>
                    </thead>
                    <tbody>
            """, unsafe_allow_html=True)
            
            # 현재포인트 기준으로 다시 재정렬하여 표를 로드
            r_master = r_master.sort_values(by="현재포인트", ascending=False).reset_index(drop=True)
            
            for idx, row in r_master.iterrows():
                p_name = row["이름"]
                if not p_name: continue
                
                cur_rank = idx + 1
                cur_tour_pts = int(pd.to_numeric(row.get("대회포인트", 0), errors="coerce")) if pd.notna(row.get("대회포인트", 0)) else 0
                cur_extra_pts = int(pd.to_numeric(row.get("부과점", 0), errors="coerce")) if pd.notna(row.get("부과점", 0)) else 0
                cur_note = str(row.get("비고", "")) if pd.notna(row.get("비고", "")) and str(row.get("비고", "")) != "nan" else ""
                
                r_col1, r_col2, r_col3, r_col4, r_col5 = st.columns([0.8, 1.2, 1.5, 1.5, 4.0])
                
                with r_col1:
                    st.markdown(f"<div style='text-align:center; padding-top:10px; font-weight:700; color:#7f8c8d;'>{cur_rank}</div>", unsafe_allow_html=True)
                with r_col2:
                    st.markdown(f"<div style='text-align:center; padding-top:10px; font-weight:700; color:#2C3E50;'>{p_name}</div>", unsafe_allow_html=True)
                with r_col3:
                    st.markdown('<div class="matrix-input-box">', unsafe_allow_html=True)
                    new_tour_pt = st.number_input("대회점수", min_value=0, max_value=5000, value=cur_tour_pts, step=1, key=f"mat_tpt_{p_name}_{idx}", label_visibility="collapsed")
                    st.markdown('</div>', unsafe_allow_html=True)
                with r_col4:
                    st.markdown('<div class="matrix-input-box">', unsafe_allow_html=True)
                    new_extra_pt = st.number_input("부가점수", min_value=-500, max_value=500, value=cur_extra_pts, step=1, key=f"mat_ept_{p_name}_{idx}", label_visibility="collapsed")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                calculated_total = new_tour_pt + new_extra_pt
                
                with r_col5:
                    st.markdown('<div style="display:flex; align-items:center; gap:12px;" class="matrix-input-box">', unsafe_allow_html=True)
                    sub_c1, sub_c2 = st.columns([1.2, 3.8])
                    with sub_c1:
                        st.markdown(f"<div style='text-align:center; padding-top:10px; font-size:0.75rem; color:#2E7D32; font-weight:900;'>{calculated_total}</div>", unsafe_allow_html=True)
                    with sub_c2:
                        new_note = st.text_input("비고내용", value=cur_note, placeholder="비고사유 입력", key=f"mat_nt_{p_name}_{idx}", label_visibility="collapsed")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                updated_rows.append({
                    "랭킹": cur_rank,
                    "이름": p_name,
                    "대회포인트": new_tour_pt,
                    "부과점": new_extra_pt,
                    "현재포인트": calculated_total,
                    "비고": new_note
                })
                st.markdown("<div style='border-bottom:1px solid #E0E4E8; margin: 2px 0;'></div>", unsafe_allow_html=True)
            
            st.markdown("</tbody></table></div>", unsafe_allow_html=True)
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            
            if st.button("💾 최종 데이터 마스터 보드에 반영 및 마감", type="primary", use_container_width=True):
                new_df = pd.DataFrame(updated_rows)
                save_rank(new_df)
                
                if active:
                    tours[active[-1]]["status"] = "완료"
                    save_tours(tours)
                
                st.success("✅ 정합성 검증 완료! 수정된 모든 내용과 비고사유가 높은 총점 순(내림차순)으로 완벽하게 연동 합산되었습니다."); st.rerun()
                
        st.divider()
        with st.expander("📝 [수동 관리용] 전체 회원 텍스트 명단 직접 조율"):
            cur_m=load_members()
            txt_area=st.text_area("클럽 전체 회원 명단 (이름을 쉼표 또는 줄바꿈으로 구분)", value=", ".join(cur_m), height=120)
            if st.button("💾 회원 명단 동기화", use_container_width=True):
                parsed=[n.strip() for n in txt_area.replace("\n",",").split(",") if n.strip()]
                save_members(parsed)
                rk_df=load_rank()
                for p in parsed:
                    if rk_df.empty or p not in rk_df["이름"].values:
                        nr={c:"" for c in COLS_RANK}
                        nr["이름"]=p; nr["현재포인트"]=0; nr["부과점"]=0; nr["대회포인트"]=0; nr["비고"]=""
                        rk_df=pd.concat([rk_df,pd.DataFrame([nr])],ignore_index=True)
                rk_df = rk_df[rk_df["이름"].isin(parsed)].reset_index(drop=True)
                save_rank(rk_df)
                st.success("✅ 회원 명단이 성공적으로 갱신되었습니다."); st.rerun()
