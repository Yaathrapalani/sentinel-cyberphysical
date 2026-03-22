"""utils/style.py — CSS injection + session state bootstrap."""
from __future__ import annotations
import streamlit as st
from collections import deque
from engine.core import CorrelationEngine, AttackInjector

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
    background: #f8fafc;
    color: #0f172a;
}
.block-container { padding: 1.1rem 1.8rem 2rem; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 2px; }

.sec-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.63rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    border-left: 2px solid #2563eb;
    padding-left: 0.6rem;
    margin: 0 0 0.65rem;
    line-height: 1;
}

.sentinel-header {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.35rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(37,99,235,0.05);
}
.sentinel-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg,
        transparent 0%, #2563eb 30%,
        #60a5fa 50%, #2563eb 70%, transparent 100%);
}
.sentinel-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.75rem;
    font-weight: 700;
    color: #1e40af;
    margin: 0;
    letter-spacing: 0.08em;
}
.sentinel-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #64748b;
    margin: 0.25rem 0 0;
    letter-spacing: 0.05em;
}
.sentinel-badge {
    position: absolute;
    right: 1.6rem; top: 50%;
    transform: translateY(-50%);
    text-align: right;
    font-family: 'JetBrains Mono', monospace;
}

.s-div {
    height: 1px;
    background: linear-gradient(90deg,
        transparent, #e2e8f0 25%, #e2e8f0 75%, transparent);
    margin: 1.1rem 0;
}

[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e2e8f0;
}
[data-testid="stSidebar"] .block-container {
    padding: 1.2rem 1rem;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label {
    color: #334155 !important;
}

.stButton > button {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.05em !important;
    border-radius: 7px !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
    background: #f8fafc !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
}
.stButton > button:hover {
    background: #f1f5f9 !important;
    border-color: #2563eb !important;
    color: #1e40af !important;
}

.js-plotly-plot .plotly .bg { fill: transparent !important; }
</style>
"""

def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def init_state() -> None:
    if "ready" in st.session_state:
        return
    st.session_state.engine   = CorrelationEngine()
    st.session_state.injector = AttackInjector()
    st.session_state.cyber_h  = deque(maxlen=160)
    st.session_state.phys_h   = deque(maxlen=160)
    st.session_state.corr_h   = deque(maxlen=160)
    st.session_state.alert_h  = deque(maxlen=160)
    st.session_state.tick_h   = deque(maxlen=160)
    st.session_state.ids_log  = deque(maxlen=160)
    st.session_state.history  = []
    st.session_state.log      = []
    st.session_state.tick     = 0
    st.session_state.running  = True
    st.session_state.noise    = 0.04
    st.session_state.refresh  = 1.5
    st.session_state.ready    = True


def safe_rerun() -> None:
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()
