# Emission factors (simplified)
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

# Industry benchmarks for emissions intensity (tCO2e per $M revenue)
INDUSTRY_BENCHMARKS = {
    "Agriculture": {"avg_intensity": 120, "best_performer": 60, "worst_performer": 250},
    "Automotive": {"avg_intensity": 65, "best_performer": 25, "worst_performer": 150},
    "Aviation": {"avg_intensity": 350, "best_performer": 180, "worst_performer": 600},
    "Chemical": {"avg_intensity": 180, "best_performer": 90, "worst_performer": 350},
    "Construction": {"avg_intensity": 75, "best_performer": 30, "worst_performer": 200},
    "Education": {"avg_intensity": 40, "best_performer": 15, "worst_performer": 100},
    "Energy": {"avg_intensity": 250, "best_performer": 100, "worst_performer": 500},
    "Financial Services": {"avg_intensity": 20, "best_performer": 5, "worst_performer": 60},
    "Food & Beverage": {"avg_intensity": 85, "best_performer": 35, "worst_performer": 200},
    "Healthcare": {"avg_intensity": 55, "best_performer": 20, "worst_performer": 120},
    "Hospitality": {"avg_intensity": 70, "best_performer": 25, "worst_performer": 150},
    "Information Technology": {"avg_intensity": 30, "best_performer": 10, "worst_performer": 80},
    "Manufacturing": {"avg_intensity": 100, "best_performer": 45, "worst_performer": 220},
    "Mining": {"avg_intensity": 300, "best_performer": 150, "worst_performer": 600},
    "Real Estate": {"avg_intensity": 60, "best_performer": 25, "worst_performer": 130},
    "Retail": {"avg_intensity": 45, "best_performer": 20, "worst_performer": 110},
    "Telecommunications": {"avg_intensity": 35, "best_performer": 15, "worst_performer": 80},
    "Transportation": {"avg_intensity": 150, "best_performer": 70, "worst_performer": 300},
    "Utilities": {"avg_intensity": 200, "best_performer": 90, "worst_performer": 400},
    "Other": {"avg_intensity": 80, "best_performer": 30, "worst_performer": 200}
}

# Industry average scope distribution (percentage)
SCOPE_DISTRIBUTIONS = {
    "Agriculture": {"scope1": 40, "scope2": 10, "scope3": 50},
    "Automotive": {"scope1": 15, "scope2": 25, "scope3": 60},
    "Aviation": {"scope1": 70, "scope2": 5, "scope3": 25},
    "Chemical": {"scope1": 45, "scope2": 25, "scope3": 30},
    "Construction": {"scope1": 20, "scope2": 15, "scope3": 65},
    "Education": {"scope1": 10, "scope2": 45, "scope3": 45},
    "Energy": {"scope1": 60, "scope2": 5, "scope3": 35},
    "Financial Services": {"scope1": 5, "scope2": 25, "scope3": 70},
    "Food & Beverage": {"scope1": 25, "scope2": 20, "scope3": 55},
    "Healthcare": {"scope1": 15, "scope2": 35, "scope3": 50},
    "Hospitality": {"scope1": 20, "scope2": 40, "scope3": 40},
    "Information Technology": {"scope1": 5, "scope2": 30, "scope3": 65},
    "Manufacturing": {"scope1": 30, "scope2": 25, "scope3": 45},
    "Mining": {"scope1": 50, "scope2": 15, "scope3": 35},
    "Real Estate": {"scope1": 10, "scope2": 50, "scope3": 40},
    "Retail": {"scope1": 10, "scope2": 30, "scope3": 60},
    "Telecommunications": {"scope1": 5, "scope2": 35, "scope3": 60},
    "Transportation": {"scope1": 65, "scope2": 10, "scope3": 25},
    "Utilities": {"scope1": 70, "scope2": 5, "scope3": 25},
    "Other": {"scope1": 25, "scope2": 25, "scope3": 50}
}

# Science-based reduction targets by framework
REDUCTION_TARGETS = {
    "Paris-Aligned (1.5°C)": {
        "by_2030": 42,  # 42% reduction by 2030
        "annual": 4.2,   # 4.2% annual reduction
        "net_zero_year": 2050
    },
    "Well Below 2°C": {
        "by_2030": 35,  # 35% reduction by 2030
        "annual": 3.5,   # 3.5% annual reduction
        "net_zero_year": 2060
    },
    "2°C": {
        "by_2030": 25,  # 25% reduction by 2030
        "annual": 2.5,   # 2.5% annual reduction
        "net_zero_year": 2070
    }
}

# Country emissions per capita (tCO2e)
COUNTRY_EMISSIONS = {
    "Qatar": 37.0,
    "United States": 15.5,
    "Australia": 15.4,
    "Canada": 15.1,
    "Russia": 11.7,
    "Japan": 8.7,
    "Germany": 8.4,
    "China": 7.4,
    "United Kingdom": 5.5,
    "France": 4.6,
    "Brazil": 2.2,
    "India": 1.9,
    "Kenya": 0.3,
    "Ethiopia": 0.1,
    "Global Average": 4.5
}

# Carbon credit types and price ranges
CARBON_CREDIT_TYPES = {
    "Renewable Energy": {"min_price": 3, "max_price": 15, "avg_price": 8},
    "Forestry & Conservation": {"min_price": 5, "max_price": 25, "avg_price": 12},
    "Methane Capture": {"min_price": 6, "max_price": 20, "avg_price": 10},
    "Energy Efficiency": {"min_price": 4, "max_price": 18, "avg_price": 9},
    "Direct Air Capture": {"min_price": 50, "max_price": 500, "avg_price": 100}
}

# Industry-specific recommendations for emissions reduction
INDUSTRY_RECOMMENDATIONS = {
    "Agriculture": [
        "Implement precision agriculture techniques to reduce fertilizer use",
        "Convert to sustainable land management practices that sequester carbon",
        "Adopt renewable energy for farm operations",
        "Optimize livestock management to reduce methane emissions",
        "Implement water conservation measures"
    ],
    "Automotive": [
        "Accelerate transition to electric vehicle manufacturing",
        "Redesign production processes to minimize waste and energy use",
        "Source sustainable materials for vehicle components",
        "Optimize supply chain logistics",
        "Implement circular economy principles in manufacturing"
    ],
    "Aviation": [
        "Invest in sustainable aviation fuels",
        "Optimize flight routes and operations",
        "Implement weight reduction strategies",
        "Electrify ground operations",
        "Collaborate on industry-wide decarbonization initiatives"
    ],
    "Chemical": [
        "Redesign processes to improve energy efficiency",
        "Implement carbon capture for high-emission processes",
        "Switch to bio-based or recycled feedstocks",
        "Optimize waste heat recovery",
        "Reduce process emissions through catalytic improvements"
    ],
    "Construction": [
        "Use low-carbon concrete and building materials",
        "Implement prefabrication to reduce on-site waste",
        "Electrify construction equipment",
        "Design buildings for energy efficiency and low embodied carbon",
        "Implement sustainable construction site practices"
    ],
    "Education": [
        "Implement campus-wide energy efficiency programs",
        "Install on-site renewable energy generation",
        "Develop sustainable transportation options for students and staff",
        "Integrate sustainability into curriculum and operations",
        "Implement sustainable procurement policies"
    ],
    "Energy": [
        "Accelerate transition to renewable energy generation",
        "Implement energy storage solutions",
        "Reduce methane leakage in natural gas operations",
        "Optimize grid efficiency and demand management",
        "Implement carbon capture and storage for remaining fossil generation"
    ],
    "Other": [
        "Implement organization-wide energy efficiency measures",
        "Transition to renewable energy through on-site generation or purchasing",
        "Develop a sustainable procurement policy",
        "Reduce business travel and support remote work",
        "Engage suppliers on emissions reduction initiatives"
    ]
}
