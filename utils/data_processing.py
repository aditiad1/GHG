import pandas as pd
import numpy as np
from utils.constants import INDUSTRY_BENCHMARKS, SCOPE_DISTRIBUTIONS

def validate_input_data(data_dict, data_type):
    """
    Validate input data for calculation
    
    Args:
        data_dict (dict): Dictionary containing input data
        data_type (str): Type of data (scope1, scope2, scope3)
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not data_dict:
        return False, f"No {data_type} data provided."
    
    # Check for negative values
    negative_fields = []
    for key, value in data_dict.items():
        if isinstance(value, (int, float)) and value < 0:
            negative_fields.append(key)
    
    if negative_fields:
        fields_str = ", ".join(negative_fields)
        return False, f"Negative values found in {fields_str}. Please provide non-negative values."
    
    return True, ""

def get_industry_data(industry):
    """
    Get benchmark data for a specific industry
    
    Args:
        industry (str): Industry name
        
    Returns:
        dict: Dictionary containing industry benchmark data
    """
    if industry in INDUSTRY_BENCHMARKS:
        return INDUSTRY_BENCHMARKS[industry]
    else:
        return INDUSTRY_BENCHMARKS["Other"]

def get_scope_distribution(industry):
    """
    Get typical scope distribution for a specific industry
    
    Args:
        industry (str): Industry name
        
    Returns:
        dict: Dictionary containing typical scope distribution
    """
    if industry in SCOPE_DISTRIBUTIONS:
        return SCOPE_DISTRIBUTIONS[industry]
    else:
        return SCOPE_DISTRIBUTIONS["Other"]

def calculate_targets(base_emissions, reduction_percentage, target_year, base_year=2023):
    """
    Calculate emissions reduction targets
    
    Args:
        base_emissions (float): Base year emissions in tCO2e
        reduction_percentage (float): Percentage to reduce by target year
        target_year (int): Year to achieve target
        base_year (int): Base year for calculations
    
    Returns:
        dict: Dictionary containing target information
    """
    years = target_year - base_year
    annual_reduction_rate = 1 - (1 - reduction_percentage/100) ** (1/years)
    annual_reduction_percentage = annual_reduction_rate * 100
    annual_reduction_absolute = base_emissions * annual_reduction_rate
    
    target_emissions = base_emissions * (1 - reduction_percentage/100)
    
    # Create yearly trajectory
    trajectory = []
    for i in range(years + 1):
        year = base_year + i
        reduction_factor = (1 - annual_reduction_rate) ** i
        yearly_emissions = base_emissions * reduction_factor
        trajectory.append({
            'year': year,
            'emissions': yearly_emissions,
            'reduction_from_base': (1 - reduction_factor) * 100
        })
    
    return {
        'base_emissions': base_emissions,
        'target_emissions': target_emissions,
        'reduction_percentage': reduction_percentage,
        'annual_reduction_percentage': annual_reduction_percentage,
        'annual_reduction_absolute': annual_reduction_absolute,
        'base_year': base_year,
        'target_year': target_year,
        'trajectory': trajectory
    }

def generate_sample_strategies(emissions_data, industry):
    """
    Generate sample emission reduction strategies based on emissions profile
    
    Args:
        emissions_data (dict): Dictionary containing emissions by scope
        industry (str): Industry name
    
    Returns:
        list: List of recommended strategies
    """
    # Get total emissions and breakdown by scope
    total_emissions = sum(emissions_data.values())
    scope_percentages = {
        scope: (emissions / total_emissions) * 100 if total_emissions > 0 else 0
        for scope, emissions in emissions_data.items()
    }
    
    # Identify dominant scope
    dominant_scope = max(emissions_data.items(), key=lambda x: x[1])[0] if total_emissions > 0 else "scope1"
    
    # Get industry-specific strategies from constants
    industry_strategies = []
    # This would be populated from a database or a more complex system in a real app
    
    # Basic strategies for all scopes
    basic_strategies = {
        "scope1": [
            {"name": "Energy efficiency improvements", "potential": "Medium", "timeframe": "Short-term"},
            {"name": "Switch to low-carbon fuels", "potential": "High", "timeframe": "Medium-term"},
            {"name": "Electrify vehicle fleet", "potential": "High", "timeframe": "Medium-term"},
            {"name": "Optimize HVAC systems", "potential": "Medium", "timeframe": "Short-term"},
            {"name": "Reduce refrigerant leaks", "potential": "Medium", "timeframe": "Short-term"}
        ],
        "scope2": [
            {"name": "Purchase renewable energy", "potential": "High", "timeframe": "Short-term"},
            {"name": "Install on-site renewables", "potential": "High", "timeframe": "Medium-term"},
            {"name": "Energy efficiency in buildings", "potential": "Medium", "timeframe": "Short-term"},
            {"name": "Smart building management", "potential": "Medium", "timeframe": "Medium-term"},
            {"name": "LED lighting upgrades", "potential": "Low", "timeframe": "Short-term"}
        ],
        "scope3": [
            {"name": "Supplier engagement program", "potential": "High", "timeframe": "Long-term"},
            {"name": "Optimize logistics", "potential": "Medium", "timeframe": "Medium-term"},
            {"name": "Reduce business travel", "potential": "Low", "timeframe": "Short-term"},
            {"name": "Sustainable procurement policy", "potential": "High", "timeframe": "Medium-term"},
            {"name": "Product redesign for efficiency", "potential": "High", "timeframe": "Long-term"}
        ]
    }
    
    # Prioritize strategies for dominant scope
    prioritized_strategies = []
    prioritized_strategies.extend(basic_strategies[dominant_scope])
    
    # Add some strategies from other scopes
    for scope, strategies in basic_strategies.items():
        if scope != dominant_scope:
            prioritized_strategies.extend(strategies[:2])  # Add top 2 strategies from other scopes
    
    return prioritized_strategies

def normalize_company_data(company_data):
    """
    Normalize company data to ensure all required fields are present
    
    Args:
        company_data (dict): Dictionary containing company data
        
    Returns:
        dict: Normalized company data
    """
    normalized_data = {
        'name': company_data.get('name', ''),
        'industry': company_data.get('industry', ''),
        'employees': max(1, company_data.get('employees', 1)),
        'revenue': max(0.1, company_data.get('revenue', 1)),
        'year': company_data.get('year', 2023)
    }
    
    return normalized_data

def calculate_emissions_intensity(total_emissions, revenue):
    """
    Calculate emissions intensity per revenue
    
    Args:
        total_emissions (float): Total emissions in tCO2e
        revenue (float): Revenue in millions USD
        
    Returns:
        float: Emissions intensity in tCO2e per million USD
    """
    if revenue <= 0:
        return 0
    
    return total_emissions / revenue

def calculate_per_employee_emissions(total_emissions, employees):
    """
    Calculate emissions per employee
    
    Args:
        total_emissions (float): Total emissions in tCO2e
        employees (int): Number of employees
        
    Returns:
        float: Emissions per employee in tCO2e
    """
    if employees <= 0:
        return 0
    
    return total_emissions / employees
