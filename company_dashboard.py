import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="Company Intelligence Dashboard", page_icon="🏢", layout="wide", initial_sidebar_state="collapsed")

# ══════════════════════════════════════════════════════════════════
# CSS — Blackstone Group look & feel
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap');
    :root {
        --bg: #f8fafc; --bg-card: #FFF; --bg-hover: #f1f4f8; --bg-muted: #fafbfc;
        --black: #000; --teal: #1B5E5C; --teal-light: rgba(27,94,92,0.06); --teal-border: rgba(27,94,92,0.15);
        --rust: #A95228; --rust-light: rgba(169,82,40,0.06);
        --blue: #006492; --blue-light: rgba(0,100,146,0.06);
        --lime: #A5CD24; --lime-light: rgba(165,205,36,0.08);
        --tan: #C39D7B; --red: #C12D27;
        --gray: #E4E4E4; --text: #2d2d2d; --text-sec: #666; --text-ter: #999;
        --border: rgba(0,0,0,0.06);
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.04); --shadow-md: 0 4px 16px rgba(0,0,0,0.06); --shadow-lg: 0 12px 40px rgba(0,0,0,0.08);
        --r: 14px; --ease: cubic-bezier(0.22,1,0.36,1);
    }
    * { -webkit-font-smoothing: antialiased; }
    #MainMenu {visibility:hidden;} footer {visibility:hidden;}
    .stApp { background: var(--bg) !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    .block-container { max-width: 1200px; padding-top: 0 !important; }
    .stApp,.stApp p,.stApp span,.stApp div,.stApp li,.stApp label,.stMarkdown,.stMarkdown p,.stMarkdown span { color: var(--text) !important; font-family: 'DM Sans',-apple-system,sans-serif !important; }

    .stTextInput > div > div { background: var(--bg-card) !important; border: 1.5px solid var(--gray) !important; border-radius: 12px !important; transition: all 0.3s var(--ease); box-shadow: var(--shadow-sm); }
    .stTextInput > div > div:focus-within { border-color: var(--teal) !important; box-shadow: 0 0 0 3px var(--teal-light), var(--shadow-md) !important; }
    .stTextInput input { color: var(--text) !important; font-family: 'DM Sans',sans-serif !important; font-size: 15px !important; padding: 14px 18px !important; }
    .stTextInput input::placeholder { color: var(--text-ter) !important; }
    .stTextInput label { display: none !important; }
    .stSlider label { color: var(--text-sec) !important; }
    .stSlider [data-baseweb="slider"] [role="slider"] { background: var(--teal) !important; border-color: var(--teal) !important; }

    /* Tabs — Blackstone underline style */
    .stTabs [data-baseweb="tab-list"] { background: transparent !important; border: none; border-bottom: 1px solid var(--gray); border-radius: 0; padding: 0; gap: 0; box-shadow: none; }
    .stTabs [data-baseweb="tab"] { background: transparent !important; border-radius: 0 !important; padding: 14px 24px !important; font-family: 'DM Sans',sans-serif !important; font-size: 13px !important; font-weight: 500 !important; letter-spacing: 0.3px !important; text-transform: none !important; color: var(--text-sec) !important; transition: all 0.3s var(--ease) !important; border-bottom: 2px solid transparent !important; margin-bottom: -1px !important; }
    .stTabs [data-baseweb="tab"]:hover { color: var(--text) !important; }
    .stTabs [aria-selected="true"] { background: transparent !important; color: var(--text) !important; border-bottom: 2px solid var(--black) !important; font-weight: 600 !important; box-shadow: none !important; }
    .stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"] { display: none !important; }

    /* Hero — Black Blackstone header */
    .hero { background: var(--black); padding: 40px 48px 36px; margin: -1rem -1rem 0 -1rem; position: relative; overflow: hidden; }
    .hero::before { content:''; position:absolute; top:-40%; right:-10%; width:600px; height:600px; background:radial-gradient(circle,rgba(255,255,255,0.03) 0%,transparent 60%); pointer-events:none; }
    .hero-top { display:flex; align-items:center; justify-content:space-between; margin-bottom:32px; position:relative; z-index:1; }
    /* Hero — override ALL Streamlit text color rules inside hero */
    .stApp .hero, .stApp .hero *, .stMarkdown .hero, .stMarkdown .hero *,
    div[data-testid="stMarkdownContainer"] .hero,
    div[data-testid="stMarkdownContainer"] .hero * { color: #FFFFFF !important; }
    div[data-testid="stMarkdownContainer"] .hero .hero-nav { color: rgba(255,255,255,0.4) !important; }
    .hero-wordmark { font-family:'DM Sans',sans-serif !important; font-size:13px; font-weight:700; letter-spacing:3px; text-transform:uppercase; color:#FFF !important; }
    .hero-nav { font-family:'DM Sans',sans-serif !important; font-size:11px; font-weight:400; color:rgba(255,255,255,0.4) !important; letter-spacing:0.5px; }
    .hero h1 { font-family:'Instrument Serif',serif !important; font-size:clamp(40px,5.5vw,64px); font-weight:400; line-height:1.08; letter-spacing:-2px; color:#FFFFFF !important; margin:0; position:relative; z-index:1; }
    .hero h1 em { font-style:italic; color:#FFFFFF !important; }
    .hero-accent-bar { height:3px; margin:0 -1rem; background:linear-gradient(90deg,var(--teal),var(--blue),var(--rust)); }

    /* Search */
    .search-hint { font-family:'DM Sans',sans-serif; font-size:12px; letter-spacing:1px; text-transform:uppercase; font-weight:600; color:var(--text-sec) !important; margin-bottom:12px; }

    /* Sections */
    .sec-label { font-family:'DM Sans',sans-serif; font-size:11px; letter-spacing:2px; font-weight:600; text-transform:uppercase; color:var(--text-sec) !important; margin-bottom:12px; }
    .sec-title { font-family:'Instrument Serif',serif; font-size:clamp(26px,3.5vw,36px); font-weight:400; line-height:1.15; letter-spacing:-1px; color:var(--text) !important; margin-bottom:28px; }
    .sec-title em { font-style:italic; }

    /* Meta grid */
    .meta-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1px; background:var(--gray); border:1px solid var(--gray); border-radius:0; overflow:hidden; margin-bottom:28px; }
    .mg-cell { background:var(--bg-card); padding:24px 22px; transition:background 0.3s var(--ease); }
    .mg-cell:hover { background:var(--bg-hover); }
    .mg-label { font-family:'DM Sans',sans-serif; font-size:10px; letter-spacing:1.5px; text-transform:uppercase; font-weight:600; color:var(--text-ter) !important; margin-bottom:8px; }
    .mg-value { font-size:14px; font-weight:600; color:var(--text) !important; line-height:1.4; }

    /* Card */
    .card { background:var(--bg-card); border:1px solid var(--gray); border-radius:0; padding:28px 26px; margin-bottom:16px; box-shadow:var(--shadow-sm); transition:all 0.4s var(--ease); position:relative; overflow:hidden; }
    .card:hover { box-shadow:var(--shadow-md); }
    .card h3 { font-family:'Instrument Serif',serif; font-size:20px; font-weight:400; color:var(--text) !important; margin-bottom:12px; }
    .card p { color:var(--text-sec) !important; font-size:14px; font-weight:300; line-height:1.8; }

    /* Info rows */
    .irow { padding:16px 20px; background:var(--bg-card); border:1px solid var(--gray); border-radius:0; margin-bottom:8px; box-shadow:var(--shadow-sm); transition:all 0.3s var(--ease); }
    .irow:hover { border-color:var(--teal-border); transform:translateX(4px); box-shadow:var(--shadow-md); }
    .irow-label { font-family:'DM Sans',sans-serif; font-size:9px; letter-spacing:1.5px; text-transform:uppercase; font-weight:600; color:var(--text-ter) !important; margin-bottom:5px; }
    .irow-val { font-size:13.5px; font-weight:400; color:var(--text) !important; line-height:1.6; }

    /* Badges */
    .badge-wrap { display:flex; flex-wrap:wrap; gap:8px; }
    .bdg { display:inline-flex; padding:6px 14px; border:1px solid var(--gray); border-radius:0; font-family:'DM Sans',sans-serif; font-size:11px; font-weight:600; letter-spacing:0.3px; color:var(--text) !important; background:var(--bg-muted); transition:all 0.3s var(--ease); }
    .bdg:hover { background:var(--teal); color:#FFF !important; border-color:var(--teal); }

    /* Metric cards */
    .met { background:var(--bg-card); border:1px solid var(--gray); border-radius:0; padding:28px 20px; text-align:center; box-shadow:var(--shadow-sm); transition:all 0.4s var(--ease); position:relative; overflow:hidden; }
    .met:hover { transform:translateY(-4px); box-shadow:var(--shadow-lg); }
    .met::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; }
    .met .m-val { font-family:'JetBrains Mono',monospace; font-size:clamp(24px,3vw,36px); font-weight:600; line-height:1; margin:10px 0; }
    .met .m-lbl { font-family:'DM Sans',sans-serif; font-size:10px; letter-spacing:1.5px; text-transform:uppercase; font-weight:600; color:var(--text-ter) !important; }
    .met-teal::before { background:var(--teal); } .met-teal .m-val { color:var(--teal) !important; }
    .met-rust::before { background:var(--rust); } .met-rust .m-val { color:var(--rust) !important; }
    .met-lime::before { background:var(--lime); } .met-lime .m-val { color:#6B8F14 !important; }
    .met-blue::before { background:var(--blue); } .met-blue .m-val { color:var(--blue) !important; }

    /* Progress bars */
    .prog { margin-bottom:16px; }
    .prog-head { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:6px; }
    .prog-name { font-size:13px; color:var(--text) !important; }
    .prog-lvl { font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:600; color:var(--teal) !important; }
    .prog-track { background:var(--gray); border-radius:0; height:6px; overflow:hidden; }
    .prog-fill { height:100%; background:var(--teal); transition:width 0.8s var(--ease); }

    /* SWOT */
    .swot { background:var(--bg-card); border:1px solid var(--gray); border-radius:0; padding:24px 22px; margin-bottom:14px; box-shadow:var(--shadow-sm); position:relative; overflow:hidden; transition:all 0.4s var(--ease); }
    .swot:hover { transform:translateX(3px); box-shadow:var(--shadow-md); }
    .swot::before { content:''; position:absolute; top:0; left:0; width:3px; height:100%; }
    .s-str::before { background:var(--lime); } .s-wk::before { background:var(--tan); } .s-op::before { background:var(--blue); } .s-th::before { background:var(--red); }
    .swot-ttl { font-family:'DM Sans',sans-serif; font-size:10px; letter-spacing:2px; font-weight:700; text-transform:uppercase; margin-bottom:14px; }
    .s-str .swot-ttl { color:#6B8F14 !important; } .s-wk .swot-ttl { color:var(--tan) !important; } .s-op .swot-ttl { color:var(--blue) !important; } .s-th .swot-ttl { color:var(--red) !important; }
    .swot ul { list-style:none; padding:0; margin:0; }
    .swot li { font-size:13px; color:var(--text-sec) !important; font-weight:300; line-height:1.7; padding:7px 0; border-bottom:1px solid var(--border); display:flex; align-items:flex-start; gap:8px; }
    .swot li:last-child { border-bottom:none; }
    .swot li::before { content:'→'; flex-shrink:0; margin-top:1px; opacity:0.4; }
    .s-str li::before { color:var(--lime); } .s-wk li::before { color:var(--tan); } .s-op li::before { color:var(--blue); } .s-th li::before { color:var(--red); }

    /* Alert boxes */
    .abox { padding:18px 22px; border-radius:0; margin-bottom:10px; border:1px solid var(--gray); background:var(--bg-card); font-size:13px; font-weight:300; color:var(--text-sec) !important; line-height:1.7; box-shadow:var(--shadow-sm); transition:all 0.3s var(--ease); }
    .abox:hover { box-shadow:var(--shadow-md); }
    .a-warn { border-left:3px solid var(--rust); } .a-ok { border-left:3px solid var(--lime); } .a-info { border-left:3px solid var(--blue); }
    .abox strong { color:var(--text) !important; font-weight:600; }

    /* Tooltips — fixed for reliable hover */
    .ws { position:relative; cursor:pointer; border-bottom:1px dotted var(--text-ter); display:inline; transition:border-color 0.3s; z-index:1; }
    .ws:hover { border-bottom-color:var(--teal); z-index:9999; }
    .tt { display:none; position:absolute; background:var(--bg-card); color:var(--text) !important; padding:18px 22px; border-radius:8px; font-size:12px; z-index:99999; max-width:420px; min-width:280px; box-shadow:0 8px 30px rgba(0,0,0,0.18); border:1px solid var(--gray); left:0; bottom:calc(100% + 10px); line-height:1.6; pointer-events:auto; }
    .tt::after { content:""; position:absolute; bottom:-14px; left:0; right:0; height:18px; background:transparent; }
    .ws:hover .tt { display:block; }
    .tt:hover { display:block; }
    .tt strong { color:var(--teal) !important; display:block; margin-bottom:6px; font-size:11px; letter-spacing:1px; text-transform:uppercase; }
    .tt a { color:var(--rust) !important; text-decoration:underline; font-weight:600; display:inline-block; margin-top:8px; padding:4px 0; font-size:12px; }
    .tt a:hover { color:var(--teal) !important; }
    .tt-q { font-style:italic; color:var(--text-sec) !important; margin:6px 0 8px 0; padding-left:12px; border-left:2px solid var(--teal); font-size:11px; line-height:1.5; }
    /* Prevent parent overflow from clipping tooltips */
    .card, .irow, .swot, .mg-cell, .abox, .met { overflow:visible !important; }

    /* Criteria & Mapping */
    .crit-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1px; background:var(--gray); border:1px solid var(--gray); border-radius:0; overflow:hidden; margin:20px 0; }
    .crit-cell { background:var(--bg-card); padding:22px 20px; transition:background 0.3s; }
    .crit-cell:hover { background:var(--bg-hover); }
    .crit-lbl { font-family:'DM Sans',sans-serif; font-size:9px; letter-spacing:1.5px; text-transform:uppercase; font-weight:600; color:var(--text-ter) !important; margin-bottom:6px; }
    .crit-val { font-size:15px; font-weight:600; color:var(--text) !important; margin-bottom:4px; }
    .crit-st { font-family:'JetBrains Mono',monospace; font-size:10px; }
    .map-flow { display:flex; align-items:center; gap:0; flex-wrap:wrap; margin:20px 0; }
    .map-node { background:var(--bg-card); border:1px solid var(--gray); border-radius:0; padding:16px 18px; flex:1; min-width:160px; box-shadow:var(--shadow-sm); transition:all 0.3s var(--ease); }
    .map-node:hover { box-shadow:var(--shadow-md); border-color:var(--teal-border); }
    .map-node.hl { border-color:var(--teal); background:var(--teal-light); }
    .map-lbl { font-family:'DM Sans',sans-serif; font-size:9px; letter-spacing:2px; text-transform:uppercase; font-weight:600; color:var(--text-ter) !important; margin-bottom:5px; }
    .map-val { font-size:13px; font-weight:500; color:var(--text) !important; line-height:1.4; }
    .map-node.hl .map-val { color:var(--teal) !important; font-family:'JetBrains Mono',monospace; font-size:18px; font-weight:700; }
    .map-arrow { font-size:16px; color:var(--text-ter); padding:0 10px; flex-shrink:0; opacity:0.3; }

    /* Misc */
    .divider { height:1px; margin:36px 0; background:var(--gray); }
    .slider-lbl { font-family:'DM Sans',sans-serif; font-size:10px; letter-spacing:1.5px; text-transform:uppercase; font-weight:600; color:var(--text-sec) !important; margin-bottom:10px; }
    .dark-footer { padding:32px 0; border-top:1px solid var(--gray); margin-top:48px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; }
    .dark-footer span { font-family:'DM Sans',sans-serif; font-size:11px; color:var(--text-ter) !important; letter-spacing:0.5px; }

    /* Welcome */
    .welcome { background:var(--bg-card); border:1px solid var(--gray); border-radius:0; padding:80px 48px; text-align:center; }
    .welcome h2 { font-family:'Instrument Serif',serif; font-size:clamp(28px,4vw,44px); font-weight:400; letter-spacing:-1px; color:var(--text) !important; margin-bottom:16px; }
    .welcome h2 em { font-style:italic; }
    .welcome p { color:var(--text-sec) !important; font-size:16px; font-weight:300; line-height:1.7; max-width:520px; margin:0 auto; }
    .welcome .avail { display:inline-block; padding:8px 20px; margin-top:32px; border:1px solid var(--gray); font-family:'DM Sans',sans-serif; font-size:12px; font-weight:600; color:var(--text) !important; background:var(--bg-muted); }
    .welcome .tip { margin-top:24px; font-size:11px; color:var(--text-ter) !important; }
    .notfound { background:var(--bg-card); border:1px solid var(--gray); border-left:3px solid var(--rust); padding:28px; text-align:center; }
    .notfound strong { color:var(--rust) !important; } .notfound p { color:var(--text-sec) !important; margin-top:6px; }

    /* ══ FLOW DIAGRAM TAB ══ */
    .flow-container { margin:24px 0; }
    .flow-step { display:flex; align-items:stretch; margin-bottom:0; position:relative; }
    .flow-line { width:48px; flex-shrink:0; display:flex; flex-direction:column; align-items:center; }
    .flow-dot { width:14px; height:14px; border-radius:50%; border:3px solid; background:var(--bg); flex-shrink:0; z-index:1; }
    .flow-connector { width:2px; flex:1; }
    .flow-content { flex:1; padding:0 0 32px 20px; }
    .flow-step-label { font-family:'DM Sans',sans-serif; font-size:9px; letter-spacing:2px; text-transform:uppercase; font-weight:700; margin-bottom:4px; }
    .flow-step-title { font-family:'Instrument Serif',serif; font-size:22px; font-weight:400; color:var(--text) !important; margin-bottom:8px; }
    .flow-step-desc { font-size:13px; color:var(--text-sec) !important; font-weight:300; line-height:1.7; }
    .flow-badge { display:inline-block; padding:3px 10px; font-size:9px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; margin-top:10px; }
    .flow-badge-ext { background:var(--blue-light); color:var(--blue) !important; border:1px solid rgba(0,100,146,0.2); }
    .flow-badge-int { background:var(--teal-light); color:var(--teal) !important; border:1px solid var(--teal-border); }
    .flow-badge-out { background:var(--rust-light); color:var(--rust) !important; border:1px solid rgba(169,82,40,0.2); }

    /* Download button */
    .dl-btn { display:inline-block; padding:12px 28px; background:var(--black); color:#FFF !important; font-family:'DM Sans',sans-serif; font-size:13px; font-weight:600; letter-spacing:0.5px; text-decoration:none; border:none; transition:all 0.3s; cursor:pointer; margin-top:16px; }
    .dl-btn:hover { background:var(--teal); }

    @media (max-width:768px) { .meta-grid{grid-template-columns:repeat(2,1fr);} .crit-grid{grid-template-columns:1fr;} .map-flow{flex-direction:column;align-items:stretch;} .map-arrow{transform:rotate(90deg);text-align:center;padding:4px 0;} }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════
BXT_L2_SAVINGS = {"Engineering, architecture and construction management": 0.02371, "Heavy Construction & Engineering": 0.045, "General Contractors": 0.038, "Oil & Gas": 0.048, "Mining": 0.041, "Default": 0.04}

COMPANY_DATA = {
    "kiewit": {
        "meta": {"company_name": {"value": "Kiewit Corporation", "quote": "Kiewit is one of North America's largest and most respected construction and engineering organizations.", "source_url": "https://www.kiewit.com/about-us/"}, "jurisdiction": {"value": "United States, Canada and Mexico", "quote": "The employee-owned organization operates through a network of subsidiaries in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"}, "listed_status": {"value": "Private (employee-owned)", "quote": "With its roots dating back to 1884, the employee-owned organization operates.", "source_url": "https://www.forbes.com/companies/kiewit/"}},
        "company_overview": {"description": {"value": "Kiewit Corporation is one of North America's largest construction and engineering organizations, delivering end-to-end EPC services for critical infrastructure and energy projects.", "quote": "Kiewit is one of North America's largest and most respected construction and engineering organizations.", "source_url": "https://www.kiewit.com/about-us/"}, "founded_year": {"value": 1884, "quote": "With its roots dating back to 1884.", "source_url": "https://www.forbes.com/companies/kiewit/"}, "headquarters": {"value": "Omaha, Nebraska, United States", "quote": "The Kiewit Corporation is a Fortune 500 contractor business headquartered in Omaha.", "source_url": "http://www.omahaimc.org/kiewit-corporation/"}, "primary_industry": {"value": "Engineering, Procurement and Construction (EPC) services", "quote": "The EPC model streamlines execution with a single contractor managing design, procurement and construction.", "source_url": "https://www.kiewit.com/services-and-solutions/project-delivery/"}, "primary_markets": [{"value": "Transportation", "quote": "Kiewit offers construction and engineering services in transportation.", "source_url": "https://www.linkedin.com/company/kiewit"}, {"value": "Oil, Gas & Chemical", "quote": "Kiewit offers services in oil, gas and chemical.", "source_url": "https://www.linkedin.com/company/kiewit"}, {"value": "Power", "quote": "Kiewit offers services in power.", "source_url": "https://www.linkedin.com/company/kiewit"}, {"value": "Building", "quote": "Kiewit offers services in building.", "source_url": "https://www.linkedin.com/company/kiewit"}, {"value": "Marine", "quote": "Kiewit offers services in marine.", "source_url": "https://www.linkedin.com/company/kiewit"}, {"value": "Water / Wastewater", "quote": "Kiewit offers services in water/wastewater.", "source_url": "https://www.linkedin.com/company/kiewit"}, {"value": "Industrial", "quote": "Kiewit offers services in industrial.", "source_url": "https://www.linkedin.com/company/kiewit"}, {"value": "Mining", "quote": "Kiewit offers services in mining.", "source_url": "https://www.linkedin.com/company/kiewit"}]},
        "operational_footprint": {"regions_of_operation": [{"value": "United States", "quote": "Operates in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"}, {"value": "Canada", "quote": "Operates in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"}, {"value": "Mexico", "quote": "Operates in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"}], "business_segments": ["Transportation", "Oil, Gas & Chemical", "Power", "Building", "Marine", "Water/Wastewater", "Industrial", "Mining"], "geographic_scope": "NAM/LATAM"},
        "workforce": {"total_employees": {"value": 31800, "quote": "31,800 EMPLOYEES 2024", "source_url": "https://www.kiewit.com/wp-content/uploads/2025/09/EN_2024-Sustainability-Report-reduced.pdf"}},
        "financials": {"revenue_2024": {"value": 16.8, "quote": "$16.8B 2024 Revenues", "source_url": "https://www.kiewit.com"}, "source_note": "Private company – estimates only; no official statutory filings."},
        "ownership_structure": {"ownership_type": {"value": "Privately held, employee-owned organization", "quote": "Backed by a multi-billion-dollar, employee-owned organization.", "source_url": "https://www.kiewit.com/about-us/"}},
        "procurement_organization": {
            "overall_maturity_level": {"value": "Defined to Managed", "quote": "Supply chain is integrated into project planning from the very beginning.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
            "maturity_dimensions": {"Governance & Org": {"value": "Managed", "score": 4, "quote": "Material procurement can account for up to 50% of total installed costs.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}, "Process & Policy": {"value": "Defined", "score": 3, "quote": "Supply chain is integrated into project planning from the very beginning.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}, "Technology & Data": {"value": "Defined", "score": 3, "quote": "Procurement experts leverage scale, strategy and technology.", "source_url": "https://www.kiewit.com/?lang=en-ca"}, "Supplier Management": {"value": "Defined", "score": 3, "quote": "The worst thing a vendor can do is hide a problem.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}, "Integration Lifecycle": {"value": "Managed", "score": 4, "quote": "We help define risk and create the roadmap for delivery.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}},
            "structure": {"value": "Supply chain sits between engineering and construction, ensuring materials arrive on time.", "quote": "Our job is to make sure materials arrive when construction needs them.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
            "category_mgmt": {"value": "Organized around categories with specialists owning domains such as valves or piping.", "quote": "Reorganized team around procurement categories.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
            "cpo": {"value": "Carsten Bernstiel — VP Procurement, OGC group", "quote": "Carsten Bernstiel, Vice President of Procurement for Kiewit's OGC group.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}},
        "procurement_risks": {"key_risks": [{"value": "High share of total installed cost tied to materials", "quote": "Material procurement can account for up to 50% of total installed costs.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}, {"value": "Global shipping disruptions impacting lead times", "quote": "We rerouted shipments through Los Angeles.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}, {"value": "Dependence on transparent supplier communication", "quote": "The worst thing a vendor can do is hide a problem.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}], "mitigation": {"value": "Early involvement in strategy, proactive planning, logistics rerouting, and transparent supplier communication.", "quote": "We rerouted shipments through Los Angeles.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}},
        "procurement_swot": {"strengths": [{"value": "Integrated EPC model — single contractor for design, procurement and construction", "quote": "The EPC model streamlines execution.", "source_url": "https://www.kiewit.com/services-and-solutions/project-delivery/"}, {"value": "Supply chain integrated from start of project planning", "quote": "Supply chain is integrated from the very beginning.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}, {"value": "Category-based procurement with domain specialists", "quote": "Reorganized team around procurement categories.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}], "weaknesses": [{"value": "Limited public transparency on procurement KPIs and ESG vs listed peers", "quote": "One of North America's largest organizations.", "source_url": "https://www.kiewit.com/about-us/"}, {"value": "Advanced practices concentrated in OGC group — maturity may be uneven", "quote": "VP of Procurement for Kiewit's OGC group.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}], "opportunities": [{"value": "AI/technology to anticipate disruptions and optimize sourcing", "quote": "EPCs transformed into partners — not just vendors.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}, {"value": "Increasing ESG and supplier diversity visibility", "quote": "Long history of partnering with the local business community.", "source_url": "https://www.kiewit.com/business-with-us/opportunities/central-florida-projects/"}, {"value": "Extending category management across all markets", "quote": "Reorganized team around procurement categories.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}], "threats": [{"value": "Materials up to 50% of installed cost — commodity/logistics exposure", "quote": "Material procurement can account for up to 50%.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}, {"value": "Canal congestion adding weeks to lead times", "quote": "We rerouted shipments through Los Angeles.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}, {"value": "Competitors investing in digital procurement and ESG branding", "quote": "The EPC model streamlines execution.", "source_url": "https://www.kiewit.com/services-and-solutions/project-delivery/"}]},
        "industry_mapping": {"original_industry": "Engineering, Procurement and Construction (EPC) services", "bxt_l2": "Engineering, architecture and construction management", "median_projected_savings_rate": 0.02371}
    }
}

# ══════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════
def get_company_data(name):
    t = name.lower().strip()
    for k, d in COMPANY_DATA.items():
        if k in t or t in d["meta"]["company_name"]["value"].lower(): return d
    return None

def src(v, q, u):
    if not q or not u: return f'<span>{v}</span>'
    return f'<span class="ws">{v}<span class="tt"><strong>Source</strong><div class="tt-q">"{q}"</div><a href="{u}" target="_blank">View source ↗</a></span></span>'

def irow(label, value, quote=None, url=None):
    val = src(value, quote, url) if quote else f'<span>{value}</span>'
    return f'<div class="irow"><div class="irow-label">{label}</div><div class="irow-val">{val}</div></div>'

def swot_card(title, items, cls):
    html = "".join([f'<li>{src(i["value"], i["quote"], i["source_url"])}</li>' for i in items])
    return f'<div class="swot {cls}"><div class="swot-ttl">{title}</div><ul>{html}</ul></div>'

def check_criteria(co):
    g = co.get("operational_footprint",{}).get("geographic_scope","")
    r = co.get("financials",{}).get("revenue_2024",{}).get("value",0) or 0
    return g in ["NAM","LATAM","NAM/LATAM"], r>10, g, r

def generate_pdf(co):
    """Generate a downloadable HTML report (renders as PDF-like in browser)."""
    m = co["meta"]; ov = co["company_overview"]; fin = co["financials"]
    proc = co["procurement_organization"]; mp = co["industry_mapping"]
    is_nam, is_10b, geo, revenue = check_criteria(co)
    meets = is_nam and is_10b
    rate = BXT_L2_SAVINGS.get(mp["bxt_l2"], BXT_L2_SAVINGS["Default"]) if meets else BXT_L2_SAVINGS["Default"]
    total_rev = revenue * 1000

    dims_html = ""
    for dim, data in proc["maturity_dimensions"].items():
        dims_html += f"<tr><td style='padding:6px 12px;border-bottom:1px solid #eee;'>{dim}</td><td style='padding:6px 12px;border-bottom:1px solid #eee;'>{data['value']} ({data['score']}/5)</td></tr>"

    swot_html = ""
    for cat, label in [("strengths","Strengths"),("weaknesses","Weaknesses"),("opportunities","Opportunities"),("threats","Threats")]:
        items = "".join([f"<li style='margin-bottom:4px;'>{i['value']}</li>" for i in co["procurement_swot"][cat]])
        swot_html += f"<div style='margin-bottom:16px;'><strong>{label}</strong><ul style='margin-top:4px;'>{items}</ul></div>"

    risks_html = "".join([f"<li style='margin-bottom:4px;'>⚠ {r['value']}</li>" for r in co["procurement_risks"]["key_risks"]])

    savings_rows = ""
    for pct in [20, 30, 40]:
        spend = total_rev * (pct / 100)
        p = spend * rate; c = spend * rate * 0.7; o = spend * rate * 1.3
        savings_rows += f"<tr><td style='padding:6px 12px;border-bottom:1px solid #eee;'>{pct}%</td><td style='padding:6px 12px;border-bottom:1px solid #eee;'>${spend:,.0f}M</td><td style='padding:6px 12px;border-bottom:1px solid #eee;'>${c:,.2f}M</td><td style='padding:6px 12px;border-bottom:1px solid #eee;'>${p:,.2f}M</td><td style='padding:6px 12px;border-bottom:1px solid #eee;'>${o:,.2f}M</td></tr>"

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <title>{m['company_name']['value']} - Intelligence Report</title>
    <style>
        @page {{ margin: 40px 50px; }}
        body {{ font-family: Helvetica, Arial, sans-serif; color: #2d2d2d; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 40px; }}
        h1 {{ font-size: 24px; font-weight: 700; margin: 0 0 4px 0; }}
        h2 {{ font-size: 16px; color: #1B5E5C; border-bottom: 2px solid #1B5E5C; padding-bottom: 6px; margin-top: 28px; }}
        .sub {{ font-size: 12px; color: #666; margin-bottom: 20px; }}
        .bar {{ height: 3px; background: #000; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 12px; margin: 10px 0; }}
        th {{ text-align: left; padding: 8px 12px; background: #f5f5f5; border-bottom: 2px solid #ddd; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: #666; }}
        p, li {{ font-size: 12px; }}
        .footer {{ margin-top: 40px; padding-top: 16px; border-top: 1px solid #ddd; font-size: 10px; color: #999; }}
    </style></head><body>
    <h1>Company Intelligence Report</h1>
    <div class="sub">{m['company_name']['value']} — Confidential</div>
    <div class="bar"></div>

    <h2>Company Overview</h2>
    <p>{ov['description']['value']}</p>
    <table>
        <tr><td style="padding:6px 12px;border-bottom:1px solid #eee;font-weight:bold;color:#666;">Founded</td><td style="padding:6px 12px;border-bottom:1px solid #eee;">{ov['founded_year']['value']}</td><td style="padding:6px 12px;border-bottom:1px solid #eee;font-weight:bold;color:#666;">Headquarters</td><td style="padding:6px 12px;border-bottom:1px solid #eee;">{ov['headquarters']['value']}</td></tr>
        <tr><td style="padding:6px 12px;border-bottom:1px solid #eee;font-weight:bold;color:#666;">Jurisdiction</td><td style="padding:6px 12px;border-bottom:1px solid #eee;">{m['jurisdiction']['value']}</td><td style="padding:6px 12px;border-bottom:1px solid #eee;font-weight:bold;color:#666;">Status</td><td style="padding:6px 12px;border-bottom:1px solid #eee;">{m['listed_status']['value']}</td></tr>
        <tr><td style="padding:6px 12px;border-bottom:1px solid #eee;font-weight:bold;color:#666;">Employees</td><td style="padding:6px 12px;border-bottom:1px solid #eee;">{co['workforce']['total_employees']['value']:,}</td><td style="padding:6px 12px;border-bottom:1px solid #eee;font-weight:bold;color:#666;">Revenue 2024</td><td style="padding:6px 12px;border-bottom:1px solid #eee;">${fin['revenue_2024']['value']}B</td></tr>
    </table>

    <h2>Procurement Organization</h2>
    <p><strong>Maturity:</strong> {proc['overall_maturity_level']['value']} &nbsp;|&nbsp; <strong>CPO:</strong> {proc['cpo']['value']}</p>
    <p><strong>Structure:</strong> {proc['structure']['value']}</p>
    <table><tr><th>Dimension</th><th>Score</th></tr>{dims_html}</table>

    <h2>Procurement SWOT</h2>
    {swot_html}

    <h2>Procurement Risks</h2>
    <ul>{risks_html}</ul>
    <p><strong>Mitigation:</strong> {co['procurement_risks']['mitigation']['value']}</p>

    <h2>Cost Optimization Projection</h2>
    <p><strong>Industry:</strong> {mp['original_industry']} → <strong>BXT L2:</strong> {mp['bxt_l2']}</p>
    <p><strong>Savings Rate:</strong> {rate*100:.4f}% &nbsp;|&nbsp; <strong>Scope:</strong> {geo} &nbsp;|&nbsp; <strong>Revenue:</strong> ${revenue}B</p>
    <table><tr><th>Spend %</th><th>Addressable</th><th>Conservative</th><th>Median</th><th>Optimistic</th></tr>{savings_rows}</table>

    <div class="footer">Confidential — For informational purposes only. Generated by BX Company Intelligence Platform.</div>
    </body></html>"""
    return html

# ══════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════
st.markdown('''<div class="hero">
    <div class="hero-top">
        <span class="hero-wordmark">Blackstone</span>
        <span class="hero-nav">Due Diligence & Procurement Analysis</span>
    </div>
    <h1>Company<br><em>Intelligence</em></h1>
</div><div class="hero-accent-bar"></div>''', unsafe_allow_html=True)

# SEARCH
st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="search-hint">Search Company</div>', unsafe_allow_html=True)
    search = st.text_input("s", placeholder="Enter company name (e.g., Kiewit Corporation)", label_visibility="collapsed")

# ══════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════
if search:
    co = get_company_data(search)
    if co:
        tab1, tab2, tab3 = st.tabs(["General Information", "Financials & Cost Optimization", "How It Works"])

        # ─── TAB 1: GENERAL INFO ───
        with tab1:
            st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

            # PDF-like HTML download
            report_html = generate_pdf(co)
            b64 = base64.b64encode(report_html.encode()).decode()
            company_name = co["meta"]["company_name"]["value"].replace(" ", "_")
            st.markdown(f'<div style="text-align:right;"><a class="dl-btn" href="data:text/html;base64,{b64}" download="{company_name}_Intelligence_Report.html">↓ Download Report</a></div>', unsafe_allow_html=True)

            st.markdown('<div class="sec-label">Overview</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="sec-title">Company <em>Profile</em></h2>', unsafe_allow_html=True)
            m=co["meta"]; ov=co["company_overview"]
            st.markdown(f'''<div class="meta-grid">
                <div class="mg-cell"><div class="mg-label">Company</div><div class="mg-value">{src(m["company_name"]["value"],m["company_name"]["quote"],m["company_name"]["source_url"])}</div></div>
                <div class="mg-cell"><div class="mg-label">Jurisdiction</div><div class="mg-value">{src(m["jurisdiction"]["value"],m["jurisdiction"]["quote"],m["jurisdiction"]["source_url"])}</div></div>
                <div class="mg-cell"><div class="mg-label">Status</div><div class="mg-value">{src(m["listed_status"]["value"],m["listed_status"]["quote"],m["listed_status"]["source_url"])}</div></div>
                <div class="mg-cell"><div class="mg-label">Founded</div><div class="mg-value">{src(str(ov["founded_year"]["value"]),ov["founded_year"]["quote"],ov["founded_year"]["source_url"])}</div></div>
            </div>''', unsafe_allow_html=True)

            d=ov["description"]
            st.markdown(f'<div class="card"><h3>Description</h3><p>{src(d["value"],d["quote"],d["source_url"])}</p></div>', unsafe_allow_html=True)
            c1,c2=st.columns(2)
            with c1:
                st.markdown('<div class="sec-label">Corporate Structure</div>', unsafe_allow_html=True)
                hq=ov["headquarters"]; st.markdown(irow("Headquarters",hq["value"],hq["quote"],hq["source_url"]), unsafe_allow_html=True)
                own=co["ownership_structure"]["ownership_type"]; st.markdown(irow("Ownership",own["value"],own["quote"],own["source_url"]), unsafe_allow_html=True)
                emp=co["workforce"]["total_employees"]; st.markdown(irow("Employees",f'{emp["value"]:,}',emp["quote"],emp["source_url"]), unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="sec-label">Business Segments</div>', unsafe_allow_html=True)
                badges="".join([f'<span class="bdg">{s}</span>' for s in co["operational_footprint"]["business_segments"]])
                st.markdown(f'<div class="card"><div class="badge-wrap">{badges}</div></div>', unsafe_allow_html=True)
                st.markdown('<div class="sec-label">Regions</div>', unsafe_allow_html=True)
                for r in co["operational_footprint"]["regions_of_operation"]:
                    st.markdown(irow("📍",r["value"],r["quote"],r["source_url"]), unsafe_allow_html=True)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-label">Supply Chain & Procurement</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="sec-title">Procurement <em>Organization</em></h2>', unsafe_allow_html=True)
            c1,c2=st.columns(2)
            with c1:
                proc=co["procurement_organization"]
                for lbl,key in [("Maturity Level","overall_maturity_level"),("Structure","structure"),("Category Mgmt","category_mgmt"),("CPO / Equivalent","cpo")]:
                    v=proc[key]; st.markdown(irow(lbl,v["value"],v["quote"],v["source_url"]), unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="sec-label">Maturity Dimensions</div>', unsafe_allow_html=True)
                for dim,data in proc["maturity_dimensions"].items():
                    pct=(data["score"]/5)*100
                    st.markdown(f'<div class="prog"><div class="prog-head"><span class="prog-name">{src(dim,data["quote"],data["source_url"])}</span><span class="prog-lvl">{data["value"]} ({data["score"]}/5)</span></div><div class="prog-track"><div class="prog-fill" style="width:{pct}%;"></div></div></div>', unsafe_allow_html=True)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-label">Analysis</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="sec-title">Procurement <em>SWOT</em></h2>', unsafe_allow_html=True)
            c1,c2=st.columns(2)
            with c1:
                st.markdown(swot_card("STRENGTHS",co["procurement_swot"]["strengths"],"s-str"), unsafe_allow_html=True)
                st.markdown(swot_card("OPPORTUNITIES",co["procurement_swot"]["opportunities"],"s-op"), unsafe_allow_html=True)
            with c2:
                st.markdown(swot_card("WEAKNESSES",co["procurement_swot"]["weaknesses"],"s-wk"), unsafe_allow_html=True)
                st.markdown(swot_card("THREATS",co["procurement_swot"]["threats"],"s-th"), unsafe_allow_html=True)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-label">Risk Assessment</div>', unsafe_allow_html=True)
            for risk in co["procurement_risks"]["key_risks"]:
                st.markdown(f'<div class="abox a-warn">{src(risk["value"],risk["quote"],risk["source_url"])}</div>', unsafe_allow_html=True)
            mit=co["procurement_risks"]["mitigation"]
            st.markdown(f'<div class="abox a-ok"><strong>Risk Mitigation</strong><br><br>{src(mit["value"],mit["quote"],mit["source_url"])}</div>', unsafe_allow_html=True)

        # ─── TAB 2: FINANCIALS ───
        with tab2:
            st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-label">Financials</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="sec-title">Financial <em>Overview</em></h2>', unsafe_allow_html=True)
            r24=co['financials']['revenue_2024']; emp=co['workforce']['total_employees']
            c1,c2,c3=st.columns(3)
            with c1:
                r24v=r24["value"]; r24q=r24["quote"]; r24u=r24["source_url"]
                st.markdown(f'<div class="met met-teal"><div class="m-lbl">2024 Revenue</div><div class="m-val">{src(f"${r24v}B",r24q,r24u)}</div><div class="m-lbl">USD</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="met met-blue"><div class="m-lbl">Geographic Scope</div><div class="m-val">{co["operational_footprint"]["geographic_scope"]}</div><div class="m-lbl">Region</div></div>', unsafe_allow_html=True)
            with c3:
                empv=emp["value"]; empq=emp["quote"]; empu=emp["source_url"]
                st.markdown(f'<div class="met met-rust"><div class="m-lbl">Employees</div><div class="m-val">{src(f"{empv:,}",empq,empu)}</div><div class="m-lbl">2024</div></div>', unsafe_allow_html=True)

            st.markdown(f'<div class="abox a-warn"><strong>Note:</strong> {co["financials"]["source_note"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-label">Projections</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="sec-title">Cost <em>Optimization</em></h2>', unsafe_allow_html=True)

            is_nam,is_10b,geo,revenue=check_criteria(co)
            meets=is_nam and is_10b; mp=co["industry_mapping"]; bxt=mp["bxt_l2"]
            rate=BXT_L2_SAVINGS.get(bxt,BXT_L2_SAVINGS["Default"]) if meets else BXT_L2_SAVINGS["Default"]

            st.markdown(f'''<div class="crit-grid">
                <div class="crit-cell"><div class="crit-lbl">Geographic Scope</div><div class="crit-val">{geo}</div><div class="crit-st" style="color:{"var(--lime)" if is_nam else "var(--red)"};">{"✓ NAM/LATAM" if is_nam else "✗ Required: NAM/LATAM"}</div></div>
                <div class="crit-cell"><div class="crit-lbl">Revenue</div><div class="crit-val">${revenue}B USD</div><div class="crit-st" style="color:{"var(--lime)" if is_10b else "var(--red)"};">{"✓ >$10B" if is_10b else "✗ Required: >$10B"}</div></div>
                <div class="crit-cell"><div class="crit-lbl">Status</div><div class="crit-val" style="color:{"var(--lime)" if meets else "var(--red)"};">{"✓ MEETS CRITERIA" if meets else "✗ DOES NOT MEET"}</div><div class="crit-st" style="color:var(--text-ter);">{"Using BXT_L2 rate" if meets else "Using default rate"}</div></div>
            </div>''', unsafe_allow_html=True)

            st.markdown(f'''<div class="map-flow">
                <div class="map-node"><div class="map-lbl">Original Industry</div><div class="map-val">{mp["original_industry"]}</div></div>
                <span class="map-arrow">→</span>
                <div class="map-node"><div class="map-lbl">BXT L2 Classification</div><div class="map-val">{bxt}</div></div>
                <span class="map-arrow">→</span>
                <div class="map-node hl"><div class="map-lbl">Median Savings Rate</div><div class="map-val">{rate*100:.4f}%</div></div>
            </div>''', unsafe_allow_html=True)

            total_revenue=revenue*1000
            c1,c2=st.columns(2)
            with c1:
                st.markdown('<div class="slider-lbl">Total Addressable Spend (% of Revenue)</div>', unsafe_allow_html=True)
                spend_pct=st.slider("s",min_value=0,max_value=100,value=30,step=5,label_visibility="collapsed")
                addressable=total_revenue*(spend_pct/100)
                st.markdown(f'<div class="abox a-info"><strong>Calculation</strong><br><br>Revenue: <strong>${total_revenue:,.0f}M</strong> × {spend_pct}% = <strong>${addressable:,.2f}M</strong> Addressable Spend</div>', unsafe_allow_html=True)
            with c2:
                st.markdown(irow("BXT L2 Category",bxt), unsafe_allow_html=True)
                st.markdown(f'<div class="irow"><div class="irow-label">Median Savings Rate</div><div class="irow-val" style="color:var(--teal) !important;font-family:JetBrains Mono,monospace;font-weight:600;">{rate*100:.4f}%</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="irow"><div class="irow-label">Total Addressable Spend</div><div class="irow-val" style="color:var(--teal) !important;font-family:JetBrains Mono,monospace;font-weight:600;">${addressable:,.2f}M</div></div>', unsafe_allow_html=True)

            proj=addressable*rate; cons=addressable*(rate*0.7); opt=addressable*(rate*1.3)
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-label">Results</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="sec-title">Projected <em>Savings</em></h2>', unsafe_allow_html=True)
            c1,c2,c3=st.columns(3)
            with c1: st.markdown(f'<div class="met met-rust"><div class="m-lbl">Conservative (70%)</div><div class="m-val">${cons:,.2f}M</div><div class="m-lbl">{rate*70:.4f}% of Spend</div></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="met met-teal"><div class="m-lbl">Median Projection</div><div class="m-val">${proj:,.2f}M</div><div class="m-lbl">{rate*100:.4f}% of Spend</div></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="met met-lime"><div class="m-lbl">Optimistic (130%)</div><div class="m-val">${opt:,.2f}M</div><div class="m-lbl">{rate*130:.4f}% of Spend</div></div>', unsafe_allow_html=True)

            st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
            df=pd.DataFrame({'Scenario':['Conservative (70%)','Median','Optimistic (130%)'],'Savings Rate':[f"{rate*70:.4f}%",f"{rate*100:.4f}%",f"{rate*130:.4f}%"],'Addressable Spend':[f"${addressable:,.2f}M"]*3,'Projected Savings':[f"${cons:,.2f}M",f"${proj:,.2f}M",f"${opt:,.2f}M"]})
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.markdown(f'<div class="abox a-info"><strong>Methodology</strong><br><br>Industry "<strong>{mp["original_industry"]}</strong>" mapped to BXT_L2 "<strong>{bxt}</strong>"<br>Total Addressable Spend = Revenue (${total_revenue:,.0f}M) × {spend_pct}% = <strong>${addressable:,.2f}M</strong><br>Median Projected Savings Rate (NAM/LATAM, >$10B): <strong>{rate*100:.4f}%</strong><br>Conservative: 30% reduction / Optimistic: 30% increase from median</div>', unsafe_allow_html=True)

        # ─── TAB 3: HOW IT WORKS ───
        with tab3:
            st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-label">Architecture</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="sec-title">How It <em>Works</em></h2>', unsafe_allow_html=True)

            # ── VISUAL FLOWCHART ──
            st.markdown('''
            <svg viewBox="0 0 960 640" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:960px;margin:0 auto 40px;display:block;font-family:Helvetica,Arial,sans-serif;">
              <defs>
                <marker id="ah-b" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#006492"/></marker>
                <marker id="ah-t" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#1B5E5C"/></marker>
                <marker id="ah-r" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#A95228"/></marker>
                <filter id="ds"><feDropShadow dx="0" dy="2" stdDeviation="4" flood-opacity="0.06"/></filter>
              </defs>

              <!-- STEP 1 -->
              <rect x="310" y="14" width="340" height="60" rx="0" fill="#fff" stroke="#E4E4E4" filter="url(#ds)"/>
              <rect x="310" y="14" width="340" height="3" fill="#666"/>
              <text x="480" y="38" text-anchor="middle" fill="#999" font-size="9" font-weight="700" letter-spacing="1.5">STEP 1</text>
              <text x="480" y="58" text-anchor="middle" fill="#2d2d2d" font-size="14" font-weight="600">Analyst enters company name</text>

              <line x1="480" y1="74" x2="480" y2="112" stroke="#006492" stroke-width="1.5" marker-end="url(#ah-b)"/>

              <!-- STEP 2 -->
              <rect x="220" y="114" width="520" height="76" rx="0" fill="#fff" stroke="#006492" stroke-width="1.5" filter="url(#ds)"/>
              <rect x="220" y="114" width="520" height="3" fill="#006492"/>
              <text x="250" y="138" fill="#006492" font-size="9" font-weight="700" letter-spacing="1.5">STEP 2 · EXTERNAL</text>
              <text x="250" y="158" fill="#2d2d2d" font-size="14" font-weight="600">Perplexity API → Company Research</text>
              <text x="250" y="178" fill="#999" font-size="11">Returns JSON: profile, financials, procurement org, SWOT</text>
              <rect x="644" y="128" width="80" height="20" rx="0" fill="rgba(0,100,146,0.08)" stroke="rgba(0,100,146,0.25)"/>
              <text x="684" y="142" text-anchor="middle" fill="#006492" font-size="8" font-weight="700" letter-spacing="1">EXTERNAL</text>

              <line x1="480" y1="190" x2="480" y2="228" stroke="#006492" stroke-width="1.5" marker-end="url(#ah-b)"/>

              <!-- STEP 3 -->
              <rect x="260" y="230" width="440" height="70" rx="0" fill="#fff" stroke="#E4E4E4" filter="url(#ds)"/>
              <rect x="260" y="230" width="440" height="3" fill="#006492"/>
              <text x="290" y="254" fill="#006492" font-size="9" font-weight="700" letter-spacing="1.5">STEP 3 · PROCESSING</text>
              <text x="290" y="274" fill="#2d2d2d" font-size="14" font-weight="600">Python normalizes JSON response</text>
              <text x="290" y="290" fill="#999" font-size="11">Validates types, cleans financials, maps sources</text>

              <!-- Split -->
              <line x1="480" y1="300" x2="480" y2="330" stroke="#999" stroke-width="1.5"/>
              <line x1="260" y1="330" x2="700" y2="330" stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
              <line x1="260" y1="330" x2="260" y2="368" stroke="#1B5E5C" stroke-width="1.5" marker-end="url(#ah-t)"/>
              <line x1="700" y1="330" x2="700" y2="368" stroke="#1B5E5C" stroke-width="1.5" marker-end="url(#ah-t)"/>

              <!-- STEP 4A -->
              <rect x="80" y="370" width="360" height="76" rx="0" fill="#fff" stroke="#1B5E5C" stroke-width="1.5" filter="url(#ds)"/>
              <rect x="80" y="370" width="360" height="3" fill="#1B5E5C"/>
              <text x="110" y="394" fill="#1B5E5C" font-size="9" font-weight="700" letter-spacing="1.5">STEP 4A · INTERNAL</text>
              <text x="110" y="414" fill="#2d2d2d" font-size="14" font-weight="600">BX AI → Industry Mapping</text>
              <text x="110" y="434" fill="#999" font-size="11">LLM maps company industry to BXT_L2</text>
              <rect x="350" y="384" width="76" height="20" rx="0" fill="rgba(27,94,92,0.06)" stroke="rgba(27,94,92,0.2)"/>
              <text x="388" y="398" text-anchor="middle" fill="#1B5E5C" font-size="8" font-weight="700" letter-spacing="1">INTERNAL</text>

              <!-- STEP 4B -->
              <rect x="520" y="370" width="360" height="76" rx="0" fill="#fff" stroke="#1B5E5C" stroke-width="1.5" filter="url(#ds)"/>
              <rect x="520" y="370" width="360" height="3" fill="#1B5E5C"/>
              <text x="550" y="394" fill="#1B5E5C" font-size="9" font-weight="700" letter-spacing="1.5">STEP 4B · INTERNAL</text>
              <text x="550" y="414" fill="#2d2d2d" font-size="14" font-weight="600">Snowflake → Salesforce Data</text>
              <text x="550" y="434" fill="#999" font-size="11">Comparables by BXT_L2, revenue, region</text>
              <rect x="790" y="384" width="76" height="20" rx="0" fill="rgba(27,94,92,0.06)" stroke="rgba(27,94,92,0.2)"/>
              <text x="828" y="398" text-anchor="middle" fill="#1B5E5C" font-size="8" font-weight="700" letter-spacing="1">INTERNAL</text>

              <!-- Merge -->
              <line x1="260" y1="446" x2="260" y2="480" stroke="#1B5E5C" stroke-width="1.5"/>
              <line x1="700" y1="446" x2="700" y2="480" stroke="#1B5E5C" stroke-width="1.5"/>
              <line x1="260" y1="480" x2="700" y2="480" stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
              <line x1="480" y1="480" x2="480" y2="518" stroke="#A95228" stroke-width="1.5" marker-end="url(#ah-r)"/>

              <!-- STEP 5 -->
              <rect x="200" y="520" width="560" height="90" rx="0" fill="#fff" stroke="#A95228" stroke-width="1.5" filter="url(#ds)"/>
              <rect x="200" y="520" width="560" height="3" fill="#A95228"/>
              <text x="230" y="546" fill="#A95228" font-size="9" font-weight="700" letter-spacing="1.5">STEP 5 · OUTPUT</text>
              <text x="230" y="566" fill="#2d2d2d" font-size="14" font-weight="600">Cost Savings Estimate &amp; Intelligence Report</text>
              <text x="230" y="586" fill="#999" font-size="11">Conservative / Median / Optimistic projections</text>
              <text x="230" y="601" fill="#999" font-size="11">Company profile, procurement SWOT, risk analysis</text>
              <rect x="660" y="536" width="76" height="20" rx="0" fill="rgba(169,82,40,0.06)" stroke="rgba(169,82,40,0.25)"/>
              <text x="698" y="550" text-anchor="middle" fill="#A95228" font-size="8" font-weight="700" letter-spacing="1">OUTPUT</text>
            </svg>
            ''', unsafe_allow_html=True)

            # ── DATA SOURCES ──
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-label">Data Sources</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="sec-title">Internal vs <em>External</em></h2>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('''<div class="card" style="border-left:3px solid var(--blue);">
                    <h3>External Data</h3>
                    <p style="margin-bottom:16px;">Sourced via Perplexity AI API in real-time for each company search.</p>
                    <div class="irow"><div class="irow-label">Perplexity Output</div><div class="irow-val">Structured JSON with company profile, financials, procurement org, SWOT, risks — each data point includes source quote and URL</div></div>
                </div>''', unsafe_allow_html=True)
            with c2:
                st.markdown('''<div class="card" style="border-left:3px solid var(--teal);">
                    <h3>Internal Data</h3>
                    <p style="margin-bottom:16px;">Proprietary Blackstone data powering benchmarks and projections.</p>
                    <div class="irow"><div class="irow-label">BXT_L2 Mappings</div><div class="irow-val">Proprietary industry classification taxonomy for benchmarking</div></div>
                    <div class="irow"><div class="irow-label">Salesforce Data in Snowflake</div><div class="irow-val">Historical engagement data, comparable companies by industry, revenue, and geography</div></div>
                    <div class="irow"><div class="irow-label">BX AI</div><div class="irow-val">LLM that maps company industry categories to BXT_L2 classifications</div></div>
                </div>''', unsafe_allow_html=True)

    else:
        st.markdown('<div class="notfound"><strong>Company not found</strong><p>Try searching for "Kiewit Corporation" or "Kiewit"</p></div>', unsafe_allow_html=True)
else:
    st.markdown('''<div class="welcome">
        <h2>Search to <em>Begin</em></h2>
        <p>Enter a company name in the search bar to view detailed due diligence, procurement analysis, and cost optimization projections.</p>
        <div class="avail">Available: Kiewit Corporation</div>
        <div class="tip">Hover over underlined values to see source references</div>
    </div>''', unsafe_allow_html=True)

st.markdown('''<div class="dark-footer">
    <span>© 2026 BLACKSTONE INC.</span>
    <span>COMPANY INTELLIGENCE · DUE DILIGENCE · PROCUREMENT ANALYSIS</span>
</div>''', unsafe_allow_html=True)
