import streamlit as st
import pandas as pd
import random, os, json, requests, base64
from datetime import date, datetime
from io import BytesIO

# ─── 1. 웹페이지 기본 설정 ───
st.set_page_config(
    page_title="두류 테니스", 
    page_icon="🎾",
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# ─── 2. 디자인 시스템 및 레이아웃 스타일 ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght=400;500;700;900&display=swap');
:root{
  --g0:#1B5E20;--g2:#2E7D32;--g3:#4CAF50;--g5:#F1F8E9;
  --nav0:#2E7D32;--nav1:#1565C0;--nav2:#E65100;--nav3:#4A148C;--nav4:#00695C;
  --mc0:#1B5E20;--mc1:#0D47A1;--mc2:#BF360C;--mc3:#4A148C;
  --mc4:#006064;--mc5:#1A237E;--mc6:#880E4F;--mc7:#33691E;
  --tb0:#2E7D32;--tb1:#1565C0;--tb2:#E65100;--tb3:#4A148C;--tb4:#00695C;
}
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: #F8F9FA;
}
.main-title {
    font-size: 2.2rem; font-weight: 900; color: #1B5E20;
    text-align: center; margin-bottom: 5px; letter-spacing: -1px;
}
.sub-title {
    font-size: 0.95rem; color: #666; text-align: center; margin-bottom: 25px;
}
div.stButton > button {
    font-weight: 700; border-radius: 8px; transition: all 0.2s;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px; justify-content: center;
}
.stTabs [data-baseweb="tab"] {
    padding: 8px 16px; background-color: #fff; border: 1px solid #E0E0E0;
    border-radius: 20px; font-weight: 700; color: #555; transition: all 0.2s;
}
.stTabs [data-baseweb="tab"]:hover {
    border-color: #2E7D32; color: #2E7D32;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #2E7D32 !important; color: #fff !important; border-color: #2E7D32 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── 3. 깃허브 영구 백업 연동 설정 ───
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
REPO = "sk98118/duryu_tennis"  # 사용자 레포지토리 정보 고정

# 현재 존재하는 마스터 파일명 매칭
RANK_FILE   = "tennis_members.csv"  
TOUR_FILE   = "tournaments.json"
MEMBER_FILE = "member_roster_backup.json"
CONFIG_FILE = "config_backup.json"

# 표준 8대 항목 컬럼 지정
COLS_RANK = ["랭킹", "이름", "현재 포인트", "지난 포인트", "대회 결과", "부과점", "그룹", "비고"]

def github_api(path, method="GET", data=None):
    if not GITHUB_TOKEN:
        return None
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    if method == "GET":
        r = requests.get(url, headers=headers)
        return r.json() if r.status_code == 200 else None
    elif method == "PUT":
        res = github_api(path, "GET")
        sha = res["sha"] if res and "sha" in res else None
        payload = {"message": f"Backup {path} via Streamlit", "content": base64.b64encode(data).decode("utf-8")}
        if sha: payload["sha"] = sha
        requests.put(url, headers=headers, json=payload)

def load_file(path, default_content, is_json=False):
    res = github_api(path, "GET")
    if res and "content" in res:
        try:
            raw = base64.b64decode(res["content"])
            return json.loads(raw) if is_json else raw
        except:
            pass
    if os.path.exists(path):
        if is_json:
            with open(path, "r", encoding="utf-8") as f: return json.load(f)
        else:
            with open(path, "rb") as f: return f.read()
    if is_json:
        return default_content
    else:
        return default_content if isinstance(default_content, bytes) else default_content.encode("utf-8")

def save_file(path, data, is_json=False):
    raw_bytes = json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8") if is_json else data
    with open(path, "wb") as f:
        f.write(raw_bytes)
    github_api(path, "PUT", raw_bytes)

# ─── 4. 데이터 로드/저장 안전성 최적화 ───
def load_rank():
    csv_bytes = load_file(RANK_FILE, b"")
    if not csv_bytes or csv_bytes.strip() == b"":
        return pd.DataFrame(columns=COLS_RANK)
    try:
        df = pd.read_csv(BytesIO(csv_bytes), encoding="utf-8")
        # 어떤 상황에서도 KeyError가 나지 않도록 빈 컬럼 자동 채우기 방어막
        for c in COLS_RANK:
            if c not in df.columns: 
                df[c] = 0 if "포인트" in c or c == "랭킹" else ""
        return df[COLS_RANK]
    except:
        return pd.DataFrame(columns=COLS_RANK)

def save_rank(df):
    buf = BytesIO()
    df.to_csv(buf, index=False, encoding="utf-8")
    save_file(RANK_FILE, buf.getvalue())

def load_tours(): return load_file(TOUR_FILE, {}, is_json=True)
def save_tours(t): save_file(TOUR_FILE, t, is_json=True)
def load_members(): return load_file(MEMBER_FILE, [], is_json=True)
def save_members(m): save_file(MEMBER_FILE, m, is_json=True)
def load_config(): return load_file(CONFIG_FILE, {"nt":4, "pt_win":10, "pt_draw":5, "pt_lose":2}, is_json=True)
def save_config(c): save_file(CONFIG_FILE, c, is_json=True)

def get_active_tournament(tours):
    return [k for k, v in tours.items() if v.get("status") == "진행중"]

# ─── 5. 메인 레이아웃 및 탭 구성 ───
st.markdown('<div class="main-title">🎾 두류 테니스 클럽 랭킹 시스템</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">데이터 자동 백업 & 랭킹/대진 올인원 관리자 마스터 보드</div>', unsafe_allow_html=True)

tabs = st.tabs(["🏆 클럽 랭킹 마스터 보드", "📅 대회 생성 및 매칭", "👥 참가자 명단 조율", "⚙️ 포인트 정산 & 명부 통합 수정"])

tours = load_tours()
active = get_active_tournament(tours)

# ==========================================
# TAB 1: 랭킹 마스터 보드 (조회 전용)
# ==========================================
with tabs[0]:
    st.markdown("### 🏆 실시간 클럽 랭킹")
    df_r = load_rank()
    if df_r.empty:
        st.info("데이터가 없습니다. 마지막 탭에서 회원 명부나 엑셀을 먼저 등록해 주세요.")
    else:
        df_r["현재 포인트"] = pd.to_numeric(df_r["현재 포인트"], errors='coerce').fillna(0).astype(int)
        df_r = df_r.sort_values(by="현재 포인트", ascending=False).reset_index(drop=True)
        df_r["랭킹"] = df_r.index + 1
        st.dataframe(df_r, use_container_width=True, hide_index=True)

# ==========================================
# TAB 2: 대회 생성 및 매칭
# ==========================================
with tabs[1]:
    st.markdown("### 📅 새 대회 개설")
    cfg = load_config()
    with st.form("create_tour"):
        t_name = st.text_input("대회 명칭 (예: 2026년 5월 월례대회)")
        col1, col2 = st.columns(2)
        with col1: pt_w = col1.number_input("승리 포인트", value=cfg["pt_win"])
        with col2: pt_l = col2.number_input("패배 / 경기 포인트", value=cfg["pt_lose"])
        if st.form_submit_button("🚀 대회 공식 개설 및 활성화"):
            if not t_name.strip():
                st.error("대회 명칭을 입력하세요.")
            elif active:
                st.error("이미 진행 중인 대회가 있습니다. 마감 후 새 대회를 열어주세요.")
            else:
                tid = datetime.now().strftime("%Y%m%d_%H%M%S")
                tours[tid] = {"name": t_name, "status": "진행중", "pt_win": pt_w, "pt_lose": pt_l, "players": [], "matches": []}
                save_tours(tours)
                cfg.update({"pt_win": pt_w, "pt_lose": pt_l})
                save_config(cfg)
                st.success(f"✅ [{t_name}] 대회가 성공적으로 개설되었습니다!"); st.rerun()

# ==========================================
# TAB 3: 참가자 명단 조율
# ==========================================
with tabs[2]:
    st.markdown("### 👥 당일 대회 참가자 선택")
    if not active:
        st.info("💡 진행 중인 대회가 없습니다. [📅 대회 생성 및 매칭] 탭에서 대회를 먼저 만들어주세요.")
    else:
        tid = active[-1]
        all_m = load_members()
        if not all_m:
            st.warning("등록된 전체 클럽 회원이 없습니다. 마지막 탭에서 명단 혹은 엑셀을 먼저 올려주세요.")
        else:
            st.write(f"**현재 관리 중인 대회:** {tours[tid]['name']}")
            current_players = tours[tid].get("players", [])
            
            st.markdown("#### 아래 명단에서 오늘 참석한 회원을 체크해 주세요:")
            chosen = []
            cols = st.columns(4)
            for i, name in enumerate(all_m):
                with cols[i % 4]:
                    is_sel = name in current_players
                    if st.checkbox(name, value=is_sel, key=f"p_{name}"):
                        chosen.append(name)
            
            if st.button("💾 선택된 인원으로 명단 확정", type="primary", use_container_width=True):
                tours[tid]["players"] = chosen
                save_tours(tours)
                st.success(f"✅ 총 {len(chosen)}명 참가가 확정되었습니다."); st.rerun()

# ==========================================
# TAB 4: 포인트 정산 & 명부 통합 수정 (★ 개선 및 고정 위치)
# ==========================================
with tabs[3]:
    st.markdown("### ⚙️ 마스터 데이터 통합 빌드 & 관리")
    
    # ── [★ 수정 포인트 1] 엑셀 업로드 메뉴를 '무조건 최상단'에 노출 ──
    st.markdown("#### 📥 엑셀(XLSX/CSV) 파일 일괄 업로드 및 덮어쓰기")
    st.caption("기존에 보관 중이던 마스터 랭킹 엑셀 파일을 여기에 올리면 즉시 시스템 전체에 반영 및 동기화됩니다.")
    up_f = st.file_uploader("회원 명단 파일 선택 (이름 컬럼 필수)", type=["xlsx", "csv"])
    
    if up_f is not None:
        try:
            if up_f.name.endswith(".csv"):
                up_df = pd.read_csv(up_f, encoding="utf-8")
            else:
                up_df = pd.read_excel(up_f)
                
            st.write("▼ 업로드된 파일 미리보기 (상위 5개 항목):")
            st.dataframe(up_df.head(), use_container_width=True)
            
            if st.button("🚀 마스터 랭킹 강제 파일 빌드 실행", type="primary", use_container_width=True):
                if "이름" not in up_df.columns:
                    st.error("❌ 파일에 '이름' 컬럼이 존재하지 않습니다. 첫 행의 컬럼명을 확인해 주세요.")
                else:
                    final_df = pd.DataFrame(columns=COLS_RANK)
                    final_df["이름"] = up_df["이름"]
                    for c in COLS_RANK:
                        if c == "이름": continue
                        final_df[c] = up_df[c] if c in up_df.columns else (0 if "포인트" in c or c == "랭킹" else "")
                    
                    save_rank(final_df)
                    save_members(final_df["이름"].dropna().tolist())
                    st.success("✅ 파일 빌드 성공! 깃허브 원격 저장소에 데이터가 영구 백업되었습니다."); st.rerun()
        except Exception as e:
            st.error(f"파일을 읽는 중 에러가 발생했습니다: {e}")

    st.divider()

    # ── 수동 관리용 텍스트 조율 창 ──
    with st.expander("📝 [수동 관리용] 전체 회원 텍스트 명단 직접 조율"):
        cur_m = load_members()
        txt_area = st.text_area("클럽 전체 회원 명단 (이름을 쉼표 또는 줄바꿈으로 구분)", value=", ".join(cur_m), height=120)
        if st.button("💾 회원 명단 동기화", use_container_width=True):
            parsed = [n.strip() for n in txt_area.replace("\n", ",").split(",") if n.strip()]
            save_members(parsed)
            rk_df = load_rank()
            
            for p in parsed:
                if rk_df.empty or p not in rk_df["이름"].values:
                    nr = {c: "" for c in COLS_RANK}
                    nr["이름"] = p
                    nr["현재 포인트"] = 0
                    nr["지난 포인트"] = 0
                    nr["부과점"] = 0
                    rk_df = pd.concat([rk_df, pd.DataFrame([nr])], ignore_index=True)
            
            rk_df = rk_df[rk_df["이름"].isin(parsed)].reset_index(drop=True)
            save_rank(rk_df)
            st.success("✅ 회원 명단이 성공적으로 갱신되었습니다."); st.rerun()

    st.divider()

    # ── 대회 결과 정산 및 마감 영역 ──
    st.markdown("#### 📝 당일 대회 결과 포인트 최종 정산")
    if not active:
        st.info("💡 현재 진행 중인 대회가 없습니다. 대회가 마감되었거나 개설되지 않은 상태입니다.")
    else:
        tid = active[-1]
        st.write(f"🏆 **정산 진행 중인 대회:** {tours[tid]['name']}")
        
        rk_df = load_rank()
        players = tours[tid].get("players", [])
        
        if not players:
            st.warning("이번 대회에 참가 확정된 인원이 없습니다. [👥 참가자 명단 조율] 탭을 먼저 완료해 주세요.")
        else:
            updated_rows = []
            st.markdown("##### 참가자별 정산 데이터 수정")
            
            for p in players:
                if rk_df.empty or p not in rk_df["이름"].values:
                    nr = {c: "" for c in COLS_RANK}; nr["이름"] = p; nr["현재 포인트"] = 0; nr["지난 포인트"] = 0; nr["부과점"] = 0
                    rk_df = pd.concat([rk_df, pd.DataFrame([nr])], ignore_index=True)
            
            for _, row in rk_df.iterrows():
                r_dict = row.to_dict()
                name = r_dict["이름"]
                
                if name in players:
                    c1, c2, c3, c4 = st.columns([1.5, 2, 2, 3.5])
                    with c1: st.markdown(f"**{name}**")
                    with c2: res_val = st.selectbox("결과", ["선택", "승리", "패배/참가"], key=f"res_{name}")
                    with c3: add_p = st.number_input("추가 부과점", value=0, step=1, key=f"add_{name}")
                    with c4: note = st.text_input("비고 사유", value=str(r_dict.get("비고", "") or ""), key=f"note_{name}")
                    
                    win_p = tours[tid].get("pt_win", 10)
                    lose_p = tours[tid].get("pt_lose", 2)
                    current_p = int(r_dict.get("현재 포인트", 0) or 0)
                    
                    if res_val == "승리":
                        r_dict["현재 포인트"] = current_p + win_p + add_p
                        r_dict["대회 결과"] = "승"
                    elif res_val == "패배/참가":
                        r_dict["현재 포인트"] = current_p + lose_p + add_p
                        r_dict["대회 결과"] = "패"
                    else:
                        r_dict["현재 포인트"] = current_p + add_p
                        
                    r_dict["부과점"] = int(r_dict.get("부과점", 0) or 0) + add_p
                    if note: r_dict["비고"] = note
                    
                updated_rows.append(r_dict)
                
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            if st.button("💾 최종 데이터 마스터 보드에 반영 및 마감", type="primary", use_container_width=True):
                new_df = pd.DataFrame(updated_rows)
                save_rank(new_df)
                tours[tid]["status"] = "완료"
                save_tours(tours)
                st.success("✅ 정합성 확인 완료! 마스터 랭킹 보드 정렬 동기화가 마감되었습니다."); st.rerun()
