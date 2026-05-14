import streamlit as st
import pandas as pd
import random, os, json
from datetime import date
from io import BytesIO

# ══════════════════════════════════════════════════════════════
# 앱 설정 (모바일 최적화 - 360x740px ~ 375x812px 대응)
# ══════════════════════════════════════════════════════════════
st.set_page_config(page_title="두류 랭킹", page_icon="🎾",
                   layout="wide", initial_sidebar_state="collapsed")

# 모바일 최적화 CSS (터치/가독성 개선, 숫자 +/- 버튼 대형화)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&display=swap');
* {
    font-family: 'Noto Sans KR', sans-serif !important;
    box-sizing: border-box;
}
.block-container { 
    padding: 0 0.5rem 0.6rem 0.5rem !important; 
    max-width: 100% !important;
}

/* 네비게이션 바 */
section.main [data-testid="stHorizontalBlock"]:first-of-type .stButton > button {
    background: transparent !important;
    color: rgba(255,255,255,0.8) !important;
    border: none !important; 
    border-radius: 0 !important;
    font-size: 0.65rem !important;
    font-weight: 600 !important;
    padding: 10px 2px 6px !important;
    line-height: 1.2 !important;
    white-space: normal !important;
    word-break: keep-all;
    box-shadow: none !important;
    min-height: 52px !important;
    border-bottom: 2px solid transparent !important;
}
section.main [data-testid="stHorizontalBlock"]:first-of-type .stButton > button:hover {
    background: rgba(255,255,255,0.1) !important;
}
section.main [data-testid="stHorizontalBlock"]:first-of-type .stButton > button[kind="primary"] {
    background: rgba(255,255,255,0.15) !important;
    color: #fff !important;
    border-bottom: 2px solid #A5D6A7 !important;
}

.main-hdr {
    background: linear-gradient(135deg,#1D5B2E,#388E3C);
    color:#fff; 
    padding: 0.5rem 0.6rem; 
    border-radius: 10px;
    margin-bottom: 0.6rem; 
    font-size: 1rem;
    font-weight: 800; 
    text-align: center;
}
.sec {
    font-size: 0.9rem; 
    font-weight: 800; 
    color:#1D5B2E;
    border-left: 4px solid #66BB6A; 
    padding-left: 8px; 
    margin: 10px 0 6px;
}

/* 탭 */
button[data-baseweb="tab"] {
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    padding: 6px 6px !important;
    border-radius: 8px 8px 0 0 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg,#1D5B2E,#388E3C) !important;
}

/* 테이블 가운데 정렬 강제 */
div[data-testid="stDataFrame"] table,
div[data-testid="stDataEditor"] table {
    width: 100% !important;
    font-size: 0.7rem !important;
    text-align: center !important;
}
div[data-testid="stDataFrame"] table th,
div[data-testid="stDataFrame"] table td,
div[data-testid="stDataFrame"] div[data-testid="glideDataEditor"] *,
div[data-testid="stDataFrame"] [role="gridcell"],
div[data-testid="stDataFrame"] [role="columnheader"] {
    text-align: center !important;
    vertical-align: middle !important;
    padding: 4px 4px !important;
    font-size: 0.7rem !important;
    white-space: nowrap;
}
div[data-testid="stDataFrame"] {
    overflow-x: auto !important;
}

/* 숫자 입력 +/- 버튼 대형화 */
div[data-testid="stNumberInput"] {
    width: 100% !important;
}
div[data-testid="stNumberInput"] > div {
    display: flex !important;
    align-items: stretch !important;
    border: 2px solid #66BB6A !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    background: #fff !important;
    min-height: 56px !important;
}
div[data-testid="stNumberInput"] input[type="number"] {
    text-align: center !important;
    font-size: 1.3rem !important;
    font-weight: 800 !important;
    border: none !important;
    outline: none !important;
    background: transparent !important;
    min-height: 56px !important;
    padding: 0 4px !important;
    flex: 1 !important;
    -moz-appearance: textfield !important;
}
div[data-testid="stNumberInput"] input[type="number"]::-webkit-outer-spin-button,
div[data-testid="stNumberInput"] input[type="number"]::-webkit-inner-spin-button {
    -webkit-appearance: none !important;
    margin: 0 !important;
}
div[data-testid="stNumberInput"] button {
    background: linear-gradient(135deg,#1D5B2E,#388E3C) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 0 !important;
    font-size: 1.6rem !important;
    font-weight: 900 !important;
    min-width: 52px !important;
    min-height: 56px !important;
    width: 52px !important;
    height: 56px !important;
    padding: 0 !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    line-height: 1 !important;
    transition: background 0.15s !important;
    flex-shrink: 0 !important;
}
div[data-testid="stNumberInput"] button:hover {
    background: linear-gradient(135deg,#388E3C,#43A047) !important;
}
div[data-testid="stNumberInput"] button:active {
    background: linear-gradient(135deg,#145222,#1D5B2E) !important;
}
div[data-testid="stNumberInput"] button:first-of-type {
    border-radius: 10px 0 0 10px !important;
}
div[data-testid="stNumberInput"] button:last-of-type {
    border-radius: 0 10px 10px 0 !important;
}

/* 팀/선수 박스 */
.team-box {
    border-radius: 10px;
    padding: 6px 5px !important;
    font-weight: 700 !important;
    font-size: 0.75rem !important;
    text-align: center;
    margin: 4px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,.08);
    line-height: 1.3;
    min-height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    word-break: keep-all;
}
.tg{background:linear-gradient(135deg,#66BB6A,#43A047);color:#fff}
.tb{background:linear-gradient(135deg,#42A5F5,#1E88E5);color:#fff}
.to{background:linear-gradient(135deg,#FFA726,#FB8C00);color:#fff}
.tp{background:linear-gradient(135deg,#AB47BC,#8E24AA);color:#fff}
.tr{background:linear-gradient(135deg,#EF5350,#E53935);color:#fff}
.tt{background:linear-gradient(135deg,#26A69A,#00897B);color:#fff}

.match-color-0 { background: linear-gradient(135deg,#66BB6A,#43A047) !important; }
.match-color-1 { background: linear-gradient(135deg,#42A5F5,#1E88E5) !important; }
.match-color-2 { background: linear-gradient(135deg,#FFA726,#FB8C00) !important; }

.vs-circle {
    background:#FFB74D;
    color:#fff;
    border-radius:50%;
    width: 32px !important;
    height: 32px !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 0.7rem;
    margin: 0 auto;
}

hr { margin: 8px 0; }

.p-tag {
    display: inline-block;
    background: #E8F5E9;
    border: 1px solid #66BB6A;
    border-radius: 20px;
    padding: 3px 8px;
    margin: 3px 4px;
    font-size: 0.7rem;
    font-weight: 600;
}

.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    padding: 8px 10px !important;
    min-height: 44px !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    min-height: 44px !important;
}

/* 매트릭스 테이블 */
.matrix-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.65rem;
    display: block;
    overflow-x: auto;
    white-space: nowrap;
}
.matrix-table th, .matrix-table td {
    padding: 5px 4px;
    border: 1px solid #ddd;
    text-align: center;
    vertical-align: middle;
}
.matrix-table thead th {
    background: #f0f4f0;
    font-weight: 700;
    color: #1D5B2E;
}
.matrix-table tbody th {
    background: #f9f9f9;
    font-weight: 700;
    text-align: center;
}
.matrix-grey { background-color: #d0d0d0; color: #d0d0d0; }
.matrix-x { color: #bbb; }

/* KDK 대진표 */
.kdk-bracket {
    background: #f5f5f5;
    border-radius: 10px;
    padding: 8px;
    margin: 6px 0;
    font-size: 0.65rem;
    overflow-x: auto;
}
.kdk-bracket table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.65rem;
}
.kdk-bracket th, .kdk-bracket td {
    padding: 5px 6px;
    border: 1px solid #ddd;
    text-align: center;
}
.kdk-bracket thead th {
    background: #e8f5e9;
    font-weight: 700;
    color: #1D5B2E;
}
.kdk-bracket tbody tr:nth-child(even) {
    background: #fafafa;
}

/* 구글 시트 배너 */
.gsheet-banner {
    background: linear-gradient(135deg,#0F9D58,#34A853);
    color: #fff;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 8px 0;
    font-size: 0.8rem;
    font-weight: 700;
}
.gsheet-banner-warn {
    background: linear-gradient(135deg,#F4B400,#F9A825);
    color: #fff;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 8px 0;
    font-size: 0.8rem;
    font-weight: 700;
}

/* 카드/랭킹 여백 */
.tour-card, .rank-card { padding: 6px 10px; margin: 6px 0; border-radius: 10px; }
.dataframe th { font-size: 0.65rem !important; padding: 4px 2px !important; }

/* 멀티셀렉트 크기 조정 */
[data-baseweb="select"] {
    min-height: 48px;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 구글 시트 연동 헬퍼 (기존과 동일, 생략 가능하지만 유지)
# ══════════════════════════════════════════════════════════════
GSHEET_CONFIG_FILE = "gsheet_config.json"

def load_gsheet_config():
    if os.path.exists(GSHEET_CONFIG_FILE):
        with open(GSHEET_CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"enabled": False, "sheet_id": "", "credentials_json": ""}

def save_gsheet_config(cfg):
    with open(GSHEET_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def get_gsheet_client(creds_json_str):
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        creds_dict = json.loads(creds_json_str)
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return gspread.authorize(creds)
    except Exception:
        return None

def sync_ranking_to_gsheet(df, sheet_id, creds_json_str):
    try:
        gc = get_gsheet_client(creds_json_str)
        if gc is None:
            return False, "gspread 패키지 없음"
        sh = gc.open_by_key(sheet_id)
        try:
            ws = sh.worksheet("랭킹")
        except Exception:
            ws = sh.add_worksheet(title="랭킹", rows=200, cols=20)
        ws.clear()
        data = [df.columns.tolist()] + df.fillna("").values.tolist()
        ws.update(data)
        return True, "✅ 구글 시트 동기화 완료!"
    except Exception as e:
        return False, f"오류: {e}"

def sync_ranking_from_gsheet(sheet_id, creds_json_str):
    try:
        gc = get_gsheet_client(creds_json_str)
        if gc is None:
            return None, "gspread 패키지 없음"
        sh = gc.open_by_key(sheet_id)
        ws = sh.worksheet("랭킹")
        rows = ws.get_all_values()
        if not rows:
            return None, "시트가 비어 있습니다."
        df = pd.DataFrame(rows[1:], columns=rows[0])
        for c in ["현재포인트", "3월 포인트", "부과점"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        return df, "✅ 구글 시트에서 불러오기 완료!"
    except Exception as e:
        return None, f"오류: {e}"

def sync_tours_to_gsheet(tours, sheet_id, creds_json_str):
    try:
        gc = get_gsheet_client(creds_json_str)
        if gc is None:
            return False, "gspread 패키지 없음"
        sh = gc.open_by_key(sheet_id)
        try:
            ws_t = sh.worksheet("대회목록")
        except Exception:
            ws_t = sh.add_worksheet(title="대회목록", rows=200, cols=10)
        ws_t.clear()
        rows_t = [["대회ID", "제목", "날짜", "장소", "코트수", "상태"]]
        for tid, tv in tours.items():
            rows_t.append([tid, tv.get("title",""), tv.get("date",""), tv.get("place",""),
                           str(tv.get("courts",2)), tv.get("status","")])
        ws_t.update(rows_t)

        try:
            ws_m = sh.worksheet("경기결과")
        except Exception:
            ws_m = sh.add_worksheet(title="경기결과", rows=2000, cols=10)
        ws_m.clear()
        rows_m = [["대회ID", "그룹", "방식", "팀1", "팀2", "점수1", "점수2"]]
        for tid, tv in tours.items():
            for gname, ginfo in tv.get("groups", {}).items():
                for m in ginfo.get("matches", []):
                    rows_m.append([
                        tid, gname, ginfo.get("mode",""),
                        " & ".join(m["t1"]), " & ".join(m["t2"]),
                        str(m.get("s1",0)), str(m.get("s2",0))
                    ])
        ws_m.update(rows_m)
        return True, "✅ 대회/경기 결과 시트 동기화 완료!"
    except Exception as e:
        return False, f"오류: {e}"

# ══════════════════════════════════════════════════════════════
# 파일 경로 / 상수
# ══════════════════════════════════════════════════════════════
RANK_FILE   = "ranking_master.csv"
MEMBER_FILE = "member_roster.json"
TOUR_FILE   = "tournaments.json"
ADMIN_PW    = "0502"
COLS_RANK   = ["랭킹","이름","현재포인트","3월 포인트","결과","부과점","그룹","비고"]

GCLS = ["tg","tb","to","tp","tr","tt"]
GHEX = ["#66BB6A","#42A5F5","#FFA726","#AB47BC","#EF5350","#26A69A"]
GLBL = ["🟢","🔵","🟠","🟣","🔴","🩵"]

# KDK 대진표
KDK_3G = {
    4: [(1,4,2,3), (1,3,2,4), (1,2,3,4)],
    8: [(1,2,3,4), (5,6,7,8), (1,8,2,7), (3,6,4,5), (1,4,5,8), (2,3,6,7)],
    12: [(1,2,3,4), (5,6,7,8), (9,10,11,12), (1,3,5,7), (2,4,6,8),
         (9,11,1,5), (4,8,9,12), (6,7,10,11), (10,12,2,3)]
}

KDK_4G = {
    5: [(1,2,3,4), (1,3,2,5), (1,4,3,5), (1,5,2,4), (2,3,4,5)],
    6: [(1,3,2,4), (1,5,4,6), (2,3,5,6), (1,4,3,5), (2,6,3,4), (1,6,2,5)],
    7: [(1,2,3,4), (5,6,1,7), (2,3,5,7), (1,4,6,7), (3,5,2,4), (1,6,2,5), (4,6,3,7)],
    8: [(1,2,3,4), (5,6,7,8), (1,3,5,7), (2,4,6,8), (1,5,2,6), (3,7,4,8), (1,6,3,8), (2,5,4,7)],
    9: [(1,2,3,4), (5,6,7,8), (1,9,5,7), (2,3,6,8), (4,9,3,8), (1,5,2,6), (3,6,4,5), (1,7,8,9), (2,4,7,9)],
    10: [(1,2,3,5), (6,7,8,10), (2,3,4,6), (7,8,1,9), (3,4,5,7), (8,9,2,10),
         (4,5,6,8), (1,3,9,10), (5,6,7,9), (1,10,2,4)],
    11: [(1,2,3,5), (6,7,8,10), (4,9,1,11), (2,3,6,8), (4,5,7,10), (9,11,2,6),
         (1,3,7,11), (4,8,5,9), (1,10,2,8), (4,7,6,11), (3,9,5,10)]
}

# ══════════════════════════════════════════════════════════════
# 데이터 함수 (기존과 동일)
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
    gcfg = load_gsheet_config()
    if gcfg.get("enabled") and gcfg.get("sheet_id") and gcfg.get("credentials_json"):
        sync_ranking_to_gsheet(df, gcfg["sheet_id"], gcfg["credentials_json"])

def load_members():
    if os.path.exists(MEMBER_FILE):
        with open(MEMBER_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    df = load_rank()
    return df["이름"].tolist() if not df.empty else []

def save_members(names: list):
    with open(MEMBER_FILE,"w",encoding="utf-8") as f:
        json.dump(names, f, ensure_ascii=False, indent=2)

def load_tours():
    if os.path.exists(TOUR_FILE):
        with open(TOUR_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_tours(d):
    with open(TOUR_FILE,"w",encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    gcfg = load_gsheet_config()
    if gcfg.get("enabled") and gcfg.get("sheet_id") and gcfg.get("credentials_json"):
        sync_tours_to_gsheet(d, gcfg["sheet_id"], gcfg["credentials_json"])

def to_excel(df):
    buf = BytesIO()
    df.to_excel(buf, index=False)
    return buf.getvalue()

def group_stats_fixed(matches):
    stats = {}
    for m in matches:
        t1 = tuple(m["t1"])
        t2 = tuple(m["t2"])
        for t in [t1, t2]:
            if t not in stats:
                stats[t] = {"승": 0, "패": 0, "득실": 0}
        s1, s2 = int(m["s1"]), int(m["s2"])
        if s1 > s2:
            stats[t1]["승"] += 1
            stats[t2]["패"] += 1
        elif s2 > s1:
            stats[t2]["승"] += 1
            stats[t1]["패"] += 1
        stats[t1]["득실"] += (s1 - s2)
        stats[t2]["득실"] += (s2 - s1)
    return stats

def group_stats_kdk(matches):
    stats = {}
    for m in matches:
        players1 = m["t1"]
        players2 = m["t2"]
        for p in players1 + players2:
            if p not in stats:
                stats[p] = {"승": 0, "패": 0, "득실": 0}
        s1, s2 = int(m["s1"]), int(m["s2"])
        if s1 > s2:
            for p in players1:
                stats[p]["승"] += 1
            for p in players2:
                stats[p]["패"] += 1
        elif s2 > s1:
            for p in players2:
                stats[p]["승"] += 1
            for p in players1:
                stats[p]["패"] += 1
        for p in players1:
            stats[p]["득실"] += (s1 - s2)
        for p in players2:
            stats[p]["득실"] += (s2 - s1)
    return stats

def rank_pts(rank, mode):
    if mode == "고정페어":
        return {1:7, 2:5, 3:3}.get(rank, 1)
    else:
        if rank <= 2: return 7
        elif rank <= 4: return 5
        elif rank <= 6: return 3
        else: return 1

def get_grade_kdk(rank):
    if rank <= 2: return "우승"
    elif rank <= 4: return "준우승"
    elif rank <= 6: return "3위"
    else: return "참가"

def make_kdk(players, games_per_person):
    n = len(players)
    bp = KDK_3G.get(n) if games_per_person == 3 else KDK_4G.get(n)
    if not bp:
        return None, {}
    shuffled = random.sample(players, n)
    player_with_number = {shuffled[i]: i+1 for i in range(n)}
    number_to_player = {i+1: shuffled[i] for i in range(n)}
    matches = []
    for a, b, c, d in bp:
        matches.append({
            "t1": [number_to_player[a], number_to_player[b]],
            "t2": [number_to_player[c], number_to_player[d]],
            "s1": 0, "s2": 0
        })
    return matches, player_with_number

def make_fixed(players):
    n = len(players)
    pairs = [(players[i], players[n-1-i]) for i in range(n//2)]
    ms = []
    for i in range(len(pairs)):
        for j in range(i+1, len(pairs)):
            ms.append({"t1": list(pairs[i]), "t2": list(pairs[j]), "s1": 0, "s2": 0})
    random.shuffle(ms)
    return ms, {}

def make_singles(players):
    pl = players[:]
    random.shuffle(pl)
    ms = [(pl[i], pl[j]) for i in range(len(pl)) for j in range(i+1, len(pl))]
    random.shuffle(ms)
    return [{"t1": [a], "t2": [b], "s1": 0, "s2": 0} for a, b in ms], {}

def display_kdk_bracket(n, games_per_person, player_with_number):
    if games_per_person == 3:
        bracket = KDK_3G.get(n)
        title = f"KDK 1인 3게임 - {n}명"
    else:
        bracket = KDK_4G.get(n)
        title = f"KDK 1인 4게임 - {n}명"
    if not bracket:
        return
    number_to_name = {v: k for k, v in player_with_number.items()}
    rows_html = ""
    for idx, (a, b, c, d) in enumerate(bracket):
        team1 = f"{number_to_name.get(a, str(a))}({a})&{number_to_name.get(b, str(b))}({b})"
        team2 = f"{number_to_name.get(c, str(c))}({c})&{number_to_name.get(d, str(d))}({d})"
        rows_html += f"<tr><td style='text-align:center'>{idx+1}</td><td style='text-align:center'>{team1} vs {team2}</td></tr>"
    html = f"""
<div class="kdk-bracket">
  <strong>📋 {title}</strong><br><br>
  <table style="width:100%">
    <thead><tr><th style="text-align:center">순서</th><th style="text-align:center">대진</th></tr></thead>
    <tbody>{rows_html}</tbody>
  </table>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 세션 초기화
# ══════════════════════════════════════════════════════════════
if "is_admin" not in st.session_state: st.session_state.is_admin = False
if "menu" not in st.session_state: st.session_state.menu = "ranking"
if "participants" not in st.session_state: st.session_state.participants = []

# ══════════════════════════════════════════════════════════════
# 네비게이션 바
# ══════════════════════════════════════════════════════════════
MENU_DEFS = [
    ("ranking", "🏆\n랭킹"),
    ("schedule", "📅\n대진"),
    ("result", "📊\n결과"),
    ("archive", "📂\n기록"),
    ("admin", "⚙️\n관리"),
]

st.markdown("""
<div style="background:#1D5B2E;padding:8px 12px 0 12px;margin:0 -0.5rem 0 -0.5rem;">
  <div style="text-align:center;color:rgba(255,255,255,0.55);font-size:0.6rem;letter-spacing:1px;margin-bottom:2px">🎾 두류 테니스</div>
</div>
""", unsafe_allow_html=True)

nav_cols = st.columns(len(MENU_DEFS))
for col, (key, label) in zip(nav_cols, MENU_DEFS):
    is_active = st.session_state.menu == key
    with col:
        btn_type = "primary" if is_active else "secondary"
        if st.button(label, key=f"nav_{key}", use_container_width=True, type=btn_type):
            st.session_state.menu = key
            st.rerun()

st.markdown("""
<div style="background:#1D5B2E;height:4px;margin:0 -0.5rem 8px -0.5rem;"></div>
""", unsafe_allow_html=True)

M = st.session_state.menu

# ══════════════════════════════════════════════════════════════
# 1. 랭킹
# ══════════════════════════════════════════════════════════════
if M == "ranking":
    st.markdown("<div class='main-hdr'>🏆 두류 랭킹</div>", unsafe_allow_html=True)
    gcfg = load_gsheet_config()
    if gcfg.get("enabled") and gcfg.get("sheet_id"):
        st.markdown("<div class='gsheet-banner'>🟢 구글 시트 연동 활성화 — 데이터가 자동으로 공유됩니다</div>", unsafe_allow_html=True)
    df = load_rank()
    if df.empty:
        st.info("등록된 랭킹이 없습니다.")
    else:
        icons = ["🥇","🥈","🥉"]
        disp = df.copy()
        disp.insert(0, "순위", [icons[i] if i<3 else str(i+1) for i in range(len(disp))])
        col_cfg = {c: st.column_config.TextColumn(c, width="small") for c in disp.columns}
        st.dataframe(disp, use_container_width=True, hide_index=True, column_config=col_cfg)
        st.download_button("📥 엑셀 다운로드", data=to_excel(df), file_name=f"랭킹_{date.today()}.xlsx", use_container_width=True)

# ══════════════════════════════════════════════════════════════
# 2. 대진·경기현황 (변경 없음)
# ══════════════════════════════════════════════════════════════
elif M == "schedule":
    tours = load_tours()
    active = [k for k,v in tours.items() if v.get("status")=="진행중"]
    if not active:
        st.warning("진행 중인 대회가 없습니다.")
        st.stop()
    tid = active[-1]
    tour = tours[tid]
    st.markdown(f"<div class='main-hdr'>📅 {tour['title']}</div>", unsafe_allow_html=True)
    st.caption(f"{tour.get('date','')} | {tour.get('place','')} | 코트 {tour.get('courts',2)}면")

    gnames = list(tour["groups"].keys())
    if not gnames:
        st.info("대진이 없습니다.")
        st.stop()

    tabs = st.tabs([f"{GLBL[i%len(GLBL)]} {gn}" for i, gn in enumerate(gnames)])
    for ti, g in enumerate(gnames):
        with tabs[ti]:
            ginfo = tour["groups"][g]
            matches = ginfo["matches"]
            mode = ginfo["mode"]
            cls = GCLS[ti % len(GCLS)]
            player_with_number = ginfo.get("player_with_number", {})
            is_fixed = (mode == "고정페어")
            
            if is_fixed:
                stats = group_stats_fixed(matches)
                rank_items = list(stats.keys())
            else:
                stats = group_stats_kdk(matches)
                rank_items = list(stats.keys())
            
            st.markdown("**📋 전적 매트릭스**")
            if matches and rank_items:
                if is_fixed:
                    lab = {t: " & ".join(list(t)) for t in rank_items}
                else:
                    lab = {p: f"{p}({player_with_number.get(p, '?')})" for p in rank_items}
                mat = {lab[t]: {lab[o]: ("■" if t==o else "X") for o in lab.keys()} for t in lab.keys()}
                for m in matches:
                    if is_fixed:
                        t1, t2 = tuple(m["t1"]), tuple(m["t2"])
                    else:
                        p1, p2 = m["t1"], m["t2"]
                    s1, s2 = int(m["s1"]), int(m["s2"])
                    if s1 > 0 or s2 > 0:
                        if is_fixed:
                            mat[lab[t1]][lab[t2]] = f"{s1}:{s2}"
                            mat[lab[t2]][lab[t1]] = f"{s2}:{s1}"
                        else:
                            for a in p1:
                                for b in p2:
                                    mat[lab[a]][lab[b]] = f"{s1}:{s2}"
                                    mat[lab[b]][lab[a]] = f"{s2}:{s1}"
                mdf = pd.DataFrame(mat).T
                header_cells = "".join(f"<th>{col}</th>" for col in mdf.columns)
                html = f'<table class="matrix-table"><thead><tr><th></th>{header_cells}</tr></thead><tbody>'
                for idx, row in mdf.iterrows():
                    html += f"叉戟<th>{idx}</th>"
                    for col in mdf.columns:
                        val = row[col]
                        if val == '■':
                            html += '<td class="matrix-grey">■</td>'
                        elif val == 'X':
                            html += '<td class="matrix-x">—</td>'
                        else:
                            html += f"<td>{val}</td>"
                    html += "</tr>"
                html += "</tbody></table>"
                st.markdown(html, unsafe_allow_html=True)
            
            if not is_fixed and player_with_number:
                st.divider()
                display_kdk_bracket(len(player_with_number), ginfo.get("games", 3), player_with_number)
            
            st.divider()
            st.markdown("**🏅 현재 순위**")
            if rank_items:
                ranked = sorted(rank_items, key=lambda x: (-stats[x]["승"], -stats[x]["득실"]))
                rows = []
                for i, item in enumerate(ranked):
                    if is_fixed:
                        rows.append({
                            "순위": i+1,
                            "팀": " & ".join(list(item)),
                            "승": stats[item]["승"],
                            "패": stats[item]["패"],
                            "득실": f'{stats[item]["득실"]:+d}'
                        })
                    else:
                        rows.append({
                            "순위": i+1,
                            "선수": item,
                            "승": stats[item]["승"],
                            "패": stats[item]["패"],
                            "득실": f'{stats[item]["득실"]:+d}',
                            "비고": get_grade_kdk(i+1)
                        })
                rank_df = pd.DataFrame(rows)
                rank_col_cfg = {c: st.column_config.TextColumn(c, width="small") for c in rank_df.columns}
                st.dataframe(rank_df, use_container_width=True, hide_index=True, column_config=rank_col_cfg)
            
            st.divider()
            st.markdown("**🎾 경기 입력**")
            changed = False
            for mi, m in enumerate(matches):
                t1 = " & ".join(m["t1"])
                t2 = " & ".join(m["t2"])
                color_class = ["match-color-0", "match-color-1", "match-color-2"][mi % 3]
                
                c1, c2, c3 = st.columns([4, 1, 4])
                with c1:
                    st.markdown(f'<div class="team-box {color_class}">{t1}</div>', unsafe_allow_html=True)
                    s1 = st.number_input("", 0, 50, int(m["s1"]), key=f"{tid}_{g}_{mi}_s1", label_visibility="collapsed")
                with c2:
                    st.markdown('<div class="vs-circle">VS</div>', unsafe_allow_html=True)
                with c3:
                    st.markdown(f'<div class="team-box {color_class}">{t2}</div>', unsafe_allow_html=True)
                    s2 = st.number_input("", 0, 50, int(m["s2"]), key=f"{tid}_{g}_{mi}_s2", label_visibility="collapsed")
                
                if s1 != int(m["s1"]) or s2 != int(m["s2"]):
                    tour["groups"][g]["matches"][mi]["s1"] = s1
                    tour["groups"][g]["matches"][mi]["s2"] = s2
                    changed = True
                if mi < len(matches)-1:
                    st.markdown("<hr>", unsafe_allow_html=True)
            
            if changed:
                tours[tid] = tour
                save_tours(tours)
                st.toast("✅ 저장됨", icon="✅")

# ══════════════════════════════════════════════════════════════
# 3. 경기 결과 (변경 없음)
# ══════════════════════════════════════════════════════════════
elif M == "result":
    tours = load_tours()
    active = [k for k,v in tours.items() if v.get("status")=="진행중"]
    if not active:
        st.warning("진행 중인 대회가 없습니다.")
        st.stop()
    tid = active[-1]
    tour = tours[tid]
    st.markdown(f"<div class='main-hdr'>📊 {tour['title']}</div>", unsafe_allow_html=True)

    for g, ginfo in tour["groups"].items():
        mode = ginfo["mode"]
        matches = ginfo["matches"]
        player_with_number = ginfo.get("player_with_number", {})
        is_fixed = (mode == "고정페어")
        
        if is_fixed:
            stats = group_stats_fixed(matches)
            ranked = sorted(stats.keys(), key=lambda t: (-stats[t]["승"], -stats[t]["득실"]))
        else:
            stats = group_stats_kdk(matches)
            ranked = sorted(stats.keys(), key=lambda p: (-stats[p]["승"], -stats[p]["득실"]))
        
        st.markdown(f'<div class="sec">{g} ({mode})</div>', unsafe_allow_html=True)
        
        if not is_fixed and player_with_number:
            display_kdk_bracket(len(player_with_number), ginfo.get("games", 3), player_with_number)
            st.divider()
        
        st.markdown("**🏆 최종 순위**")
        rows = []
        for i, item in enumerate(ranked):
            pt = rank_pts(i+1, mode)
            if is_fixed:
                rows.append({
                    "순위": i+1, "팀": " & ".join(list(item)),
                    "승": stats[item]["승"], "패": stats[item]["패"],
                    "득실": f'{stats[item]["득실"]:+d}', "포인트": pt,
                    "등급": ["우승","준우승","3위"][i] if i<3 else "참가"
                })
            else:
                rows.append({
                    "순위": i+1, "선수": item,
                    "승": stats[item]["승"], "패": stats[item]["패"],
                    "득실": f'{stats[item]["득실"]:+d}', "포인트": pt,
                    "비고": get_grade_kdk(i+1)
                })
        res_df = pd.DataFrame(rows)
        res_col_cfg = {c: st.column_config.TextColumn(c, width="small") for c in res_df.columns}
        st.dataframe(res_df, use_container_width=True, hide_index=True, column_config=res_col_cfg)
        
        with st.expander("📋 전체 경기 결과"):
            mrows = [{"경기": f"{' & '.join(m['t1'])} vs {' & '.join(m['t2'])}", 
                      "결과": f"{m['s1']}:{m['s2']}"} for m in matches]
            st.dataframe(pd.DataFrame(mrows), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# 4. 지난 대회 (변경 없음)
# ══════════════════════════════════════════════════════════════
elif M == "archive":
    st.markdown("<div class='main-hdr'>📂 지난 대회</div>", unsafe_allow_html=True)
    tours = load_tours()
    past = {k:v for k,v in tours.items() if v.get("status")!="진행중"}
    if not past:
        st.info("완료된 대회가 없습니다.")
        st.stop()
    sel = st.selectbox("대회 선택", list(past.keys()), format_func=lambda k: f"{past[k]['title']} ({past[k].get('date','')})")
    tour = past[sel]
    st.markdown(f"**🏆 {tour['title']}** | {tour.get('date','')} | {tour.get('place','')}")
    st.divider()
    if not tour.get("groups"):
        st.info("대진 정보 없음")
        st.stop()
    for g, ginfo in tour["groups"].items():
        mode = ginfo["mode"]
        matches = ginfo["matches"]
        player_with_number = ginfo.get("player_with_number", {})
        is_fixed = (mode == "고정페어")
        
        if is_fixed:
            stats = group_stats_fixed(matches)
            ranked = sorted(stats.keys(), key=lambda t: (-stats[t]["승"], -stats[t]["득실"]))
        else:
            stats = group_stats_kdk(matches)
            ranked = sorted(stats.keys(), key=lambda p: (-stats[p]["승"], -stats[p]["득실"]))
        
        st.markdown(f'<div class="sec">{g} ({mode})</div>', unsafe_allow_html=True)
        if not is_fixed and player_with_number:
            display_kdk_bracket(len(player_with_number), ginfo.get("games", 3), player_with_number)
            st.divider()
        
        rows = []
        for i, item in enumerate(ranked):
            pt = rank_pts(i+1, mode)
            if is_fixed:
                rows.append({
                    "순위": i+1, "팀/선수": " & ".join(list(item)),
                    "승": stats[item]["승"], "패": stats[item]["패"],
                    "득실": f'{stats[item]["득실"]:+d}', "포인트": pt,
                    "등급": ["우승","준우승","3위"][i] if i<3 else "참가"
                })
            else:
                rows.append({
                    "순위": i+1, "선수": item,
                    "승": stats[item]["승"], "패": stats[item]["패"],
                    "득실": f'{stats[item]["득실"]:+d}', "포인트": pt,
                    "비고": get_grade_kdk(i+1)
                })
        arc_df = pd.DataFrame(rows)
        arc_col_cfg = {c: st.column_config.TextColumn(c, width="small") for c in arc_df.columns}
        st.dataframe(arc_df, use_container_width=True, hide_index=True, column_config=arc_col_cfg)

# ══════════════════════════════════════════════════════════════
# 5. 관리자 (핵심 수정: 그룹 먼저 만들기 + 체크박스 배정)
# ══════════════════════════════════════════════════════════════
elif M == "admin":
    st.markdown("<div class='main-hdr'>⚙️ 관리자</div>", unsafe_allow_html=True)
    pw = st.text_input("🔒 비밀번호", type="password", placeholder="비밀번호 입력")
    if pw == ADMIN_PW:
        st.session_state.is_admin = True
    if not st.session_state.is_admin:
        if pw and pw != ADMIN_PW:
            st.error("비밀번호 오류")
        st.stop()
    st.success("관리자 모드")

    adm = st.tabs(["🏆 대회", "👥 참가자·대진", "📋 랭킹", "💾 반영", "🔗 구글 시트"])

    # ── 대회 관리 (기존과 동일) ─────────────────────────────────
    with adm[0]:
        st.markdown('<div class="sec">새 대회 생성</div>', unsafe_allow_html=True)
        with st.form("f_new_tour"):
            tn = st.text_input("대회명")
            td = st.date_input("날짜", value=date.today())
            tp = st.text_input("장소")
            courts = st.selectbox("코트 수", [1,2,3], index=1)
            if st.form_submit_button("✅ 생성", use_container_width=True):
                if tn.strip():
                    tours = load_tours()
                    tid = f"{td}_{tn.strip()}"
                    if tid not in tours:
                        tours[tid] = {"title": tn.strip(), "date": str(td), "place": tp,
                                      "courts": courts, "status": "진행중", "groups": {}}
                        save_tours(tours)
                        st.success("생성됨!")
                        st.rerun()
                    else:
                        st.warning("이미 존재")
        
        st.divider()
        st.markdown('<div class="sec">대회 목록</div>', unsafe_allow_html=True)
        tours = load_tours()
        if tours:
            for tid2, tv in list(tours.items()):
                col1, col2, col3 = st.columns([2, 1.5, 1.5])
                with col1:
                    st.markdown(f"**{tv['title']}** ({tv.get('date','')})")
                with col2:
                    cur_status = tv.get("status","진행중")
                    status_opts = ["진행중","완료","예정"]
                    new_st = st.selectbox(
                        "상태",
                        status_opts,
                        index=status_opts.index(cur_status) if cur_status in status_opts else 0,
                        key=f"status_sel_{tid2}",
                        label_visibility="collapsed"
                    )
                with col3:
                    if st.button("💾 상태 수정", key=f"edit_status_{tid2}", use_container_width=True):
                        tours[tid2]["status"] = new_st
                        save_tours(tours)
                        st.success("상태 수정됨!")
                        st.rerun()
                
                if st.button(f"✏️ 상세 수정", key=f"detail_edit_{tid2}", use_container_width=True):
                    st.session_state.edit_tour_id = tid2
                    st.rerun()
                
                if st.button(f"🗑 삭제", key=f"del_{tid2}", use_container_width=True):
                    del tours[tid2]
                    save_tours(tours)
                    st.rerun()
                st.divider()
        
        # 상세 수정 모드
        edit_id = st.session_state.get("edit_tour_id")
        if edit_id and edit_id in tours:
            edit_tour = tours[edit_id]
            st.markdown(f'<div class="sec">✏️ "{edit_tour["title"]}" 상세 수정</div>', unsafe_allow_html=True)
            
            new_title  = st.text_input("대회명", value=edit_tour["title"], key="edit_title")
            try:
                default_date = pd.to_datetime(edit_tour.get("date", str(date.today()))).date()
            except Exception:
                default_date = date.today()
            new_date   = st.date_input("날짜", value=default_date, key="edit_date")
            new_place  = st.text_input("장소", value=edit_tour.get("place", ""), key="edit_place")
            new_courts = st.selectbox("코트 수", [1,2,3], index=max(0, edit_tour.get("courts", 2)-1), key="edit_courts")
            
            col_save, col_cancel = st.columns(2)
            with col_save:
                if st.button("💾 기본 정보 저장", type="primary", use_container_width=True, key="save_basic_info"):
                    edit_tour["title"]  = new_title
                    edit_tour["date"]   = str(new_date)
                    edit_tour["place"]  = new_place
                    edit_tour["courts"] = new_courts
                    save_tours(tours)
                    st.success("저장 완료!")
                    st.session_state.edit_tour_id = None
                    st.rerun()
            with col_cancel:
                if st.button("취소", use_container_width=True, key="cancel_edit"):
                    st.session_state.edit_tour_id = None
                    st.rerun()
            st.divider()
            
            st.markdown('<div class="sec">🎲 그룹 설정 수정</div>', unsafe_allow_html=True)
            st.caption("※ 그룹 설정을 변경하면 기존 대진이 초기화됩니다.")
            
            current_groups     = edit_tour.get("groups", {})
            current_group_names = list(current_groups.keys())
            
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                gcnt = st.number_input("그룹 수", 1, 6, value=max(1, len(current_group_names)), key="edit_gcnt")
            with col_info2:
                st.write(f"현재 {len(current_group_names)}개 그룹")
            
            gcfg = {}
            group_names = [f"{chr(65+i)}그룹" for i in range(int(gcnt))]
            for i, gn in enumerate(group_names):
                existing = current_groups.get(gn, {})
                st.markdown(f"**{gn}**")
                col_a, col_b, col_c, col_d = st.columns(4)
                with col_a:
                    default_sz = len(existing.get("players", [])) if existing else 8
                    sz = st.number_input("인원", 2, 30, value=default_sz, key=f"edit_sz_{edit_id}_{i}")
                with col_b:
                    default_md = existing.get("mode", "고정페어")
                    md_opts    = ["고정페어","KDK","단식"]
                    md = st.selectbox("방식", md_opts,
                                      index=md_opts.index(default_md) if default_md in md_opts else 0,
                                      key=f"edit_md_{edit_id}_{i}")
                with col_c:
                    default_gc = existing.get("games", 4)
                    gc_opts    = [3, 4, 5]
                    gc = st.selectbox("게임수", gc_opts,
                                      index=gc_opts.index(default_gc) if default_gc in gc_opts else 1,
                                      key=f"edit_gc_{edit_id}_{i}")
                with col_d:
                    current_count = len(existing.get("players", []))
                    st.write(f"현재 {current_count}명")
                gcfg[gn] = (sz, md, gc)
            
            total       = sum(c[0] for c in gcfg.values())
            all_players = edit_tour.get("players", [])
            if total == len(all_players):
                st.success(f"✅ 참가자 {len(all_players)}명 / 배정 {total}명")
            else:
                st.warning(f"⚠️ 참가자 {len(all_players)}명 / 배정 {total}명 (차이 {len(all_players)-total:+d}명)")
            
            if st.button("🎲 그룹 설정 적용 및 대진 재생성", type="primary", use_container_width=True, key="apply_group_config"):
                players_sorted = all_players
                ptr = 0
                new_groups = {}
                for gn, (sz, md, gc) in gcfg.items():
                    gp = players_sorted[ptr:ptr+sz]
                    ptr += sz
                    if md == "고정페어":
                        ms, pwn = make_fixed(gp), {}
                        ms = ms[0]
                    elif md == "KDK":
                        ms, pwn = make_kdk(gp, gc)
                        if not ms:
                            ms, pwn = make_singles(gp), {}
                            ms = ms[0]
                    else:
                        ms, pwn = make_singles(gp), {}
                        ms = ms[0]
                    new_groups[gn] = {"players": gp, "mode": md, "games": gc, "matches": ms, "player_with_number": pwn}
                edit_tour["groups"] = new_groups
                save_tours(tours)
                st.success("그룹 설정 적용 완료!")
                st.rerun()

    # ── 참가자·대진 (개선: 그룹 먼저 생성, 체크박스 배정) ─────────
    with adm[1]:
        tours = load_tours()
        active_t = [k for k,v in tours.items() if v.get("status") == "진행중"]
        if not active_t:
            st.warning("진행 중인 대회 없음")
            st.stop()
        sel_tid = st.selectbox("대회 선택", active_t,
                               format_func=lambda k: tours[k]['title'],
                               key="adm1_sel_tid")
        tour = tours[sel_tid]

        # ========== 1. 그룹 구성 설정 (저장된 그룹 정보가 없으면 설정) ==========
        st.markdown('<div class="sec">🎲 1. 그룹 구성 설정</div>', unsafe_allow_html=True)
        st.caption("그룹 수, 인원, 방식, 게임수를 설정합니다. (기존 그룹이 있으면 불러옵니다)")

        # 현재 그룹 정보 불러오기
        current_groups = tour.get("groups", {})
        if current_groups:
            # 기존 그룹이 있으면 설정값을 표시 (편집 가능)
            current_group_names = list(current_groups.keys())
            default_gcnt = len(current_group_names)
        else:
            default_gcnt = 4

        col_gcnt, _ = st.columns([1, 3])
        with col_gcnt:
            gcnt = st.number_input("그룹 수", 1, 6, value=default_gcnt, key="group_cnt")

        group_names = [f"{chr(65+i)}그룹" for i in range(gcnt)]
        gcfg = {}   # {그룹명: (인원수, 방식, 게임수)}

        for i, gn in enumerate(group_names):
            existing = current_groups.get(gn, {})
            st.markdown(f"**{gn}**")
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                default_sz = len(existing.get("players", [])) if existing else 8
                sz = st.number_input("인원", 2, 30, value=default_sz, key=f"grp_sz_{i}")
            with col_b:
                default_md = existing.get("mode", "고정페어")
                md_opts = ["고정페어","KDK","단식"]
                md = st.selectbox("방식", md_opts, index=md_opts.index(default_md), key=f"grp_md_{i}")
            with col_c:
                default_gc = existing.get("games", 4)
                gc_opts = [3,4,5]
                gc = st.selectbox("게임수", gc_opts, index=gc_opts.index(default_gc), key=f"grp_gc_{i}")
            with col_d:
                st.write(f"현재 {len(existing.get('players', []))}명")
            gcfg[gn] = (sz, md, gc)

        # 그룹 구성 저장 버튼 (세션에만 저장, 실제 대진은 참가자 배정 후 생성)
        if st.button("💾 그룹 구성 저장 (참가자 배정 단계로 이동)", use_container_width=True, key="save_group_config"):
            # 임시로 세션에 그룹 설정 저장 (tour에 임시 필드 추가)
            st.session_state.temp_group_config = gcfg
            st.session_state.temp_tour_id = sel_tid
            st.success("그룹 구성이 저장되었습니다. 아래에서 참가자를 배정하세요.")
            st.rerun()

        st.divider()

        # ========== 2. 참가자 배정 (체크박스/전체선택) ==========
        st.markdown('<div class="sec">👥 2. 참가자 배정</div>', unsafe_allow_html=True)

        # 임시 저장된 그룹 구성이 있는지 확인
        if st.session_state.get("temp_group_config") and st.session_state.get("temp_tour_id") == sel_tid:
            gcfg = st.session_state.temp_group_config
        else:
            # 없으면 현재 tour의 그룹 설정 사용 (기존 대진이 있을 경우)
            if current_groups:
                # 현재 그룹에서 설정 추출
                gcfg = {}
                for gn, ginfo in current_groups.items():
                    gcfg[gn] = (len(ginfo.get("players", [])), ginfo.get("mode", "고정페어"), ginfo.get("games", 4))
            else:
                st.info("먼저 '그룹 구성 저장' 버튼을 눌러 그룹을 설정하세요.")
                st.stop()

        # 전체 회원 명단 (랭킹순)
        all_members = load_members()
        if not all_members:
            st.warning("회원 명단이 없습니다. 먼저 '랭킹 관리'에서 엑셀을 업로드하세요.")
            st.stop()

        # 현재 각 그룹에 배정된 선수들 (기존 대진 정보에서 가져오거나 빈 리스트)
        assigned = {}
        for gn in gcfg.keys():
            if gn in current_groups:
                assigned[gn] = current_groups[gn].get("players", []).copy()
            else:
                assigned[gn] = []

        # 전체 미배정 선수 (모든 멤버에서 이미 배정된 선수 제외)
        already_assigned = set()
        for lst in assigned.values():
            already_assigned.update(lst)
        available_members = [m for m in all_members if m not in already_assigned]

        st.markdown("**각 그룹에 참가할 선수를 선택하세요.** (멀티 선택 가능)")
        st.caption("※ 한 선수는 하나의 그룹에만 배정될 수 있습니다. 이미 배정된 선수는 다른 그룹에 나타나지 않습니다.")

        # 각 그룹별 멀티셀렉트 표시
        new_assigned = {}
        for gn, (sz, md, gc) in gcfg.items():
            st.markdown(f"#### {gn} (최대 {sz}명)")
            # 현재 이 그룹에 배정된 선수들
            current_assigned = assigned.get(gn, [])
            # 전체 사용 가능한 목록 (이미 다른 그룹에 배정된 선수는 제외)
            # 단, 현재 그룹에 이미 배정된 선수는 목록에 포함
            other_assigned = set()
            for other_gn, lst in assigned.items():
                if other_gn != gn:
                    other_assigned.update(lst)
            selectable = [m for m in all_members if m not in other_assigned or m in current_assigned]

            # 멀티셀렉트
            selected = st.multiselect(
                f"{gn} 참가자",
                options=selectable,
                default=current_assigned,
                key=f"assign_{gn}"
            )
            # 제한 인원 초과 시 경고
            if len(selected) > sz:
                st.warning(f"{gn}의 최대 인원은 {sz}명입니다. 현재 {len(selected)}명 선택됨")
            new_assigned[gn] = selected[:sz]  # 초과 시 자름

            # 전체선택/전체해제 버튼 (해당 그룹)
            col_sel, col_desel = st.columns(2)
            with col_sel:
                if st.button(f"✅ {gn} 전체선택", key=f"select_all_{gn}", use_container_width=True):
                    # 전체 선택 가능한 선수들 중에서 sz 만큼만 선택 (원칙적으로는 전체 가능한 목록)
                    full_select = selectable[:sz]
                    st.session_state[f"temp_select_{gn}"] = full_select
                    st.rerun()
            with col_desel:
                if st.button(f"❌ {gn} 전체해제", key=f"deselect_all_{gn}", use_container_width=True):
                    st.session_state[f"temp_select_{gn}"] = []
                    st.rerun()

            # 세션 임시 저장값 처리 (rerun 후에도 유지)
            if f"temp_select_{gn}" in st.session_state:
                new_assigned[gn] = st.session_state[f"temp_select_{gn}"]
                del st.session_state[f"temp_select_{gn}"]

        # 배정된 총 인원 확인
        total_assigned = sum(len(lst) for lst in new_assigned.values())
        total_needed = sum(sz for sz, _, _ in gcfg.values())
        if total_assigned != total_needed:
            st.warning(f"⚠️ 현재 배정된 인원: {total_assigned}명 / 필요한 총 인원: {total_needed}명")
        else:
            st.success(f"✅ 배정 완료! 총 {total_assigned}명")

        # 대진 생성 버튼
        if st.button("🎲 3. 대진 생성 (이 배정으로 경기 생성)", type="primary", use_container_width=True, key="generate_matches"):
            # 중복 검사
            all_selected = []
            for lst in new_assigned.values():
                all_selected.extend(lst)
            if len(set(all_selected)) != len(all_selected):
                st.error("같은 선수가 여러 그룹에 배정되었습니다! 중복을 제거하세요.")
                st.stop()
            if total_assigned != total_needed:
                st.error(f"인원 수가 맞지 않습니다. (필요 {total_needed}, 배정 {total_assigned})")
                st.stop()

            # 각 그룹별로 대진 생성
            new_groups = {}
            for gn, players in new_assigned.items():
                sz, md, gc = gcfg[gn]
                if len(players) != sz:
                    st.error(f"{gn}의 인원이 {sz}명이 아닙니다. (현재 {len(players)}명)")
                    st.stop()
                if md == "고정페어":
                    ms, pwn = make_fixed(players)
                elif md == "KDK":
                    ms, pwn = make_kdk(players, gc)
                    if not ms:
                        st.warning(f"{gn}: {gc}게임 기준 {len(players)}명은 지원하지 않습니다. 단식 리그로 대체합니다.")
                        ms, pwn = make_singles(players)
                else:
                    ms, pwn = make_singles(players)
                new_groups[gn] = {
                    "players": players,
                    "mode": md,
                    "games": gc,
                    "matches": ms,
                    "player_with_number": pwn
                }
            tour["groups"] = new_groups
            # 전체 players 목록 업데이트 (전체 참가자 명단)
            tour["players"] = all_selected
            save_tours(tours)
            # 임시 그룹 구성 삭제
            if "temp_group_config" in st.session_state:
                del st.session_state.temp_group_config
            if "temp_tour_id" in st.session_state:
                del st.session_state.temp_tour_id
            st.success("✅ 대진 생성 완료! '대진·경기현황'에서 확인하세요.")
            st.rerun()

        st.divider()

        # ========== 기존 개별 참가자 수정 (대진 유지) ==========
        st.markdown('<div class="sec">✏️ 개별 참가자 수정 (대진 유지)</div>', unsafe_allow_html=True)
        if tour.get("groups"):
            groups = list(tour["groups"].keys())
            if groups:
                sel_group = st.selectbox("그룹 선택", groups, key="adm1_edit_group")
                current_players = tour["groups"][sel_group]["players"].copy()
                st.markdown(f"**현재 {sel_group} 참가자:** {', '.join(current_players) if current_players else '없음'}")
                
                if current_players:
                    sel_player = st.selectbox("삭제할 참가자", current_players, key="adm1_del_player")
                    if st.button("🗑 삭제", use_container_width=True, key="adm1_del_btn"):
                        tour["groups"][sel_group]["players"].remove(sel_player)
                        new_matches = [m for m in tour["groups"][sel_group]["matches"]
                                       if sel_player not in m["t1"] and sel_player not in m["t2"]]
                        tour["groups"][sel_group]["matches"] = new_matches
                        all_group_players = [p for g in groups for p in tour["groups"][g]["players"]]
                        if sel_player not in all_group_players:
                            if sel_player in tour.get("players", []):
                                tour["players"].remove(sel_player)
                        save_tours(tours)
                        st.success(f"'{sel_player}' 삭제됨")
                        st.rerun()
                
                st.markdown("---")
                new_name = st.text_input("새 참가자 이름", placeholder="예: 홍길동", key="adm1_add_player")
                if st.button("➕ 추가", use_container_width=True, key="adm1_add_btn"):
                    if new_name and new_name.strip():
                        new_name = new_name.strip()
                        if new_name not in tour["groups"][sel_group]["players"]:
                            tour["groups"][sel_group]["players"].append(new_name)
                            if new_name not in tour.get("players", []):
                                if "players" not in tour:
                                    tour["players"] = []
                                tour["players"].append(new_name)
                            mode = tour["groups"][sel_group]["mode"]
                            gc = tour["groups"][sel_group].get("games", 3)
                            if mode == "고정페어":
                                new_ms, _ = make_fixed(tour["groups"][sel_group]["players"])
                            elif mode == "KDK":
                                new_ms, new_pwn = make_kdk(tour["groups"][sel_group]["players"], gc)
                                if new_ms:
                                    tour["groups"][sel_group]["player_with_number"] = new_pwn
                                else:
                                    new_ms, _ = make_singles(tour["groups"][sel_group]["players"])
                            else:
                                new_ms, _ = make_singles(tour["groups"][sel_group]["players"])
                            tour["groups"][sel_group]["matches"] = new_ms
                            save_tours(tours)
                            st.success(f"'{new_name}' 추가됨")
                            st.rerun()
                        else:
                            st.warning("이미 있는 참가자입니다.")
                
                st.markdown("---")
                all_players_with_group = [(p, g) for g in groups for p in tour["groups"][g]["players"]]
                if all_players_with_group:
                    move_player = st.selectbox("이동할 참가자", [p for p,_ in all_players_with_group], key="adm1_move_player")
                    current_group = next((g for p, g in all_players_with_group if p == move_player), groups[0])
                    other_groups = [g for g in groups if g != current_group]
                    if other_groups:
                        target_group = st.selectbox("이동할 그룹", other_groups, key="adm1_target_group")
                        if st.button("🔄 이동", use_container_width=True, key="adm1_move_btn"):
                            tour["groups"][current_group]["players"].remove(move_player)
                            tour["groups"][target_group]["players"].append(move_player)
                            for grp in [current_group, target_group]:
                                mode = tour["groups"][grp]["mode"]
                                gc = tour["groups"][grp].get("games", 3)
                                if mode == "고정페어":
                                    new_ms, _ = make_fixed(tour["groups"][grp]["players"])
                                elif mode == "KDK":
                                    new_ms, new_pwn = make_kdk(tour["groups"][grp]["players"], gc)
                                    if new_ms:
                                        tour["groups"][grp]["player_with_number"] = new_pwn
                                    else:
                                        new_ms, _ = make_singles(tour["groups"][grp]["players"])
                                else:
                                    new_ms, _ = make_singles(tour["groups"][grp]["players"])
                                tour["groups"][grp]["matches"] = new_ms
                            save_tours(tours)
                            st.success(f"'{move_player}' {target_group}으로 이동됨")
                            st.rerun()
                    else:
                        st.info("이동할 다른 그룹이 없습니다.")
        else:
            st.info("아직 생성된 그룹이 없습니다. 위에서 그룹 구성 후 대진을 생성하세요.")

        # ========== 일괄 입력(텍스트) 방식도 유지 (선택사항) ==========
        with st.expander("📝 대체 방식: 참가자 명단 텍스트 일괄 입력 (기존 그룹 유지)"):
            st.markdown('<div class="sec">📝 참가자 명단 (일괄 입력)</div>', unsafe_allow_html=True)
            member_roster = load_members()
            default_text = ", ".join(tour.get("players", st.session_state.participants))
            part_input = st.text_area("참가자 명단", value=default_text, height=100)
            if st.button("✅ 명단 저장 (기존 그룹 유지)", use_container_width=True, key="save_roster_bulk"):
                raw_names = part_input.replace("\n", ",").split(",")
                parsed = [n.strip() for n in raw_names if n.strip()]
                roster_order = {nm: i for i, nm in enumerate(member_roster)}
                parsed_sorted = sorted(set(parsed), key=lambda x: roster_order.get(x, len(member_roster)+1))
                st.session_state.participants = parsed_sorted
                tours[sel_tid]["players"] = parsed_sorted
                save_tours(tours)
                st.success(f"{len(parsed_sorted)}명 저장됨")
                st.rerun()

    # ── 랭킹 관리 (기존과 동일) ─────────────────────────────────
    with adm[2]:
        st.markdown('<div class="sec">📁 엑셀 업로드</div>', unsafe_allow_html=True)
        up = st.file_uploader("파일 선택", type=["xlsx","csv"])
        if up:
            try:
                df_up = (pd.read_excel(up) if up.name.endswith("xlsx") else pd.read_csv(up, encoding_errors="replace"))
                if "현재포인트" in df_up.columns:
                    df_up["현재포인트"] = pd.to_numeric(df_up["현재포인트"], errors="coerce").fillna(0)
                    df_up = df_up.sort_values("현재포인트", ascending=False).reset_index(drop=True)
                    df_up["랭킹"] = df_up.index + 1
                st.dataframe(df_up, use_container_width=True)
                if st.button("💾 저장", type="primary", key="adm2_save_upload"):
                    save_rank(df_up)
                    if "이름" in df_up.columns:
                        save_members(df_up["이름"].tolist())
                    st.success("저장 완료!")
                    st.rerun()
            except Exception as e:
                st.error(f"오류: {e}")
        
        st.divider()
        st.markdown('<div class="sec">📊 현재 랭킹</div>', unsafe_allow_html=True)
        df_cur = load_rank()
        if not df_cur.empty:
            st.dataframe(df_cur, use_container_width=True)
            st.download_button("📥 다운로드", data=to_excel(df_cur),
                               file_name=f"랭킹_{date.today()}.xlsx",
                               key="adm2_download")
        
        st.divider()
        st.markdown('<div class="sec">✏️ 직접 수정</div>', unsafe_allow_html=True)
        df_edit = load_rank()
        if not df_edit.empty:
            edited = st.data_editor(df_edit, use_container_width=True, hide_index=True, num_rows="dynamic")
            if st.button("💾 수정 저장", type="primary", key="adm2_save_edit"):
                save_rank(edited)
                save_members(edited["이름"].tolist())
                st.success("저장 완료!")
                st.rerun()

    # ── 결과 반영 (기존과 동일) ─────────────────────────────────
    with adm[3]:
        tours = load_tours()
        active2 = [k for k,v in tours.items() if v.get("status") == "진행중"]
        if not active2:
            st.warning("진행 중인 대회 없음")
            st.stop()
        sel_tid2 = st.selectbox("대회 선택", active2,
                                format_func=lambda k: tours[k]['title'],
                                key="adm3_sel_tid")
        tour3 = tours[sel_tid2]
        if not tour3.get("groups"):
            st.warning("대진 없음")
            st.stop()
        
        earn = {}
        for g, ginfo in tour3["groups"].items():
            mode = ginfo["mode"]
            matches = ginfo["matches"]
            is_fixed = (mode == "고정페어")
            if is_fixed:
                stats = group_stats_fixed(matches)
                ranked = sorted(stats.keys(), key=lambda t: (-stats[t]["승"], -stats[t]["득실"]))
            else:
                stats = group_stats_kdk(matches)
                ranked = sorted(stats.keys(), key=lambda p: (-stats[p]["승"], -stats[p]["득실"]))
            for i, item in enumerate(ranked):
                pt = rank_pts(i+1, mode)
                if is_fixed:
                    for p in list(item):
                        earn[p] = earn.get(p, 0) + pt
                else:
                    earn[item] = earn.get(item, 0) + pt
        
        if earn:
            earn_df = pd.DataFrame(earn.items(), columns=["선수", "획득포인트"])
            earn_col_cfg = {c: st.column_config.TextColumn(c, width="small") for c in earn_df.columns}
            st.dataframe(earn_df, use_container_width=True, column_config=earn_col_cfg)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🏆 랭킹 반영", type="primary", use_container_width=True, key="adm3_apply"):
                df_r = load_rank()
                if df_r.empty:
                    df_r = pd.DataFrame(columns=COLS_RANK)
                for p, pt in earn.items():
                    if p in df_r["이름"].values:
                        cur = df_r.loc[df_r["이름"] == p, "현재포인트"].values[0]
                        df_r.loc[df_r["이름"] == p, "현재포인트"] = cur + pt
                    else:
                        nr = {c: "" for c in COLS_RANK}
                        nr["이름"] = p
                        nr["현재포인트"] = pt
                        df_r = pd.concat([df_r, pd.DataFrame([nr])], ignore_index=True)
                save_rank(df_r)
                tours[sel_tid2]["status"] = "완료"
                save_tours(tours)
                st.success("반영 완료!")
                st.rerun()
        with c2:
            if st.button("🗑 점수 초기화", use_container_width=True, key="adm3_reset"):
                for g in tour3["groups"]:
                    for m in tour3["groups"][g]["matches"]:
                        m["s1"] = 0
                        m["s2"] = 0
                save_tours(tours)
                st.success("초기화 완료!")
                st.rerun()

    # ── 구글 시트 연동 (기존과 동일) ──────────────────────────────
    with adm[4]:
        st.markdown('<div class="sec">🔗 구글 시트 연동 설정</div>', unsafe_allow_html=True)
        gcfg = load_gsheet_config()
        st.markdown("""
<div style="background:#E8F5E9;border-radius:10px;padding:10px 14px;font-size:0.78rem;margin-bottom:10px;">
<b>📌 연동 방법 (3단계)</b><br><br>
① Google Cloud Console → 새 프로젝트 생성<br>
② "Google Sheets API" + "Google Drive API" 활성화<br>
③ 서비스 계정 생성 → JSON 키 다운로드<br>
④ 구글 시트를 만들고, 서비스 계정 이메일을 편집자로 공유<br>
⑤ 아래에 시트 ID와 JSON 키 붙여넣기<br><br>
<b>시트 ID 찾기:</b> 시트 URL에서 <code>docs.google.com/spreadsheets/d/<b>[여기가 ID]</b>/edit</code>
</div>
""", unsafe_allow_html=True)

        enabled = st.toggle("구글 시트 연동 활성화", value=gcfg.get("enabled", False), key="gs_toggle")
        sheet_id = st.text_input("구글 시트 ID", value=gcfg.get("sheet_id", ""), placeholder="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms")
        creds_input = st.text_area("서비스 계정 JSON 키", value=gcfg.get("credentials_json", ""), height=160)

        col_gs1, col_gs2 = st.columns(2)
        with col_gs1:
            if st.button("💾 설정 저장", type="primary", use_container_width=True, key="gs_save"):
                new_cfg = {"enabled": enabled, "sheet_id": sheet_id.strip(), "credentials_json": creds_input.strip()}
                save_gsheet_config(new_cfg)
                st.success("설정 저장됨!")
                st.rerun()
        with col_gs2:
            if st.button("🔄 연결 테스트", use_container_width=True, key="gs_test"):
                if not sheet_id.strip() or not creds_input.strip():
                    st.warning("시트 ID와 JSON 키를 먼저 입력하세요.")
                else:
                    gc = get_gsheet_client(creds_input.strip())
                    if gc is None:
                        st.error("❌ gspread 패키지 없음. 서버에 `pip install gspread google-auth` 실행 필요.")
                    else:
                        try:
                            sh = gc.open_by_key(sheet_id.strip())
                            st.success(f"✅ 연결 성공! 시트명: {sh.title}")
                        except Exception as e:
                            st.error(f"❌ 연결 실패: {e}")
        st.divider()
        st.markdown('<div class="sec">📤 수동 동기화</div>', unsafe_allow_html=True)
        col_up1, col_up2 = st.columns(2)
        with col_up1:
            if st.button("📤 랭킹 → 시트 업로드", use_container_width=True, key="gs_upload_rank"):
                gcfg2 = load_gsheet_config()
                if not gcfg2.get("sheet_id") or not gcfg2.get("credentials_json"):
                    st.warning("설정을 먼저 저장하세요.")
                else:
                    df_r2 = load_rank()
                    ok, msg = sync_ranking_to_gsheet(df_r2, gcfg2["sheet_id"], gcfg2["credentials_json"])
                    (st.success if ok else st.error)(msg)
        with col_up2:
            if st.button("📤 경기결과 → 시트 업로드", use_container_width=True, key="gs_upload_tours"):
                gcfg2 = load_gsheet_config()
                if not gcfg2.get("sheet_id") or not gcfg2.get("credentials_json"):
                    st.warning("설정을 먼저 저장하세요.")
                else:
                    tours2 = load_tours()
                    ok, msg = sync_tours_to_gsheet(tours2, gcfg2["sheet_id"], gcfg2["credentials_json"])
                    (st.success if ok else st.error)(msg)
        st.divider()
        st.markdown('<div class="sec">📥 시트 → 랭킹 가져오기</div>', unsafe_allow_html=True)
        if st.button("📥 구글 시트에서 랭킹 불러오기", use_container_width=True, key="gs_download_rank"):
            gcfg2 = load_gsheet_config()
            if not gcfg2.get("sheet_id") or not gcfg2.get("credentials_json"):
                st.warning("설정을 먼저 저장하세요.")
            else:
                df_from_gs, msg = sync_ranking_from_gsheet(gcfg2["sheet_id"], gcfg2["credentials_json"])
                if df_from_gs is not None:
                    save_rank(df_from_gs)
                    st.success(msg + f" ({len(df_from_gs)}명 로드됨)")
                    st.rerun()
                else:
                    st.error(msg)
        st.divider()
        st.markdown("""
<div style="background:#FFF8E1;border-radius:10px;padding:10px 14px;font-size:0.75rem;">
<b>⚙️ 패키지 설치 안내</b><br>
Streamlit Cloud 사용 시 <code>requirements.txt</code>에 아래 추가:<br>
<code>gspread</code><br><code>google-auth</code>
</div>
""", unsafe_allow_html=True)
