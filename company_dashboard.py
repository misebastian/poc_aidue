import streamlit as st
import pandas as pd

st.set_page_config(page_title="Company Intelligence Dashboard", page_icon="🏢", layout="wide", initial_sidebar_state="collapsed")

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

    .stTabs [data-baseweb="tab-list"] { background: var(--bg-card) !important; border: 1.5px solid var(--gray); border-radius: 14px; padding: 5px; gap: 4px; box-shadow: var(--shadow-sm); }
    .stTabs [data-baseweb="tab"] { background: transparent !important; border-radius: 10px !important; padding: 12px 28px !important; font-family: 'JetBrains Mono',monospace !important; font-size: 10px !important; font-weight: 600 !important; letter-spacing: 2px !important; text-transform: uppercase !important; color: var(--text-sec) !important; transition: all 0.3s var(--ease) !important; }
    .stTabs [data-baseweb="tab"]:hover { color: var(--text) !important; background: var(--bg-muted) !important; }
    .stTabs [aria-selected="true"] { background: var(--teal) !important; color: #FFF !important; box-shadow: 0 2px 8px rgba(27,94,92,0.2) !important; }
    .stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"] { display: none !important; }

    .hero { background: var(--bg-card); padding: 36px 48px 32px; margin: -1rem -1rem 0 -1rem; position: relative; overflow: hidden; border-bottom: 1px solid var(--gray); }
    .hero-top { display:flex; align-items:center; gap:10px; margin-bottom:20px; position:relative; z-index:1; }
    .hero-logo { width:26px; height:26px; border-radius:6px; background:var(--teal); display:flex; align-items:center; justify-content:center; }
    .hero-logo::after { content:''; width:8px; height:8px; border:1.5px solid #FFF; border-radius:50%; }
    .hero-label { font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:500; letter-spacing:4px; text-transform:uppercase; color:var(--text-ter); }
    .hero h1 { font-family:'Instrument Serif',serif; font-size:clamp(32px,4.5vw,46px); font-weight:400; line-height:1.05; letter-spacing:-2px; color:var(--text) !important; margin:0; position:relative; z-index:1; }
    .hero h1 em { font-style:italic; color:var(--teal) !important; position:relative; }
    .hero h1 em::after { content:''; position:absolute; bottom:2px; left:0; width:100%; height:2px; background:linear-gradient(90deg,var(--teal),transparent); opacity:0.3; }
    .hero-sub { font-size:14px; font-weight:300; color:var(--text-sec) !important; margin-top:8px; position:relative; z-index:1; }
    .hero-accent-bar { height:3px; margin:0 -1rem; background:linear-gradient(90deg,var(--rust),var(--teal),var(--blue)); }

    .search-hint { font-family:'JetBrains Mono',monospace; font-size:9px; letter-spacing:2.5px; text-transform:uppercase; color:var(--teal) !important; display:flex; align-items:center; gap:10px; margin-bottom:12px; }
    .search-hint::before { content:''; width:24px; height:1.5px; background:var(--teal); }

    .sec-label { font-family:'JetBrains Mono',monospace; font-size:9px; letter-spacing:3px; text-transform:uppercase; color:var(--teal) !important; display:flex; align-items:center; gap:10px; margin-bottom:12px; }
    .sec-label::before { content:''; width:28px; height:1.5px; background:linear-gradient(90deg,var(--teal),transparent); }
    .sec-title { font-family:'Instrument Serif',serif; font-size:clamp(26px,3.5vw,36px); font-weight:400; line-height:1.15; letter-spacing:-1px; color:var(--text) !important; margin-bottom:28px; }
    .sec-title em { font-style:italic; color:var(--teal) !important; }

    .meta-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1px; background:var(--gray); border:1px solid var(--gray); border-radius:var(--r); overflow:hidden; margin-bottom:28px; box-shadow:var(--shadow-sm); }
    .mg-cell { background:var(--bg-card); padding:24px 22px; transition:background 0.3s var(--ease); }
    .mg-cell:hover { background:var(--bg-hover); }
    .mg-label { font-family:'JetBrains Mono',monospace; font-size:8px; letter-spacing:2.5px; text-transform:uppercase; color:var(--text-ter) !important; margin-bottom:8px; }
    .mg-value { font-size:14px; font-weight:600; color:var(--text) !important; line-height:1.4; }

    .card { background:var(--bg-card); border:1px solid var(--gray); border-radius:var(--r); padding:28px 26px; margin-bottom:16px; box-shadow:var(--shadow-sm); transition:all 0.4s var(--ease); position:relative; overflow:hidden; }
    .card:hover { box-shadow:var(--shadow-md); transform:translateY(-2px); }
    .card::after { content:''; position:absolute; top:0; left:0; right:0; height:2px; opacity:0; background:linear-gradient(90deg,transparent,var(--teal),transparent); transition:opacity 0.4s; }
    .card:hover::after { opacity:1; }
    .card h3 { font-family:'Instrument Serif',serif; font-size:20px; font-weight:400; color:var(--text) !important; margin-bottom:12px; }
    .card p { color:var(--text-sec) !important; font-size:14px; font-weight:300; line-height:1.8; }

    .irow { padding:16px 20px; background:var(--bg-card); border:1px solid var(--gray); border-radius:12px; margin-bottom:8px; box-shadow:var(--shadow-sm); transition:all 0.3s var(--ease); }
    .irow:hover { border-color:var(--teal-border); transform:translateX(4px); box-shadow:var(--shadow-md); }
    .irow-label { font-family:'JetBrains Mono',monospace; font-size:8px; letter-spacing:2px; text-transform:uppercase; color:var(--text-ter) !important; margin-bottom:5px; }
    .irow-val { font-size:13.5px; font-weight:400; color:var(--text) !important; line-height:1.6; }

    .badge-wrap { display:flex; flex-wrap:wrap; gap:8px; }
    .bdg { display:inline-flex; padding:6px 14px; border:1px solid var(--teal-border); border-radius:100px; font-family:'JetBrains Mono',monospace; font-size:9px; font-weight:600; letter-spacing:0.5px; text-transform:uppercase; color:var(--teal) !important; background:var(--teal-light); transition:all 0.3s var(--ease); }
    .bdg:hover { background:var(--teal); color:#FFF !important; box-shadow:0 2px 8px rgba(27,94,92,0.2); }

    .met { background:var(--bg-card); border:1px solid var(--gray); border-radius:var(--r); padding:28px 20px; text-align:center; box-shadow:var(--shadow-sm); transition:all 0.4s var(--ease); position:relative; overflow:hidden; }
    .met:hover { transform:translateY(-4px); box-shadow:var(--shadow-lg); }
    .met::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; }
    .met .m-val { font-family:'JetBrains Mono',monospace; font-size:clamp(24px,3vw,36px); font-weight:600; line-height:1; margin:10px 0; }
    .met .m-lbl { font-family:'JetBrains Mono',monospace; font-size:9px; letter-spacing:2px; text-transform:uppercase; color:var(--text-ter) !important; }
    .met-teal::before { background:var(--teal); } .met-teal .m-val { color:var(--teal) !important; }
    .met-rust::before { background:var(--rust); } .met-rust .m-val { color:var(--rust) !important; }
    .met-lime::before { background:var(--lime); } .met-lime .m-val { color:#6B8F14 !important; }
    .met-blue::before { background:var(--blue); } .met-blue .m-val { color:var(--blue) !important; }

    .prog { margin-bottom:16px; }
    .prog-head { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:6px; }
    .prog-name { font-size:13px; color:var(--text) !important; }
    .prog-lvl { font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:600; color:var(--teal) !important; }
    .prog-track { background:var(--gray); border-radius:6px; height:7px; overflow:hidden; }
    .prog-fill { height:100%; border-radius:6px; background:linear-gradient(90deg,var(--teal),var(--blue)); transition:width 0.8s var(--ease); position:relative; }
    .prog-fill::after { content:''; position:absolute; right:0; top:0; bottom:0; width:12px; background:linear-gradient(90deg,transparent,rgba(255,255,255,0.35)); border-radius:0 6px 6px 0; }

    .swot { background:var(--bg-card); border:1px solid var(--gray); border-radius:var(--r); padding:24px 22px; margin-bottom:14px; box-shadow:var(--shadow-sm); position:relative; overflow:hidden; transition:all 0.4s var(--ease); }
    .swot:hover { transform:translateX(3px); box-shadow:var(--shadow-md); }
    .swot::before { content:''; position:absolute; top:0; left:0; width:3px; height:100%; }
    .s-str::before { background:var(--lime); } .s-wk::before { background:var(--tan); } .s-op::before { background:var(--blue); } .s-th::before { background:var(--red); }
    .swot-ttl { font-family:'JetBrains Mono',monospace; font-size:9px; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:14px; }
    .s-str .swot-ttl { color:#6B8F14 !important; } .s-wk .swot-ttl { color:var(--tan) !important; } .s-op .swot-ttl { color:var(--blue) !important; } .s-th .swot-ttl { color:var(--red) !important; }
    .swot ul { list-style:none; padding:0; margin:0; }
    .swot li { font-size:13px; color:var(--text-sec) !important; font-weight:300; line-height:1.7; padding:7px 0; border-bottom:1px solid var(--border); display:flex; align-items:flex-start; gap:8px; }
    .swot li:last-child { border-bottom:none; }
    .swot li::before { content:'→'; flex-shrink:0; margin-top:1px; opacity:0.4; }
    .s-str li::before { color:var(--lime); } .s-wk li::before { color:var(--tan); } .s-op li::before { color:var(--blue); } .s-th li::before { color:var(--red); }

    .abox { padding:18px 22px; border-radius:12px; margin-bottom:10px; border:1px solid var(--gray); background:var(--bg-card); font-size:13px; font-weight:300; color:var(--text-sec) !important; line-height:1.7; box-shadow:var(--shadow-sm); transition:all 0.3s var(--ease); }
    .abox:hover { box-shadow:var(--shadow-md); }
    .a-warn { border-left:3px solid var(--rust); } .a-ok { border-left:3px solid var(--lime); } .a-info { border-left:3px solid var(--blue); }
    .abox strong { color:var(--text) !important; font-weight:600; }

    .ws { position:relative; cursor:pointer; border-bottom:1px dotted var(--text-ter); display:inline; transition:border-color 0.3s; }
    .ws:hover { border-bottom-color:var(--teal); }
    .tt { display:none; position:absolute; background:var(--bg-card); color:var(--text) !important; padding:16px 20px; border-radius:12px; font-size:12px; z-index:9999; max-width:400px; min-width:260px; box-shadow:0 12px 40px rgba(0,0,0,0.15); border:1px solid var(--gray); left:0; top:calc(100% + 8px); line-height:1.6; }
    .tt::before { content:""; position:absolute; top:-12px; left:0; right:0; height:16px; background:transparent; }
    .ws:hover .tt, .tt:hover { display:block; }
    .tt strong { color:var(--teal) !important; } .tt a { color:var(--rust) !important; text-decoration:underline; font-weight:600; }
    .tt-q { font-style:italic; color:var(--text-sec) !important; margin:6px 0; padding-left:10px; border-left:2px solid var(--teal); font-size:11px; }

    .crit-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1px; background:var(--gray); border:1px solid var(--gray); border-radius:var(--r); overflow:hidden; margin:20px 0; box-shadow:var(--shadow-sm); }
    .crit-cell { background:var(--bg-card); padding:22px 20px; transition:background 0.3s; }
    .crit-cell:hover { background:var(--bg-hover); }
    .crit-lbl { font-family:'JetBrains Mono',monospace; font-size:8px; letter-spacing:2px; text-transform:uppercase; color:var(--text-ter) !important; margin-bottom:6px; }
    .crit-val { font-size:15px; font-weight:600; color:var(--text) !important; margin-bottom:4px; }
    .crit-st { font-family:'JetBrains Mono',monospace; font-size:10px; }

    .map-flow { display:flex; align-items:center; gap:0; flex-wrap:wrap; margin:20px 0; }
    .map-node { background:var(--bg-card); border:1px solid var(--gray); border-radius:12px; padding:16px 18px; flex:1; min-width:160px; box-shadow:var(--shadow-sm); transition:all 0.3s var(--ease); }
    .map-node:hover { box-shadow:var(--shadow-md); border-color:var(--teal-border); }
    .map-node.hl { border-color:var(--teal); background:var(--teal-light); }
    .map-lbl { font-family:'JetBrains Mono',monospace; font-size:8px; letter-spacing:2.5px; text-transform:uppercase; color:var(--text-ter) !important; margin-bottom:5px; }
    .map-val { font-size:13px; font-weight:500; color:var(--text) !important; line-height:1.4; }
    .map-node.hl .map-val { color:var(--teal) !important; font-family:'JetBrains Mono',monospace; font-size:18px; font-weight:700; }
    .map-arrow { font-size:16px; color:var(--text-ter); padding:0 10px; flex-shrink:0; opacity:0.3; }

    .divider { height:1px; margin:36px 0; background:linear-gradient(90deg,transparent,var(--gray),transparent); }
    .slider-lbl { font-family:'JetBrains Mono',monospace; font-size:9px; letter-spacing:2px; text-transform:uppercase; color:var(--text-sec) !important; margin-bottom:10px; }
    .dark-footer { padding:28px 0; border-top:1px solid var(--gray); margin-top:48px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; }
    .dark-footer span { font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--text-ter) !important; letter-spacing:1.5px; }

    .welcome { background:var(--bg-card); border:1px solid var(--gray); border-radius:16px; padding:72px 44px; text-align:center; box-shadow:var(--shadow-md); position:relative; overflow:hidden; }
    .welcome::before { content:''; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:400px; height:400px; background:radial-gradient(circle,var(--teal-light) 0%,transparent 60%); pointer-events:none; }
    .welcome h2 { font-family:'Instrument Serif',serif; font-size:clamp(26px,4vw,40px); font-weight:400; letter-spacing:-1px; color:var(--text) !important; position:relative; margin-bottom:14px; }
    .welcome h2 em { font-style:italic; color:var(--teal) !important; }
    .welcome p { color:var(--text-sec) !important; font-size:15px; font-weight:300; position:relative; line-height:1.7; max-width:480px; margin:0 auto; }
    .welcome .avail { display:inline-flex; align-items:center; gap:8px; padding:6px 16px; margin-top:28px; border:1px solid var(--teal-border); border-radius:100px; font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:600; color:var(--teal) !important; background:var(--teal-light); position:relative; }
    .welcome .avail::before { content:''; width:6px; height:6px; border-radius:50%; background:var(--teal); animation:pulse 2.5s ease-in-out infinite; box-shadow:0 0 6px var(--teal); }
    @keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.2;} }
    .welcome .tip { margin-top:20px; font-family:'JetBrains Mono',monospace; font-size:9px; letter-spacing:2px; text-transform:uppercase; color:var(--text-ter) !important; position:relative; }
    .notfound { background:var(--bg-card); border:1px solid var(--gray); border-left:3px solid var(--rust); border-radius:12px; padding:28px; text-align:center; box-shadow:var(--shadow-sm); }
    .notfound strong { color:var(--rust) !important; } .notfound p { color:var(--text-sec) !important; margin-top:6px; }

    @media (max-width:768px) { .meta-grid{grid-template-columns:repeat(2,1fr);} .crit-grid{grid-template-columns:1fr;} .map-flow{flex-direction:column;align-items:stretch;} .map-arrow{transform:rotate(90deg);text-align:center;padding:4px 0;} }
</style>
""", unsafe_allow_html=True)

BXT_L2_SAVINGS = {"Engineering, architecture and construction management": 0.02371, "Heavy Construction & Engineering": 0.045, "General Contractors": 0.038, "Oil & Gas": 0.048, "Mining": 0.041, "Default": 0.04}

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
            "primary_industry": {"value": "Engineering, Procurement and Construction (EPC) services", "quote": "The EPC model streamlines execution with a single contractor managing design, procurement and construction.", "source_url": "https://www.kiewit.com/services-and-solutions/project-delivery/"},
            "primary_markets": [
                {"value": "Transportation", "quote": "Kiewit offers construction and engineering services in transportation.", "source_url": "https://www.linkedin.com/company/kiewit"},
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
        "workforce": {"total_employees": {"value": 31800, "quote": "16.8 BILLION 31,800 EMPLOYEES 2024 REVENUE 2024 EMPLOYEES", "source_url": "https://www.kiewit.com/wp-content/uploads/2025/09/EN_2024-Sustainability-Report-reduced.pdf"}},
        "financials": {"revenue_2024": {"value": 16.8, "quote": "Proven Results. $16.8B 2024 Revenues 31,800 Craft and Staff Employees", "source_url": "https://www.kiewit.com"}, "source_note": "Private company – estimates only; no official statutory filings."},
        "ownership_structure": {"ownership_type": {"value": "Privately held, employee-owned organization", "quote": "Kiewit's diversified services and unique network of decentralized offices — backed by a multi-billion-dollar, employee-owned organization.", "source_url": "https://www.kiewit.com/about-us/"}},
        "procurement_organization": {
            "overall_maturity_level": {"value": "Defined to Managed", "quote": "At Kiewit, supply chain is integrated into project planning from the very beginning.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
            "maturity_dimensions": {
                "Governance & Org": {"value": "Managed", "score": 4, "quote": "Material procurement can account for up to 50% of total installed costs.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                "Process & Policy": {"value": "Defined", "score": 3, "quote": "At Kiewit, supply chain is integrated into project planning from the very beginning.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                "Technology & Data": {"value": "Defined", "score": 3, "quote": "Our procurement and supply chain experts leverage scale, strategy and technology.", "source_url": "https://www.kiewit.com/?lang=en-ca"},
                "Supplier Management": {"value": "Defined", "score": 3, "quote": "The worst thing a vendor can do is hide a problem. If we know early, we can help.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                "Integration Lifecycle": {"value": "Managed", "score": 4, "quote": "Supply chain is integrated into project planning from the very beginning. We help define risk and create the roadmap.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
            },
            "structure": {"value": "Supply chain sits between engineering and construction, ensuring materials arrive on time to support EPC execution.", "quote": "We sit between engineering and construction. Our job is to make sure materials arrive when construction needs them.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
            "category_mgmt": {"value": "Procurement organized around categories with specialists owning domains such as valves or piping.", "quote": "He's reorganized his team around procurement categories — giving specialists ownership over specific domains.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
            "cpo": {"value": "Carsten Bernstiel — VP Procurement, OGC group", "quote": "At the center is Carsten Bernstiel, Vice President of Procurement for Kiewit's Oil, Gas & Chemical group.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
        },
        "procurement_risks": {
            "key_risks": [
                {"value": "High share of total installed cost tied to materials, exposing projects to price and availability risks", "quote": "Material procurement can account for up to 50% of total installed costs.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                {"value": "Global shipping and logistics disruptions impacting lead times", "quote": "We rerouted shipments through Los Angeles and handled final delivery by train and truck.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                {"value": "Dependence on timely, transparent supplier communication to resolve issues early", "quote": "The worst thing a vendor can do is hide a problem. If we know early, we can help.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
            ],
            "mitigation": {"value": "Kiewit mitigates risk through early involvement in strategy, proactive planning, logistics rerouting, and transparent supplier communication.", "quote": "We rerouted shipments through Los Angeles and handled final delivery by train and truck.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
        },
        "procurement_swot": {
            "strengths": [
                {"value": "Integrated EPC model with single contractor managing design, procurement and construction", "quote": "The EPC model streamlines execution with a single contractor managing design, procurement and construction.", "source_url": "https://www.kiewit.com/services-and-solutions/project-delivery/"},
                {"value": "Supply chain integrated from start of project planning, defining risk and delivery roadmap", "quote": "At Kiewit, supply chain is integrated into project planning from the very beginning.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                {"value": "Category-based procurement with domain specialists emphasizing partnership and transparency", "quote": "He's reorganized his team around procurement categories.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
            ],
            "weaknesses": [
                {"value": "Limited public transparency on procurement systems, KPIs and ESG vs listed peers", "quote": "Kiewit is one of North America's largest and most respected construction and engineering organizations.", "source_url": "https://www.kiewit.com/about-us/"},
                {"value": "Advanced procurement evidence concentrated in OGC group — maturity may be uneven across markets", "quote": "Carsten Bernstiel, Vice President of Procurement for Kiewit's Oil, Gas & Chemical group.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
            ],
            "opportunities": [
                {"value": "Deepening AI/technology in procurement to anticipate disruptions and optimize sourcing", "quote": "This consultative role has transformed EPCs into partners — not just vendors.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                {"value": "Increasing ESG and supplier diversity visibility for client/regulatory alignment", "quote": "Kiewit has a long history of partnering with the local business community.", "source_url": "https://www.kiewit.com/business-with-us/opportunities/central-florida-projects/"},
                {"value": "Extending OGC-style category management across all markets", "quote": "He's reorganized his team around procurement categories.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
            ],
            "threats": [
                {"value": "Materials up to 50% of installed cost — high exposure to commodity/logistics shocks", "quote": "Material procurement can account for up to 50% of total installed costs.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                {"value": "Canal congestion and global shipping adding weeks to lead times", "quote": "We rerouted shipments through Los Angeles and handled final delivery by train and truck.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                {"value": "Competitors investing aggressively in digital procurement and ESG branding", "quote": "The EPC model streamlines execution with a single contractor.", "source_url": "https://www.kiewit.com/services-and-solutions/project-delivery/"}
            ]
        },
        "industry_mapping": {"original_industry": "Engineering, Procurement and Construction (EPC) services", "bxt_l2": "Engineering, architecture and construction management", "median_projected_savings_rate": 0.02371}
    }
}

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

# ═══ HEADER ═══
st.markdown('''<div class="hero">
    <div class="hero-top"><div class="hero-logo"></div><span class="hero-label">Intelligence Platform</span></div>
    <h1>Company<br><em>Intelligence</em></h1>
    <p class="hero-sub">Due Diligence & Procurement Analysis</p>
</div><div class="hero-accent-bar"></div>''', unsafe_allow_html=True)

st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="search-hint">Search Company</div>', unsafe_allow_html=True)
    search = st.text_input("s", placeholder="Enter company name (e.g., Kiewit Corporation)", label_visibility="collapsed")

if search:
    co = get_company_data(search)
    if co:
        tab1, tab2 = st.tabs(["GENERAL INFO", "FINANCIALS & COST OPTIMIZATION"])
        with tab1:
            st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
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
            st.markdown('<div class="sec-label">Primary Markets</div>', unsafe_allow_html=True)
            mkts="".join([f'<span class="bdg">{m_["value"]}</span>' for m_ in ov["primary_markets"]])
            st.markdown(f'<div class="card"><div class="badge-wrap">{mkts}</div></div>', unsafe_allow_html=True)

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
            st.markdown('<h2 class="sec-title">Procurement <em>Risks</em></h2>', unsafe_allow_html=True)
            for risk in co["procurement_risks"]["key_risks"]:
                st.markdown(f'<div class="abox a-warn">{src(risk["value"],risk["quote"],risk["source_url"])}</div>', unsafe_allow_html=True)
            mit=co["procurement_risks"]["mitigation"]
            st.markdown(f'<div class="abox a-ok"><strong>Risk Mitigation</strong><br><br>{src(mit["value"],mit["quote"],mit["source_url"])}</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-label">Financials</div>', unsafe_allow_html=True)
            st.markdown('<h2 class="sec-title">Financial <em>Overview</em></h2>', unsafe_allow_html=True)
            r24=co['financials']['revenue_2024']; emp=co['workforce']['total_employees']
            c1,c2,c3=st.columns(3)
            with c1:
                r24v = r24["value"]; r24q = r24["quote"]; r24u = r24["source_url"]
                st.markdown(f'<div class="met met-teal"><div class="m-lbl">2024 Revenue</div><div class="m-val">{src(f"${r24v}B",r24q,r24u)}</div><div class="m-lbl">USD</div></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="met met-blue"><div class="m-lbl">Geographic Scope</div><div class="m-val">{co["operational_footprint"]["geographic_scope"]}</div><div class="m-lbl">Region</div></div>', unsafe_allow_html=True)
            with c3:
                empv = emp["value"]; empq = emp["quote"]; empu = emp["source_url"]
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
    else:
        st.markdown('<div class="notfound"><strong>Company not found</strong><p>Try searching for "Kiewit Corporation" or "Kiewit"</p></div>', unsafe_allow_html=True)
else:
    st.markdown('''<div class="welcome">
        <h2>Company <em>Intelligence</em></h2>
        <p>Enter a company name in the search bar to view detailed due diligence, procurement analysis, and cost optimization projections.</p>
        <div class="avail">Kiewit Corporation</div>
        <div class="tip">Hover over underlined values to see source references</div>
    </div>''', unsafe_allow_html=True)

st.markdown('<div class="dark-footer"><span>COMPANY INTELLIGENCE DASHBOARD © 2025</span><span>DUE DILIGENCE · PROCUREMENT ANALYSIS · COST OPTIMIZATION</span></div>', unsafe_allow_html=True)


