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
# CSS (모바일 최적화 + 다양한 색상 + 정사각 점수 버튼)
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

:root {
  /* 그린 계열 */
  --g0:#1B5E20; --g1:#2E7D32; --g2:#388E3C; --g3:#66BB6A; --g4:#C8E6C9; --g5:#E8F5E9;
  /* 메뉴 색상 (5개 메뉴) */
  --nav0:#2E7D32;  /* 랭킹 - 딥그린 */
  --nav1:#1565C0;  /* 대진 - 딥블루 */
  --nav2:#E65100;  /* 결과 - 오렌지 */
  --nav3:#6A1B9A;  /* 생성 - 퍼플 */
  --nav4:#37474F;  /* 관리 - 챠콜 */
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: #F8F9FA;
}

/* 상단 카드 장식 */
.top-bar {
    height: 6px;
    background: linear-gradient(90deg, #2E7D32, #1565C0, #E65100, #6A1B9A);
    margin-bottom: 25px;
    border-radius: 3px;
}

/* 커스텀 메뉴 버튼 스타일 */
.menu-box {
    display: flex;
    justify-content: space-between;
    gap: 4px;
    margin-bottom: 25px;
    background: #FFF;
    padding: 6px;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.menu-btn {
    flex: 1;
    text-align: center;
    padding: 12px 2px;
    font-size: 13px;
    font-weight: 700;
    color: #555;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    background: transparent;
}

/* 타이틀 디자인 */
.section-title {
    font-size: 24px;
    font-weight: 900;
    color: #1A237E;
    text-align: center;
    margin: 20px 0;
    letter-spacing: -0.5px;
}

/* 경기 카드 */
.match-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    border: 1px solid #EFEFEF;
}
.match-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    border-bottom: 1px dashed #E0E0E0;
    padding-bottom: 8px;
}
.match-badge {
    background: #E8F5E9;
    color: #2E7D32;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
}
.match-status {
    font-size: 11px;
    font-weight: 700;
    color: #757575;
}
.match-body {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.team-area {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 8px;
}
.team-left { justify-content: flex-start; text-align: left; }
.team-right { justify-content: flex-end; text-align: right; }

.player-name {
    font-size: 15px;
    font-weight: 700;
    color: #212121;
}

/* 정사각 스텝퍼 점수판 스타일 (가장 중요) */
.score-stepper-container {
    display: flex;
    align-items: center;
    gap: 15px;
    background: #F1F3F5;
    padding: 4px 8px;
    border-radius: 12px;
}
.score-box-wrapper {
    display: flex;
    align-items: center;
    gap: 2px;
}

/* Streamlit 기본요소 숨기기 및 패딩 초기화 */
div[data-testid="stBlock"] { padding: 0 !important; }
div.block-container { padding-top: 2rem !important; padding-bottom: 3rem !important; }

/* 테이블 헤더 커스텀 */
th { background-color: #F1F3F5 !important; font-weight: 700 !important; color: #495057 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 전역 변수 및 데이터 경로 설정
# ══════════════════════════════════════════════════════════════
DB_DIR     = "db"
DIR_TOURS  = os.path.join(DB_DIR, "tours")
PATH_RANK  = os.path.join(DB_DIR, "rank.csv")
PATH_MEMB  = os.path.join(DB_DIR, "members.csv")
PATH_TS    = os.path.join(DB_DIR, "tours_state.json")

for d in [DB_DIR, DIR_TOURS]:
    if not os.path.exists(d): os.makedirs(d)

COLS_RANK = ["순위", "이름", "현재포인트", "3월포인트", "4월포인트"]
COLS_MEMB = ["성명", "전화번호", "급수", "성별", "상태"]

# ══════════════════════════════════════════════════════════════
# 데이터 헬퍼 함수
# ═══════════════════════════════════════════════════════════
def load_rank():
    if os.path.exists(PATH_RANK):
        df = pd.read_csv(PATH_RANK)
        for c in ["현재포인트","3월포인트","4월포인트"]:
            if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
        return df
    return pd.DataFrame(columns=COLS_RANK)

def save_rank(df):
    df.to_csv(PATH_RANK, index=False, encoding="utf-8-sig")

def load_memb():
    if os.path.exists(PATH_MEMB): return pd.read_csv(PATH_MEMB)
    return pd.DataFrame(columns=COLS_MEMB)

def save_memb(df):
    df.to_csv(PATH_MEMB, index=False, encoding="utf-8-sig")

def load_tours():
    if os.path.exists(PATH_TS):
        with open(PATH_TS, "r", encoding="utf-8") as f: return json.load(f)
    return {}

def save_tours(d):
    with open(PATH_TS, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=2)

def get_tour_path(tid):
    return os.path.join(DIR_TOURS, f"{tid}.csv")

# ══════════════════════════════════════════════════════════════
# 세션 상태 초기화
# ══════════════════════════════════════════════════════════════
if "menu" not in st.session_state: st.session_state.menu = 0

# ══════════════════════════════════════════════════════════════
# 상단 내비게이션 바 (5개 메뉴 버튼)
# ══════════════════════════════════════════════════════════════
menus = ["🏆 전체랭킹", "⚔️ 대진/진행", "📊 경기결과", "🆕 대회생성", "🛠️ 정보관리"]
bg_colors = ["var(--nav0)", "var(--nav1)", "var(--nav2)", "var(--nav3)", "var(--nav4)"]

cols_menu = st.columns(5)
for idx, m_name in enumerate(menus):
    with cols_menu[idx]:
        is_sel = (st.session_state.menu == idx)
        btn_style = f"""
            background-color: {bg_colors[idx] if is_sel else '#FFFFFF'};
            color: {'#FFFFFF' if is_sel else '#495057'};
            border: 1px solid {bg_colors[idx] if is_sel else '#CED4DA'};
            box-shadow: {'0 4px 10px rgba(0,0,0,0.15)' if is_sel else 'none'};
            width: 100%; padding: 10px 0px; font-size: 12px; font-weight: bold; border-radius: 12px; cursor: pointer;
        """
        if st.button(m_name, key=f"nav_{idx}", use_container_width=True):
            st.session_state.menu = idx
            st.rerun()

st.markdown("---")

# ══════════════════════════════════════════════════════════════
# [MENU 0] 전체 랭킹 현황
# ══════════════════════════════════════════════════════════════
if st.session_state.menu == 0:
    st.markdown('<div class="section-title">🏆 두류 테니스 클럽 전체 랭킹</div>', unsafe_allow_html=True)
    dr = load_rank()
    if dr.empty:
        st.info("💡 등록된 랭킹 데이터가 없습니다. 정보관리 메뉴에서 회원 정보를 먼저 등록해 주세요.")
    else:
        dr = dr.sort_values(by="현재포인트", ascending=False).reset_index(drop=True)
        dr["순위"] = range(1, len(dr) + 1)
        
        # 포인트 상승/하락 폭 계산 서브 로직
        if "4월포인트" in dr.columns and "현재포인트" in dr.columns:
            dr["변동"] = dr["현재포인트"] - dr["4월포인트"]
            dr["변동"] = dr["변동"].apply(lambda x: f"🔺{x}" if x > 0 else (f"🔻{abs(x)}" if x < 0 else "💨 0"))
        
        c_conf = {
            "순위": st.column_config.NumberColumn("순위", width="small"),
            "이름": st.column_config.TextColumn("선수명", width="medium"),
            "현재포인트": st.column_config.NumberColumn("현재 포인트", width="medium"),
            "변동": st.column_config.TextColumn("최근 변동", width="small")
        }
        st.dataframe(dr[["순위", "이름", "현재포인트", "변동"]], use_container_width=True, column_config=c_conf, hide_index=True)

# ══════════════════════════════════════════════════════════════
# [MENU 1] 대진 및 경기 진행 (★ 이 부분의 증감 컨트롤러 버그를 직접 수정 및 통합함 ★)
# ══════════════════════════════════════════════════════════════
elif st.session_state.menu == 1:
    st.markdown('<div class="section-title">⚔️ 실시간 대진 및 경기 현황</div>', unsafe_allow_html=True)
    ts = load_tours()
    active_tours = {k: v for k, v in ts.items() if v.get("status", "진행중") == "진행중"}
    
    if not active_tours:
        st.info("💡 현재 진행 중인 대회가 없습니다. 새 대회 생성 메뉴에서 대회를 먼저 개설해 주세요.")
    else:
        stid = st.selectbox("🎯 경기 진행할 대회 선택", list(active_tours.keys()), format_func=lambda x: active_tours[x]["name"])
        tpath = get_tour_path(stid)
        
        if os.path.exists(tpath):
            mdf = pd.read_csv(tpath)
            # 데이터 정합성 보장 코드
            mdf["A점수"] = mdf["A점수"].fillna(0).astype(int)
            mdf["B점수"] = mdf["B점수"].fillna(0).astype(int)
            
            grps = sorted(mdf["그룹"].unique())
            sel_g = st.radio("Group Filter", grps, horizontal=True, label_visibility="collapsed")
            
            gdf = mdf[mdf["그룹"] == sel_g]
            
            # ──────────────────────────────────────────────────
            # ★ 완벽 통합된 직접 작동하는 스텝퍼 및 실시간 점수 입력란 ★
            # ──────────────────────────────────────────────────
            for idx, row in gdf.iterrows():
                st.markdown(f"""
                <div class="match-card">
                    <div class="match-header">
                        <span class="match-badge">순번 {row['순서']} ({row['방식']})</span>
                        <span class="match-status">진행중</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 껍데기를 지우고 가로 배열 레이아웃 내부에 완벽 작동하는 st.number_input 단일 배치
                cc = st.columns([4, 2, 1, 2, 4])
                
                with cc[0]:
                    st.markdown(f"<div style='padding-top:10px; font-weight:bold; font-size:16px; text-align:right;'>{row['팀A']}</div>", unsafe_allow_html=True)
                
                with cc[1]:
                    # 실시간 +, - 버튼 연동 기능이 내장된 입력 컨트롤러 단독 배치 (직접 타이핑 가능)
                    val_a = st.number_input("A 점수 입력", min_value=0, max_value=99, value=int(row["A점수"]), step=1, key=f"ea_{idx}", label_visibility="collapsed")
                
                with cc[2]:
                    st.markdown("<div style='text-align:center; font-weight:900; font-size:18px; padding-top:8px; color:#A0A0A0;'>VS</div>", unsafe_allow_html=True)
                
                with cc[3]:
                    # 실시간 +, - 버튼 연동 기능이 내장된 입력 컨트롤러 단독 배치 (직접 타이핑 가능)
                    val_b = st.number_input("B 점수 입력", min_value=0, max_value=99, value=int(row["B점수"]), step=1, key=f"eb_{idx}", label_visibility="collapsed")
                    
                with cc[4]:
                    st.markdown(f"<div style='padding-top:10px; font-weight:bold; font-size:16px; text-align:left;'>{row['팀B']}</div>", unsafe_allow_html=True)
                
                # 수정한 값을 즉시 메인 데이터프레임 구조에 매핑 처리함
                mdf.at[idx, "A점수"] = val_a
                mdf.at[idx, "B점수"] = val_b
                
                st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)
            
            st.markdown("---")
            if st.button("💾 경기 결과 안전하게 저장", type="primary", use_container_width=True):
                mdf.to_csv(tpath, index=False, encoding="utf-8-sig")
                st.success("✅ 경기 현황 및 스코어가 완벽하게 저장되었습니다!")
                st.rerun()

# ══════════════════════════════════════════════════════════════
# [MENU 2] 경기 결과 및 승패/득실 기반 최종 순위표
# ══════════════════════════════════════════════════════════════
elif st.session_state.menu == 2:
    st.markdown('<div class="section-title">📊 경기 결과 및 그룹별 최종 순위</div>', unsafe_allow_html=True)
    ts = load_tours()
    if not ts:
        st.info("💡 조회 가능한 대회 이력이 존재하지 않습니다.")
    else:
        stid2 = st.selectbox("📅 대회 이력 선택", list(ts.keys()), format_func=lambda x: ts[x]["name"])
        tpath2 = get_tour_path(stid2)
        
        if os.path.exists(tpath2):
            mdf2 = pd.read_csv(tpath2)
            grps2 = sorted(mdf2["그룹"].unique())
            
            tab_objs = st.tabs([f"🔹 {g} 그룹 결과" for g in grps2])
            
            for g_idx, g_name in enumerate(grps2):
                with tab_objs[g_idx]:
                    gdf2 = mdf2[mdf2["그룹"] == g_name]
                    
                    # 승률, 승점, 총 득실차 정밀 연산 서브 모듈
                    stats = {}
                    for _, r in gdf2.iterrows():
                        pA, pB = r["팀A"], r["팀B"]
                        sA, sB = int(r.get("A점수", 0)), int(r.get("B점수", 0))
                        
                        # 다인 복식 페어일 경우 분해해서 각 개별 인원단위 묶음 연산
                        items_a = pA.split("/") if "/" in pA else [pA]
                        items_b = pB.split("/") if "/" in pB else [pB]
                        
                        all_p = items_a + items_b
                        for p in all_p:
                            if p not in stats: stats[p] = {"승":0, "패":0, "득점":0, "실점":0}
                        
                        for p in items_a:
                            stats[p]["득점"] += sA; stats[p]["실점"] += sB
                            if sA > sB: stats[p]["승"] += 1
                            elif sA < sB: stats[p]["패"] += 1
                        for p in items_b:
                            stats[p]["득점"] += sB; stats[p]["실점"] += sA
                            if sB > sA: stats[p]["승"] += 1
                            elif sB < sA: stats[p]["패"] += 1
                    
                    # 딕셔너리 기반 데이터를 순위 가독 전용 데이터프레임으로 변환
                    rows_stats = []
                    for name, s in stats.items():
                        diff = s["득점"] - s["실점"]
                        rows_stats.append({
                            "선수명": name, "승": s["승"], "패": s["패"],
                            "총득점": s["득점"], "총실점": s["실점"], "득실차": diff
                        })
                    
                    if rows_stats:
                        sf = pd.DataFrame(rows_stats)
                        # 승수 -> 득실차 -> 총득점 내림차순 정렬 원칙 기준적용
                        sf = sf.sort_values(by=["승", "득실차", "총득점"], ascending=False).reset_index(drop=True)
                        sf.insert(0, "순위", range(1, len(sf)+1))
                        st.markdown(f"##### 📈 {g_name} 그룹 실시간 종합 순위표")
                        st.dataframe(sf, use_container_width=True, hide_index=True)
                    
                    st.markdown("---")
                    st.markdown(f"##### 📑 {g_name} 그룹 세부 매치 기록")
                    st.dataframe(gdf2[["순서", "방식", "팀A", "A점수", "B점수", "팀B"]], use_container_width=True, hide_index=True)
        
        st.write("")
        st.markdown("---")
        st.markdown("##### 🎖️ 대회 종료 및 전체 랭킹 점수 부여")
        
        earn = {}
        # 각 순위 테이블의 포인트를 계산하는 연산 로직 루프
        mdf_all = pd.read_csv(tpath2)
        for g_name in sorted(mdf_all["그룹"].unique()):
            gdf2 = mdf_all[mdf_all["그룹"] == g_name]
            stats = {}
            for _, r in gdf2.iterrows():
                pA, pB = r["팀A"], r["팀B"]
                sA, sB = int(r.get("A점수", 0)), int(r.get("B점수", 0))
                items_a = pA.split("/") if "/" in pA else [pA]
                items_b = pB.split("/") if "/" in pB else [pB]
                for p in items_a+items_b:
                    if p not in stats: stats[p] = {"승":0, "득실차":0}
                for p in items_a:
                    stats[p]["득실차"] += (sA - sB)
                    if sA > sB: stats[p]["승"] += 1
                for p in items_b:
                    stats[p]["득실차"] += (sB - sA)
                    if sB > sA: stats[p]["승"] += 1
            
            res_list = [{"name": k, "승": v["승"], "득실차": v["득실차"]} for k, v in stats.items()]
            res_list.sort(key=lambda x: (x["승"], x["득실차"]), reverse=True)
            
            for rank_idx, item in enumerate(res_list):
                pname = item["name"]
                pt = 1  # 기본 참가 점수
                if rank_idx == 0: pt = 7     # 우승
                elif rank_idx == 1: pt = 5   # 준우승
                elif rank_idx == 2: pt = 3   # 3위
                
                # 복식조인 경우 문자열 슬라이싱 파싱 처리 후 개별 반영
                if "/" in pname:
                    for p in pname.split("/"):
                        earn[p] = earn.get(p, 0) + pt
                else:
                    earn[pname] = earn.get(pname, 0) + pt

        if earn:
            ef  = pd.DataFrame(earn.items(), columns=["선수","획득포인트"])
            ec  = {c: st.column_config.TextColumn(c, width="small") for c in ef.columns}
            st.dataframe(ef, use_container_width=True, column_config=ec, hide_index=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🏆 계산된 점수를 랭킹에 공식 반영", type="primary", use_container_width=True, key="a3ap"):
                dr = load_rank()
                if dr.empty: dr = pd.DataFrame(columns=COLS_RANK)
                for p, pt in earn.items():
                    if p in dr["이름"].values:
                        cur = dr.loc[dr["이름"]==p, "현재포인트"].values[0]
                        dr.loc[dr["이름"]==p, "현재포인트"] = cur + pt
                    else:
                        nr = {c:"" for c in COLS_RANK}; nr["이름"]=p; nr["현재포인트"]=pt
                        dr = pd.concat([dr, pd.DataFrame([nr])], ignore_index=True)
                save_rank(dr)
                ts[stid2]["status"] = "완료"
                save_tours(ts)
                st.success("✅ 최종 랭킹 포인트 반영 완료!"); st.rerun()

# ══════════════════════════════════════════════════════════════
# [MENU 3] 새 대회 자동 생성 및 그룹 분할 운영 관리
# ══════════════════════════════════════════════════════════════
elif st.session_state.menu == 3:
    st.markdown('<div class="section-title">🆕 실력 기반 그룹 자동분할 대회 생성</div>', unsafe_allow_html=True)
    
    tname = st.text_input("📝 대회 명칭 입력", f"{date.today().strftime('%m월')} 월례대회")
    
    dr = load_rank()
    dm = load_memb()
    
    if dm.empty:
        st.warning("💡 등록된 회원 정보가 존재하지 않습니다. 5번째 '정보관리' 탭에서 명단을 먼저 구비하세요.")
    else:
        active_members = dm[dm["상태"]=="정회원"]["성명"].tolist() if "상태" in dm.columns else dm["성명"].tolist()
        
        # 전체 랭킹 테이블 기준 동기화 정렬 작업
        rank_order = {r["이름"]: r["현재포인트"] for _, r in dr.iterrows()}
        active_members.sort(key=lambda x: rank_order.get(x, 0), reverse=True)
        
        selected_players = st.multiselect(
            f"👥 오늘 참석한 선수 선택 (총 {len(active_members)}명 중 선택)",
            active_members, default=active_members[:min(12, len(active_members))]
        )
        
        st.markdown("---")
        g_cnt = st.number_input("🔢 생성할 그룹 개수 (A조, B조...)", min_value=1, max_value=5, value=2)
        
        # 랭킹 데이터 스코어 기준 역순 재정렬 후 그룹 자동 분할 분배 처리 기법
        final_players = [p for p in active_members if p in selected_players]
        
        if final_players:
            chunks = np.array_split(final_players, g_cnt)
            g_set = {}
            
            st.markdown("##### 📍 실력 랭킹순 자동 분할 조편성 결과")
            for i, chunk in enumerate(chunks):
                g_letter = chr(65 + i) # A, B, C, D...
                g_set[g_letter] = list(chunk)
                st.info(f"**{g_letter} 그룹** ({len(chunk)}명): {', '.join(chunk)}")
            
            st.markdown("---")
            st.markdown("##### ⚙️ 그룹별 대진 방식 및 세부 옵션 커스텀")
            
            g_modes = {}
            for g_letter in g_set.keys():
                g_modes[g_letter] = st.selectbox(
                    f"⚙️ {g_letter} 그룹 매칭 메커니즘 선택",
                    ["복식(KDK 방식)", "복식(고정페어 방식)", "단식(1:1 풀리그)"],
                    key=f"mode_{g_letter}"
                )
            
            if st.button("🚀 대진표 자동 구성 및 대회 시작", type="primary", use_container_width=True):
                match_list = []
                
                for g_letter, p_list in g_set.items():
                    mode = g_modes[g_letter]
                    
                    # 1) 단식 리그 매칭 생성 로직
                    if mode == "단식(1:1) 풀리그":
                        seq = 1
                        for i in range(len(p_list)):
                            for j in range(i+1, len(p_list)):
                                match_list.append({
                                    "그룹": g_letter, "순서": f"{g_letter}-{seq}", "방식": "단식",
                                    "팀A": p_list[i], "팀B": p_list[j], "A점수": 0, "B점수": 0
                                })
                                seq += 1
                                
                    # 2) 고정 페어 밸런싱 조합 생성 로직 (1위 + 최하위 밸런스 매칭)
                    elif mode == "복식(고정페어 방식)":
                        half = len(p_list) // 2
                        pairs = []
                        for k in range(half):
                            pairs.append(f"{p_list[k]}/{p_list[-(k+1)]}")
                        
                        seq = 1
                        for i in range(len(pairs)):
                            for j in range(i+1, len(pairs)):
                                match_list.append({
                                    "그룹": g_letter, "순서": f"{g_letter}-{seq}", "방식": "고정복식",
                                    "팀A": pairs[i], "팀B": pairs[j], "A점수": 0, "B점수": 0
                                })
                                seq += 1
                                
                    # 3) KDK 정통 대진 난수 표 기반 조합 생성 로직
                    else:
                        n = len(p_list)
                        raw_matches = []
                        for i in range(n):
                            for j in range(i+1, n):
                                for k in range(j+1, n):
                                    for l in range(k+1, n):
                                        raw_matches.append((i,j,k,l))
                        
                        # 인원 가용 대진 리스트 중복 방지 분배 샘플링 처리
                        sampled = random.sample(raw_matches, min(len(raw_matches), max(6, n)))
                        seq = 1
                        for idx_tuple in sampled:
                            idx_l = list(idx_tuple)
                            random.shuffle(idx_l)
                            tA = f"{p_list[idx_l[0]]}/{p_list[idx_l[1]]}"
                            tB = f"{p_list[idx_l[2]]}/{p_list[idx_l[3]]}"
                            match_list.append({
                                "그룹": g_letter, "순서": f"{g_letter}-{seq}", "방식": "KDK복식",
                                "팀A": tA, "팀B": tB, "A점수": 0, "B점수": 0
                            })
                            seq += 1
                
                if match_list:
                    tid = f"tour_{int(random.random()*100000)}"
                    new_df = pd.DataFrame(match_list)
                    new_df.to_csv(get_tour_path(tid), index=False, encoding="utf-8-sig")
                    
                    ts = load_tours()
                    ts[tid] = {"name": tname, "date": str(date.today()), "status": "진행중"}
                    save_tours(ts)
                    
                    st.success(f"🎉 '{tname}' 대회가 성공적으로 개설되었습니다! 대진/진행 탭으로 이동하세요.")
                    st.session_state.menu = 1
                    st.rerun()

# ══════════════════════════════════════════════════════════════
# [MENU 4] 정보 관리 및 회원 엑셀 명단 업로드 컨트롤 타워
# ══════════════════════════════════════════════════════════════
elif st.session_state.menu == 4:
    st.markdown('<div class="section-title">🛠️ 클럽 회원 명단 및 데이터 마스터 관리</div>', unsafe_allow_html=True)
    
    # 엑셀 패키지 누락으로 인한 크래시 안전 장치 블록화 기법
    try:
        import openpyxl
    except ImportError:
        st.error("🚨 시스템 백엔드에 'openpyxl' 라이브러리가 유실되었습니다. 터미널 환경에 pip install openpyxl 명령어를 반드시 수행하여 활성화해야 정상 구동됩니다.")
        
    st.markdown("##### 📂 통합 관리 엑셀(XLSX / CSV) 파일 명단 동기화 업로드")
    up_file = st.file_uploader("작성하신 엑셀 파일을 여기에 끌어다 놓으세요", type=["xlsx", "csv"])
    
    if up_file:
        try:
            if up_file.name.endswith(".csv"):
                raw_df = pd.read_csv(up_file)
            else:
                raw_df = pd.read_excel(up_file)
            
            st.markdown("👀 업로드된 데이터 파일 데이터 선행 검증")
            st.dataframe(raw_df.head(5), use_container_width=True)
            
            if st.button("💾 업로드 명단 데이터를 마스터 DB 파일에 최종 병합", type="primary"):
                # 랭킹 테이블 데이터 동기화 파싱 추출
                r_rows = []
                m_rows = []
                for idx, r in raw_df.iterrows():
                    name = str(r.get("성명", "")).strip() if "성명" in raw_df.columns else str(r.get("이름", "")).strip()
                    if not name or name == "nan": continue
                    
                    pt_cur = r.get("4월(최종)랭킹포인트", r.get("현재포인트", 0))
                    pt_m3  = r.get("3월(최종)랭킹포인트", r.get("3월포인트", 0))
                    pt_m4  = r.get("4월(최종)랭킹포인트", r.get("4월포인트", 0))
                    
                    r_rows.append({"순위": idx+1, "이름": name, "현재포인트": pt_cur, "3월포인트": pt_m3, "4월포인트": pt_m4})
                    m_rows.append({"성명": name, "전화번호": r.get("전화번호", ""), "급수": r.get("급수", ""), "성별": r.get("성별", ""), "상태": "정회원"})
                
                if r_rows:
                    save_rank(pd.DataFrame(r_rows))
                    save_memb(pd.DataFrame(m_rows))
                    st.success("✅ 회원 전체 명단 및 기존 포인트 이력이 에러 없이 성공적으로 반영되었습니다!")
        except Exception as e:
            st.error(f"❌ 파일 처리 분석 도중 구조적 에러가 발생했습니다: {e}")
            
    st.markdown("---")
    st.markdown("##### 💾 시스템 초기 리셋 리셋 세션 관리자 초기화")
    if st.button("⚠️ 시스템 내 모든 가동중인 대회 데이터 강제 포맷 및 리셋", type="secondary"):
        if os.path.exists(PATH_TS): os.remove(PATH_TS)
        st.success("데이터베이스 이력 연동 테이블이 완전히 리셋되었습니다.")
        st.rerun()
