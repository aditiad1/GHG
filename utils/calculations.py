import numpy as np
import pandas as pd

# Emission factors (simplified for this example)
# These would normally be more detailed and region-specific
EMISSION_FACTORS = {
    # Scope 1 emission factors
    "natural_gas": 0.00185,  # tCO2e per m³
    "diesel_stationary": 0.00269,  # tCO2e per liter
    "fuel_oil": 0.00276,  # tCO2e per liter
    "propane": 0.00151,  # tCO2e per kg
    "coal": 0.00246,  # tCO2e per kg
    "gasoline": 0.00231,  # tCO2e per liter
    "diesel_mobile": 0.00267,  # tCO2e per liter
    "jet_fuel": 0.00249,  # tCO2e per liter
    "marine_fuel": 0.00276,  # tCO2e per liter
    "refrigerant_r22": 1.810,  # tCO2e per kg
    "refrigerant_r410a": 2.088,  # tCO2e per kg
    
    # Scope 2 emission factors for electricity by region (tCO2e per kWh)
    "electricity": {
        "North America": 0.000429,
        "Europe": 0.000276,
        "Asia - China": 0.000623,
        "Asia - India": 0.000708,
        "Asia - Japan": 0.000457,
        "Asia - Other": 0.000536,
        "South America": 0.000192,
        "Africa": 0.000639,
        "Australia & Oceania": 0.000533
    },
    "steam": 0.072,  # tCO2e per GJ
    "cooling": 0.065,  # tCO2e per GJ
    "heating": 0.067,  # tCO2e per GJ
    
    # Scope 3 emission factors (simplified)
    "purchased_goods": 0.00033,  # tCO2e per USD
    "capital_goods": 0.00026,  # tCO2e per USD
    "fuel_energy_related": 0.0187,  # tCO2e per GJ
    "upstream_transport": 0.00011,  # tCO2e per tonne-km
    "waste_operations": 0.433,  # tCO2e per tonne
    "business_travel": 0.00017,  # tCO2e per passenger-km
    "employee_commuting": 0.00015,  # tCO2e per passenger-km
    "upstream_leased": 0.025,  # tCO2e per m²
    "downstream_transport": 0.00011,  # tCO2e per tonne-km
    "processing_products": 0.36,  # tCO2e per tonne
    "use_of_products": 0.23,  # tCO2e per unit-year
    "end_of_life": 0.252,  # tCO2e per tonne
    "downstream_leased": 0.023,  # tCO2e per m²
    "franchises": 18.5,  # tCO2e per franchise
    "investments": 0.00001  # tCO2e per USD
}

def calculate_emissions(scope1_data, scope2_data, scope3_data):
    """
    Calculate total emissions from all scopes
    
    Args:
        scope1_data (dict): Dictionary of scope 1 emission sources and values
        scope2_data (dict): Dictionary of scope 2 emission sources and values
        scope3_data (dict): Dictionary of scope 3 emission sources and values
        
    Returns:
        dict: Dictionary containing total emissions and breakdown by scope
    """
    results = {
        'scope1_total': 0,
        'scope2_total': 0,
        'scope3_total': 0,
        'total': 0,
        'scope1_breakdown': {},
        'scope2_breakdown': {},
        'scope3_breakdown': {}
    }
    
    # Calculate Scope 1 emissions
    scope1_emissions = 0
    scope1_breakdown = {}
    
    # Stationary combustion
    if 'natural_gas' in scope1_data:
        natural_gas_emissions = scope1_data['natural_gas'] * EMISSION_FACTORS['natural_gas']
        scope1_emissions += natural_gas_emissions
        scope1_breakdown['Natural Gas'] = natural_gas_emissions
    
    if 'diesel_stationary' in scope1_data:
        diesel_stationary_emissions = scope1_data['diesel_stationary'] * EMISSION_FACTORS['diesel_stationary']
        scope1_emissions += diesel_stationary_emissions
        scope1_breakdown['Stationary Diesel'] = diesel_stationary_emissions
    
    if 'fuel_oil' in scope1_data:
        fuel_oil_emissions = scope1_data['fuel_oil'] * EMISSION_FACTORS['fuel_oil']
        scope1_emissions += fuel_oil_emissions
        scope1_breakdown['Fuel Oil'] = fuel_oil_emissions
    
    if 'propane' in scope1_data:
        propane_emissions = scope1_data['propane'] * EMISSION_FACTORS['propane']
        scope1_emissions += propane_emissions
        scope1_breakdown['Propane'] = propane_emissions
    
    if 'coal' in scope1_data:
        coal_emissions = scope1_data['coal'] * EMISSION_FACTORS['coal']
        scope1_emissions += coal_emissions
        scope1_breakdown['Coal'] = coal_emissions
    
    # Mobile combustion
    if 'gasoline' in scope1_data:
        gasoline_emissions = scope1_data['gasoline'] * EMISSION_FACTORS['gasoline']
        scope1_emissions += gasoline_emissions
        scope1_breakdown['Gasoline'] = gasoline_emissions
    
    if 'diesel_mobile' in scope1_data:
        diesel_mobile_emissions = scope1_data['diesel_mobile'] * EMISSION_FACTORS['diesel_mobile']
        scope1_emissions += diesel_mobile_emissions
        scope1_breakdown['Mobile Diesel'] = diesel_mobile_emissions
    
    if 'jet_fuel' in scope1_data:
        jet_fuel_emissions = scope1_data['jet_fuel'] * EMISSION_FACTORS['jet_fuel']
        scope1_emissions += jet_fuel_emissions
        scope1_breakdown['Jet Fuel'] = jet_fuel_emissions
    
    if 'marine_fuel' in scope1_data:
        marine_fuel_emissions = scope1_data['marine_fuel'] * EMISSION_FACTORS['marine_fuel']
        scope1_emissions += marine_fuel_emissions
        scope1_breakdown['Marine Fuel'] = marine_fuel_emissions
    
    # Refrigerants and process emissions
    if 'refrigerant_r22' in scope1_data:
        r22_emissions = scope1_data['refrigerant_r22'] * EMISSION_FACTORS['refrigerant_r22']
        scope1_emissions += r22_emissions
        scope1_breakdown['R-22 Refrigerant'] = r22_emissions
    
    if 'refrigerant_r410a' in scope1_data:
        r410a_emissions = scope1_data['refrigerant_r410a'] * EMISSION_FACTORS['refrigerant_r410a']
        scope1_emissions += r410a_emissions
        scope1_breakdown['R-410A Refrigerant'] = r410a_emissions
    
    if 'process_emissions' in scope1_data:
        process_emissions = scope1_data['process_emissions']  # Already in tCO2e
        scope1_emissions += process_emissions
        scope1_breakdown['Process Emissions'] = process_emissions
    
    if 'other_direct' in scope1_data:
        other_direct_emissions = scope1_data['other_direct']  # Already in tCO2e
        scope1_emissions += other_direct_emissions
        scope1_breakdown['Other Direct'] = other_direct_emissions
    
    # Calculate Scope 2 emissions
    scope2_emissions = 0
    scope2_breakdown = {}
    
    if 'purchased_electricity' in scope2_data:
        electricity_emissions = 0
        
        if scope2_data.get('calculation_method') == 'Location-based' and 'grid_region' in scope2_data:
            grid_region = scope2_data['grid_region']
            electricity_factor = EMISSION_FACTORS['electricity'].get(grid_region, EMISSION_FACTORS['electricity']['North America'])
            electricity_emissions = scope2_data['purchased_electricity'] * electricity_factor
        else:  # Market-based method
            electricity_factor = EMISSION_FACTORS['electricity']['North America']  # Default factor
            has_renewable_ppa = scope2_data.get('has_renewable_ppa', False)
            renewable_percentage = scope2_data.get('renewable_percentage', 0) if has_renewable_ppa else 0
            
            # Apply renewable percentage reduction if applicable
            conventional_electricity = scope2_data['purchased_electricity'] * (1 - renewable_percentage / 100)
            electricity_emissions = conventional_electricity * electricity_factor
        
        scope2_emissions += electricity_emissions
        scope2_breakdown['Purchased Electricity'] = electricity_emissions
    
    if 'purchased_steam' in scope2_data:
        steam_emissions = scope2_data['purchased_steam'] * EMISSION_FACTORS['steam']
        scope2_emissions += steam_emissions
        scope2_breakdown['Purchased Steam'] = steam_emissions
    
    if 'purchased_cooling' in scope2_data:
        cooling_emissions = scope2_data['purchased_cooling'] * EMISSION_FACTORS['cooling']
        scope2_emissions += cooling_emissions
        scope2_breakdown['Purchased Cooling'] = cooling_emissions
    
    if 'purchased_heating' in scope2_data:
        heating_emissions = scope2_data['purchased_heating'] * EMISSION_FACTORS['heating']
        scope2_emissions += heating_emissions
        scope2_breakdown['Purchased Heating'] = heating_emissions
    
    # Calculate Scope 3 emissions
    scope3_emissions = 0
    scope3_breakdown = {}
    
    # Upstream categories
    if 'purchased_goods' in scope3_data:
        purchased_goods_emissions = scope3_data['purchased_goods'] * EMISSION_FACTORS['purchased_goods']
        scope3_emissions += purchased_goods_emissions
        scope3_breakdown['Purchased Goods & Services'] = purchased_goods_emissions
    
    if 'capital_goods' in scope3_data:
        capital_goods_emissions = scope3_data['capital_goods'] * EMISSION_FACTORS['capital_goods']
        scope3_emissions += capital_goods_emissions
        scope3_breakdown['Capital Goods'] = capital_goods_emissions
    
    if 'fuel_energy_related' in scope3_data:
        fuel_energy_emissions = scope3_data['fuel_energy_related'] * EMISSION_FACTORS['fuel_energy_related']
        scope3_emissions += fuel_energy_emissions
        scope3_breakdown['Fuel & Energy-Related'] = fuel_energy_emissions
    
    if 'upstream_transport' in scope3_data:
        upstream_transport_emissions = scope3_data['upstream_transport'] * EMISSION_FACTORS['upstream_transport']
        scope3_emissions += upstream_transport_emissions
        scope3_breakdown['Upstream Transportation'] = upstream_transport_emissions
    
    if 'waste_operations' in scope3_data:
        waste_emissions = scope3_data['waste_operations'] * EMISSION_FACTORS['waste_operations']
        scope3_emissions += waste_emissions
        scope3_breakdown['Waste in Operations'] = waste_emissions
    
    if 'business_travel' in scope3_data:
        travel_emissions = scope3_data['business_travel'] * EMISSION_FACTORS['business_travel']
        scope3_emissions += travel_emissions
        scope3_breakdown['Business Travel'] = travel_emissions
    
    if 'employee_commuting' in scope3_data:
        commuting_emissions = scope3_data['employee_commuting'] * EMISSION_FACTORS['employee_commuting']
        scope3_emissions += commuting_emissions
        scope3_breakdown['Employee Commuting'] = commuting_emissions
    
    if 'upstream_leased' in scope3_data:
        upstream_leased_emissions = scope3_data['upstream_leased'] * EMISSION_FACTORS['upstream_leased']
        scope3_emissions += upstream_leased_emissions
        scope3_breakdown['Upstream Leased Assets'] = upstream_leased_emissions
    
    # Downstream categories
    if 'downstream_transport' in scope3_data:
        downstream_transport_emissions = scope3_data['downstream_transport'] * EMISSION_FACTORS['downstream_transport']
        scope3_emissions += downstream_transport_emissions
        scope3_breakdown['Downstream Transportation'] = downstream_transport_emissions
    
    if 'processing_products' in scope3_data:
        processing_emissions = scope3_data['processing_products'] * EMISSION_FACTORS['processing_products']
        scope3_emissions += processing_emissions
        scope3_breakdown['Processing of Sold Products'] = processing_emissions
    
    if 'use_of_products' in scope3_data and 'product_avg_lifetime' in scope3_data:
        use_phase_emissions = (
            scope3_data['use_of_products'] * 
            EMISSION_FACTORS['use_of_products'] * 
            scope3_data['product_avg_lifetime']
        )
        scope3_emissions += use_phase_emissions
        scope3_breakdown['Use of Sold Products'] = use_phase_emissions
    
    if 'end_of_life' in scope3_data:
        end_of_life_emissions = scope3_data['end_of_life'] * EMISSION_FACTORS['end_of_life']
        scope3_emissions += end_of_life_emissions
        scope3_breakdown['End-of-Life Treatment'] = end_of_life_emissions
    
    if 'downstream_leased' in scope3_data:
        downstream_leased_emissions = scope3_data['downstream_leased'] * EMISSION_FACTORS['downstream_leased']
        scope3_emissions += downstream_leased_emissions
        scope3_breakdown['Downstream Leased Assets'] = downstream_leased_emissions
    
    if 'franchises' in scope3_data:
        franchise_emissions = scope3_data['franchises'] * EMISSION_FACTORS['franchises']
        scope3_emissions += franchise_emissions
        scope3_breakdown['Franchises'] = franchise_emissions
    
    if 'investments' in scope3_data:
        investment_emissions = scope3_data['investments'] * EMISSION_FACTORS['investments']
        scope3_emissions += investment_emissions
        scope3_breakdown['Investments'] = investment_emissions
    
    # Set results
    results['scope1_total'] = scope1_emissions
    results['scope2_total'] = scope2_emissions
    results['scope3_total'] = scope3_emissions
    results['total'] = scope1_emissions + scope2_emissions + scope3_emissions
    
    # Create breakdown dictionaries with non-zero values only
    results['scope1_breakdown'] = {k: v for k, v in scope1_breakdown.items() if v > 0}
    results['scope2_breakdown'] = {k: v for k, v in scope2_breakdown.items() if v > 0}
    results['scope3_breakdown'] = {k: v for k, v in scope3_breakdown.items() if v > 0}
    
    return results
