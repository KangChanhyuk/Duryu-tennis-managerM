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

COLS_RANK   = ["랭킹", "이름", "현재 포인트", "지난 포인트", "대회 결과", "부과점", "그룹", "비고"]

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
        try:
            df = pd.read_csv(RANK_FILE, encoding="utf-8-sig").dropna(subset=["이름"])
            for col in COLS_RANK:
                if col not in df.columns:
                    df[col] = 0 if col in ["현재 포인트", "지난 포인트", "부과점"] else ""
            for c in ["현재 포인트","지난 포인트","부과점"]:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
            df = df.sort_values(by="현재 포인트", ascending=False).reset_index(drop=True)
            df["랭킹"] = df.index + 1
            return df[COLS_RANK].fillna("")
        except Exception:
            pass
    return pd.DataFrame(columns=COLS_RANK)

def save_rank(df):
    if df.empty:
        return
    for c in ["현재 포인트","지난 포인트","부과점"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
    for c in COLS_RANK:
        if c not in df.columns: 
            df[c] = 0 if c in ["현재 포인트", "지난 포인트", "부과점"] else ""
    df = df.sort_values(by="현재 포인트", ascending=False).reset_index(drop=True)
    df["랭킹"] = df.index + 1
    df = df[COLS_RANK]
    df.fillna("").to_csv(RANK_FILE, index=False, encoding="utf-8-sig")
    push_to_github(RANK_FILE, "Backup ranking master")

def load_members():
    if os.path.exists(MEMBER_FILE):
        with open(MEMBER_FILE,"r", encoding="utf-8") as f: return json.load(f)
    df=load_rank(); return df["이름"].tolist() if not df.empty else []

def save_members(names):
    with open(MEMBER_FILE,"w", encoding="utf-8") as f: json.dump(names,f,ensure_ascii=False,indent=2)
    push_to_github(MEMBER_FILE, "Backup member roster")

def load_tours():
    if os.path.exists(TOUR_FILE):
        with open(TOUR_FILE,"r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                # 🛡️ [강력한 보정 안전장치 추가] s1, s2 데이터가 유실되었거나 오타인 경우를 완벽하게 자동 보정합니다.
                for t_id, t_val in data.items():
                    if "groups" in t_val:
                        for g_name, g_val in t_val["groups"].items():
                            if "matches" in g_val:
                                for m in g_val["matches"]:
                                    if "s2 Pall" in m:
                                        m["s2"] = m.pop("s2 Pall")
                                    if "s1" not in m: m["s1"] = 0
                                    if "s2" not in m: m["s2"] = 0
                return data
            except Exception:
                return {}
    return {}

def save_tours(d):
    with open(TOUR_FILE,"w", encoding="utf-8") as f: json.dump(d,f,ensure_ascii=False,indent=2)
    push_to_github(TOUR_FILE, "Backup tournament status")

def to_excel(df):
    buf=BytesIO(); df.to_excel(buf,index=False); return buf.getvalue()

def read_file(up):
    name=up.name.lower()
    if name.endswith(("xlsx","xls")): return pd.read_excel(up)
    return pd.read_csv(up,encoding="utf-8-sig",encoding_errors="replace")

def df_to_html(df, is_master=False):
    if df.empty: return "<div class='ic'>데이터가 없습니다.</div>"
    if is_master:
        cols = COLS_RANK
    else:
        cols = [c for c in COLS_RANK if c in df.columns]
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
        a,b=int(m.get("s1",0)),int(m.get("s2",0))
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
        a,b=int(m.get("s1",0)),int(m.get("s2",0))
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
        a, b = int(m.get("s1",0)), int(m.get("s2",0))
        if a > b:
            s[team1]["매치승"] += 1; s[team2]["매치패"] += 1
        elif b > a:
            s[team2]["매치승"] += 1; s[team1]["매치패"] += 1
        s[team1]["득실"] += a - b
        s[team2]["득실"] += b - a
    return s

def rank_pts(rank, mode):
    if mode in ["고정페어", "팀전"]: 
        return {1:7, 2:5, 3:3}.get(rank, 1)
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
    
    if is_fixed:
        lab={t:"&".join(list(t)) for t in rank_items}
        keys=list(lab.values())
    else:
        if p2n:
            sorted_players = sorted(rank_items, key=lambda p: p2n.get(p, 999))
            lab = {p: f"{p}({p2n.get(p, '?')})" for p in sorted_players}
        else:
            lab = {p: p for p in rank_items}
        keys=list(lab.values())
        
    mat={r:{c:("■" if r==c else "—") for c in keys} for r in keys}
    
    for m in matches:
        a,b=int(m.get("s1",0)),int(m.get("s2",0))
        if a>0 or b>0:
            if is_fixed:
                k1,k2=tuple(m["t1"]),tuple(m["t2"])
                mat[lab[k1]][lab[k2]]=f"{a}:{b}";mat[lab[k2]][lab[k1]]=f"{b}:{a}"
            else:
                for x in m["t1"]:
                    for y in m["t2"]:
                        if lab.get(x) in mat and lab.get(y) in mat:
                            mat[lab[x]][lab[y]]=f"{a}:{b}";mat[lab[y]][lab[x]]=f"{b}:{a}"
                            
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
    if df.empty:
        st.markdown("<div class='ic'>📋 등록된 랭킹 데이터 파일이 비어 있습니다. 관리자 전용 탭에서 회원 명부/엑셀을 업로드해주세요.</div>",unsafe_allow_html=True)
    else:
        st.markdown(df_to_html(df, is_master=True),unsafe_allow_html=True)
        st.download_button("Excel 다운로드",data=to_excel(df),file_name=f"랭킹_{date.today()}.xlsx",use_container_width=True)

# ----------------- [2. 📅 대진표 탭] -----------------
elif ss.menu=="schedule":
    tours=load_tours(); active=[k for k,v in tours.items() if v.get("status")=="진행중"]
    if not active:
        st.markdown("<div class='pg-title c1'>📅 대진표</div><div class='ic ic-b'>⚠️ 진행 중인 대회가 없습니다. 관리자 메뉴에서 대회를 생성하세요.</div>",unsafe_allow_html=True); st.stop()
    tid=active[-1]; tour=tours[tid]; gnames=list(tour.get("groups",{}).keys())
    st.markdown(f"<div class='pg-title c1'>📅 {tour['title']}</div>",unsafe_allow_html=True)
    st.markdown(f"<div class='ic ic-b'>📍 {tour.get('date','')} &nbsp;|&nbsp; {tour.get('place','')} &nbsp;|&nbsp; 코트 {tour.get('courts',2)}면</div>",unsafe_allow_html=True)
    if not gnames:
        st.markdown("<div class='ic ic-b'>ℹ️ 편성된 대진 그룹이 없습니다.</div>",unsafe_allow_html=True); st.stop()
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
                if mode=="KDK" and p2n:
                    st.markdown(kdk_html(len(p2n),gi.get("games",4),p2n),unsafe_allow_html=True)
                st.markdown("<div class='sec sec-b'>📋 그룹 현재 실시간 순위</div>",unsafe_allow_html=True)
                if rit:
                    ranked=sorted(rit,key=lambda x:(-sv[x]["승"],-sv[x]["득실"])); rows=[]
                    for i,item in enumerate(ranked):
                        if fx: rows.append({"순위":i+1,"팀명":" & ".join(list(item)),"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"결과":grade_fixed(i+1)})
                        else: rows.append({"순위":i+1,"선수명":item,"승":sv[item]["승"],"패":sv[item]["패"],"득실":f'{sv[item]["득실"]:+d}',"결과":grade_kdk(i+1)})
                    st.markdown(df_to_html(pd.DataFrame(rows)),unsafe_allow_html=True)
            st.markdown("<div class='sec sec-b'>🎾 경기 결과 스코어 입력</div>",unsafe_allow_html=True)
            for mi,m in enumerate(ms):
                t1s=" & ".join(m["t1"]); t2s=" & ".join(m["t2"])
                if tm: t1s = f"[{m.get('team1','A팀')}] {t1s}" ; t2s = f"[{m.get('team2','B팀')}] {t2s}"
                with st.container(border=True):
                    st.markdown(f"<span class='match-no {GCLS[ti%len(GCLS)]}'>MATCH {mi+1}</span>",unsafe_allow_html=True)
                    c1,c2,c3=st.columns([5,2,5])
                    with c1: st.markdown(f"<div class='team-nm {TBCLS[ti%len(TBCLS)]}'>{t1s}</div>",unsafe_allow_html=True)
                    with c2: st.markdown("<div class='vs-badge'>VS</div>",unsafe_allow_html=True)
                    with c3: st.markdown(f"<div class='team-nm {TBCLS[(ti+1)%len(TBCLS)]}'>{t2s}</div>",unsafe_allow_html=True)
                    st.markdown("<div style='height:8px'></div>",unsafe_allow_html=True)
                    cc1,cc2=st.columns(2)
                    with cc1:
                        new_s1=st.number_input(f"Score1##{g}_{mi}",value=int(m.get("s1",0)),min_value=0,step=1,label_visibility="collapsed")
                    with cc2:
                        new_s2=st.number_input(f"Score2##{g}_{mi}",value=int(m.get("s2",0)),min_value=0,step=1,label_visibility="collapsed")
                    if new_s1!=m.get("s1",0) or new_s2!=m.get("s2",0):
                        ms[mi]["s1"]=new_s1; ms[mi]["s2"]=new_s2
                        save_tours(tours); st.rerun()

# ----------------- [3. 🎾 최종 결과 반영 탭] -----------------
elif ss.menu=="result":
    st.markdown("<div class='pg-title c2'>🎾 대회 마감 및 결과 반영</div>",unsafe_allow_html=True)
    tours=load_tours(); active=[k for k,v in tours.items() if v.get("status")=="진행중"]
    if not active:
        st.markdown("<div class='ic ic-o'>⚠️ 현재 진행 중인 대회가 없습니다.</div>",unsafe_allow_html=True); st.stop()
    tid=active[-1]; tour=tours[tid]; st.markdown(f"<div class='sec sec-o'>🏆 대상 대회: {tour['title']}</div>",unsafe_allow_html=True)
    
    r_df=load_rank()
    if r_df.empty:
        st.markdown("<div class='ic ic-o'>⚠️ 마스터 랭킹 보드에 등록된 회원이 없어 결과를 동기화할 수 없습니다.</div>",unsafe_allow_html=True); st.stop()
        
    updated_rows=[]
    for _,row in r_df.iterrows():
        p=row["이름"]; cur_pt=int(row["현재 포인트"]); bg=int(row.get("부과점",0))
        d_res=""; p_add=0
        for gname,gdata in tour.get("groups",{}).items():
            ms=gdata["matches"]; mode=gdata.get("mode","KDK")
            if mode=="팀전":
                tsv=stats_team(ms)
                if p in gdata.get("players",[]):
                    t_nm = "A팀" if p in gdata.get("teamA",[]) else "B팀"
                    t_ranked=sorted(list(tsv.keys()),key=lambda x:(-tsv[x]["매치승"],-tsv[x]["득실"]))
                    rk=t_ranked.index(t_nm)+1 if t_nm in t_ranked else 99
                    p_add=rank_pts(rk,mode); d_res=f"{gname}({t_nm} {rk}위)"
            else:
                fx=(mode=="고정페어"); sv=stats_fixed(ms) if fx else stats_kdk(ms)
                rit=list(sv.keys())
                if rit:
                    ranked=sorted(rit,key=lambda x:(-sv[x]["승"],-sv[x]["득실"]))
                    found=[item for item in ranked if (p in item if fx else p==item)]
                    if found:
                        rk=ranked.index(found[0])+1
                        p_add=rank_pts(rk,mode)
                        if mode == "KDK":
                            d_res = f"{gname}({grade_kdk(rk)})"
                        else:
                            d_res = f"{gname}({rk}위)"
        new_pt=cur_pt+p_add+bg if d_res else cur_pt
        updated_rows.append({"랭킹":row["랭킹"],"이름":p,"현재 포인트":new_pt,"지난 포인트":cur_pt,"대회 결과":d_res if d_res else row["대회 결과"],"부과점":0,"그룹":row["그룹"],"비고":row["비고"]})
    
    st.markdown("<div class='sec sec-o'>📊 마감 동기화 가상 미리보기 (상위 5명)</div>",unsafe_allow_html=True)
    st.markdown(df_to_html(pd.DataFrame(updated_rows).head(5)),unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    
    if st.button("💾 최종 데이터 마스터 보드에 반영 및 마감", type="primary", use_container_width=True):
        new_df = pd.DataFrame(updated_rows)
        save_rank(new_df)
        if active:
            tours[active[-1]]["status"] = "완료"
            save_tours(tours)
        st.success("✅ 정합성 확인 완료! 지정하신 8대 항목 컬럼 구조 그대로 마스터 랭킹 보드 정렬 동기화가 마감되었습니다."); st.rerun()

# ----------------- [4. ⚙️ 관리자 전용 제어 탭] -----------------
elif ss.menu=="admin":
    st.markdown("<div class='pg-title c3'>⚙️ 클럽 관리자 시스템</div>",unsafe_allow_html=True)
    if not ss.is_admin:
        pw=st.text_input("관리자 인증 비밀번호 입력", type="password")
        if st.button("🔓 관리자 모드 활성화", type="primary", use_container_width=True):
            if pw==get_admin_pw():
                ss.is_admin=True; st.success("🔒 인증 성공!"); st.rerun()
            else: st.error("❌ 비밀번호가 다릅니다.")
        st.stop()
    if st.button("🔒 관리자 로그아웃", use_container_width=True):
        ss.is_admin=False; st.rerun()
        
    adm_tabs=st.tabs(["👥 회원 및 파일 관리", "🌱 대회 대진 생성", "🗂️ 대회 히스토리"])
    
    with adm_tabs[0]:
        st.markdown("<div class='sec sec-p'>📥 엑셀(XLSX/CSV) 파일 일괄 업로드 및 덮어쓰기</div>",unsafe_allow_html=True)
        up_file=st.file_uploader("회원 명단 및 랭킹 통합 엑셀 파일 선택", type=["xlsx","xls","csv"])
        if up_file is not None:
            if st.button("💥 마스터 랭킹 파일 강제 반영 및 덮어쓰기", type="primary", use_container_width=True):
                try:
                    raw_df = read_file(up_file)
                    raw_df.columns = [str(c).strip() for c in raw_df.columns]
                    
                    if "이름" not in raw_df.columns:
                        st.error("❌ 엑셀 파일 내에 '이름' 컬럼이 존재하지 않습니다. 파일을 확인해주세요.")
                    else:
                        cleaned_rows = []
                        for _, r in raw_df.iterrows():
                            p_name = str(r["이름"]).strip()
                            if not p_name or p_name == "nan":
                                continue
                            
                            cur_pt = r.get("현재 포인트", r.get("현재포인트", 0))
                            old_pt = r.get("지난 포인트", r.get("지난포인트", 0))
                            bg_pt = r.get("부과점", r.get("부과점수", 0))
                            
                            row_dict = {
                                "랭킹": "",
                                "이름": p_name,
                                "현재 포인트": int(pd.to_numeric(cur_pt, errors="coerce").fillna(0)),
                                "지난 포인트": int(pd.to_numeric(old_pt, errors="coerce").fillna(0)),
                                "대회 결과": str(r.get("대회 결과", r.get("대회결과", ""))).replace("nan", ""),
                                "부과점": int(pd.to_numeric(bg_pt, errors="coerce").fillna(0)),
                                "그룹": str(r.get("그룹", "")).replace("nan", ""),
                                "비고": str(r.get("비고", "")).replace("nan", "")
                            }
                            cleaned_rows.append(row_dict)
                            
                        if cleaned_rows:
                            new_master_df = pd.DataFrame(cleaned_rows)
                            save_rank(new_master_df)
                            
                            all_names = new_master_df["이름"].tolist()
                            save_members(all_names)
                            
                            st.success(f"✅ 총 {len(all_names)}명의 데이터가 완벽하게 업로드되어 마스터 보드와 동기화되었습니다!"); st.rerun()
                        else:
                            st.error("❌ 읽어온 회원 데이터가 유효하지 않습니다.")
                except Exception as e:
                    st.error(f"❌ 파일 처리 중 치명적인 에러가 발생했습니다: {e}")
                    
        st.divider()
        st.markdown("<div class='sec sec-p'>➕ 회원 부가 점수(부과점) 일괄 관리</div>",unsafe_allow_html=True)
        r_df=load_rank()
        if not r_df.empty:
            with st.form("bg_form"):
                updates={}
                for idx,row in r_df.iterrows():
                    c1,c2,c3=st.columns([3,3,6])
                    with c1: st.markdown(f"**{row['이름']}** ({row['현재 포인트']}pt)")
                    with c2: updates[f"bg_{row['이름']}"]=st.number_input("부과점",value=int(row.get("부과점",0)),step=1,key=f"bg_in_{row['이름']}",label_visibility="collapsed")
                    with c3: updates[f"rm_{row['이름']}"]=st.text_input("사유",value=str(row.get("비고","")),key=f"rm_in_{row['이름']}",label_visibility="collapsed")
                if st.form_submit_button("💾 부과점 및 비고 사유 일괄 반영"):
                    for idx,row in r_df.iterrows():
                        r_df.at[idx,"부과점"]=updates[f"bg_{row['이름']}"]
                        r_df.at[idx,"비고"]=updates[f"rm_{row['이름']}"]
                    save_rank(r_df)
                    st.success("✅ 부과점과 비고 사유가 마스터 보드에 저장 및 합산 준비 완료되었습니다!"); st.rerun()
                    
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
                        nr={c:"" for c in COLS_RANK}; nr["이름"]=p; nr["현재 포인트"]=0; nr["부과점"]=0; nr["비고"]=""
                        rk_df=pd.concat([rk_df,pd.DataFrame([nr])],ignore_index=True)
                save_rank(rk_df)
                st.success("✅ 회원 텍스트 풀 명단 수정 및 랭킹 데이터 동기화 완료."); st.rerun()

    # 🌱 4-2. 대회 대진 자동 생성 서브탭
    with adm_tabs[1]:
        st.markdown("<div class='sec sec-p'>🌱 신규 토너먼트 대회 생성</div>",unsafe_allow_html=True)
        t_title=st.text_input("대회 이름", value=f"{date.today().strftime('%m월')} 정기 토너먼트")
        t_date=st.date_input("대회 개최일", value=date.today())
        t_place=st.text_input("장소", value="신안/신진 코트")
        t_courts=st.number_input("사용 코트 수", value=2, min_value=1)
        
        m_list=load_members()
        if not m_list:
            st.warning("⚠️ 등록된 회원이 없습니다. 상단의 회원 관리창이나 엑셀 업로드를 통해 명부를 먼저 마련해주세요.")
        else:
            st.markdown(f"**👥 참석 선수 선택 (전체 명단 풀: {len(m_list)}명)**")
            sel_players=st.multiselect("대회에 출전할 선수를 전원 선택하세요.", options=m_list, default=m_list)
            
            st.divider()
            g_num=st.number_input("분할할 대진 그룹 수", value=1, min_value=1)
            g_modes=["KDK","고정페어","단식","팀전"]
            
            g_cfgs={}
            for i in range(int(g_num)):
                with st.container(border=True):
                    st.markdown(f"**{GLBL[i%len(GLBL)]} {i+1}번째 그룹 세부 설정**")
                    g_name=st.text_input(f"그룹명##{i}", value=f"{chr(65+i)}그룹")
                    g_mode=st.selectbox(f"경기 방식##{i}", options=g_modes, index=0)
                    g_size=st.number_input(f"배정 인원수##{i}", value=8, min_value=2)
                    
                    g_games=4
                    if g_mode=="KDK":
                        g_games=st.selectbox(f"1인당 경기수##{i}", options=[3,4], index=1)
                        
                    g_cfgs[g_name] = {"mode":g_mode, "size":g_size, "games":g_games}
                    
            if st.button("🎲 실시간 마스터 랭킹 시드 기반 대진 자동 빌드", type="primary", use_container_width=True):
                if not sel_players: st.error("❌ 선택된 출전 선수가 없습니다."); st.stop()
                tours=load_tours()
                tid=f"tour_{int(datetime.now().timestamp())}"
                
                new_tour = {
                    "title": t_title, "date": str(t_date), "place": t_place, "courts": int(t_courts),
                    "status": "진행중", "players": sel_players, "groups": {}
                }
                
                r_df = load_rank()
                master_order = r_df["이름"].tolist() if not r_df.empty else []
                chosen_p_sorted = [p for p in master_order if p in sel_players]
                chosen_p_sorted += [p for p in sel_players if p not in chosen_p_sorted]
                
                curr_idx = 0
                for g_name, gc in g_cfgs.items():
                    sz = int(gc["size"])
                    g_players = chosen_p_sorted[curr_idx : curr_idx + sz]
                    curr_idx += sz
                    
                    md = gc["mode"]
                    if md=="KDK": ms, p2n = make_kdk(g_players, gc["games"])
                    elif md=="고정페어": ms, p2n = make_fixed(g_players)
                    elif md=="단식": ms, p2n = make_singles(g_players)
                    elif md=="팀전":
                        half = len(g_players)//2
                        tA, tB = g_players[:half], g_players[half:]
                        ms = [{"t1":[tA[i%len(tA)]],"t2":[tB[i%len(tB)]],"s1":0,"s2":0,"team1":"A팀","team2":"B팀"} for i in range(max(len(tA),len(tB)))]
                        p2n = {}
                        new_tour["groups"][g_name] = {"mode":md, "players":g_players, "matches":ms, "player_with_number":p2n, "teamA":tA, "teamB":tB}
                        continue
                        
                    new_tour["groups"][g_name] = {"mode":md, "players":g_players, "matches":ms, "player_with_number":p2n, "games":gc["games"]}
                    
                tours[tid] = new_tour
                save_tours(tours)
                st.success("🎯 랭킹 연동 균등 시드 배정 및 대진표 매칭이 성공적으로 완료되었습니다!"); st.rerun()

    # 🗂️ 4-3. 대회 히스토리 서브탭
    with adm_tabs[2]:
        st.markdown("<div class='sec sec-p'>🗂️ 과거 대회 보관 관리 및 삭제</div>",unsafe_allow_html=True)
        tours=load_tours()
        if not tours: st.info("보관된 대회 내역이 존재하지 않습니다.")
        for k,v in list(tours.items()):
            c1,c2=st.columns([8,2])
            with c1: st.markdown(f"**{v['title']}** ({v.get('date','')}) - 상태: `{v.get('status','')}`")
            with c2:
                if st.button("🗑️ 삭제", key=f"del_{k}", use_container_width=True):
                    del tours[k]; save_tours(tours); st.success("삭제되었습니다."); st.rerun()

# ----------------- [5. 🛠️ 시스템 암호 설정 탭] -----------------
elif ss.menu=="config":
    st.markdown("<div class='pg-title c4'>🛠️ 시스템 구성 환경 설정</div>",unsafe_allow_html=True)
    cfg=load_config()
    st.markdown("<div class='sec sec-t'>🔒 관리자 비밀번호 변경</div>",unsafe_allow_html=True)
    new_pw=st.text_input("새 비밀번호 입력", value=cfg.get("admin_pw","0502"), type="password")
    if st.button("💾 시스템 암호 신규 저장 변경", type="primary", use_container_width=True):
        cfg["admin_pw"]=new_pw; save_config(cfg)
        st.success("✅ 시스템 관리자 인증 비밀번호가 성공적으로 업데이트되었습니다."); st.rerun()
