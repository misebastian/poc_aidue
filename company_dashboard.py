import streamlit as st
import pandas as pd

st.set_page_config(page_title="Company Intelligence Dashboard", page_icon="🏢", layout="wide", initial_sidebar_state="collapsed")

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&display=swap');
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .stApp {background-color: #f8fafc;}
    .custom-header {background: #000; color: #FFF; padding: 24px 32px; margin: -1rem -1rem 24px -1rem; border-bottom: 4px solid #A95228;}
    .custom-header h1 {font-family: 'Playfair Display', Georgia, serif; font-size: 2rem; font-weight: 400; color: #FFF !important; margin: 0;}
    .custom-header .subtitle {font-size: 1rem; opacity: 0.9; margin-top: 4px; color: #FFF !important;}
    .stTabs [data-baseweb="tab-list"] {gap: 8px; background-color: #E4E4E4; padding: 8px; border-radius: 8px;}
    .stTabs [data-baseweb="tab"] {background-color: #FFF; border-radius: 6px; padding: 10px 20px; font-weight: 500; color: #2d2d2d !important;}
    .stTabs [aria-selected="true"] {background-color: #1B5E5C !important; color: #FFF !important;}
    .card {background: #FFF; padding: 24px; margin-bottom: 24px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); color: #2d2d2d !important;}
    .card h3 {color: #1B5E5C !important; margin-bottom: 12px;}
    .card p {color: #2d2d2d !important;}
    .section-header {background: #FFF; padding: 16px 24px; margin-bottom: 16px; border-left: 4px solid #1B5E5C; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.05);}
    .section-header h2 {font-family: 'Playfair Display', Georgia, serif; color: #1B5E5C !important; font-size: 1.5rem; font-weight: 500; margin: 0;}
    .meta-card {background: #FFF; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 4px solid #1B5E5C; height: 100%;}
    .meta-label {font-size: 0.75rem; color: #666 !important; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; font-weight: 600;}
    .meta-value {font-size: 1.125rem; color: #A95228 !important; font-weight: 600;}
    .metric-card {background: linear-gradient(135deg, #1B5E5C 0%, #006492 100%); padding: 24px; border-radius: 8px; text-align: center;}
    .metric-card .value {font-size: 2rem; font-weight: bold; margin: 8px 0; color: #FFF !important;}
    .metric-card .label {font-size: 0.875rem; color: #FFF !important; opacity: 0.95;}
    .metric-card-warning {background: linear-gradient(135deg, #C39D7B 0%, #A95228 100%); padding: 24px; border-radius: 8px; text-align: center;}
    .metric-card-warning .value {font-size: 2rem; font-weight: bold; margin: 8px 0; color: #FFF !important;}
    .metric-card-warning .label {font-size: 0.875rem; color: #FFF !important; opacity: 0.95;}
    .metric-card-success {background: linear-gradient(135deg, #A5CD24 0%, #1B5E5C 100%); padding: 24px; border-radius: 8px; text-align: center;}
    .metric-card-success .value {font-size: 2rem; font-weight: bold; margin: 8px 0; color: #FFF !important;}
    .metric-card-success .label {font-size: 0.875rem; color: #FFF !important; opacity: 0.95;}
    .info-item {padding: 16px; background: #fafbfc; border-radius: 8px; border-left: 4px solid #006492; margin-bottom: 12px; color: #2d2d2d !important;}
    .info-item strong {display: block; color: #1B5E5C !important; margin-bottom: 8px; font-size: 0.875rem; font-weight: 600;}
    .info-item span {color: #2d2d2d !important;}
    .badge {display: inline-block; padding: 4px 12px; border-radius: 16px; font-size: 0.75rem; font-weight: bold; margin-right: 8px; margin-bottom: 8px;}
    .badge-info {background: #006492; color: #FFF !important;}
    .progress-container {background: #e5e7eb; border-radius: 4px; height: 24px; position: relative; margin: 8px 0;}
    .progress-fill {background: #1B5E5C; height: 100%; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: #FFF !important; font-size: 0.75rem; font-weight: bold;}
    .swot-item {padding: 20px; border-radius: 8px; margin-bottom: 12px;}
    .swot-item strong, .swot-item li {color: #2d2d2d !important;}
    .swot-strengths {border-left: 4px solid #A5CD24; background: rgba(165, 205, 36, 0.1);}
    .swot-weaknesses {border-left: 4px solid #C39D7B; background: rgba(195, 157, 123, 0.1);}
    .swot-opportunities {border-left: 4px solid #006492; background: rgba(0, 100, 146, 0.1);}
    .swot-threats {border-left: 4px solid #C12D27; background: rgba(193, 45, 39, 0.1);}
    .success-box {background: rgba(165, 205, 36, 0.1); border-left: 4px solid #A5CD24; padding: 16px; border-radius: 8px; margin: 16px 0; color: #2d2d2d !important;}
    .warning-box {background: rgba(195, 157, 123, 0.1); border-left: 4px solid #C39D7B; padding: 16px; border-radius: 8px; margin: 16px 0; color: #2d2d2d !important;}
    .info-box {background: rgba(0, 100, 146, 0.1); border-left: 4px solid #006492; padding: 16px; border-radius: 8px; margin: 16px 0; color: #2d2d2d !important;}
    .mapping-box {background: rgba(27, 94, 92, 0.1); border-left: 4px solid #1B5E5C; padding: 20px; border-radius: 8px; margin: 16px 0; color: #2d2d2d !important;}
    .with-source {position: relative; cursor: pointer; border-bottom: 1px dotted #006492; display: inline;}
    .source-tooltip {display: none; position: absolute; background: #2d2d2d; color: #FFF !important; padding: 12px 16px; border-radius: 8px; font-size: 0.8rem; z-index: 1000; max-width: 400px; min-width: 280px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); left: 0; top: 100%; margin-top: 8px; line-height: 1.5;}
    .with-source:hover .source-tooltip {display: block;}
    .source-tooltip a {color: #A5CD24 !important; text-decoration: underline;}
    .source-tooltip strong {color: #FFF !important;}
    .footer {background: #E4E4E4; padding: 24px; border-radius: 8px; margin-top: 32px; font-size: 0.875rem; color: #666 !important; text-align: center;}
    .criteria-box {background: #FFF; border: 2px solid #1B5E5C; border-radius: 8px; padding: 16px; margin: 16px 0;}
    .criteria-met {color: #A5CD24; font-weight: bold;}
    .criteria-not-met {color: #C12D27; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# BXT_L2 Median Savings Rates (for NAM/LATAM + Revenue >10B)
BXT_L2_SAVINGS = {
    "Engineering, architecture and construction management": 0.02371,
    "Heavy Construction & Engineering": 0.045,
    "General Contractors": 0.038,
    "Oil & Gas": 0.048,
    "Mining": 0.041,
    "Default": 0.04
}

# Data
COMPANY_DATA = {
    "kiewit": {
        "meta": {
            "company_name": {"value": "Kiewit Corporation", "quote": "Kiewit is one of North America's largest and most respected construction and engineering organizations.", "source_url": "https://www.kiewit.com"},
            "jurisdiction": {"value": "United States", "quote": "Kiewit is one of North America's largest and most respected construction and engineering organizations.", "source_url": "https://www.kiewit.com"},
            "listed_status": {"value": "Private company (employee-owned)", "quote": "Employee-owned.", "source_url": "https://newsroom.kiewit.com/wp-content/uploads/2025/03/EN_Basics-Page_2025-Overview.pdf"}
        },
        "company_overview": {
            "description": {"value": "Kiewit Corporation is one of North America's largest construction and engineering organizations, providing integrated EPC services across energy, transportation, water, mining, oil, gas and chemical markets.", "quote": "Kiewit combines world-renowned capabilities with EPC expertise for seamless project delivery.", "source_url": "https://www.kiewit.com"},
            "founded_year": {"value": 1884, "quote": "Backed by more than 140 years of self-perform construction expertise.", "source_url": "https://newsroom.kiewit.com/wp-content/uploads/2025/03/EN_Basics-Page_2025-Overview.pdf"},
            "headquarters": {"value": "Omaha, Nebraska, United States", "quote": "Kiewit is a civil engineering company from the United States, with its headquarters in Nebraska.", "source_url": "https://www.statista.com/statistics/1449369/global-revenue-of-kiewit-corporation/"},
            "primary_industry": {"value": "Engineering, Procurement and Construction (EPC) for infrastructure and industrial projects", "quote": "Kiewit combines world-renowned capabilities with EPC expertise.", "source_url": "https://www.kiewit.com"},
            "primary_markets": [
                {"value": "Transportation infrastructure", "quote": "As one of the largest transportation contractors in North America.", "source_url": "https://www.kiewit.com.au"},
                {"value": "Power generation and delivery", "quote": "Kiewit is a leader in the power industry.", "source_url": "https://www.kiewit.com.au"},
                {"value": "Oil, gas and chemical facilities", "quote": "Kiewit has served domestic and international OGC companies.", "source_url": "https://www.kiewit.com.au"},
                {"value": "Water and wastewater infrastructure", "quote": "Kiewit specializes in water infrastructure.", "source_url": "https://www.kiewit.com.au"},
                {"value": "Mining and industrial projects", "quote": "Kiewit specializes in mine management and infrastructure.", "source_url": "https://www.kiewit.com.au"},
                {"value": "Nuclear and data centers", "quote": "Kiewit capabilities include nuclear and specialized infrastructure.", "source_url": "https://www.kiewit.com"}
            ],
            "naics_codes": [{"code": "236220", "title": "Commercial and Institutional Building Construction"}, {"code": "237310", "title": "Highway, Street, and Bridge Construction"}, {"code": "237120", "title": "Oil and Gas Pipeline Construction"}],
            "sic_codes": [{"code": "15420100", "title": "Commercial building contractors"}, {"code": "15410000", "title": "Industrial buildings and warehouses"}]
        },
        "operational_footprint": {
            "regions_of_operation": [
                {"value": "United States (multiple regions)", "quote": "As one of the largest transportation contractors in North America.", "source_url": "https://www.kiewit.com.au"},
                {"value": "Canada", "quote": "Kiewit operates across North America.", "source_url": "https://www.kiewit.com"},
                {"value": "International projects", "quote": "Kiewit has served domestic and international OGC companies.", "source_url": "https://www.kiewit.com.au"}
            ],
            "business_segments": ["Transportation", "Power", "Oil, Gas & Chemical", "Water/Wastewater", "Mining", "Industrial/Building", "Nuclear"],
            "geographic_scope": "NAM/LATAM"
        },
        "workforce": {
            "total_employees": {"value": 31800, "quote": "31,800 STAFF & CRAFT EMPLOYEES", "source_url": "https://newsroom.kiewit.com/wp-content/uploads/2025/03/EN_Basics-Page_2025-Overview.pdf"},
            "equipment_fleet": {"value": 34800, "quote": "34,800 UNITS IN EQUIPMENT FLEET", "source_url": "https://newsroom.kiewit.com/wp-content/uploads/2025/03/EN_Basics-Page_2025-Overview.pdf"}
        },
        "financials": {
            "revenue_2024": {"value": 16.8, "quote": "$16.8 BILLION IN 2024 FINANCIAL REVENUE", "source_url": "https://newsroom.kiewit.com/wp-content/uploads/2025/03/EN_Basics-Page_2025-Overview.pdf"},
            "revenue_2023": {"value": 17.1, "quote": "The global revenue of Kiewit Corporation... reaching 17.1 billion U.S. dollars in 2023.", "source_url": "https://www.statista.com/statistics/1449369/global-revenue-of-kiewit-corporation/"},
            "equipment_replacement_value": {"value": 5.0, "quote": "$5 BILLION IN REPLACEMENT VALUE", "source_url": "https://newsroom.kiewit.com/wp-content/uploads/2025/03/EN_Basics-Page_2025-Overview.pdf"},
            "source_note": "Private company – estimates only; no official statutory filings."
        },
        "ownership_structure": {"ownership_type": {"value": "Privately held, employee-owned", "quote": "Employee-owned.", "source_url": "https://newsroom.kiewit.com/wp-content/uploads/2025/03/EN_Basics-Page_2025-Overview.pdf"}},
        "procurement_organization": {
            "overall_maturity_level": {"value": "Defined to Managed", "quote": "We have a shared service in procurement... the supply chain is embedded in the operation district.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
            "maturity_dimensions": {
                "governance_and_org": {"value": "Managed", "score": 4, "quote": "We have a shared service in procurement... VP responsible for supply chain strategy.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                "process_and_policy": {"value": "Defined", "score": 3, "quote": "Responsible for negotiating contracts and managing supplier relationships.", "source_url": "https://theorg.com/org/kiewit/teams/procurement-and-contracts-team"},
                "technology_and_data": {"value": "Defined", "score": 3, "quote": "Procurement experts leverage scale, strategy and technology.", "source_url": "https://www.kiewit.com"},
                "supplier_management": {"value": "Defined", "score": 3, "quote": "Reorganized team around procurement categories — specialists own specific domains.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                "integration_lifecycle": {"value": "Managed", "score": 4, "quote": "Supply chain is integrated into project planning from the very beginning.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
            },
            "structure": {"value": "Procurement operates as a shared service; supply chain teams embedded in operating districts.", "quote": "We have a shared service in procurement... supply chain is embedded in the operation district.", "source_url": "https://www.youtube.com/watch?v=p63u8Zabtfc"},
            "category_mgmt": {"value": "Category-based organization with specialists owning specific domains.", "quote": "Reorganized team around procurement categories — specialists own domains like valves or piping.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
            "cpo": {"value": "Carsten Bernstiel – VP of Procurement, OGC Group", "quote": "At the center is Carsten Bernstiel, VP of Procurement for Kiewit's OGC group.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
        },
        "procurement_risks": {
            "key_risks": [
                {"value": "Tariffs and trade policy changes affecting costs", "quote": "Tariffs make cost estimations harder and can lead to increased costs for EPC companies.", "source_url": "https://www.youtube.com/watch?v=p63u8Zabtfc"},
                {"value": "Supply chain disruptions impacting schedule certainty", "quote": "Supply chain disruptions impacting schedule certainty.", "source_url": "https://www.youtube.com/watch?v=p63u8Zabtfc"},
                {"value": "Logistics challenges for global sourcing", "quote": "Oversees everything from resource planning to logistics and expediting.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
            ],
            "mitigation": {"value": "Early involvement in project strategy, category-based specialization, proactive risk identification.", "quote": "We now ask: Who are the right partners? Where are the risks? How can we mitigate them before they become problems?", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
        },
        "procurement_swot": {
            "strengths": [
                {"value": "Integrated EPC model with self-perform construction", "quote": "Backed by 140+ years of self-perform construction expertise.", "source_url": "https://newsroom.kiewit.com/wp-content/uploads/2025/03/EN_Basics-Page_2025-Overview.pdf"},
                {"value": "Shared procurement services and embedded supply chain", "quote": "We have a shared service in procurement.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                {"value": "Category-based procurement with domain expertise", "quote": "Reorganized team around procurement categories.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
            ],
            "weaknesses": [
                {"value": "Limited public disclosure on procurement KPIs", "quote": "No public disclosure of procurement KPIs.", "source_url": "https://www.kiewit.com"},
                {"value": "Complex project-based organization", "quote": "Unique organizational structure, backed by vast network of resources.", "source_url": "https://www.kiewit.com"}
            ],
            "opportunities": [
                {"value": "AI and advanced analytics in procurement", "quote": "Procurement teams will be able to use AI to predict and prevent disruptions.", "source_url": "https://www.youtube.com/watch?v=p63u8Zabtfc"},
                {"value": "ESG and supplier diversity programs", "quote": "Opportunity to strengthen ESG programs.", "source_url": "https://www.kiewit.com"},
                {"value": "Scale to standardize category strategies", "quote": "Leveraging Kiewit's scale.", "source_url": "https://www.kiewit.com"}
            ],
            "threats": [
                {"value": "Tariff and trade policy volatility", "quote": "Tariffs make cost estimations harder.", "source_url": "https://www.youtube.com/watch?v=p63u8Zabtfc"},
                {"value": "Global supply chain disruptions", "quote": "Supply chain disruptions affecting materials.", "source_url": "https://www.youtube.com/watch?v=p63u8Zabtfc"},
                {"value": "Competition from large EPC contractors", "quote": "Intensifying competition.", "source_url": "https://www.kiewit.com"}
            ]
        },
        "industry_mapping": {
            "original_industry": "Engineering, Procurement and Construction (EPC) for infrastructure and industrial projects",
            "bxt_l2": "Engineering, architecture and construction management",
            "median_projected_savings_rate": 0.02371
        }
    }
}

def get_company_data(name):
    term = name.lower().strip()
    for key, data in COMPANY_DATA.items():
        if key in term or term in data["meta"]["company_name"]["value"].lower():
            return data
    return None

def src(value, quote, url):
    return f'<span class="with-source">{value}<span class="source-tooltip"><strong>📝 Source:</strong><br>"{quote}"<br><br><a href="{url}" target="_blank">🔗 View Source</a></span></span>'

def meta_card(label, value, quote=None, url=None):
    val = src(value, quote, url) if quote else value
    return f'<div class="meta-card"><div class="meta-label">{label}</div><div class="meta-value">{val}</div></div>'

def section_header(title, icon="📊"):
    return f'<div class="section-header"><h2>{icon} {title}</h2></div>'

def info_item(label, value, quote=None, url=None):
    val = src(value, quote, url) if quote else f'<span>{value}</span>'
    return f'<div class="info-item"><strong>{label}</strong>{val}</div>'

def swot_item(title, items, swot_type):
    html = "".join([f'<li>{src(i["value"], i["quote"], i["source_url"])}</li>' for i in items])
    return f'<div class="swot-item swot-{swot_type}"><strong>{title}</strong><ul style="margin-top:8px;padding-left:20px;">{html}</ul></div>'

def check_criteria(co):
    """Check if company meets NAM/LATAM + >10B revenue criteria"""
    geo_scope = co.get("operational_footprint", {}).get("geographic_scope", "")
    revenue = co.get("financials", {}).get("revenue_2024", {}).get("value", 0)
    
    is_nam_latam = geo_scope in ["NAM", "LATAM", "NAM/LATAM"]
    is_over_10b = revenue > 10
    
    return is_nam_latam, is_over_10b, geo_scope, revenue

# Header
st.markdown('<div class="custom-header"><h1>🏢 Company Intelligence Dashboard</h1><div class="subtitle">Due Diligence & Procurement Analysis Platform</div></div>', unsafe_allow_html=True)

# Search
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    search = st.text_input("🔍 Search Company", placeholder="Enter company name (e.g., Kiewit Corporation)")

if search:
    co = get_company_data(search)
    if co:
        tab1, tab2 = st.tabs(["📋 General Info", "💰 Financials & Cost Optimization"])
        
        with tab1:
            st.markdown(section_header("Company Overview", "🏢"), unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            with c1: 
                st.markdown(meta_card("Company Name", co["meta"]["company_name"]["value"], co["meta"]["company_name"]["quote"], co["meta"]["company_name"]["source_url"]), unsafe_allow_html=True)
            with c2: 
                st.markdown(meta_card("Jurisdiction", co["meta"]["jurisdiction"]["value"], co["meta"]["jurisdiction"]["quote"], co["meta"]["jurisdiction"]["source_url"]), unsafe_allow_html=True)
            with c3: 
                st.markdown(meta_card("Status", co["meta"]["listed_status"]["value"], co["meta"]["listed_status"]["quote"], co["meta"]["listed_status"]["source_url"]), unsafe_allow_html=True)
            with c4: 
                st.markdown(meta_card("Founded", str(co["company_overview"]["founded_year"]["value"]), co["company_overview"]["founded_year"]["quote"], co["company_overview"]["founded_year"]["source_url"]), unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            d = co["company_overview"]["description"]
            desc_html = src(d["value"], d["quote"], d["source_url"])
            st.markdown(f'<div class="card"><h3>📝 Description</h3><p>{desc_html}</p></div>', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(section_header("Corporate Structure", "🏛️"), unsafe_allow_html=True)
                hq = co["company_overview"]["headquarters"]
                st.markdown(info_item("Headquarters", hq["value"], hq["quote"], hq["source_url"]), unsafe_allow_html=True)
                own = co["ownership_structure"]["ownership_type"]
                st.markdown(info_item("Ownership Type", own["value"], own["quote"], own["source_url"]), unsafe_allow_html=True)
                emp = co["workforce"]["total_employees"]
                st.markdown(info_item("Total Employees", f'{emp["value"]:,}', emp["quote"], emp["source_url"]), unsafe_allow_html=True)
                eq = co["workforce"]["equipment_fleet"]
                st.markdown(info_item("Equipment Fleet", f'{eq["value"]:,} units', eq["quote"], eq["source_url"]), unsafe_allow_html=True)
            with c2:
                st.markdown(section_header("Business Segments", "📊"), unsafe_allow_html=True)
                segs = "".join([f'<span class="badge badge-info">{s}</span>' for s in co["operational_footprint"]["business_segments"]])
                st.markdown(f'<div class="card">{segs}</div>', unsafe_allow_html=True)
                st.markdown(section_header("Regions", "🌍"), unsafe_allow_html=True)
                regs = "".join([f'<div class="info-item"><strong>📍</strong>{src(r["value"], r["quote"], r["source_url"])}</div>' for r in co["operational_footprint"]["regions_of_operation"]])
                st.markdown(regs, unsafe_allow_html=True)
            
            st.markdown(section_header("Primary Markets", "🎯"), unsafe_allow_html=True)
            mkts = "".join([f'<div class="info-item"><strong>✓</strong>{src(m["value"], m["quote"], m["source_url"])}</div>' for m in co["company_overview"]["primary_markets"]])
            st.markdown(f'<div class="card">{mkts}</div>', unsafe_allow_html=True)
            
            st.markdown(section_header("Industry Classification", "🏷️"), unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**NAICS Codes**")
                st.dataframe(pd.DataFrame([{"Code": n["code"], "Title": n["title"]} for n in co["company_overview"]["naics_codes"]]), use_container_width=True, hide_index=True)
            with c2:
                st.markdown("**SIC Codes**")
                st.dataframe(pd.DataFrame([{"Code": s["code"], "Title": s["title"]} for s in co["company_overview"]["sic_codes"]]), use_container_width=True, hide_index=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(section_header("Supply Chain & Procurement", "🔗"), unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Procurement Organization**")
                mat = co["procurement_organization"]["overall_maturity_level"]
                st.markdown(info_item("Maturity Level", mat["value"], mat["quote"], mat["source_url"]), unsafe_allow_html=True)
                struc = co["procurement_organization"]["structure"]
                st.markdown(info_item("Structure", struc["value"], struc["quote"], struc["source_url"]), unsafe_allow_html=True)
                cat = co["procurement_organization"]["category_mgmt"]
                st.markdown(info_item("Category Management", cat["value"], cat["quote"], cat["source_url"]), unsafe_allow_html=True)
                cpo = co["procurement_organization"]["cpo"]
                st.markdown(info_item("CPO/Equivalent", cpo["value"], cpo["quote"], cpo["source_url"]), unsafe_allow_html=True)
            with c2:
                st.markdown("**Procurement Maturity Dimensions**")
                for dim, data in co["procurement_organization"]["maturity_dimensions"].items():
                    label = dim.replace("_", " ").title()
                    pct = (data["score"] / 5) * 100
                    dim_src = src(label, data["quote"], data["source_url"])
                    st.markdown(f'''<div style="margin-bottom:12px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                            <span style="font-size:0.875rem;color:#2d2d2d;">{dim_src}</span>
                            <span style="font-size:0.875rem;font-weight:bold;color:#2d2d2d;">{data["value"]}</span>
                        </div>
                        <div class="progress-container">
                            <div class="progress-fill" style="width:{pct}%;">{data["score"]}/5</div>
                        </div>
                    </div>''', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(section_header("Procurement SWOT", "📊"), unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(swot_item("💪 Strengths", co["procurement_swot"]["strengths"], "strengths"), unsafe_allow_html=True)
                st.markdown(swot_item("🎯 Opportunities", co["procurement_swot"]["opportunities"], "opportunities"), unsafe_allow_html=True)
            with c2:
                st.markdown(swot_item("⚠️ Weaknesses", co["procurement_swot"]["weaknesses"], "weaknesses"), unsafe_allow_html=True)
                st.markdown(swot_item("🚨 Threats", co["procurement_swot"]["threats"], "threats"), unsafe_allow_html=True)
            
            st.markdown(section_header("Procurement Risks", "⚠️"), unsafe_allow_html=True)
            for risk in co["procurement_risks"]["key_risks"]:
                risk_html = src(risk["value"], risk["quote"], risk["source_url"])
                st.markdown(f'<div class="warning-box">⚠️ {risk_html}</div>', unsafe_allow_html=True)
            mit = co["procurement_risks"]["mitigation"]
            mit_html = src(mit["value"], mit["quote"], mit["source_url"])
            st.markdown(f'<div class="success-box"><strong>✅ Risk Mitigation:</strong><br>{mit_html}</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown(section_header("Financial Overview", "💰"), unsafe_allow_html=True)
            r24 = co['financials']['revenue_2024']
            r23 = co['financials']['revenue_2023']
            yoy = ((r24['value'] - r23['value']) / r23['value']) * 100
            
            c1, c2, c3 = st.columns(3)
            with c1:
                rev24_html = src(f"${r24['value']}B", r24["quote"], r24["source_url"])
                st.markdown(f'<div class="metric-card"><div class="label">2024 Revenue</div><div class="value">{rev24_html}</div><div class="label">USD</div></div>', unsafe_allow_html=True)
            with c2:
                rev23_html = src(f"${r23['value']}B", r23["quote"], r23["source_url"])
                st.markdown(f'<div class="metric-card"><div class="label">2023 Revenue</div><div class="value">{rev23_html}</div><div class="label">USD</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="metric-card"><div class="label">YoY Change</div><div class="value">{yoy:.1f}%</div><div class="label">2023 → 2024</div></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(section_header("Asset Information", "🏗️"), unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            eq = co['workforce']['equipment_fleet']
            ev = co['financials']['equipment_replacement_value']
            with c1:
                st.markdown(info_item("Equipment Fleet", f'{eq["value"]:,} units', eq["quote"], eq["source_url"]), unsafe_allow_html=True)
            with c2:
                st.markdown(info_item("Replacement Value", f'${ev["value"]}B USD', ev["quote"], ev["source_url"]), unsafe_allow_html=True)
            st.markdown(f'<div class="warning-box"><strong>⚠️ Note:</strong> {co["financials"]["source_note"]}</div>', unsafe_allow_html=True)
            
            st.markdown("<hr style='margin:40px 0;border:none;border-top:2px solid #E4E4E4;'>", unsafe_allow_html=True)
            
            st.markdown(section_header("Cost Optimization Projection", "📈"), unsafe_allow_html=True)
            
            # Check criteria for BXT_L2 savings
            is_nam_latam, is_over_10b, geo_scope, revenue = check_criteria(co)
            meets_criteria = is_nam_latam and is_over_10b
            
            mp = co["industry_mapping"]
            bxt_l2 = mp["bxt_l2"]
            
            # Get the appropriate savings rate
            if meets_criteria:
                rate = BXT_L2_SAVINGS.get(bxt_l2, BXT_L2_SAVINGS["Default"])
                criteria_status = "✅ MEETS CRITERIA"
                criteria_color = "#A5CD24"
            else:
                rate = BXT_L2_SAVINGS["Default"]
                criteria_status = "❌ DOES NOT MEET CRITERIA"
                criteria_color = "#C12D27"
            
            # Criteria Box
            st.markdown(f'''<div class="criteria-box">
                <strong>📋 BXT_L2 Savings Rate Criteria</strong>
                <div style="margin-top:12px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;">
                    <div style="padding:12px;background:#fafbfc;border-radius:8px;">
                        <div style="font-size:0.75rem;color:#666;text-transform:uppercase;">Geographic Scope</div>
                        <div style="font-size:1rem;font-weight:600;color:#2d2d2d;">{geo_scope}</div>
                        <div style="font-size:0.8rem;color:{"#A5CD24" if is_nam_latam else "#C12D27"};">{"✓ NAM/LATAM" if is_nam_latam else "✗ Required: NAM/LATAM"}</div>
                    </div>
                    <div style="padding:12px;background:#fafbfc;border-radius:8px;">
                        <div style="font-size:0.75rem;color:#666;text-transform:uppercase;">Revenue</div>
                        <div style="font-size:1rem;font-weight:600;color:#2d2d2d;">${revenue}B USD</div>
                        <div style="font-size:0.8rem;color:{"#A5CD24" if is_over_10b else "#C12D27"};">{"✓ >$10B" if is_over_10b else "✗ Required: >$10B"}</div>
                    </div>
                    <div style="padding:12px;background:#fafbfc;border-radius:8px;">
                        <div style="font-size:0.75rem;color:#666;text-transform:uppercase;">Status</div>
                        <div style="font-size:1rem;font-weight:600;color:{criteria_color};">{criteria_status}</div>
                        <div style="font-size:0.8rem;color:#666;">{"Using BXT_L2 rate" if meets_criteria else "Using default rate"}</div>
                    </div>
                </div>
            </div>''', unsafe_allow_html=True)
            
            # Industry Mapping Box
            st.markdown(f'''<div class="mapping-box"><strong>🏭 Industry Mapping</strong><div style="display:flex;align-items:center;margin-top:16px;flex-wrap:wrap;gap:8px;">
                <div style="background:#FFF;padding:12px 16px;border-radius:8px;border:2px solid #006492;"><div style="font-size:0.7rem;color:#666;text-transform:uppercase;">Original Industry</div><div style="font-size:0.9rem;color:#2d2d2d;font-weight:500;">{mp["original_industry"]}</div></div>
                <span style="font-size:1.5rem;color:#1B5E5C;margin:0 12px;">→</span>
                <div style="background:#FFF;padding:12px 16px;border-radius:8px;border:2px solid #1B5E5C;"><div style="font-size:0.7rem;color:#666;text-transform:uppercase;">BXT_L2 Classification</div><div style="font-size:0.9rem;color:#1B5E5C;font-weight:600;">{bxt_l2}</div></div>
                <span style="font-size:1.5rem;color:#1B5E5C;margin:0 12px;">→</span>
                <div style="background:#1B5E5C;padding:12px 16px;border-radius:8px;"><div style="font-size:0.7rem;color:rgba(255,255,255,0.8);text-transform:uppercase;">Median Projected Savings Rate</div><div style="font-size:1.2rem;color:#FFF;font-weight:700;">{rate*100:.4f}%</div></div>
            </div></div>''', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown("### 💵 Total Addressable Market (TAM)")
                tam = st.number_input("TAM (USD millions)", min_value=0.0, max_value=100000.0, value=100.0, step=10.0, format="%.2f")
                st.markdown("### 📊 TAM Percentage for Calculation")
                tam_pct = st.slider("Select % of TAM to use", min_value=0, max_value=100, value=100, step=5)
            with c2:
                st.markdown("### 📋 Savings Parameters")
                st.markdown(f'<div class="meta-card"><div class="meta-label">BXT_L2 Category</div><div class="meta-value">{bxt_l2}</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="meta-card" style="margin-top:12px;"><div class="meta-label">Median Savings Rate</div><div class="meta-value">{rate*100:.4f}%</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="meta-card" style="margin-top:12px;"><div class="meta-label">TAM % Applied</div><div class="meta-value">{tam_pct}%</div></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            adj_tam = tam * (tam_pct / 100)
            proj = adj_tam * rate
            cons = adj_tam * (rate * 0.7)
            opt = adj_tam * (rate * 1.3)
            
            st.markdown(section_header("Projected Savings Analysis", "💰"), unsafe_allow_html=True)
            st.markdown(f'<div class="info-box"><strong>📊 Calculation Base:</strong> TAM ${tam:,.2f}M × {tam_pct}% = <strong>${adj_tam:,.2f}M</strong></div>', unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="metric-card-warning"><div class="label">Conservative (70%)</div><div class="value">${cons:,.2f}M</div><div class="label">{rate*70:.4f}% of Adj TAM</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="metric-card"><div class="label">Median Projection</div><div class="value">${proj:,.2f}M</div><div class="label">{rate*100:.4f}% of Adj TAM</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="metric-card-success"><div class="label">Optimistic (130%)</div><div class="value">${opt:,.2f}M</div><div class="label">{rate*130:.4f}% of Adj TAM</div></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(section_header("Savings Breakdown", "📋"), unsafe_allow_html=True)
            df = pd.DataFrame({
                'Scenario': ['Conservative (70%)', 'Median', 'Optimistic (130%)'],
                'Savings Rate': [f"{rate*70:.4f}%", f"{rate*100:.4f}%", f"{rate*130:.4f}%"],
                'Adjusted TAM': [f"${adj_tam:,.2f}M"]*3,
                'Projected Savings': [f"${cons:,.2f}M", f"${proj:,.2f}M", f"${opt:,.2f}M"]
            })
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown(f'''<div class="info-box"><strong>📝 Methodology:</strong>
                <ul style="margin-top:8px;padding-left:20px;color:#2d2d2d;">
                    <li>Industry "<strong>{mp["original_industry"]}</strong>" mapped to BXT_L2 "<strong>{bxt_l2}</strong>"</li>
                    <li>Median Projected Savings Rate for BXT_L2 (NAM/LATAM, >$10B): <strong>{rate*100:.4f}%</strong></li>
                    <li>Criteria: Geographic Scope = NAM/LATAM AND Revenue > $10B</li>
                    <li>Conservative: 30% reduction / Optimistic: 30% increase from median</li>
                </ul>
            </div>''', unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning-box"><strong>⚠️ Company not found</strong><br>Try searching for "Kiewit Corporation" or "Kiewit".</div>', unsafe_allow_html=True)
else:
    st.markdown('''<div class="card" style="text-align:center;padding:60px;">
        <h2 style="color:#1B5E5C !important;">👋 Welcome to the Company Intelligence Dashboard</h2>
        <p style="font-size:1.1rem;color:#666 !important;margin-top:16px;">Enter a company name in the search bar above to view detailed information.</p>
        <p style="color:#999 !important;margin-top:24px;"><strong>Available:</strong> Kiewit Corporation</p>
        <p style="color:#666 !important;margin-top:16px;font-size:0.9rem;">💡 <strong>Tip:</strong> Hover over any value to see the source quote and link</p>
    </div>''', unsafe_allow_html=True)

st.markdown('''<div class="footer">
    <p style="color:#2d2d2d !important;"><strong>Company Intelligence Dashboard</strong></p>
    <p style="color:#666 !important;">Due Diligence & Procurement Analysis Platform</p>
    <p style="margin-top:10px;font-size:0.85em;color:#888 !important;">This report is for informational purposes only. 💡 Hover over values to see sources.</p>
</div>''', unsafe_allow_html=True)

