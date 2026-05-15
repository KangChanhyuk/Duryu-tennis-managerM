import streamlit as st
import pandas as pd
import numpy as np
import random
import json
import os
import math
import time
from datetime import datetime, date
from io import BytesIO

# ============================================================
# 앱 설정
# ============================================================

st.set_page_config(
    page_title="두류 테니스 Ultimate",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# 세션
# ============================================================

if 'menu' not in st.session_state:
    st.session_state.menu = 'ranking'

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

if 'live_timer' not in st.session_state:
    st.session_state.live_timer = 0

if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False

if 'score_flash' not in st.session_state:
    st.session_state.score_flash = False

# ============================================================
# CSS 끝판왕
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

:root {
    --green-dark:#0B3D0B;
    --green-main:#1B5E20;
    --green-light:#43A047;
    --gold:#FFD700;
    --silver:#ECEFF1;
    --bronze:#D2691E;
    --bg:#F1F8F1;
    --card:#FFFFFF;
}

html, body, [class*="css"] {
    font-family:'Noto Sans KR', sans-serif !important;
}

.stApp {
    background:linear-gradient(180deg,#F1F8F1,#E8F5E9) !important;
}
    if df
