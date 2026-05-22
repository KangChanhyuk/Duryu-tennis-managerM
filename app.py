import streamlit as st
import pandas as pd
import random, os, json
from datetime import date
from io import BytesIO

# --- [상단 설정 및 CSS 코드는 기존 파일의 내용을 그대로 복사해 붙여넣으세요] ---
# (st.set_page_config 및 st.markdown("...", unsafe_allow_html=True) 부분)

# --- [기존 상수 및 함수들] ---
# (RANK_FILE, MEMBER_FILE, ... load_config, save_rank 등 기존 파일의 모든 함수를 그대로 유지)

# [새로 추가된 팀전 매칭 로직]
def make_team(team_a_list, team_b_list):
    ms = []
    max_len = max(len(team_a_list), len(team_b_list))
    for i in range(max_len):
        p1 = team_a_list[i % len(team_a_list)]
        p2 = team_b_list[i % len(team_b_list)]
        # '&'를 기준으로 복식(리스트)과 단식(단일) 구분
        t1 = [n.strip() for n in p1.split("&")]
        t2 = [n.strip() for n in p2.split("&")]
        ms.append({"t1": t1, "t2": t2, "s1": 0, "s2": 0})
    return ms, {}

# ... (기존 KDK, 고정페어, 싱글 매칭 함수 등은 그대로 유지) ...

# --- [관리자 탭 2번(참가자 조율) 통합 구현] ---
with adm[2]:
    ts=load_tours(); act_tids=[k for k,v in ts.items() if v.get("status")=="진행중"]
    if not act_tids: st.info("현재 진행 중인 대회가 존재하지 않습니다."); st.stop()
    sel_tid=act_tids[-1]; tour=ts[sel_tid]
    st.markdown(f"### 👥 {tour['title']} 참가자 조율")
    
    # [1단계, 2단계 기존 로직 유지]
    
    st.markdown("#### [2단계] 그룹별 세부 배정")
    for gname, gdata in list(tour["groups"].items()):
        st.markdown(f"##### 🏷️ **{gname}** 설정")
        m_opts=["KDK","고정페어","단식", "팀전"]
        gdata["mode"] = st.selectbox(f"방식 ({gname})", m_opts, index=m_opts.index(gdata.get("mode","KDK")), key=f"md_edit_{gname}")
        
        if gdata["mode"] == "팀전":
            ta = st.text_area(f"{gname} - 팀A (단식:이름 / 복식:이름&이름)", value="\n".join(gdata.get("team_a", [])), height=80, key=f"tA_{gname}")
            tb = st.text_area(f"{gname} - 팀B (단식:이름 / 복식:이름&이름)", value="\n".join(gdata.get("team_b", [])), height=80, key=f"tB_{gname}")
            gdata["team_a"] = [n.strip() for n in ta.split("\n") if n.strip()]
            gdata["team_b"] = [n.strip() for n in tb.split("\n") if n.strip()]
        else:
            cur_grp_players = gdata.get("players", [])
            grp_text = st.text_area(f"✍️ {gname} 명단 (쉼표 구분)", value=", ".join(cur_grp_players), height=80, key=f"grp_txt_{gname}")
            gdata["players"] = [n.strip() for n in grp_text.replace("\n",",").split(",") if n.strip()]

    if st.button("💾 모든 그룹 셋팅값 & 소속 선수 백업", type="primary", use_container_width=True):
        save_tours(ts); st.success("⚙️ 설정이 저장되었습니다."); st.rerun()

    st.markdown("#### [3단계] 대진표 최종 빌드")
    if st.button("🔥 설정 맞춰 대진표 자동 매칭 실행", use_container_width=True, type="primary"):
        for gn, gd in tour["groups"].items():
            if gd["mode"] == "팀전":
                ms, p2n = make_team(gd.get("team_a", []), gd.get("team_b", []))
                gd["matches"] = ms; gd["player_with_number"] = p2n
            elif gd["mode"] == "KDK":
                ms, p2n = make_kdk(gd.get("players", []), gd.get("games", 4))
                gd["matches"] = ms; gd["player_with_number"] = p2n
            elif gd["mode"] == "고정페어":
                ms, p2n = make_fixed(gd.get("players", []))
                gd["matches"] = ms; gd["player_with_number"] = p2n
            else:
                ms, p2n = make_singles(gd.get("players", []))
                gd["matches"] = ms; gd["player_with_number"] = p2n
        save_tours(ts); st.success("🎉 대진표가 빌드되었습니다.")

# ... (나머지 하단 코드 유지) ...
