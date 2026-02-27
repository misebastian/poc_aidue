import streamlit as st
import pandas as pd

st.set_page_config(page_title="Company Intelligence Dashboard", page_icon="🏢", layout="wide", initial_sidebar_state="collapsed")

# ══════════════════════════════════════════════════════════════════
# DARK MODERN AESTHETIC — Dataveil-inspired with original brand colors
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-primary: #07070a;
        --bg-secondary: #0d0d11;
        --bg-card: #121217;
        --bg-card-hover: #18181f;
        --teal: #1B5E5C;
        --teal-glow: rgba(27, 94, 92, 0.15);
        --teal-dim: rgba(27, 94, 92, 0.08);
        --rust: #A95228;
        --rust-glow: rgba(169, 82, 40, 0.15);
        --blue: #006492;
        --blue-glow: rgba(0, 100, 146, 0.15);
        --lime: #A5CD24;
        --lime-glow: rgba(165, 205, 36, 0.15);
        --lime-dim: rgba(165, 205, 36, 0.08);
        --tan: #C39D7B;
        --red: #C12D27;
        --text-primary: #f0f0f2;
        --text-secondary: #85858f;
        --text-tertiary: #4a4a54;
        --border: rgba(255,255,255,0.06);
        --border-teal: rgba(27, 94, 92, 0.25);
    }

    /* ── GLOBAL RESET ── */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background: var(--bg-primary) !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    .block-container { max-width: 1200px; padding-top: 0 !important; }

    /* Fix all streamlit text colors */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp li, .stApp label,
    .stMarkdown, .stMarkdown p, .stMarkdown span {
        color: var(--text-primary) !important;
    }

    /* Fix streamlit dataframe */
    .stDataFrame { border-radius: 12px; overflow: hidden; }

    /* Fix slider */
    div[data-baseweb="slider"] div { color: var(--text-primary) !important; }
    .stSlider label { color: var(--text-secondary) !important; }
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: var(--teal) !important;
        border-color: var(--teal) !important;
    }

    /* Fix text input */
    .stTextInput > div > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        transition: border-color 0.3s ease;
    }
    .stTextInput > div > div:focus-within {
        border-color: var(--teal) !important;
        box-shadow: 0 0 0 1px var(--teal), 0 0 20px var(--teal-dim) !important;
    }
    .stTextInput input {
        color: var(--text-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stTextInput input::placeholder { color: var(--text-tertiary) !important; }
    .stTextInput label { display: none !important; }

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 6px;
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 10px !important;
        padding: 12px 28px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        color: var(--text-secondary) !important;
        transition: all 0.3s cubic-bezier(0.22,1,0.36,1) !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-primary) !important;
        background: var(--bg-card) !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--teal) !important;
        color: #FFF !important;
        box-shadow: 0 4px 16px var(--teal-glow) !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none !important; }
    .stTabs [data-baseweb="tab-border"] { display: none !important; }

    /* ── NOISE TEXTURE OVERLAY ── */
    .stApp::before {
        content: '';
        position: fixed; inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.025'/%3E%3C/svg%3E");
        pointer-events: none; z-index: 0;
    }

    /* ── HERO HEADER ── */
    .hero-header {
        position: relative;
        padding: 56px 48px 48px;
        margin: -1rem -1rem 40px -1rem;
        overflow: hidden;
        background: var(--bg-primary);
    }
    .hero-header::before {
        content: '';
        position: absolute; top: -60%; right: -15%;
        width: 700px; height: 700px;
        background: radial-gradient(circle, var(--teal-glow) 0%, transparent 60%);
        pointer-events: none;
        animation: drift 12s ease-in-out infinite;
    }
    .hero-header::after {
        content: '';
        position: absolute; bottom: -50%; left: -10%;
        width: 500px; height: 500px;
        background: radial-gradient(circle, var(--blue-glow) 0%, transparent 60%);
        pointer-events: none;
        animation: drift 16s ease-in-out infinite reverse;
    }
    @keyframes drift {
        0%, 100% { opacity: 0.5; transform: translate(0,0) scale(1); }
        33% { opacity: 0.8; transform: translate(20px,-15px) scale(1.05); }
        66% { opacity: 0.4; transform: translate(-15px,10px) scale(0.98); }
    }
    .hero-brand {
        display: inline-flex; align-items: center; gap: 10px;
        margin-bottom: 24px; position: relative; z-index: 1;
    }
    .hero-brand-logo {
        width: 28px; height: 28px; border-radius: 7px;
        background: var(--teal);
        display: flex; align-items: center; justify-content: center;
    }
    .hero-brand-logo::after {
        content: ''; width: 9px; height: 9px;
        border: 2px solid var(--bg-primary); border-radius: 50%;
    }
    .hero-brand-name {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px; font-weight: 500;
        letter-spacing: 4px; text-transform: uppercase;
        color: var(--text-secondary);
    }
    .hero-title {
        font-family: 'Instrument Serif', serif;
        font-size: clamp(36px, 5vw, 56px);
        font-weight: 400; line-height: 1.05;
        letter-spacing: -2px;
        color: var(--text-primary) !important;
        margin: 0 0 8px 0;
        position: relative; z-index: 1;
    }
    .hero-title em {
        font-style: italic; color: var(--teal) !important;
        position: relative;
    }
    .hero-title em::after {
        content: '';
        position: absolute; bottom: 2px; left: 0;
        width: 100%; height: 2px;
        background: linear-gradient(90deg, var(--teal), transparent);
        opacity: 0.3;
    }
    .hero-sub {
        font-family: 'DM Sans', sans-serif;
        font-size: 15px; color: var(--text-secondary) !important;
        font-weight: 300; position: relative; z-index: 1;
        margin: 0;
    }
    .hero-divider {
        height: 1px; margin: 0 -1rem;
        background: linear-gradient(90deg, transparent 5%, var(--border) 50%, transparent 95%);
    }

    /* ── SEARCH CONTAINER ── */
    .search-wrapper {
        position: relative;
        max-width: 560px;
        margin: 0 auto 48px;
    }
    .search-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px; letter-spacing: 3px;
        text-transform: uppercase;
        color: var(--teal) !important;
        display: flex; align-items: center; gap: 12px;
        margin-bottom: 16px;
    }
    .search-label::before {
        content: ''; width: 32px; height: 1px;
        background: linear-gradient(90deg, var(--teal), transparent);
    }

    /* ── SECTION LABEL ── */
    .section-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px; letter-spacing: 3px;
        text-transform: uppercase;
        color: var(--teal);
        display: flex; align-items: center; gap: 12px;
        margin-bottom: 16px;
    }
    .section-label::before {
        content: ''; width: 32px; height: 1px;
        background: linear-gradient(90deg, var(--teal), transparent);
    }
    .section-title {
        font-family: 'Instrument Serif', serif;
        font-size: clamp(28px, 3.5vw, 40px);
        font-weight: 400; line-height: 1.1;
        letter-spacing: -1px;
        color: var(--text-primary) !important;
        margin-bottom: 32px;
    }
    .section-title em {
        font-style: italic; color: var(--teal) !important;
    }

    /* ── META CARDS (top row) ── */
    .meta-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1px;
        background: var(--border);
        border: 1px solid var(--border);
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 32px;
    }
    .meta-cell {
        background: var(--bg-card);
        padding: 28px 24px;
        transition: background 0.4s cubic-bezier(0.22,1,0.36,1);
    }
    .meta-cell:hover { background: var(--bg-card-hover); }
    .meta-cell-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 9px; letter-spacing: 2.5px;
        text-transform: uppercase;
        color: var(--text-tertiary) !important;
        margin-bottom: 10px;
    }
    .meta-cell-value {
        font-family: 'DM Sans', sans-serif;
        font-size: 15px; font-weight: 600;
        color: var(--text-primary) !important;
        line-height: 1.4;
    }

    /* ── CARD ── */
    .dark-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 32px 28px;
        margin-bottom: 20px;
        transition: all 0.4s cubic-bezier(0.22,1,0.36,1);
        position: relative;
        overflow: hidden;
    }
    .dark-card:hover {
        border-color: var(--border-teal);
        background: var(--bg-card-hover);
    }
    .dark-card::after {
        content: '';
        position: absolute; top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-teal), transparent);
        opacity: 0; transition: opacity 0.4s;
    }
    .dark-card:hover::after { opacity: 1; }
    .dark-card h3 {
        font-family: 'Instrument Serif', serif;
        font-size: 22px; font-weight: 400;
        color: var(--text-primary) !important;
        margin-bottom: 14px;
    }
    .dark-card p {
        color: var(--text-secondary) !important;
        font-size: 14px; font-weight: 300; line-height: 1.8;
    }

    /* ── INFO ITEMS ── */
    .info-row {
        padding: 18px 22px;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        margin-bottom: 10px;
        transition: all 0.3s ease;
    }
    .info-row:hover {
        border-color: var(--border-teal);
        background: var(--bg-card-hover);
        transform: translateX(4px);
    }
    .info-row-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 9px; letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--text-tertiary) !important;
        margin-bottom: 6px;
    }
    .info-row-value {
        font-size: 14px; font-weight: 400;
        color: var(--text-primary) !important;
        line-height: 1.6;
    }

    /* ── BADGES ── */
    .badge-grid { display: flex; flex-wrap: wrap; gap: 8px; }
    .badge-dark {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 6px 16px;
        border: 1px solid var(--border-teal);
        border-radius: 100px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px; font-weight: 500;
        letter-spacing: 1px;
        color: var(--teal) !important;
        background: var(--teal-dim);
        transition: all 0.3s ease;
    }
    .badge-dark:hover {
        background: var(--teal-glow);
        box-shadow: 0 0 16px var(--teal-dim);
    }

    /* ── METRIC CARDS ── */
    .metric-dark {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 32px 24px;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.22,1,0.36,1);
    }
    .metric-dark:hover {
        border-color: var(--border-teal);
        transform: translateY(-4px);
        box-shadow: 0 24px 64px rgba(0,0,0,0.4);
    }
    .metric-dark::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--teal), transparent);
    }
    .metric-dark .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: clamp(28px, 3.5vw, 40px);
        font-weight: 500; line-height: 1;
        color: var(--text-primary) !important;
        margin: 12px 0;
    }
    .metric-dark .metric-label {
        font-size: 10px; letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--text-tertiary) !important;
        font-family: 'JetBrains Mono', monospace;
    }

    .metric-teal::before { background: linear-gradient(90deg, transparent, var(--teal), transparent); }
    .metric-teal .metric-value { color: var(--teal) !important; }

    .metric-rust::before { background: linear-gradient(90deg, transparent, var(--rust), transparent); }
    .metric-rust .metric-value { color: var(--rust) !important; }

    .metric-lime::before { background: linear-gradient(90deg, transparent, var(--lime), transparent); }
    .metric-lime .metric-value { color: var(--lime) !important; }

    .metric-blue::before { background: linear-gradient(90deg, transparent, var(--blue), transparent); }
    .metric-blue .metric-value { color: var(--blue) !important; }

    /* ── PROGRESS BARS ── */
    .progress-item { margin-bottom: 18px; }
    .progress-header {
        display: flex; justify-content: space-between;
        align-items: baseline; margin-bottom: 8px;
    }
    .progress-header .dim-name {
        font-size: 13px; font-weight: 400;
        color: var(--text-primary) !important;
    }
    .progress-header .dim-level {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px; font-weight: 500;
        color: var(--teal) !important;
    }
    .progress-track {
        background: rgba(255,255,255,0.04);
        border-radius: 6px; height: 8px;
        overflow: hidden; position: relative;
    }
    .progress-fill-bar {
        height: 100%; border-radius: 6px;
        background: linear-gradient(90deg, var(--teal), var(--blue));
        position: relative;
        transition: width 0.6s cubic-bezier(0.22,1,0.36,1);
    }
    .progress-fill-bar::after {
        content: '';
        position: absolute; right: 0; top: 0; bottom: 0;
        width: 20px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2));
        border-radius: 0 6px 6px 0;
    }

    /* ── SWOT ── */
    .swot-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 28px 24px;
        margin-bottom: 16px;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.22,1,0.36,1);
    }
    .swot-card:hover {
        background: var(--bg-card-hover);
        transform: translateX(3px);
    }
    .swot-card::before {
        content: '';
        position: absolute; top: 0; left: 0;
        width: 3px; height: 100%;
    }
    .swot-strengths::before { background: var(--lime); }
    .swot-weaknesses::before { background: var(--tan); }
    .swot-opportunities::before { background: var(--blue); }
    .swot-threats::before { background: var(--red); }

    .swot-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px; letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-bottom: 16px;
    }
    .swot-strengths .swot-title { color: var(--lime) !important; }
    .swot-weaknesses .swot-title { color: var(--tan) !important; }
    .swot-opportunities .swot-title { color: var(--blue) !important; }
    .swot-threats .swot-title { color: var(--red) !important; }

    .swot-card ul {
        list-style: none; padding: 0; margin: 0;
    }
    .swot-card li {
        font-size: 13px; color: var(--text-secondary) !important;
        font-weight: 300; line-height: 1.7;
        padding: 8px 0;
        border-bottom: 1px solid var(--border);
        display: flex; align-items: flex-start; gap: 10px;
    }
    .swot-card li:last-child { border-bottom: none; }
    .swot-card li::before {
        content: '→'; flex-shrink: 0; margin-top: 1px; opacity: 0.5;
    }
    .swot-strengths li::before { color: var(--lime); }
    .swot-weaknesses li::before { color: var(--tan); }
    .swot-opportunities li::before { color: var(--blue); }
    .swot-threats li::before { color: var(--red); }

    /* ── RISK / ALERT BOXES ── */
    .alert-box {
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid var(--border);
        background: var(--bg-card);
        font-size: 13px; font-weight: 300;
        color: var(--text-secondary) !important;
        line-height: 1.7;
        transition: all 0.3s ease;
    }
    .alert-box:hover { background: var(--bg-card-hover); }
    .alert-warning {
        border-left: 3px solid var(--rust);
    }
    .alert-success {
        border-left: 3px solid var(--lime);
    }
    .alert-info {
        border-left: 3px solid var(--blue);
    }
    .alert-box strong {
        color: var(--text-primary) !important;
        font-weight: 600;
    }

    /* ── TOOLTIP (hover sources) ── */
    .with-source {
        position: relative; cursor: pointer;
        border-bottom: 1px dotted var(--text-tertiary);
        display: inline;
        transition: border-color 0.3s;
    }
    .with-source:hover { border-bottom-color: var(--teal); }
    .source-tooltip {
        display: none;
        position: absolute;
        background: #1a1a22;
        border: 1px solid var(--border-teal);
        color: var(--text-primary) !important;
        padding: 18px 22px;
        border-radius: 12px;
        font-size: 12px; z-index: 9999;
        max-width: 420px; min-width: 280px;
        box-shadow: 0 16px 48px rgba(0,0,0,0.6);
        left: 0; top: calc(100% + 8px);
        line-height: 1.6;
        backdrop-filter: blur(12px);
    }
    .source-tooltip::before {
        content: "";
        position: absolute; top: -12px; left: 0; right: 0;
        height: 16px; background: transparent;
    }
    .with-source:hover .source-tooltip,
    .source-tooltip:hover { display: block; }
    .source-tooltip strong { color: var(--text-primary) !important; }
    .source-tooltip a {
        color: var(--teal) !important;
        text-decoration: underline;
        font-weight: 600;
    }
    .source-quote {
        font-style: italic;
        color: var(--text-secondary) !important;
        margin: 8px 0; padding-left: 10px;
        border-left: 2px solid var(--teal);
        font-size: 11px;
    }

    /* ── CRITERIA BOX ── */
    .criteria-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1px;
        background: var(--border);
        border: 1px solid var(--border);
        border-radius: 14px;
        overflow: hidden;
        margin: 24px 0;
    }
    .criteria-cell {
        background: var(--bg-card);
        padding: 24px 20px;
        transition: background 0.3s;
    }
    .criteria-cell:hover { background: var(--bg-card-hover); }
    .criteria-cell-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 9px; letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--text-tertiary) !important;
        margin-bottom: 8px;
    }
    .criteria-cell-value {
        font-size: 16px; font-weight: 600;
        color: var(--text-primary) !important;
        margin-bottom: 6px;
    }
    .criteria-cell-status {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px; letter-spacing: 1px;
    }

    /* ── MAPPING FLOW ── */
    .mapping-flow {
        display: flex; align-items: center;
        gap: 0; flex-wrap: wrap;
        margin: 24px 0;
    }
    .mapping-node {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 18px 20px;
        flex: 1; min-width: 180px;
        transition: all 0.3s ease;
    }
    .mapping-node:hover {
        border-color: var(--border-teal);
        background: var(--bg-card-hover);
    }
    .mapping-node-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 8px; letter-spacing: 2.5px;
        text-transform: uppercase;
        color: var(--text-tertiary) !important;
        margin-bottom: 6px;
    }
    .mapping-node-value {
        font-size: 13px; font-weight: 500;
        color: var(--text-primary) !important;
        line-height: 1.4;
    }
    .mapping-node.highlight {
        border-color: var(--teal);
        background: var(--teal-dim);
    }
    .mapping-node.highlight .mapping-node-value {
        color: var(--teal) !important;
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px; font-weight: 600;
    }
    .mapping-arrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px; color: var(--text-tertiary);
        padding: 0 12px; flex-shrink: 0;
        opacity: 0.3;
    }

    /* ── DIVIDER ── */
    .section-divider {
        height: 1px; margin: 40px 0;
        background: linear-gradient(90deg, transparent 5%, var(--border) 50%, transparent 95%);
    }

    /* ── FOOTER ── */
    .dark-footer {
        padding: 32px 0;
        border-top: 1px solid var(--border);
        margin-top: 56px;
        display: flex; justify-content: space-between;
        align-items: center; flex-wrap: wrap; gap: 12px;
    }
    .dark-footer span {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px; color: var(--text-tertiary) !important;
        letter-spacing: 1.5px;
    }

    /* ── WELCOME CARD ── */
    .welcome-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 80px 48px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .welcome-card::before {
        content: '';
        position: absolute; top: 50%; left: 50%;
        transform: translate(-50%,-50%);
        width: 500px; height: 500px;
        background: radial-gradient(circle, var(--teal-dim) 0%, transparent 60%);
        pointer-events: none;
    }
    .welcome-card h2 {
        font-family: 'Instrument Serif', serif;
        font-size: clamp(28px, 4vw, 44px);
        font-weight: 400; letter-spacing: -1px;
        color: var(--text-primary) !important;
        position: relative; margin-bottom: 16px;
    }
    .welcome-card h2 em {
        font-style: italic; color: var(--teal) !important;
    }
    .welcome-card p {
        color: var(--text-secondary) !important;
        font-size: 15px; font-weight: 300;
        position: relative; line-height: 1.7;
    }
    .welcome-card .tip {
        margin-top: 32px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px; letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--text-tertiary) !important;
        position: relative;
    }
    .welcome-card .available {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 6px 16px; margin-top: 24px;
        border: 1px solid var(--border-teal);
        border-radius: 100px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px; font-weight: 500;
        color: var(--teal) !important;
        background: var(--teal-dim);
        position: relative;
    }
    .welcome-card .available::before {
        content: ''; width: 6px; height: 6px; border-radius: 50%;
        background: var(--teal);
        animation: blink 2.5s ease-in-out infinite;
        box-shadow: 0 0 8px var(--teal);
    }
    @keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: 0.2; } }

    /* ── NOT FOUND ── */
    .not-found {
        background: var(--bg-card);
        border: 1px solid rgba(169, 82, 40, 0.2);
        border-left: 3px solid var(--rust);
        border-radius: 12px;
        padding: 32px;
        text-align: center;
    }
    .not-found strong { color: var(--rust) !important; }
    .not-found p { color: var(--text-secondary) !important; margin-top: 8px; }

    /* ── SLIDER LABEL ── */
    .slider-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px; letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--text-secondary) !important;
        margin-bottom: 12px;
    }

    /* ── DATAFRAME STYLING ── */
    .stDataFrame [data-testid="stDataFrameResizable"] {
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }

    /* Responsive meta grid */
    @media (max-width: 768px) {
        .meta-grid { grid-template-columns: repeat(2, 1fr); }
        .criteria-grid { grid-template-columns: 1fr; }
        .mapping-flow { flex-direction: column; }
        .mapping-arrow { transform: rotate(90deg); }
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════
BXT_L2_SAVINGS = {
    "Engineering, architecture and construction management": 0.02371,
    "Heavy Construction & Engineering": 0.045,
    "General Contractors": 0.038,
    "Oil & Gas": 0.048,
    "Mining": 0.041,
    "Default": 0.04
}

COMPANY_DATA = {
    "kiewit": {
        "meta": {
            "company_name": {"value": "Kiewit Corporation", "quote": "Kiewit is one of North America's largest and most respected construction and engineering organizations.", "source_url": "https://www.kiewit.com/about-us/"},
            "jurisdiction": {"value": "United States, Canada and Mexico", "quote": "The employee-owned organization operates through a network of subsidiaries in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"},
            "listed_status": {"value": "Private (employee-owned)", "quote": "With its roots dating back to 1884, the employee-owned organization operates through a network of subsidiaries in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"}
        },
        "company_overview": {
            "description": {"value": "Kiewit Corporation is one of North America's largest construction and engineering organizations, delivering end-to-end engineering, procurement and construction (EPC) services for critical infrastructure and energy projects.", "quote": "Kiewit is one of North America's largest and most respected construction and engineering organizations.", "source_url": "https://www.kiewit.com/about-us/"},
            "founded_year": {"value": 1884, "quote": "With its roots dating back to 1884, the employee-owned organization operates through a network of subsidiaries in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"},
            "headquarters": {"value": "Omaha, Nebraska, United States", "quote": "The Kiewit Corporation is a Fortune 500 contractor business headquartered in Omaha.", "source_url": "http://www.omahaimc.org/kiewit-corporation/"},
            "primary_industry": {"value": "Engineering, Procurement and Construction (EPC) services", "quote": "The EPC model streamlines execution with a single contractor managing design, procurement and construction — ensuring cost certainty, schedule reliability and reduced owner risk.", "source_url": "https://www.kiewit.com/services-and-solutions/project-delivery/"},
            "primary_markets": [
                {"value": "Transportation", "quote": "Kiewit offers construction and engineering services in a variety of markets including transportation.", "source_url": "https://www.linkedin.com/company/kiewit"},
                {"value": "Oil, Gas & Chemical", "quote": "Kiewit offers construction and engineering services in oil, gas and chemical.", "source_url": "https://www.linkedin.com/company/kiewit"},
                {"value": "Power", "quote": "Kiewit offers construction and engineering services in power.", "source_url": "https://www.linkedin.com/company/kiewit"},
                {"value": "Building", "quote": "Kiewit offers construction and engineering services in building.", "source_url": "https://www.linkedin.com/company/kiewit"},
                {"value": "Marine", "quote": "Kiewit offers construction and engineering services in marine.", "source_url": "https://www.linkedin.com/company/kiewit"},
                {"value": "Water / Wastewater", "quote": "Kiewit offers construction and engineering services in water/wastewater.", "source_url": "https://www.linkedin.com/company/kiewit"},
                {"value": "Industrial", "quote": "Kiewit offers construction and engineering services in industrial.", "source_url": "https://www.linkedin.com/company/kiewit"},
                {"value": "Mining", "quote": "Kiewit offers construction and engineering services in mining.", "source_url": "https://www.linkedin.com/company/kiewit"}
            ],
        },
        "operational_footprint": {
            "regions_of_operation": [
                {"value": "United States", "quote": "The employee-owned organization operates through a network of subsidiaries in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"},
                {"value": "Canada", "quote": "The employee-owned organization operates through a network of subsidiaries in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"},
                {"value": "Mexico", "quote": "The employee-owned organization operates through a network of subsidiaries in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"}
            ],
            "business_segments": ["Transportation", "Oil, Gas & Chemical", "Power", "Building", "Marine", "Water/Wastewater", "Industrial", "Mining"],
            "geographic_scope": "NAM/LATAM"
        },
        "workforce": {
            "total_employees": {"value": 31800, "quote": "16.8 BILLION 31,800 EMPLOYEES 2024 REVENUE 2024 EMPLOYEES", "source_url": "https://www.kiewit.com/wp-content/uploads/2025/09/EN_2024-Sustainability-Report-reduced.pdf"},
        },
        "financials": {
            "revenue_2024": {"value": 16.8, "quote": "Proven Results. $16.8B 2024 Revenues 31,800 Craft and Staff Employees", "source_url": "https://www.kiewit.com"},
            "source_note": "Private company – estimates only; no official statutory filings."
        },
        "ownership_structure": {"ownership_type": {"value": "Privately held, employee-owned organization", "quote": "Kiewit's diversified services and unique network of decentralized offices — backed by a multi-billion-dollar, employee-owned organization — enable us to tackle construction and engineering projects of any size.", "source_url": "https://www.kiewit.com/about-us/"}},
        "procurement_organization": {
            "overall_maturity_level": {"value": "Defined to Managed", "quote": "At Kiewit, supply chain is integrated into project planning from the very beginning. We're part of the strategy, the estimate, the bid.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
            "maturity_dimensions": {
                "Governance & Org": {"value": "Managed", "score": 4, "quote": "Depending on the project, material procurement can account for up to 50% of total installed costs. That makes Carsten's team critical to the bottom line.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                "Process & Policy": {"value": "Defined", "score": 3, "quote": "At Kiewit, supply chain is integrated into project planning from the very beginning. We're part of the strategy, the estimate, the bid.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                "Technology & Data": {"value": "Defined", "score": 3, "quote": "Our procurement and supply chain experts leverage scale, strategy and technology to ensure materials, equipment and services keep projects on track.", "source_url": "https://www.kiewit.com/?lang=en-ca"},
                "Supplier Management": {"value": "Defined", "score": 3, "quote": "What distinguishes strong suppliers during these moments is transparency. The worst thing a vendor can do is hide a problem. If we know early, we can help.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                "Integration Lifecycle": {"value": "Managed", "score": 4, "quote": "At Kiewit, supply chain is integrated into project planning from the very beginning. We're part of the strategy, the estimate, the bid. We help define risk and create the roadmap for delivery.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
            },
            "structure": {"value": "Supply chain sits between engineering and construction, responsible for ensuring materials arrive on time and in full to support EPC project execution.", "quote": "We sit between engineering and construction. Our job is to make sure materials arrive when construction needs them — not a day late, not a piece short.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
            "category_mgmt": {"value": "Procurement is organized around categories with specialists owning domains such as valves or piping, building technical expertise and deep supplier relationships.", "quote": "He's also reorganized his team around procurement categories — giving specialists ownership over specific domains like valves or piping.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
            "cpo": {"value": "Carsten Bernstiel — VP of Procurement, Oil, Gas & Chemical group", "quote": "At the center of this complex machinery is Carsten Bernstiel, Vice President of Procurement for Kiewit's Oil, Gas & Chemical group, a veteran of the energy industry.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
        },
        "procurement_risks": {
            "key_risks": [
                {"value": "High share of total installed cost tied to materials, exposing projects to price and availability risks", "quote": "Depending on the project, material procurement can account for up to 50% of total installed costs. That makes Carsten's team critical to the bottom line.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                {"value": "Global shipping and logistics disruptions, such as canal delays, impacting lead times", "quote": "We rerouted shipments through Los Angeles and handled final delivery by train and truck. That's the kind of creative triage we do every day.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                {"value": "Dependence on timely, transparent communication from suppliers to identify and resolve issues early", "quote": "The worst thing a vendor can do is hide a problem. If we know early, we can help. That's the foundation of real partnership.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
            ],
            "mitigation": {"value": "Kiewit's OGC procurement team mitigates risk through early involvement in strategy and estimating, proactive planning of procurement cycles, rerouting logistics when corridors are constrained, and insisting on early, transparent supplier communication.", "quote": "We rerouted shipments through Los Angeles and handled final delivery by train and truck. That's the kind of creative triage we do every day.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
        },
        "procurement_swot": {
            "strengths": [
                {"value": "Integrated EPC model with a single contractor managing design, procurement and construction for cost and schedule control", "quote": "The EPC model streamlines execution with a single contractor managing design, procurement and construction — ensuring cost certainty, schedule reliability and reduced owner risk.", "source_url": "https://www.kiewit.com/services-and-solutions/project-delivery/"},
                {"value": "Supply chain function integrated from the start of project planning, helping define risk and delivery roadmap", "quote": "At Kiewit, supply chain is integrated into project planning from the very beginning.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                {"value": "Category-based procurement structure with domain specialists and emphasis on partnership and transparency with suppliers", "quote": "He's also reorganized his team around procurement categories — giving specialists ownership over specific domains like valves or piping.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
            ],
            "weaknesses": [
                {"value": "Limited public transparency on procurement systems, quantitative KPIs and ESG programs compared with listed EPC peers", "quote": "Kiewit is one of North America's largest and most respected construction and engineering organizations.", "source_url": "https://www.kiewit.com/about-us/"},
                {"value": "Public evidence on advanced procurement practices is concentrated in the Oil, Gas & Chemical group, so maturity may be uneven across markets", "quote": "At the center of this complex machinery is Carsten Bernstiel, Vice President of Procurement for Kiewit's Oil, Gas & Chemical group.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
            ],
            "opportunities": [
                {"value": "Deepening use of technology and AI in procurement to anticipate supply chain disruptions and optimize sourcing", "quote": "This consultative role has transformed EPCs into partners — not just vendors.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                {"value": "Making ESG, sustainability and supplier diversity practices more visible to align with client and regulatory expectations", "quote": "Kiewit has a long history of partnering with the local business community.", "source_url": "https://www.kiewit.com/business-with-us/opportunities/central-florida-projects/"},
                {"value": "Extending OGC-style category management and early supplier engagement practices across all markets", "quote": "He's also reorganized his team around procurement categories — giving specialists ownership over specific domains.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
            ],
            "threats": [
                {"value": "Material procurement representing up to half of total installed cost, increasing exposure to commodity and logistics shocks", "quote": "Depending on the project, material procurement can account for up to 50% of total installed costs.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                {"value": "Global shipping issues such as canal congestion adding weeks to lead times and stressing project schedules", "quote": "We rerouted shipments through Los Angeles and handled final delivery by train and truck.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                {"value": "Competitive EPC contractors investing aggressively in digital procurement and ESG branding", "quote": "The EPC model streamlines execution with a single contractor managing design, procurement and construction.", "source_url": "https://www.kiewit.com/services-and-solutions/project-delivery/"}
            ]
        },
        "industry_mapping": {
            "original_industry": "Engineering, Procurement and Construction (EPC) services",
            "bxt_l2": "Engineering, architecture and construction management",
            "median_projected_savings_rate": 0.02371
        }
    }
}

# ══════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════

def get_company_data(name):
    term = name.lower().strip()
    for key, data in COMPANY_DATA.items():
        if key in term or term in data["meta"]["company_name"]["value"].lower():
            return data
    return None

def src(value, quote, url):
    if not quote or not url:
        return f'<span style="color:var(--text-primary);">{value}</span>'
    return f'''<span class="with-source">{value}<span class="source-tooltip">
        <strong>Source</strong>
        <div class="source-quote">"{quote}"</div>
        <a href="{url}" target="_blank">View source ↗</a>
    </span></span>'''

def info_row(label, value, quote=None, url=None):
    val = src(value, quote, url) if quote else f'<span>{value}</span>'
    return f'<div class="info-row"><div class="info-row-label">{label}</div><div class="info-row-value">{val}</div></div>'

def swot_card(title, items, swot_type):
    html = "".join([f'<li>{src(i["value"], i["quote"], i["source_url"])}</li>' for i in items])
    return f'<div class="swot-card swot-{swot_type}"><div class="swot-title">{title}</div><ul>{html}</ul></div>'

def check_criteria(co):
    geo_scope = co.get("operational_footprint", {}).get("geographic_scope", "")
    revenue = co.get("financials", {}).get("revenue_2024", {}).get("value", 0) or 0
    is_nam_latam = geo_scope in ["NAM", "LATAM", "NAM/LATAM"]
    is_over_10b = revenue > 10
    return is_nam_latam, is_over_10b, geo_scope, revenue

# ══════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════
st.markdown('''<div class="hero-header">
    <div class="hero-brand">
        <div class="hero-brand-logo"></div>
        <span class="hero-brand-name">Intelligence</span>
    </div>
    <h1 class="hero-title">Company<br><em>Intelligence</em></h1>
    <p class="hero-sub">Due diligence & procurement analysis platform</p>
</div>
<div class="hero-divider"></div>''', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# SEARCH
# ══════════════════════════════════════════════════════════════════
st.markdown('<div style="height:32px;"></div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="search-label">Search Company</div>', unsafe_allow_html=True)
    search = st.text_input("Search", placeholder="Enter company name (e.g., Kiewit Corporation)", label_visibility="collapsed")

# ══════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════
if search:
    co = get_company_data(search)
    if co:
        tab1, tab2 = st.tabs(["GENERAL INFO", "FINANCIALS & COST OPTIMIZATION"])

        # ─── TAB 1: GENERAL INFO ───
        with tab1:
            st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="section-title">Company <em>Profile</em></h2>', unsafe_allow_html=True)

            # Meta grid
            m = co["meta"]
            ov = co["company_overview"]
            st.markdown(f'''<div class="meta-grid">
                <div class="meta-cell">
                    <div class="meta-cell-label">Company</div>
                    <div class="meta-cell-value">{src(m["company_name"]["value"], m["company_name"]["quote"], m["company_name"]["source_url"])}</div>
                </div>
                <div class="meta-cell">
                    <div class="meta-cell-label">Jurisdiction</div>
                    <div class="meta-cell-value">{src(m["jurisdiction"]["value"], m["jurisdiction"]["quote"], m["jurisdiction"]["source_url"])}</div>
                </div>
                <div class="meta-cell">
                    <div class="meta-cell-label">Status</div>
                    <div class="meta-cell-value">{src(m["listed_status"]["value"], m["listed_status"]["quote"], m["listed_status"]["source_url"])}</div>
                </div>
                <div class="meta-cell">
                    <div class="meta-cell-label">Founded</div>
                    <div class="meta-cell-value">{src(str(ov["founded_year"]["value"]), ov["founded_year"]["quote"], ov["founded_year"]["source_url"])}</div>
                </div>
            </div>''', unsafe_allow_html=True)

            # Description
            d = ov["description"]
            st.markdown(f'''<div class="dark-card">
                <h3>Description</h3>
                <p>{src(d["value"], d["quote"], d["source_url"])}</p>
            </div>''', unsafe_allow_html=True)

            # Corporate structure + Segments
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="section-label">Corporate Structure</div>', unsafe_allow_html=True)
                hq = ov["headquarters"]
                st.markdown(info_row("Headquarters", hq["value"], hq["quote"], hq["source_url"]), unsafe_allow_html=True)
                own = co["ownership_structure"]["ownership_type"]
                st.markdown(info_row("Ownership", own["value"], own["quote"], own["source_url"]), unsafe_allow_html=True)
                emp = co["workforce"]["total_employees"]
                st.markdown(info_row("Employees", f'{emp["value"]:,}', emp["quote"], emp["source_url"]), unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="section-label">Business Segments</div>', unsafe_allow_html=True)
                badges = "".join([f'<span class="badge-dark">{s}</span>' for s in co["operational_footprint"]["business_segments"]])
                st.markdown(f'<div class="dark-card"><div class="badge-grid">{badges}</div></div>', unsafe_allow_html=True)

                st.markdown('<div class="section-label">Regions</div>', unsafe_allow_html=True)
                for r in co["operational_footprint"]["regions_of_operation"]:
                    st.markdown(info_row("📍", r["value"], r["quote"], r["source_url"]), unsafe_allow_html=True)

            # Primary Markets
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Primary Markets</div>', unsafe_allow_html=True)
            mkts = "".join([f'<span class="badge-dark">{m["value"]}</span>' for m in ov["primary_markets"]])
            st.markdown(f'<div class="dark-card"><div class="badge-grid">{mkts}</div></div>', unsafe_allow_html=True)

            # Procurement
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Supply Chain & Procurement</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="section-title">Procurement <em>Organization</em></h2>', unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                proc = co["procurement_organization"]
                mat = proc["overall_maturity_level"]
                st.markdown(info_row("Maturity Level", mat["value"], mat["quote"], mat["source_url"]), unsafe_allow_html=True)
                struc = proc["structure"]
                st.markdown(info_row("Structure", struc["value"], struc["quote"], struc["source_url"]), unsafe_allow_html=True)
                cat = proc["category_mgmt"]
                st.markdown(info_row("Category Mgmt", cat["value"], cat["quote"], cat["source_url"]), unsafe_allow_html=True)
                cpo = proc["cpo"]
                st.markdown(info_row("CPO / Equivalent", cpo["value"], cpo["quote"], cpo["source_url"]), unsafe_allow_html=True)

            with c2:
                st.markdown('<div style="margin-bottom:8px;"><span class="section-label">Maturity Dimensions</span></div>', unsafe_allow_html=True)
                for dim, data in proc["maturity_dimensions"].items():
                    pct = (data["score"] / 5) * 100
                    st.markdown(f'''<div class="progress-item">
                        <div class="progress-header">
                            <span class="dim-name">{src(dim, data["quote"], data["source_url"])}</span>
                            <span class="dim-level">{data["value"]} ({data["score"]}/5)</span>
                        </div>
                        <div class="progress-track">
                            <div class="progress-fill-bar" style="width:{pct}%;"></div>
                        </div>
                    </div>''', unsafe_allow_html=True)

            # SWOT
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Analysis</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="section-title">Procurement <em>SWOT</em></h2>', unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown(swot_card("STRENGTHS", co["procurement_swot"]["strengths"], "strengths"), unsafe_allow_html=True)
                st.markdown(swot_card("OPPORTUNITIES", co["procurement_swot"]["opportunities"], "opportunities"), unsafe_allow_html=True)
            with c2:
                st.markdown(swot_card("WEAKNESSES", co["procurement_swot"]["weaknesses"], "weaknesses"), unsafe_allow_html=True)
                st.markdown(swot_card("THREATS", co["procurement_swot"]["threats"], "threats"), unsafe_allow_html=True)

            # Risks
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Risk Assessment</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="section-title">Procurement <em>Risks</em></h2>', unsafe_allow_html=True)

            for risk in co["procurement_risks"]["key_risks"]:
                risk_html = src(risk["value"], risk["quote"], risk["source_url"])
                st.markdown(f'<div class="alert-box alert-warning">{risk_html}</div>', unsafe_allow_html=True)

            mit = co["procurement_risks"]["mitigation"]
            mit_html = src(mit["value"], mit["quote"], mit["source_url"])
            st.markdown(f'<div class="alert-box alert-success"><strong>Risk Mitigation</strong><br><br>{mit_html}</div>', unsafe_allow_html=True)

        # ─── TAB 2: FINANCIALS ───
        with tab2:
            st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Financials</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="section-title">Financial <em>Overview</em></h2>', unsafe_allow_html=True)

            r24 = co['financials']['revenue_2024']
            emp = co['workforce']['total_employees']

            c1, c2, c3 = st.columns(3)
            with c1:
                rev_html = src(f"${r24['value']}B", r24["quote"], r24["source_url"])
                st.markdown(f'''<div class="metric-dark metric-teal">
                    <div class="metric-label">2024 Revenue</div>
                    <div class="metric-value">{rev_html}</div>
                    <div class="metric-label">USD</div>
                </div>''', unsafe_allow_html=True)
            with c2:
                st.markdown(f'''<div class="metric-dark metric-blue">
                    <div class="metric-label">Geographic Scope</div>
                    <div class="metric-value">{co["operational_footprint"]["geographic_scope"]}</div>
                    <div class="metric-label">Region</div>
                </div>''', unsafe_allow_html=True)
            with c3:
                emp_html = src(f"{emp['value']:,}", emp["quote"], emp["source_url"])
                st.markdown(f'''<div class="metric-dark metric-rust">
                    <div class="metric-label">Employees</div>
                    <div class="metric-value">{emp_html}</div>
                    <div class="metric-label">2024</div>
                </div>''', unsafe_allow_html=True)

            st.markdown(f'<div class="alert-box alert-warning"><strong>Note:</strong> {co["financials"]["source_note"]}</div>', unsafe_allow_html=True)

            # Cost Optimization
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Projections</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="section-title">Cost <em>Optimization</em></h2>', unsafe_allow_html=True)

            is_nam_latam, is_over_10b, geo_scope, revenue = check_criteria(co)
            meets_criteria = is_nam_latam and is_over_10b
            mp = co["industry_mapping"]
            bxt_l2 = mp["bxt_l2"]

            if meets_criteria:
                rate = BXT_L2_SAVINGS.get(bxt_l2, BXT_L2_SAVINGS["Default"])
            else:
                rate = BXT_L2_SAVINGS["Default"]

            # Criteria grid
            st.markdown(f'''<div class="criteria-grid">
                <div class="criteria-cell">
                    <div class="criteria-cell-label">Geographic Scope</div>
                    <div class="criteria-cell-value">{geo_scope}</div>
                    <div class="criteria-cell-status" style="color:{"var(--lime)" if is_nam_latam else "var(--red)"};">{"✓ NAM/LATAM" if is_nam_latam else "✗ Required: NAM/LATAM"}</div>
                </div>
                <div class="criteria-cell">
                    <div class="criteria-cell-label">Revenue</div>
                    <div class="criteria-cell-value">${revenue}B USD</div>
                    <div class="criteria-cell-status" style="color:{"var(--lime)" if is_over_10b else "var(--red)"};">{"✓ >$10B" if is_over_10b else "✗ Required: >$10B"}</div>
                </div>
                <div class="criteria-cell">
                    <div class="criteria-cell-label">Status</div>
                    <div class="criteria-cell-value" style="color:{"var(--lime)" if meets_criteria else "var(--red)"};">{"✓ MEETS CRITERIA" if meets_criteria else "✗ DOES NOT MEET"}</div>
                    <div class="criteria-cell-status" style="color:var(--text-tertiary);">{"Using BXT_L2 rate" if meets_criteria else "Using default rate"}</div>
                </div>
            </div>''', unsafe_allow_html=True)

            # Mapping flow
            st.markdown(f'''<div class="mapping-flow">
                <div class="mapping-node">
                    <div class="mapping-node-label">Original Industry</div>
                    <div class="mapping-node-value">{mp["original_industry"]}</div>
                </div>
                <span class="mapping-arrow">→</span>
                <div class="mapping-node">
                    <div class="mapping-node-label">BXT L2 Classification</div>
                    <div class="mapping-node-value">{bxt_l2}</div>
                </div>
                <span class="mapping-arrow">→</span>
                <div class="mapping-node highlight">
                    <div class="mapping-node-label">Median Savings Rate</div>
                    <div class="mapping-node-value">{rate*100:.4f}%</div>
                </div>
            </div>''', unsafe_allow_html=True)

            # Spend slider
            st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
            total_revenue = revenue * 1000

            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown('<div class="slider-label">Total Addressable Spend (% of Revenue)</div>', unsafe_allow_html=True)
                spend_pct = st.slider("Spend %", min_value=0, max_value=100, value=30, step=5, label_visibility="collapsed")
                addressable_spend = total_revenue * (spend_pct / 100)
                st.markdown(f'''<div class="alert-box alert-info">
                    <strong>Calculation</strong><br><br>
                    Revenue: <strong>${total_revenue:,.0f}M</strong> × {spend_pct}% = <strong>${addressable_spend:,.2f}M</strong> Addressable Spend
                </div>''', unsafe_allow_html=True)

            with c2:
                st.markdown(f'''<div class="info-row"><div class="info-row-label">BXT L2 Category</div><div class="info-row-value">{bxt_l2}</div></div>''', unsafe_allow_html=True)
                st.markdown(f'''<div class="info-row"><div class="info-row-label">Median Savings Rate</div><div class="info-row-value" style="color:var(--teal) !important;font-family:'JetBrains Mono',monospace;">{rate*100:.4f}%</div></div>''', unsafe_allow_html=True)
                st.markdown(f'''<div class="info-row"><div class="info-row-label">Total Addressable Spend</div><div class="info-row-value" style="color:var(--teal) !important;font-family:'JetBrains Mono',monospace;">${addressable_spend:,.2f}M</div></div>''', unsafe_allow_html=True)

            # Projected savings
            proj = addressable_spend * rate
            cons = addressable_spend * (rate * 0.7)
            opt = addressable_spend * (rate * 1.3)

            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="section-title">Projected <em>Savings</em></h2>', unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'''<div class="metric-dark metric-rust">
                    <div class="metric-label">Conservative (70%)</div>
                    <div class="metric-value">${cons:,.2f}M</div>
                    <div class="metric-label">{rate*70:.4f}% of Spend</div>
                </div>''', unsafe_allow_html=True)
            with c2:
                st.markdown(f'''<div class="metric-dark metric-teal">
                    <div class="metric-label">Median Projection</div>
                    <div class="metric-value">${proj:,.2f}M</div>
                    <div class="metric-label">{rate*100:.4f}% of Spend</div>
                </div>''', unsafe_allow_html=True)
            with c3:
                st.markdown(f'''<div class="metric-dark metric-lime">
                    <div class="metric-label">Optimistic (130%)</div>
                    <div class="metric-value">${opt:,.2f}M</div>
                    <div class="metric-label">{rate*130:.4f}% of Spend</div>
                </div>''', unsafe_allow_html=True)

            st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

            df = pd.DataFrame({
                'Scenario': ['Conservative (70%)', 'Median', 'Optimistic (130%)'],
                'Savings Rate': [f"{rate*70:.4f}%", f"{rate*100:.4f}%", f"{rate*130:.4f}%"],
                'Addressable Spend': [f"${addressable_spend:,.2f}M"]*3,
                'Projected Savings': [f"${cons:,.2f}M", f"${proj:,.2f}M", f"${opt:,.2f}M"]
            })
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.markdown(f'''<div class="alert-box alert-info"><strong>Methodology</strong><br><br>
                Industry "<strong>{mp["original_industry"]}</strong>" mapped to BXT_L2 "<strong>{bxt_l2}</strong>"<br>
                Total Addressable Spend = Revenue (${total_revenue:,.0f}M) × {spend_pct}% = <strong>${addressable_spend:,.2f}M</strong><br>
                Median Projected Savings Rate (NAM/LATAM, >$10B): <strong>{rate*100:.4f}%</strong><br>
                Conservative: 30% reduction / Optimistic: 30% increase from median
            </div>''', unsafe_allow_html=True)

    else:
        st.markdown('''<div class="not-found">
            <strong>Company not found</strong>
            <p>Try searching for "Kiewit Corporation" or "Kiewit"</p>
        </div>''', unsafe_allow_html=True)
else:
    st.markdown('''<div class="welcome-card">
        <h2>Company <em>Intelligence</em></h2>
        <p>Enter a company name in the search bar above to view detailed due diligence, procurement analysis, and cost optimization projections.</p>
        <div class="available">Kiewit Corporation</div>
        <div class="tip">Hover over underlined values to see source references</div>
    </div>''', unsafe_allow_html=True)

# Footer
st.markdown('''<div class="dark-footer">
    <span>COMPANY INTELLIGENCE DASHBOARD © 2025</span>
    <span>DUE DILIGENCE · PROCUREMENT ANALYSIS · COST OPTIMIZATION</span>
</div>''', unsafe_allow_html=True)

