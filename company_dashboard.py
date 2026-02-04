import streamlit as st
import pandas as pd

st.set_page_config(page_title="Company Intelligence Dashboard", page_icon="🏢", layout="wide", initial_sidebar_state="collapsed")

# CSS con tooltip mejorado que no desaparece al mover el mouse
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
    .footer {background: #E4E4E4; padding: 24px; border-radius: 8px; margin-top: 32px; font-size: 0.875rem; color: #666 !important; text-align: center;}
    .criteria-box {background: #FFF; border: 2px solid #1B5E5C; border-radius: 8px; padding: 16px; margin: 16px 0;}
    
    /* TOOLTIP MEJORADO - no desaparece al mover el mouse */
    .with-source {
        position: relative;
        cursor: pointer;
        border-bottom: 1px dotted #006492;
        display: inline;
    }
    .source-tooltip {
        display: none;
        position: absolute;
        background: #2d2d2d;
        color: #FFF !important;
        padding: 16px 20px;
        border-radius: 8px;
        font-size: 0.85rem;
        z-index: 9999;
        max-width: 450px;
        min-width: 300px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        left: 0;
        top: calc(100% + 5px);
        line-height: 1.6;
    }
    /* Pseudo-elemento para crear puente entre el texto y el tooltip */
    .source-tooltip::before {
        content: "";
        position: absolute;
        top: -10px;
        left: 0;
        right: 0;
        height: 15px;
        background: transparent;
    }
    .with-source:hover .source-tooltip,
    .source-tooltip:hover {
        display: block;
    }
    .source-tooltip a {
        color: #A5CD24 !important;
        text-decoration: underline;
        font-weight: 600;
    }
    .source-tooltip strong {
        color: #FFF !important;
    }
    .source-quote {
        font-style: italic;
        color: #ccc !important;
        margin: 8px 0;
        padding-left: 10px;
        border-left: 2px solid #A5CD24;
    }
    
    /* Input label color fix */
    .input-label {
        color: #2d2d2d !important;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
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

# Data actualizada con los links correctos
COMPANY_DATA = {
    "kiewit": {
        "meta": {
            "company_name": {"value": "Kiewit Corporation", "quote": "Kiewit is one of North America's largest and most respected construction and engineering organizations.", "source_url": "https://www.kiewit.com/about-us/"},
            "jurisdiction": {"value": "United States, Canada and Mexico", "quote": "The employee-owned organization operates through a network of subsidiaries in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"},
            "listed_status": {"value": "Private company (employee-owned)", "quote": "With its roots dating back to 1884, the employee-owned organization operates through a network of subsidiaries in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"}
        },
        "company_overview": {
            "description": {"value": "Kiewit Corporation is one of North America's largest construction and engineering organizations, delivering end-to-end engineering, procurement and construction (EPC) services for critical infrastructure and energy projects.", "quote": "Kiewit is one of North America's largest and most respected construction and engineering organizations.", "source_url": "https://www.kiewit.com/about-us/"},
            "founded_year": {"value": 1884, "quote": "With its roots dating back to 1884, the employee-owned organization operates through a network of subsidiaries in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"},
            "headquarters": {"value": "Omaha, Nebraska, United States", "quote": "The Kiewit Corporation is a Fortune 500 contractor business headquartered in Omaha.", "source_url": "http://www.omahaimc.org/kiewit-corporation/"},
            "primary_industry": {"value": "Engineering, Procurement and Construction (EPC) services", "quote": "The EPC model streamlines execution with a single contractor managing design, procurement and construction — ensuring cost certainty, schedule reliability and reduced owner risk.", "source_url": "https://www.kiewit.com/services-and-solutions/project-delivery/"},
            "primary_markets": [
                {"value": "Transportation", "quote": "Kiewit offers construction and engineering services in a variety of markets including transportation.", "source_url": "https://www.linkedin.com/company/kiewit"},
                {"value": "Oil, gas and chemical", "quote": "Kiewit offers construction and engineering services in oil, gas and chemical.", "source_url": "https://www.linkedin.com/company/kiewit"},
                {"value": "Power", "quote": "Kiewit offers construction and engineering services in power.", "source_url": "https://www.linkedin.com/company/kiewit"},
                {"value": "Building", "quote": "Kiewit offers construction and engineering services in building.", "source_url": "https://www.linkedin.com/company/kiewit"},
                {"value": "Marine", "quote": "Kiewit offers construction and engineering services in marine.", "source_url": "https://www.linkedin.com/company/kiewit"},
                {"value": "Water/wastewater", "quote": "Kiewit offers construction and engineering services in water/wastewater.", "source_url": "https://www.linkedin.com/company/kiewit"},
                {"value": "Industrial", "quote": "Kiewit offers construction and engineering services in industrial.", "source_url": "https://www.linkedin.com/company/kiewit"},
                {"value": "Mining", "quote": "Kiewit offers construction and engineering services in mining.", "source_url": "https://www.linkedin.com/company/kiewit"}
            ],
            "naics_codes": [],
            "sic_codes": []
        },
        "operational_footprint": {
            "regions_of_operation": [
                {"value": "United States", "quote": "The employee-owned organization operates through a network of subsidiaries in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"},
                {"value": "Canada", "quote": "The employee-owned organization operates through a network of subsidiaries in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"},
                {"value": "Mexico", "quote": "The employee-owned organization operates through a network of subsidiaries in the United States, Canada and Mexico.", "source_url": "https://www.forbes.com/companies/kiewit/"}
            ],
            "business_segments": ["Transportation", "Oil, gas and chemical", "Power", "Building", "Marine", "Water/wastewater", "Industrial", "Mining"],
            "geographic_scope": "NAM/LATAM"
        },
        "workforce": {
            "total_employees": {"value": 31800, "quote": "16.8 BILLION 31,800 EMPLOYEES 2024 REVENUE 2024 EMPLOYEES", "source_url": "https://www.kiewit.com/wp-content/uploads/2025/09/EN_2024-Sustainability-Report-reduced.pdf"},
            "equipment_fleet": {"value": None, "quote": "", "source_url": ""}
        },
        "financials": {
            "revenue_2024": {"value": 16.8, "quote": "Proven Results. $16.8B 2024 Revenues 31,800 Craft and Staff Employees", "source_url": "https://www.kiewit.com"},
            "revenue_2023": {"value": None, "quote": "", "source_url": ""},
            "equipment_replacement_value": {"value": None, "quote": "", "source_url": ""},
            "source_note": "Private company – estimates only; no official statutory filings."
        },
        "ownership_structure": {"ownership_type": {"value": "Privately held, employee-owned organization", "quote": "Kiewit's diversified services and unique network of decentralized offices — backed by a multi-billion-dollar, employee-owned organization — enable us to tackle construction and engineering projects of any size.", "source_url": "https://www.kiewit.com/about-us/"}},
        "procurement_organization": {
            "overall_maturity_level": {"value": "Defined to Managed", "quote": "At Kiewit, supply chain is integrated into project planning from the very beginning. We're part of the strategy, the estimate, the bid.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
            "maturity_dimensions": {
                "governance_and_org": {"value": "Managed", "score": 4, "quote": "Depending on the project, material procurement can account for up to 50% of total installed costs. That makes Carsten's team critical to the bottom line.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                "process_and_policy": {"value": "Defined", "score": 3, "quote": "At Kiewit, supply chain is integrated into project planning from the very beginning. We're part of the strategy, the estimate, the bid.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                "technology_and_data": {"value": "Defined", "score": 3, "quote": "Our procurement and supply chain experts leverage scale, strategy and technology to ensure materials, equipment and services keep projects on track.", "source_url": "https://www.kiewit.com/?lang=en-ca"},
                "supplier_management": {"value": "Defined", "score": 3, "quote": "What distinguishes strong suppliers during these moments is transparency. The worst thing a vendor can do is hide a problem. If we know early, we can help.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
                "integration_lifecycle": {"value": "Managed", "score": 4, "quote": "At Kiewit, supply chain is integrated into project planning from the very beginning. We're part of the strategy, the estimate, the bid. We help define risk and create the roadmap for delivery.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
            },
            "structure": {"value": "Supply chain sits between engineering and construction, responsible for ensuring materials arrive on time and in full to support EPC project execution.", "quote": "We sit between engineering and construction. Our job is to make sure materials arrive when construction needs them — not a day late, not a piece short.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
            "category_mgmt": {"value": "Procurement is organized around categories with specialists owning domains such as valves or piping, building technical expertise and deep supplier relationships.", "quote": "He's also reorganized his team around procurement categories — giving specialists ownership over specific domains like valves or piping.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"},
            "cpo": {"value": "Carsten Bernstiel – Vice President of Procurement, Oil, Gas & Chemical group", "quote": "At the center of this complex machinery is Carsten Bernstiel, Vice President of Procurement for Kiewit's Oil, Gas & Chemical group, a veteran of the energy industry.", "source_url": "https://pipingtech.com/putting-the-p-in-epc-kiewits-vp-of-procurement-ogc-talks-supply-chain-risk-management/"}
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

def get_company_data(name):
    term = name.lower().strip()
    for key, data in COMPANY_DATA.items():
        if key in term or term in data["meta"]["company_name"]["value"].lower():
            return data
    return None

def src(value, quote, url):
    if not quote or not url:
        return f'<span style="color:#2d2d2d;">{value}</span>'
    return f'''<span class="with-source">{value}<span class="source-tooltip">
        <strong>📝 Source:</strong>
        <div class="source-quote">"{quote}"</div>
        <a href="{url}" target="_blank">🔗 View Source</a>
    </span></span>'''

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
    geo_scope = co.get("operational_footprint", {}).get("geographic_scope", "")
    revenue = co.get("financials", {}).get("revenue_2024", {}).get("value", 0) or 0
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
            
            c1, c2, c3 = st.columns(3)
            with c1:
                rev24_html = src(f"${r24['value']}B", r24["quote"], r24["source_url"])
                st.markdown(f'<div class="metric-card"><div class="label">2024 Revenue</div><div class="value">{rev24_html}</div><div class="label">USD</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="metric-card"><div class="label">Geographic Scope</div><div class="value">{co["operational_footprint"]["geographic_scope"]}</div><div class="label">Region</div></div>', unsafe_allow_html=True)
            with c3:
                emp = co['workforce']['total_employees']
                emp_html = src(f"{emp['value']:,}", emp["quote"], emp["source_url"])
                st.markdown(f'<div class="metric-card"><div class="label">Employees</div><div class="value">{emp_html}</div><div class="label">2024</div></div>', unsafe_allow_html=True)
            
            st.markdown(f'<div class="warning-box"><strong>⚠️ Note:</strong> {co["financials"]["source_note"]}</div>', unsafe_allow_html=True)
            
            st.markdown("<hr style='margin:40px 0;border:none;border-top:2px solid #E4E4E4;'>", unsafe_allow_html=True)
            
            st.markdown(section_header("Cost Optimization Projection", "📈"), unsafe_allow_html=True)
            
            is_nam_latam, is_over_10b, geo_scope, revenue = check_criteria(co)
            meets_criteria = is_nam_latam and is_over_10b
            
            mp = co["industry_mapping"]
            bxt_l2 = mp["bxt_l2"]
            
            if meets_criteria:
                rate = BXT_L2_SAVINGS.get(bxt_l2, BXT_L2_SAVINGS["Default"])
                criteria_status = "✅ MEETS CRITERIA"
                criteria_color = "#A5CD24"
            else:
                rate = BXT_L2_SAVINGS["Default"]
                criteria_status = "❌ DOES NOT MEET CRITERIA"
                criteria_color = "#C12D27"
            
            st.markdown(f'''<div class="criteria-box">
                <strong style="color:#2d2d2d;">📋 BXT_L2 Savings Rate Criteria</strong>
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
            
            st.markdown(f'''<div class="mapping-box"><strong style="color:#2d2d2d;">🏭 Industry Mapping</strong><div style="display:flex;align-items:center;margin-top:16px;flex-wrap:wrap;gap:8px;">
                <div style="background:#FFF;padding:12px 16px;border-radius:8px;border:2px solid #006492;"><div style="font-size:0.7rem;color:#666;text-transform:uppercase;">Original Industry</div><div style="font-size:0.9rem;color:#2d2d2d;font-weight:500;">{mp["original_industry"]}</div></div>
                <span style="font-size:1.5rem;color:#1B5E5C;margin:0 12px;">→</span>
                <div style="background:#FFF;padding:12px 16px;border-radius:8px;border:2px solid #1B5E5C;"><div style="font-size:0.7rem;color:#666;text-transform:uppercase;">BXT_L2 Classification</div><div style="font-size:0.9rem;color:#1B5E5C;font-weight:600;">{bxt_l2}</div></div>
                <span style="font-size:1.5rem;color:#1B5E5C;margin:0 12px;">→</span>
                <div style="background:#1B5E5C;padding:12px 16px;border-radius:8px;"><div style="font-size:0.7rem;color:rgba(255,255,255,0.8);text-transform:uppercase;">Median Projected Savings Rate</div><div style="font-size:1.2rem;color:#FFF;font-weight:700;">{rate*100:.4f}%</div></div>
            </div></div>''', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Total Addressable Spend section
            total_revenue = revenue * 1000  # Convert to millions
            
            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown('<p class="input-label">💵 Total Addressable Spend (% of Revenue)</p>', unsafe_allow_html=True)
                spend_pct = st.slider("Select % of Revenue as Addressable Spend", min_value=0, max_value=100, value=30, step=5, help="Percentage of total revenue that represents addressable procurement spend")
                
                addressable_spend = total_revenue * (spend_pct / 100)
                st.markdown(f'''<div class="info-box">
                    <strong>📊 Calculation:</strong><br>
                    Revenue: <strong>${total_revenue:,.0f}M</strong> × {spend_pct}% = <strong>${addressable_spend:,.2f}M</strong> Addressable Spend
                </div>''', unsafe_allow_html=True)
                
            with c2:
                st.markdown('<p class="input-label">📋 Savings Parameters</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="meta-card"><div class="meta-label">BXT_L2 Category</div><div class="meta-value" style="font-size:0.95rem;">{bxt_l2}</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="meta-card" style="margin-top:12px;"><div class="meta-label">Median Savings Rate</div><div class="meta-value">{rate*100:.4f}%</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="meta-card" style="margin-top:12px;"><div class="meta-label">Total Addressable Spend</div><div class="meta-value">${addressable_spend:,.2f}M</div></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Calculations based on addressable spend
            proj = addressable_spend * rate
            cons = addressable_spend * (rate * 0.7)
            opt = addressable_spend * (rate * 1.3)
            
            st.markdown(section_header("Projected Savings Analysis", "💰"), unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="metric-card-warning"><div class="label">Conservative (70%)</div><div class="value">${cons:,.2f}M</div><div class="label">{rate*70:.4f}% of Spend</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="metric-card"><div class="label">Median Projection</div><div class="value">${proj:,.2f}M</div><div class="label">{rate*100:.4f}% of Spend</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="metric-card-success"><div class="label">Optimistic (130%)</div><div class="value">${opt:,.2f}M</div><div class="label">{rate*130:.4f}% of Spend</div></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(section_header("Savings Breakdown", "📋"), unsafe_allow_html=True)
            df = pd.DataFrame({
                'Scenario': ['Conservative (70%)', 'Median', 'Optimistic (130%)'],
                'Savings Rate': [f"{rate*70:.4f}%", f"{rate*100:.4f}%", f"{rate*130:.4f}%"],
                'Addressable Spend': [f"${addressable_spend:,.2f}M"]*3,
                'Projected Savings': [f"${cons:,.2f}M", f"${proj:,.2f}M", f"${opt:,.2f}M"]
            })
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown(f'''<div class="info-box"><strong style="color:#2d2d2d;">📝 Methodology:</strong>
                <ul style="margin-top:8px;padding-left:20px;color:#2d2d2d;">
                    <li>Industry "<strong>{mp["original_industry"]}</strong>" mapped to BXT_L2 "<strong>{bxt_l2}</strong>"</li>
                    <li>Total Addressable Spend = Revenue (${total_revenue:,.0f}M) × {spend_pct}% = <strong>${addressable_spend:,.2f}M</strong></li>
                    <li>Median Projected Savings Rate (NAM/LATAM, >$10B): <strong>{rate*100:.4f}%</strong></li>
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
        <p style="color:#666 !important;margin-top:16px;font-size:0.9rem;">💡 <strong>Tip:</strong> Hover over any underlined value to see the source quote and link</p>
    </div>''', unsafe_allow_html=True)

st.markdown('''<div class="footer">
    <p style="color:#2d2d2d !important;"><strong>Company Intelligence Dashboard</strong></p>
    <p style="color:#666 !important;">Due Diligence & Procurement Analysis Platform</p>
    <p style="margin-top:10px;font-size:0.85em;color:#888 !important;">This report is for informational purposes only. 💡 Hover over underlined values to see sources.</p>
</div>''', unsafe_allow_html=True)


