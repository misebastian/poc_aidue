import streamlit as st
import json
import pandas as pd

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="Company Intelligence Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# PALETA DE COLORES (del HTML)
# ============================================
COLORS = {
    "black": "#000000",
    "white": "#FFFFFF",
    "slate": "#CACED7",
    "module_gray": "#E4E4E4",
    "copper": "#A95228",
    "avocado": "#CF9F8B",
    "emerald": "#1B5E5C",
    "taupe": "#C39D7B",
    "cobalt": "#006492",
    "chartreuse": "#A5CD24",
    "crimson": "#C12D27",
}

# ============================================
# CSS PERSONALIZADO
# ============================================
st.markdown(f"""
<style>
    /* Importar fuentes */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&display=swap');
    
    /* Variables CSS */
    :root {{
        --black: {COLORS['black']};
        --white: {COLORS['white']};
        --slate: {COLORS['slate']};
        --module-gray: {COLORS['module_gray']};
        --copper: {COLORS['copper']};
        --avocado: {COLORS['avocado']};
        --emerald: {COLORS['emerald']};
        --taupe: {COLORS['taupe']};
        --cobalt: {COLORS['cobalt']};
        --chartreuse: {COLORS['chartreuse']};
        --crimson: {COLORS['crimson']};
    }}
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Fondo general */
    .stApp {{
        background-color: #f8fafc;
    }}
    
    /* Header personalizado */
    .custom-header {{
        background: var(--black);
        color: var(--white);
        padding: 24px 32px;
        margin: -1rem -1rem 24px -1rem;
        border-bottom: 4px solid var(--copper);
    }}
    
    .custom-header h1 {{
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2rem;
        font-weight: 400;
        color: var(--white);
        margin: 0;
    }}
    
    .custom-header .subtitle {{
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 4px;
    }}
    
    /* Tabs personalizados */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: var(--module-gray);
        padding: 8px;
        border-radius: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: var(--white);
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 500;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: var(--emerald) !important;
        color: var(--white) !important;
    }}
    
    /* Cards */
    .card {{
        background: var(--white);
        padding: 24px;
        margin-bottom: 24px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}
    
    /* Section Headers */
    .section-header {{
        background: var(--white);
        padding: 16px 24px;
        margin-bottom: 16px;
        border-left: 4px solid var(--emerald);
        border-radius: 8px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }}
    
    .section-header h2 {{
        font-family: 'Playfair Display', Georgia, serif;
        color: var(--emerald);
        font-size: 1.5rem;
        font-weight: 500;
        margin: 0;
    }}
    
    .section-header h3 {{
        font-family: 'Playfair Display', Georgia, serif;
        color: var(--black);
        font-size: 1.125rem;
        font-weight: 500;
        margin: 0;
    }}
    
    /* Meta Cards */
    .meta-card {{
        background: var(--white);
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid var(--emerald);
        height: 100%;
    }}
    
    .meta-label {{
        font-size: 0.75rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        font-weight: 600;
    }}
    
    .meta-value {{
        font-size: 1.125rem;
        color: var(--copper);
        font-weight: 600;
    }}
    
    /* Metric Cards */
    .metric-card {{
        background: linear-gradient(135deg, var(--emerald) 0%, var(--cobalt) 100%);
        color: var(--white);
        padding: 24px;
        border-radius: 8px;
        text-align: center;
    }}
    
    .metric-card .value {{
        font-size: 2rem;
        font-weight: bold;
        margin: 8px 0;
    }}
    
    .metric-card .label {{
        font-size: 0.875rem;
        opacity: 0.9;
    }}
    
    /* Info Items */
    .info-item {{
        padding: 16px;
        background: #fafbfc;
        border-radius: 8px;
        border-left: 4px solid var(--cobalt);
        margin-bottom: 12px;
    }}
    
    .info-item strong {{
        display: block;
        color: var(--emerald);
        margin-bottom: 8px;
        font-size: 0.875rem;
        font-weight: 600;
    }}
    
    /* Badges */
    .badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.75rem;
        font-weight: bold;
        margin-right: 8px;
        margin-bottom: 8px;
    }}
    
    .badge-high {{
        background: var(--chartreuse);
        color: var(--white);
    }}
    
    .badge-medium {{
        background: var(--taupe);
        color: var(--white);
    }}
    
    .badge-low {{
        background: var(--crimson);
        color: var(--white);
    }}
    
    .badge-info {{
        background: var(--cobalt);
        color: var(--white);
    }}
    
    /* Progress Bar */
    .progress-container {{
        background: #e5e7eb;
        border-radius: 4px;
        height: 24px;
        position: relative;
        margin: 8px 0;
    }}
    
    .progress-fill {{
        background: var(--avocado);
        height: 100%;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--white);
        font-size: 0.75rem;
        font-weight: bold;
    }}
    
    /* SWOT Grid */
    .swot-item {{
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 12px;
    }}
    
    .swot-strengths {{
        border-left: 4px solid var(--chartreuse);
        background: rgba(165, 205, 36, 0.1);
    }}
    
    .swot-weaknesses {{
        border-left: 4px solid var(--taupe);
        background: rgba(195, 157, 123, 0.1);
    }}
    
    .swot-opportunities {{
        border-left: 4px solid var(--cobalt);
        background: rgba(0, 100, 146, 0.1);
    }}
    
    .swot-threats {{
        border-left: 4px solid var(--crimson);
        background: rgba(193, 45, 39, 0.1);
    }}
    
    /* Success/Warning/Info Boxes */
    .success-box {{
        background: rgba(165, 205, 36, 0.1);
        border-left: 4px solid var(--chartreuse);
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
    }}
    
    .warning-box {{
        background: rgba(195, 157, 123, 0.1);
        border-left: 4px solid var(--taupe);
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
    }}
    
    .info-box {{
        background: rgba(0, 100, 146, 0.1);
        border-left: 4px solid var(--cobalt);
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
    }}
    
    /* Input styling */
    .stTextInput > div > div > input {{
        border: 2px solid var(--module-gray);
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 1rem;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: var(--emerald);
        box-shadow: 0 0 0 2px rgba(27, 94, 92, 0.2);
    }}
    
    /* Number input styling */
    .stNumberInput > div > div > input {{
        border: 2px solid var(--module-gray);
        border-radius: 8px;
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        background-color: var(--white);
        border-radius: 8px;
        font-weight: 500;
    }}
    
    /* Tables */
    .dataframe {{
        border: none !important;
    }}
    
    .dataframe th {{
        background: var(--module-gray) !important;
        color: var(--black) !important;
        font-weight: 600 !important;
        border-bottom: 2px solid var(--emerald) !important;
    }}
    
    .dataframe td {{
        border-bottom: 1px solid var(--module-gray) !important;
    }}
    
    /* Footer */
    .footer {{
        background: var(--module-gray);
        padding: 24px;
        border-radius: 8px;
        margin-top: 32px;
        font-size: 0.875rem;
        color: #666;
        text-align: center;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# DATOS DE LA EMPRESA (JSON)
# ============================================
COMPANY_DATA = {
    "kiewit": {
        "meta": {
            "company_name": "Kiewit Corporation",
            "jurisdiction": "United States",
            "listed_status": "Private company (employee-owned)",
            "data_cutoff_note": "Information reflects public sources available as of 2026-02-04"
        },
        "company_overview": {
            "legal_name": "Kiewit Corporation",
            "description": "Kiewit Corporation is one of North America's largest construction and engineering organizations, providing integrated engineering, procurement and construction (EPC) services across energy, transportation, water, mining, oil, gas and chemical markets.",
            "founded_year": 1884,
            "headquarters": "Omaha, Nebraska, United States",
            "primary_markets": [
                "Transportation infrastructure (highways, bridges, rail, mass transit, airports)",
                "Power generation and delivery (gas-fired, renewables, power delivery)",
                "Oil, gas and chemical facilities (offshore, oil sands, gas processing, pipelines, LNG, refining, petrochemicals)",
                "Water and wastewater infrastructure",
                "Mining and industrial projects",
                "Nuclear, data centers and other large capital projects"
            ],
            "industry_classification": {
                "primary_industries": [
                    "Engineering, Procurement and Construction (EPC) for infrastructure and industrial projects",
                    "Heavy and civil engineering construction",
                    "Industrial and commercial building construction"
                ],
                "primary_industry_confidence_score": 92
            },
            "naics_codes": [
                {"code": "236220", "title": "Commercial and Institutional Building Construction"},
                {"code": "237310", "title": "Highway, Street, and Bridge Construction"},
                {"code": "237120", "title": "Oil and Gas Pipeline and Related Structures Construction"}
            ],
            "sic_codes": [
                {"code": "15420100", "title": "Commercial and office building contractors"},
                {"code": "15410000", "title": "Industrial buildings and warehouses"}
            ]
        },
        "operational_footprint": {
            "regions_of_operation": [
                "United States (multiple regions)",
                "Canada",
                "Other international projects (select markets)"
            ],
            "notable_facilities": [
                "Offshore fabrication yard in Ingleside, Texas",
                "Multiple district and project offices across North America"
            ],
            "business_segments": [
                "Transportation",
                "Power",
                "Oil, Gas & Chemical (OGC)",
                "Water and Wastewater",
                "Mining",
                "Industrial / Building",
                "Nuclear and specialized infrastructure"
            ]
        },
        "workforce": {
            "total_employees": 31800,
            "workforce_profile": "Kiewit employs approximately 31,800 staff and craft employees, supported by a large owned equipment fleet, to self-perform critical elements of heavy civil, industrial and EPC projects.",
            "equipment_fleet": 34800
        },
        "financials": {
            "revenue_estimates": {
                "2023": 17.1,
                "2024": 16.8
            },
            "units": "USD billions",
            "equipment_replacement_value": 5.0,
            "source_note": "Private company – estimates only; no official statutory filings."
        },
        "ownership_structure": {
            "ownership_type": "Privately held, employee-owned construction and engineering company",
            "governance_notes": "Kiewit operates with a traditional corporate governance structure and market-focused business groups."
        },
        "procurement_organization": {
            "overall_maturity_level": "Defined to Managed",
            "maturity_dimensions": {
                "governance_and_org": {"value": "Managed", "score": 4},
                "process_and_policy": {"value": "Defined", "score": 3},
                "technology_and_data": {"value": "Defined", "score": 3},
                "supplier_management_and_esg": {"value": "Defined", "score": 3},
                "integration_in_project_lifecycle": {"value": "Managed", "score": 4}
            },
            "structure_and_reporting": "Procurement operates as a shared service for activities such as expediting, inspection and logistics, while supply chain teams are embedded in operating districts.",
            "category_management": "Category-based organization, with specialists owning specific domains (e.g., valves, piping).",
            "chief_procurement_officer": "Carsten Bernstiel – Vice President of Procurement, Oil, Gas & Chemical (OGC) Group",
            "linkedin": "https://www.linkedin.com/in/carsten-bernstiel-93458b34/"
        },
        "procurement_risks": {
            "key_risks": [
                "Tariffs and trade policy changes affecting material and equipment costs",
                "Supply chain disruptions impacting schedule certainty for EPC projects",
                "Logistics and expediting challenges for global sourcing of specialized equipment"
            ],
            "risk_mitigation_approach": "Early involvement in project strategy and estimating, category-based specialization, proactive risk identification."
        },
        "procurement_swot": {
            "strengths": [
                "Integrated EPC model with self-perform construction and large owned equipment fleet",
                "Shared procurement services and embedded supply chain teams",
                "Category-based procurement organization with domain expertise"
            ],
            "weaknesses": [
                "Limited public disclosure on procurement systems, KPIs and ESG programs",
                "Complex, project-based organization across many markets"
            ],
            "opportunities": [
                "Greater use of AI and advanced analytics in procurement",
                "Strengthening ESG and supplier diversity programs",
                "Leveraging scale to standardize category strategies"
            ],
            "threats": [
                "Tariff and trade policy volatility",
                "Global supply chain disruptions",
                "Intensifying competition from other large EPC contractors"
            ]
        },
        "bxt_l2": "Heavy Construction & Engineering"
    }
}

# ============================================
# MEDIAN PROJECTED SAVINGS POR BXT_L2
# ============================================
MEDIAN_SAVINGS_BY_BXT_L2 = {
    "Heavy Construction & Engineering": 0.045,  # 4.5%
    "General Contractors": 0.038,
    "Specialty Trade Contractors": 0.042,
    "Industrial Manufacturing": 0.052,
    "Oil & Gas": 0.048,
    "Mining": 0.041,
    "Transportation Infrastructure": 0.044,
    "Power & Utilities": 0.046,
    "Water & Environmental": 0.039,
    "Default": 0.04
}

# ============================================
# FUNCIONES HELPER
# ============================================
def get_company_data(company_name: str):
    """Busca datos de la empresa por nombre"""
    search_term = company_name.lower().strip()
    for key, data in COMPANY_DATA.items():
        if key in search_term or search_term in data["meta"]["company_name"].lower():
            return data
    return None

def render_badge(text: str, badge_type: str = "info"):
    """Renderiza un badge con estilo"""
    return f'<span class="badge badge-{badge_type}">{text}</span>'

def render_meta_card(label: str, value: str):
    """Renderiza una meta card"""
    return f'''
    <div class="meta-card">
        <div class="meta-label">{label}</div>
        <div class="meta-value">{value}</div>
    </div>
    '''

def render_section_header(title: str, icon: str = "📊"):
    """Renderiza un header de sección"""
    return f'''
    <div class="section-header">
        <h2>{icon} {title}</h2>
    </div>
    '''

def render_info_item(label: str, value: str):
    """Renderiza un info item"""
    return f'''
    <div class="info-item">
        <strong>{label}</strong>
        {value}
    </div>
    '''

def render_swot_item(title: str, items: list, swot_type: str):
    """Renderiza un item de SWOT"""
    items_html = "".join([f"<li>{item}</li>" for item in items])
    return f'''
    <div class="swot-item swot-{swot_type}">
        <strong>{title}</strong>
        <ul style="margin-top: 8px; padding-left: 20px;">
            {items_html}
        </ul>
    </div>
    '''

# ============================================
# HEADER
# ============================================
st.markdown("""
<div class="custom-header">
    <h1>🏢 Company Intelligence Dashboard</h1>
    <div class="subtitle">Due Diligence & Procurement Analysis Platform</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# BARRA DE BÚSQUEDA
# ============================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    company_search = st.text_input(
        "🔍 Search Company",
        placeholder="Enter company name (e.g., Kiewit Corporation)",
        key="company_search"
    )

# ============================================
# CONTENIDO PRINCIPAL
# ============================================
if company_search:
    company = get_company_data(company_search)
    
    if company:
        # Crear las 3 tabs
        tab1, tab2, tab3 = st.tabs(["📋 General Info", "💰 Financials", "📈 Cost Optimization"])
        
        # =============================================
        # TAB 1: GENERAL INFO
        # =============================================
        with tab1:
            st.markdown(render_section_header("Company Overview", "🏢"), unsafe_allow_html=True)
            
            # Meta información principal
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(render_meta_card("Company Name", company["meta"]["company_name"]), unsafe_allow_html=True)
            with col2:
                st.markdown(render_meta_card("Jurisdiction", company["meta"]["jurisdiction"]), unsafe_allow_html=True)
            with col3:
                st.markdown(render_meta_card("Status", company["meta"]["listed_status"]), unsafe_allow_html=True)
            with col4:
                st.markdown(render_meta_card("Founded", str(company["company_overview"]["founded_year"])), unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Descripción
            st.markdown("""
            <div class="card">
                <h3 style="color: #1B5E5C; margin-bottom: 12px;">📝 Description</h3>
                <p>{}</p>
            </div>
            """.format(company["company_overview"]["description"]), unsafe_allow_html=True)
            
            # Headquarters & Primary Markets
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(render_section_header("Corporate Structure", "🏛️"), unsafe_allow_html=True)
                st.markdown(render_info_item("Headquarters", company["company_overview"]["headquarters"]), unsafe_allow_html=True)
                st.markdown(render_info_item("Ownership Type", company["ownership_structure"]["ownership_type"]), unsafe_allow_html=True)
                st.markdown(render_info_item("Total Employees", f"{company['workforce']['total_employees']:,}"), unsafe_allow_html=True)
                st.markdown(render_info_item("Equipment Fleet", f"{company['workforce']['equipment_fleet']:,} units"), unsafe_allow_html=True)
            
            with col2:
                st.markdown(render_section_header("Business Segments", "📊"), unsafe_allow_html=True)
                segments_html = "".join([f'<span class="badge badge-info">{seg}</span>' for seg in company["operational_footprint"]["business_segments"]])
                st.markdown(f'<div class="card">{segments_html}</div>', unsafe_allow_html=True)
                
                st.markdown(render_section_header("Regions of Operation", "🌍"), unsafe_allow_html=True)
                regions_html = "<br>".join([f"• {region}" for region in company["operational_footprint"]["regions_of_operation"]])
                st.markdown(f'<div class="card">{regions_html}</div>', unsafe_allow_html=True)
            
            # Primary Markets
            st.markdown(render_section_header("Primary Markets", "🎯"), unsafe_allow_html=True)
            markets_html = "".join([f'<div class="info-item"><strong>✓</strong> {market}</div>' for market in company["company_overview"]["primary_markets"]])
            st.markdown(f'<div class="card">{markets_html}</div>', unsafe_allow_html=True)
            
            # Industry Classification
            st.markdown(render_section_header("Industry Classification", "🏷️"), unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**NAICS Codes**")
                naics_df = pd.DataFrame(company["company_overview"]["naics_codes"])
                st.dataframe(naics_df, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("**SIC Codes**")
                sic_df = pd.DataFrame(company["company_overview"]["sic_codes"])
                st.dataframe(sic_df, use_container_width=True, hide_index=True)
            
            # Supply Chain & Procurement Analysis
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(render_section_header("Supply Chain & Procurement Analysis", "🔗"), unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Procurement Organization**")
                st.markdown(render_info_item("Maturity Level", company["procurement_organization"]["overall_maturity_level"]), unsafe_allow_html=True)
                st.markdown(render_info_item("Structure", company["procurement_organization"]["structure_and_reporting"]), unsafe_allow_html=True)
                st.markdown(render_info_item("Category Management", company["procurement_organization"]["category_management"]), unsafe_allow_html=True)
                st.markdown(render_info_item("CPO/Equivalent", company["procurement_organization"]["chief_procurement_officer"]), unsafe_allow_html=True)
            
            with col2:
                st.markdown("**Procurement Maturity Dimensions**")
                maturity = company["procurement_organization"]["maturity_dimensions"]
                for dim, data in maturity.items():
                    label = dim.replace("_", " ").title()
                    score = data["score"]
                    percentage = (score / 5) * 100
                    st.markdown(f"""
                    <div style="margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span style="font-size: 0.875rem;">{label}</span>
                            <span style="font-size: 0.875rem; font-weight: bold;">{data['value']}</span>
                        </div>
                        <div class="progress-container">
                            <div class="progress-fill" style="width: {percentage}%;">{score}/5</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # SWOT Analysis
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(render_section_header("Procurement SWOT Analysis", "📊"), unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(render_swot_item("💪 Strengths", company["procurement_swot"]["strengths"], "strengths"), unsafe_allow_html=True)
                st.markdown(render_swot_item("🎯 Opportunities", company["procurement_swot"]["opportunities"], "opportunities"), unsafe_allow_html=True)
            
            with col2:
                st.markdown(render_swot_item("⚠️ Weaknesses", company["procurement_swot"]["weaknesses"], "weaknesses"), unsafe_allow_html=True)
                st.markdown(render_swot_item("🚨 Threats", company["procurement_swot"]["threats"], "threats"), unsafe_allow_html=True)
            
            # Key Risks
            st.markdown(render_section_header("Procurement Risks", "⚠️"), unsafe_allow_html=True)
            risks_html = "".join([f'<div class="warning-box">⚠️ {risk}</div>' for risk in company["procurement_risks"]["key_risks"]])
            st.markdown(f'{risks_html}', unsafe_allow_html=True)
            st.markdown(f'''
            <div class="success-box">
                <strong>✅ Risk Mitigation Approach:</strong><br>
                {company["procurement_risks"]["risk_mitigation_approach"]}
            </div>
            ''', unsafe_allow_html=True)
        
        # =============================================
        # TAB 2: FINANCIALS
        # =============================================
        with tab2:
            st.markdown(render_section_header("Financial Overview", "💰"), unsafe_allow_html=True)
            
            # Métricas principales
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="label">2024 Revenue</div>
                    <div class="value">${company['financials']['revenue_estimates']['2024']}B</div>
                    <div class="label">USD</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="label">2023 Revenue</div>
                    <div class="value">${company['financials']['revenue_estimates']['2023']}B</div>
                    <div class="label">USD</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                yoy_change = ((company['financials']['revenue_estimates']['2024'] - company['financials']['revenue_estimates']['2023']) / company['financials']['revenue_estimates']['2023']) * 100
                st.markdown(f"""
                <div class="metric-card">
                    <div class="label">YoY Change</div>
                    <div class="value">{yoy_change:.1f}%</div>
                    <div class="label">2023 → 2024</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Revenue Chart
            st.markdown(render_section_header("Revenue Trend", "📈"), unsafe_allow_html=True)
            
            revenue_data = pd.DataFrame({
                'Year': ['2023', '2024'],
                'Revenue (USD Billions)': [
                    company['financials']['revenue_estimates']['2023'],
                    company['financials']['revenue_estimates']['2024']
                ]
            })
            
            st.bar_chart(revenue_data.set_index('Year'), color=COLORS['emerald'])
            
            # Additional Financial Metrics
            st.markdown(render_section_header("Asset Information", "🏗️"), unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(render_info_item("Equipment Fleet", f"{company['workforce']['equipment_fleet']:,} units"), unsafe_allow_html=True)
            with col2:
                st.markdown(render_info_item("Equipment Replacement Value", f"${company['financials']['equipment_replacement_value']}B USD"), unsafe_allow_html=True)
            
            # Disclaimer
            st.markdown(f"""
            <div class="warning-box">
                <strong>⚠️ Note:</strong> {company['financials']['source_note']}
            </div>
            """, unsafe_allow_html=True)
        
        # =============================================
        # TAB 3: COST OPTIMIZATION PROJECTION
        # =============================================
        with tab3:
            st.markdown(render_section_header("Cost Optimization Projection", "📈"), unsafe_allow_html=True)
            
            # Obtener el BXT_L2 y el median savings correspondiente
            bxt_l2 = company.get("bxt_l2", "Default")
            median_savings_rate = MEDIAN_SAVINGS_BY_BXT_L2.get(bxt_l2, MEDIAN_SAVINGS_BY_BXT_L2["Default"])
            
            st.markdown(f"""
            <div class="info-box">
                <strong>📊 Industry Classification (BXT_L2):</strong> {bxt_l2}<br>
                <strong>📈 Median Projected Savings Rate:</strong> {median_savings_rate*100:.1f}%
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Input para TAM
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### 💵 Enter Total Addressable Market (TAM)")
                tam_input = st.number_input(
                    "TAM (in USD millions)",
                    min_value=0.0,
                    max_value=100000.0,
                    value=100.0,
                    step=10.0,
                    format="%.2f",
                    help="Enter the Total Addressable Market in millions of USD"
                )
            
            with col2:
                st.markdown("### 📊 Savings Parameters")
                st.markdown(f"""
                <div class="meta-card">
                    <div class="meta-label">BXT_L2 Category</div>
                    <div class="meta-value">{bxt_l2}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="meta-card">
                    <div class="meta-label">Median Projected Savings</div>
                    <div class="meta-value">{median_savings_rate*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Cálculos
            projected_savings = tam_input * median_savings_rate
            conservative_savings = tam_input * (median_savings_rate * 0.7)
            optimistic_savings = tam_input * (median_savings_rate * 1.3)
            
            # Resultados
            st.markdown(render_section_header("Projected Savings Analysis", "💰"), unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #C39D7B 0%, #A95228 100%);">
                    <div class="label">Conservative Estimate</div>
                    <div class="value">${conservative_savings:,.2f}M</div>
                    <div class="label">({median_savings_rate*70:.1f}% of TAM)</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="label">Median Projection</div>
                    <div class="value">${projected_savings:,.2f}M</div>
                    <div class="label">({median_savings_rate*100:.1f}% of TAM)</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #A5CD24 0%, #1B5E5C 100%);">
                    <div class="label">Optimistic Estimate</div>
                    <div class="value">${optimistic_savings:,.2f}M</div>
                    <div class="label">({median_savings_rate*130:.1f}% of TAM)</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tabla de proyección
            st.markdown(render_section_header("Savings Breakdown", "📋"), unsafe_allow_html=True)
            
            savings_df = pd.DataFrame({
                'Scenario': ['Conservative (70%)', 'Median', 'Optimistic (130%)'],
                'Savings Rate': [f"{median_savings_rate*70:.2f}%", f"{median_savings_rate*100:.2f}%", f"{median_savings_rate*130:.2f}%"],
                'Projected Savings (USD M)': [f"${conservative_savings:,.2f}", f"${projected_savings:,.2f}", f"${optimistic_savings:,.2f}"],
                'Savings as % of TAM': [f"{(conservative_savings/tam_input)*100:.2f}%" if tam_input > 0 else "0%",
                                        f"{(projected_savings/tam_input)*100:.2f}%" if tam_input > 0 else "0%",
                                        f"{(optimistic_savings/tam_input)*100:.2f}%" if tam_input > 0 else "0%"]
            })
            
            st.dataframe(savings_df, use_container_width=True, hide_index=True)
            
            # Visualización
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(render_section_header("Savings Visualization", "📊"), unsafe_allow_html=True)
            
            chart_data = pd.DataFrame({
                'Scenario': ['Conservative', 'Median', 'Optimistic'],
                'Savings (USD M)': [conservative_savings, projected_savings, optimistic_savings]
            })
            
            st.bar_chart(chart_data.set_index('Scenario'), color=COLORS['emerald'])
            
            # Notas y metodología
            st.markdown(f"""
            <div class="info-box">
                <strong>📝 Methodology Notes:</strong><br>
                <ul style="margin-top: 8px; padding-left: 20px;">
                    <li>Median Projected Savings is determined by the BXT_L2 industry classification</li>
                    <li>Conservative estimate applies a 30% reduction to the median rate</li>
                    <li>Optimistic estimate applies a 30% increase to the median rate</li>
                    <li>Actual savings may vary based on implementation, market conditions, and company-specific factors</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Tabla de referencia de BXT_L2
            with st.expander("📋 View BXT_L2 Savings Reference Table"):
                ref_data = pd.DataFrame([
                    {"BXT_L2 Category": k, "Median Savings Rate": f"{v*100:.1f}%"} 
                    for k, v in MEDIAN_SAVINGS_BY_BXT_L2.items() if k != "Default"
                ])
                st.dataframe(ref_data, use_container_width=True, hide_index=True)
    
    else:
        st.markdown("""
        <div class="warning-box">
            <strong>⚠️ Company not found</strong><br>
            No data available for the searched company. Try searching for "Kiewit Corporation" or "Kiewit".
        </div>
        """, unsafe_allow_html=True)

else:
    # Estado inicial - mostrar instrucciones
    st.markdown("""
    <div class="card" style="text-align: center; padding: 60px;">
        <h2 style="color: #1B5E5C;">👋 Welcome to the Company Intelligence Dashboard</h2>
        <p style="font-size: 1.1rem; color: #666; margin-top: 16px;">
            Enter a company name in the search bar above to view detailed information.
        </p>
        <p style="color: #999; margin-top: 24px;">
            <strong>Available companies:</strong> Kiewit Corporation
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p><strong>Company Intelligence Dashboard</strong></p>
    <p>Due Diligence & Procurement Analysis Platform</p>
    <p style="margin-top: 10px; font-size: 0.85em; opacity: 0.8;">
        This report is intended for informational and due diligence purposes only.
    </p>
</div>
""", unsafe_allow_html=True)
