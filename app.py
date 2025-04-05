import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="GHG Emissions Calculator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'company_data' not in st.session_state:
    st.session_state.company_data = {
        'name': '',
        'industry': '',
        'employees': 0,
        'revenue': 0,
        'year': 2023
    }

if 'emissions_data' not in st.session_state:
    st.session_state.emissions_data = {
        'scope1': {},
        'scope2': {},
        'scope3': {}
    }

if 'calculation_complete' not in st.session_state:
    st.session_state.calculation_complete = False

if 'total_emissions' not in st.session_state:
    st.session_state.total_emissions = 0

if 'emissions_by_scope' not in st.session_state:
    st.session_state.emissions_by_scope = {
        'scope1': 0,
        'scope2': 0,
        'scope3': 0
    }

if 'targets' not in st.session_state:
    st.session_state.targets = {
        '2030': 0
    }

# Main page content
st.title("Organizational GHG Emissions Calculator")

st.markdown("""
### Welcome to the GHG Emissions Calculator
This tool helps organizations:
- Calculate their greenhouse gas emissions across Scope 1, 2, and 3
- Set science-based reduction targets for 2030
- Explore carbon credit options
- Compare with global benchmarks
- Receive tailored suggestions to reduce emissions

**Use the sidebar to navigate through different sections of the application.**
""")

# Company information collection
st.header("Organization Information")
st.markdown("Before calculating your emissions, please provide some basic information about your organization.")

col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input("Organization Name", st.session_state.company_data['name'])
    industry = st.selectbox(
        "Industry Sector",
        [
            "",
            "Agriculture",
            "Automotive",
            "Aviation",
            "Chemical",
            "Construction",
            "Education",
            "Energy",
            "Financial Services",
            "Food & Beverage",
            "Healthcare",
            "Hospitality",
            "Information Technology",
            "Manufacturing",
            "Mining",
            "Real Estate",
            "Retail",
            "Telecommunications",
            "Transportation",
            "Utilities",
            "Other"
        ],
        index=0 if st.session_state.company_data['industry'] == '' else 
              [
                  "",
                  "Agriculture",
                  "Automotive",
                  "Aviation",
                  "Chemical",
                  "Construction",
                  "Education",
                  "Energy",
                  "Financial Services",
                  "Food & Beverage",
                  "Healthcare",
                  "Hospitality",
                  "Information Technology",
                  "Manufacturing",
                  "Mining",
                  "Real Estate",
                  "Retail",
                  "Telecommunications",
                  "Transportation",
                  "Utilities",
                  "Other"
              ].index(st.session_state.company_data['industry'])
    )

with col2:
    employees = st.number_input("Number of Employees", min_value=1, value=st.session_state.company_data['employees'] if st.session_state.company_data['employees'] > 0 else 1)
    revenue = st.number_input("Annual Revenue (USD millions)", min_value=0.0, value=float(st.session_state.company_data['revenue'] if st.session_state.company_data['revenue'] > 0 else 0.0))
    reporting_year = st.selectbox(
        "Reporting Year",
        list(range(2020, 2024)),
        index=list(range(2020, 2024)).index(st.session_state.company_data['year']) if st.session_state.company_data['year'] in range(2020, 2024) else 3
    )

if st.button("Save Organization Information"):
    st.session_state.company_data = {
        'name': company_name,
        'industry': industry,
        'employees': employees,
        'revenue': revenue,
        'year': reporting_year
    }
    st.success("Organization information saved successfully!")

# Display instructions for next steps
if st.session_state.company_data['name']:
    st.info("""
    **Next Steps**:
    
    1. Navigate to the **Emissions Calculator** page to input your emissions data
    2. Once calculations are complete, explore your reduction targets for 2030
    3. Browse the carbon credits marketplace to offset your remaining emissions
    4. See how your footprint compares to global benchmarks
    5. Review tailored suggestions to reduce your emissions
    6. Access third-party calculators and resources in the External Resources page
    
    Use the sidebar menu to navigate between these sections.
    """)

# Footer
st.markdown("---")
st.markdown("© 2025 GHG Emissions Calculator | Helping organizations track and reduce their carbon footprint")
