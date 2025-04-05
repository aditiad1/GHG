import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from utils.calculations import calculate_emissions
from utils.reports import generate_report
from utils.visualization import create_emissions_pie_chart, create_emissions_bar_chart
import os

st.set_page_config(
    page_title="Emissions Calculator",
    page_icon="🧮",
    layout="wide"
)

st.title("GHG Emissions Calculator")

if not st.session_state.company_data['name']:
    st.warning("Please enter your organization information on the home page first.")
    st.stop()

# Tabs for different scopes
st.markdown("### Enter your emissions data")
st.markdown("Complete each section to calculate your organization's carbon footprint.")

tabs = st.tabs(["Scope 1 (Direct)", "Scope 2 (Indirect)", "Scope 3 (Value Chain)", "Results"])

# Scope 1 emissions (direct emissions)
with tabs[0]:
    st.subheader("Scope 1: Direct Emissions")
    st.markdown("""
    Direct emissions from owned or controlled sources. These include:
    - Stationary combustion (boilers, furnaces, etc.)
    - Mobile combustion (vehicles)
    - Process emissions
    - Fugitive emissions (leaks, refrigerants)
    """)
    
    # Stationary combustion
    st.markdown("#### Stationary Combustion")
    col1, col2 = st.columns(2)
    
    with col1:
        natural_gas = st.number_input("Natural Gas (m³)", min_value=0.0, 
                                      value=float(st.session_state.emissions_data['scope1'].get('natural_gas', 0)))
        diesel_stationary = st.number_input("Diesel for Generators (liters)", min_value=0.0, 
                                           value=float(st.session_state.emissions_data['scope1'].get('diesel_stationary', 0)))
        fuel_oil = st.number_input("Fuel Oil (liters)", min_value=0.0, 
                                  value=float(st.session_state.emissions_data['scope1'].get('fuel_oil', 0)))
    
    with col2:
        propane = st.number_input("Propane (kg)", min_value=0.0, 
                                 value=float(st.session_state.emissions_data['scope1'].get('propane', 0)))
        coal = st.number_input("Coal (kg)", min_value=0.0, 
                              value=float(st.session_state.emissions_data['scope1'].get('coal', 0)))

    # Mobile combustion
    st.markdown("#### Mobile Combustion")
    col1, col2 = st.columns(2)
    
    with col1:
        gasoline = st.number_input("Gasoline (liters)", min_value=0.0, 
                                  value=float(st.session_state.emissions_data['scope1'].get('gasoline', 0)))
        diesel_mobile = st.number_input("Diesel for Vehicles (liters)", min_value=0.0, 
                                       value=float(st.session_state.emissions_data['scope1'].get('diesel_mobile', 0)))
    
    with col2:
        jet_fuel = st.number_input("Jet Fuel (liters)", min_value=0.0, 
                                  value=float(st.session_state.emissions_data['scope1'].get('jet_fuel', 0)))
        marine_fuel = st.number_input("Marine Fuel (liters)", min_value=0.0, 
                                     value=float(st.session_state.emissions_data['scope1'].get('marine_fuel', 0)))

    # Refrigerants and process emissions
    st.markdown("#### Refrigerants and Process Emissions")
    col1, col2 = st.columns(2)
    
    with col1:
        refrigerant_r22 = st.number_input("R-22 Refrigerant (kg)", min_value=0.0, 
                                         value=float(st.session_state.emissions_data['scope1'].get('refrigerant_r22', 0)))
        refrigerant_r410a = st.number_input("R-410A Refrigerant (kg)", min_value=0.0, 
                                           value=float(st.session_state.emissions_data['scope1'].get('refrigerant_r410a', 0)))
    
    with col2:
        process_emissions = st.number_input("Process Emissions (tCO2e)", min_value=0.0, 
                                           value=float(st.session_state.emissions_data['scope1'].get('process_emissions', 0)))
        other_direct = st.number_input("Other Direct Emissions (tCO2e)", min_value=0.0, 
                                       value=float(st.session_state.emissions_data['scope1'].get('other_direct', 0)))
    
    if st.button("Save Scope 1 Data"):
        st.session_state.emissions_data['scope1'] = {
            'natural_gas': natural_gas,
            'diesel_stationary': diesel_stationary,
            'fuel_oil': fuel_oil,
            'propane': propane,
            'coal': coal,
            'gasoline': gasoline,
            'diesel_mobile': diesel_mobile,
            'jet_fuel': jet_fuel,
            'marine_fuel': marine_fuel,
            'refrigerant_r22': refrigerant_r22,
            'refrigerant_r410a': refrigerant_r410a,
            'process_emissions': process_emissions,
            'other_direct': other_direct
        }
        st.success("Scope 1 emissions data saved successfully!")

# Scope 2 emissions (indirect emissions from purchased energy)
with tabs[1]:
    st.subheader("Scope 2: Indirect Emissions from Purchased Energy")
    st.markdown("""
    Indirect emissions from the generation of purchased energy. These include:
    - Purchased electricity
    - Purchased steam, heat, or cooling
    
    You can calculate Scope 2 emissions using either the location-based or market-based method.
    """)
    
    calculation_method = st.radio(
        "Calculation Method",
        ["Location-based", "Market-based"], 
        index=0 if st.session_state.emissions_data['scope2'].get('calculation_method', 'Location-based') == 'Location-based' else 1
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        purchased_electricity = st.number_input("Purchased Electricity (kWh)", min_value=0.0, 
                                              value=float(st.session_state.emissions_data['scope2'].get('purchased_electricity', 0)))
        
        if calculation_method == "Location-based":
            grid_region = st.selectbox(
                "Electricity Grid Region",
                [
                    "North America", "Europe", "Asia - China", "Asia - India",
                    "Asia - Japan", "Asia - Other", "South America", "Africa",
                    "Australia & Oceania"
                ],
                index=0 if st.session_state.emissions_data['scope2'].get('grid_region', '') == '' else 
                      [
                          "North America", "Europe", "Asia - China", "Asia - India",
                          "Asia - Japan", "Asia - Other", "South America", "Africa",
                          "Australia & Oceania"
                      ].index(st.session_state.emissions_data['scope2'].get('grid_region', 'North America'))
            )
        else:  # Market-based
            has_renewable_ppa = st.checkbox(
                "Renewable Energy Purchase Agreement", 
                value=st.session_state.emissions_data['scope2'].get('has_renewable_ppa', False)
            )
            if has_renewable_ppa:
                renewable_percentage = st.slider(
                    "Percentage of Renewable Energy (%)", 
                    min_value=0, 
                    max_value=100, 
                    value=int(st.session_state.emissions_data['scope2'].get('renewable_percentage', 0))
                )
            else:
                renewable_percentage = 0
    
    with col2:
        purchased_steam = st.number_input("Purchased Steam (GJ)", min_value=0.0, 
                                         value=float(st.session_state.emissions_data['scope2'].get('purchased_steam', 0)))
        purchased_cooling = st.number_input("Purchased Cooling (GJ)", min_value=0.0, 
                                          value=float(st.session_state.emissions_data['scope2'].get('purchased_cooling', 0)))
        purchased_heating = st.number_input("Purchased Heating (GJ)", min_value=0.0, 
                                          value=float(st.session_state.emissions_data['scope2'].get('purchased_heating', 0)))
    
    if st.button("Save Scope 2 Data"):
        scope2_data = {
            'calculation_method': calculation_method,
            'purchased_electricity': purchased_electricity,
            'purchased_steam': purchased_steam,
            'purchased_cooling': purchased_cooling,
            'purchased_heating': purchased_heating
        }
        
        if calculation_method == "Location-based":
            scope2_data['grid_region'] = grid_region
        else:  # Market-based
            scope2_data['has_renewable_ppa'] = has_renewable_ppa
            scope2_data['renewable_percentage'] = renewable_percentage if has_renewable_ppa else 0
        
        st.session_state.emissions_data['scope2'] = scope2_data
        st.success("Scope 2 emissions data saved successfully!")

# Scope 3 emissions (all other indirect emissions)
with tabs[2]:
    st.subheader("Scope 3: Value Chain Emissions")
    st.markdown("""
    All other indirect emissions that occur in a company's value chain. These include 15 categories:
    1. Purchased goods and services
    2. Capital goods
    3. Fuel and energy-related activities
    4. Upstream transportation and distribution
    5. Waste generated in operations
    6. Business travel
    7. Employee commuting
    8. Upstream leased assets
    9. Downstream transportation and distribution
    10. Processing of sold products
    11. Use of sold products
    12. End-of-life treatment of sold products
    13. Downstream leased assets
    14. Franchises
    15. Investments
    
    Note: Not all categories are relevant for all organizations.
    """)
    
    st.markdown("#### Upstream Categories")
    
    col1, col2 = st.columns(2)
    
    with col1:
        purchased_goods = st.number_input("1. Purchased Goods and Services ($ USD)", min_value=0.0,
                                        value=float(st.session_state.emissions_data['scope3'].get('purchased_goods', 0)))
        capital_goods = st.number_input("2. Capital Goods ($ USD)", min_value=0.0,
                                      value=float(st.session_state.emissions_data['scope3'].get('capital_goods', 0)))
        fuel_energy_related = st.number_input("3. Fuel and Energy-Related Activities (GJ)", min_value=0.0,
                                            value=float(st.session_state.emissions_data['scope3'].get('fuel_energy_related', 0)))
        upstream_transport = st.number_input("4. Upstream Transportation (tonne-km)", min_value=0.0,
                                           value=float(st.session_state.emissions_data['scope3'].get('upstream_transport', 0)))
        waste_operations = st.number_input("5. Waste Generated in Operations (tonnes)", min_value=0.0,
                                         value=float(st.session_state.emissions_data['scope3'].get('waste_operations', 0)))
    
    with col2:
        business_travel = st.number_input("6. Business Travel (passenger-km)", min_value=0.0,
                                        value=float(st.session_state.emissions_data['scope3'].get('business_travel', 0)))
        employee_commuting = st.number_input("7. Employee Commuting (passenger-km)", min_value=0.0,
                                           value=float(st.session_state.emissions_data['scope3'].get('employee_commuting', 0)))
        upstream_leased = st.number_input("8. Upstream Leased Assets (m²)", min_value=0.0,
                                        value=float(st.session_state.emissions_data['scope3'].get('upstream_leased', 0)))
    
    st.markdown("#### Downstream Categories")
    
    col1, col2 = st.columns(2)
    
    with col1:
        downstream_transport = st.number_input("9. Downstream Transportation (tonne-km)", min_value=0.0,
                                             value=float(st.session_state.emissions_data['scope3'].get('downstream_transport', 0)))
        processing_products = st.number_input("10. Processing of Sold Products (tonnes)", min_value=0.0,
                                            value=float(st.session_state.emissions_data['scope3'].get('processing_products', 0)))
        use_of_products = st.number_input("11. Use of Sold Products (units)", min_value=0.0,
                                        value=float(st.session_state.emissions_data['scope3'].get('use_of_products', 0)))
        product_avg_lifetime = st.number_input("Average Product Lifetime (years)", min_value=0.0, max_value=50.0, 
                                               value=float(st.session_state.emissions_data['scope3'].get('product_avg_lifetime', 10.0)))
    
    with col2:
        end_of_life = st.number_input("12. End-of-Life Treatment (tonnes)", min_value=0.0,
                                    value=float(st.session_state.emissions_data['scope3'].get('end_of_life', 0)))
        downstream_leased = st.number_input("13. Downstream Leased Assets (m²)", min_value=0.0,
                                          value=float(st.session_state.emissions_data['scope3'].get('downstream_leased', 0)))
        franchises = st.number_input("14. Franchises (number)", min_value=0.0,
                                   value=float(st.session_state.emissions_data['scope3'].get('franchises', 0)))
        investments = st.number_input("15. Investments ($ USD)", min_value=0.0,
                                    value=float(st.session_state.emissions_data['scope3'].get('investments', 0)))
    
    if st.button("Save Scope 3 Data"):
        st.session_state.emissions_data['scope3'] = {
            'purchased_goods': purchased_goods,
            'capital_goods': capital_goods,
            'fuel_energy_related': fuel_energy_related,
            'upstream_transport': upstream_transport,
            'waste_operations': waste_operations,
            'business_travel': business_travel,
            'employee_commuting': employee_commuting,
            'upstream_leased': upstream_leased,
            'downstream_transport': downstream_transport,
            'processing_products': processing_products,
            'use_of_products': use_of_products,
            'product_avg_lifetime': product_avg_lifetime,
            'end_of_life': end_of_life,
            'downstream_leased': downstream_leased,
            'franchises': franchises,
            'investments': investments
        }
        st.success("Scope 3 emissions data saved successfully!")

# Results tab
with tabs[3]:
    st.subheader("Emissions Calculation Results")
    
    if st.button("Calculate Total Emissions"):
        # Calculate emissions using the data from all scopes
        emissions_results = calculate_emissions(
            st.session_state.emissions_data['scope1'],
            st.session_state.emissions_data['scope2'],
            st.session_state.emissions_data['scope3']
        )
        
        st.session_state.total_emissions = emissions_results['total']
        st.session_state.emissions_by_scope = {
            'scope1': emissions_results['scope1_total'],
            'scope2': emissions_results['scope2_total'],
            'scope3': emissions_results['scope3_total']
        }
        
        # Set breakdown by category
        st.session_state.scope1_breakdown = emissions_results['scope1_breakdown']
        st.session_state.scope2_breakdown = emissions_results['scope2_breakdown']
        st.session_state.scope3_breakdown = emissions_results['scope3_breakdown']
        
        # Calculate targets
        base_emissions = st.session_state.total_emissions
        # Science-based target: 42% reduction by 2030 (aligned with 1.5°C pathway)
        st.session_state.targets = {
            '2030': base_emissions * 0.58,  # 42% reduction
            'annual_reduction': base_emissions * 0.042  # 4.2% annual reduction
        }
        
        st.session_state.calculation_complete = True
        st.success("Emissions calculation completed successfully!")
    
    if st.session_state.calculation_complete:
        st.markdown("### Total GHG Emissions")
        
        # Display total emissions and breakdown
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Emissions", f"{st.session_state.total_emissions:.2f} tCO2e")
        with col2:
            st.metric("Emissions per Employee", 
                     f"{st.session_state.total_emissions / st.session_state.company_data['employees']:.2f} tCO2e")
        with col3:
            if st.session_state.company_data['revenue'] > 0:
                st.metric("Emissions Intensity", 
                         f"{st.session_state.total_emissions / st.session_state.company_data['revenue']:.2f} tCO2e/million USD")
        
        st.markdown("### Emissions by Scope")
        
        # Create pie chart for scope breakdown
        fig_pie = create_emissions_pie_chart(
            [
                st.session_state.emissions_by_scope['scope1'],
                st.session_state.emissions_by_scope['scope2'],
                st.session_state.emissions_by_scope['scope3']
            ],
            ["Scope 1", "Scope 2", "Scope 3"]
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Create bar chart for detailed breakdown
        scope1_data = st.session_state.scope1_breakdown
        scope2_data = st.session_state.scope2_breakdown
        scope3_data = st.session_state.scope3_breakdown
        
        # Prepare data for bar chart
        categories = []
        values = []
        scopes = []
        
        # Add Scope 1 breakdown
        for category, value in scope1_data.items():
            categories.append(category)
            values.append(value)
            scopes.append("Scope 1")
        
        # Add Scope 2 breakdown
        for category, value in scope2_data.items():
            categories.append(category)
            values.append(value)
            scopes.append("Scope 2")
        
        # Add Scope 3 breakdown
        for category, value in scope3_data.items():
            categories.append(category)
            values.append(value)
            scopes.append("Scope 3")
        
        # Create the bar chart
        fig_bar = create_emissions_bar_chart(categories, values, scopes)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Generate and download report
        st.markdown("### Emissions Report")
        if st.button("Generate Emissions Report PDF"):
            # Call function to generate report
            report_path = generate_report(
                st.session_state.company_data,
                st.session_state.total_emissions,
                st.session_state.emissions_by_scope,
                st.session_state.scope1_breakdown,
                st.session_state.scope2_breakdown,
                st.session_state.scope3_breakdown,
                st.session_state.targets
            )
            
            # Provide download link (in a real app this would be a file download)
            st.success("Report generated successfully!")
            st.info("Your report would normally be available for download here. In this environment, please see the console for the report output.")
    else:
        st.info("Please enter your emissions data in the Scope 1, 2, and 3 tabs, then click 'Calculate Total Emissions' to see your results.")
