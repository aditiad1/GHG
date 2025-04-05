import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Global Comparison",
    page_icon="🌎",
    layout="wide"
)

st.title("Global Emissions Comparison")

if not st.session_state.company_data['name']:
    st.warning("Please enter your organization information on the home page first.")
    st.stop()

if not st.session_state.calculation_complete:
    st.warning("Please complete your emissions calculation before viewing global comparisons.")
    st.stop()

# Company data
company_name = st.session_state.company_data['name']
company_industry = st.session_state.company_data['industry']
company_employees = st.session_state.company_data['employees']
company_emissions = st.session_state.total_emissions
company_intensity = company_emissions / st.session_state.company_data['revenue'] if st.session_state.company_data['revenue'] > 0 else 0

# Sample industry average data
# In a real implementation, this would come from an API or database
industry_emissions_data = {
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

# Scope distribution by industry
industry_scope_data = {
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

# Country emissions per capita (tCO2e)
country_emissions = {
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

# Introduction section
st.markdown("""
### Benchmarking Your Emissions

Comparing your organization's carbon footprint with industry benchmarks and global averages 
helps identify areas for improvement and opportunities to stand out as a sustainability leader.

This section provides:
- Comparison with industry peers
- Benchmarking against global emissions
- Analysis of your emissions profile compared to industry norms
""")

# Industry comparison
st.markdown("### Industry Comparison")

if company_industry and company_industry in industry_emissions_data:
    industry_data = industry_emissions_data[company_industry]
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = company_intensity,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Emissions Intensity (tCO2e per $M revenue)"},
        delta = {'reference': industry_data['avg_intensity'], 'relative': True, 'valueformat': '.1%'},
        gauge = {
            'axis': {'range': [None, industry_data['worst_performer']], 
                     'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, industry_data['best_performer']], 'color': 'green'},
                {'range': [industry_data['best_performer'], industry_data['avg_intensity']], 'color': 'yellow'},
                {'range': [industry_data['avg_intensity'], industry_data['worst_performer']], 'color': 'orange'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': company_intensity
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        font=dict(size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance assessment
    if company_intensity <= industry_data["best_performer"]:
        performance_class = "Leading"
        perf_color = "green"
        description = "Your organization is among the top performers in your industry. Your carbon management strategies can serve as best practices for others."
    elif company_intensity <= industry_data["avg_intensity"]:
        performance_class = "Above Average"
        perf_color = "lightgreen"
        description = "Your organization is performing better than the industry average. Continue implementing your carbon reduction strategies."
    elif company_intensity <= (industry_data["avg_intensity"] + industry_data["worst_performer"])/2:
        performance_class = "Below Average"
        perf_color = "orange"
        description = "Your organization's emissions intensity is higher than the industry average. There is significant room for improvement."
    else:
        performance_class = "Lagging"
        perf_color = "red"
        description = "Your organization's emissions intensity is significantly higher than industry peers. Immediate action is recommended."
    
    # Display performance class
    st.markdown(f"**Performance Class**: <span style='color:{perf_color};font-size:1.5em;'>{performance_class}</span>", unsafe_allow_html=True)
    st.markdown(f"**Assessment**: {description}")
    
    # Create comparison bar chart
    comparison_data = {
        "Category": ["Your Organization", "Industry Best", "Industry Average", "Industry Worst"],
        "Emissions Intensity": [company_intensity, industry_data["best_performer"], industry_data["avg_intensity"], industry_data["worst_performer"]]
    }
    
    comp_df = pd.DataFrame(comparison_data)
    
    fig_bar = px.bar(
        comp_df,
        x="Category",
        y="Emissions Intensity",
        title=f"{company_industry} Industry Emissions Intensity (tCO2e/$M revenue)",
        color="Category",
        color_discrete_map={
            "Your Organization": "blue",
            "Industry Best": "green",
            "Industry Average": "yellow",
            "Industry Worst": "red"
        }
    )
    
    fig_bar.update_layout(
        xaxis_title="",
        yaxis_title="Emissions Intensity (tCO2e/$M revenue)",
        plot_bgcolor="white",
        showlegend=False
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Scope comparison
    st.markdown("### Emissions Scope Distribution")
    
    # Your organization's scope breakdown
    company_scope1_pct = st.session_state.emissions_by_scope['scope1'] / company_emissions * 100
    company_scope2_pct = st.session_state.emissions_by_scope['scope2'] / company_emissions * 100
    company_scope3_pct = st.session_state.emissions_by_scope['scope3'] / company_emissions * 100
    
    # Industry typical scope breakdown
    industry_scope = industry_scope_data[company_industry]
    
    # Prepare data for radar chart
    scope_labels = ["Scope 1 (%)", "Scope 2 (%)", "Scope 3 (%)"]
    company_values = [company_scope1_pct, company_scope2_pct, company_scope3_pct]
    industry_values = [industry_scope["scope1"], industry_scope["scope2"], industry_scope["scope3"]]
    
    # Create radar chart
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=company_values,
        theta=scope_labels,
        fill='toself',
        name='Your Organization'
    ))
    
    fig_radar.add_trace(go.Scatterpolar(
        r=industry_values,
        theta=scope_labels,
        fill='toself',
        name=f'{company_industry} Industry Average'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(company_values), max(industry_values)) * 1.1]
            )
        ),
        title="Scope Distribution Comparison",
        showlegend=True,
        height=500
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Analysis of scope distribution
    st.markdown("#### Scope Distribution Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        scope1_diff = company_scope1_pct - industry_scope["scope1"]
        st.metric(
            "Scope 1 Comparison", 
            f"{company_scope1_pct:.1f}%", 
            f"{scope1_diff:+.1f}% vs. Industry",
            delta_color="inverse"
        )
        
        if abs(scope1_diff) >= 10:
            if scope1_diff > 0:
                st.markdown("Your direct emissions are significantly higher than industry average. Focus on reducing fuel consumption and process emissions.")
            else:
                st.markdown("Your direct emissions are lower than industry average, which is positive. Continue to maintain efficient operations.")
                
    with col2:
        scope2_diff = company_scope2_pct - industry_scope["scope2"]
        st.metric(
            "Scope 2 Comparison", 
            f"{company_scope2_pct:.1f}%", 
            f"{scope2_diff:+.1f}% vs. Industry",
            delta_color="inverse"
        )
        
        if abs(scope2_diff) >= 10:
            if scope2_diff > 0:
                st.markdown("Your energy-related emissions are higher than industry average. Consider renewable energy procurement or efficiency improvements.")
            else:
                st.markdown("Your energy-related emissions are lower than industry average, suggesting effective energy management.")
                
    with col3:
        scope3_diff = company_scope3_pct - industry_scope["scope3"]
        st.metric(
            "Scope 3 Comparison", 
            f"{company_scope3_pct:.1f}%", 
            f"{scope3_diff:+.1f}% vs. Industry",
            delta_color="inverse"
        )
        
        if abs(scope3_diff) >= 10:
            if scope3_diff > 0:
                st.markdown("Your value chain emissions are higher than industry average. Focus on supplier engagement and more efficient products.")
            else:
                st.markdown("Your value chain emissions are lower than industry average, indicating effective supply chain management.")
else:
    st.info("Please select an industry on the home page to see industry comparisons.")

# Global comparison
st.markdown("### Global Emissions Context")

# Emissions per employee vs country per capita
per_employee = company_emissions / company_employees if company_employees > 0 else 0

# Selected countries for comparison
selected_countries = ["United States", "Germany", "China", "India", "Global Average"]
comparison_values = [country_emissions[country] for country in selected_countries]
comparison_values.append(per_employee)
comparison_labels = selected_countries + ["Your Org (per employee)"]

# Create bar chart
fig_global = px.bar(
    x=comparison_labels,
    y=comparison_values,
    title="Emissions per Employee vs. National per Capita Emissions",
    color=comparison_labels,
    labels={'x': '', 'y': 'tCO2e per Person/Employee'}
)

fig_global.update_layout(
    showlegend=False,
    plot_bgcolor="white"
)

st.plotly_chart(fig_global, use_container_width=True)

# Interpret the comparison
if per_employee > 0:
    st.markdown("#### How to Interpret This Comparison")
    st.markdown("""
    This comparison provides context by comparing your per-employee emissions with national averages:
    
    - **Corporate vs. Individual Impact**: Corporate emissions per employee are often higher than national per capita averages due to business operations.
    - **Benchmarking**: Compare your per-employee emissions against global and national averages to understand your relative impact.
    - **Goal Setting**: Consider setting targets to bring your per-employee emissions closer to advanced economies with lower emissions.
    
    Note that this is not a perfect comparison since companies produce goods and services that individuals consume, but it provides useful context.
    """)

# Global benchmarking dashboard
st.markdown("### Interactive Global Benchmarking")

# Create sorting options for countries
sort_option = st.selectbox(
    "Sort Countries By:",
    ["Highest to Lowest Emissions", "Lowest to Highest Emissions", "Alphabetical"]
)

# Sort the country data based on selection
country_df = pd.DataFrame({
    "Country": list(country_emissions.keys()),
    "Emissions per Capita (tCO2e)": list(country_emissions.values())
})

if sort_option == "Highest to Lowest Emissions":
    country_df = country_df.sort_values("Emissions per Capita (tCO2e)", ascending=False)
elif sort_option == "Lowest to Highest Emissions":
    country_df = country_df.sort_values("Emissions per Capita (tCO2e)", ascending=True)
else:  # Alphabetical
    country_df = country_df.sort_values("Country")

# Allow user to select countries to compare
selected_countries = st.multiselect(
    "Select Countries to Compare",
    country_df["Country"].tolist(),
    default=["United States", "China", "India", "Global Average"]
)

if selected_countries:
    # Filter dataframe to selected countries
    filtered_df = country_df[country_df["Country"].isin(selected_countries)]
    
    # Add the organization's per employee emissions
    if per_employee > 0:
        filtered_df = pd.concat([
            filtered_df,
            pd.DataFrame({
                "Country": [f"{company_name} (per employee)"],
                "Emissions per Capita (tCO2e)": [per_employee]
            })
        ])
    
    # Create comparison chart
    fig_comparison = px.bar(
        filtered_df,
        x="Country",
        y="Emissions per Capita (tCO2e)",
        title="Emissions Comparison",
        color="Country"
    )
    
    fig_comparison.update_layout(
        xaxis_title="",
        yaxis_title="tCO2e per Capita/Employee",
        plot_bgcolor="white",
        showlegend=False
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
else:
    st.info("Please select at least one country to compare.")

# Contextualize the organization's total emissions
st.markdown("### Contextualizing Your Organization's Total Emissions")

# Sample national emissions for context
country_total_emissions = {
    "United States": 5.0e9,
    "Germany": 7.0e8,
    "Finland": 5.0e7,
    "Jamaica": 7.8e6,
    "Barbados": 4.4e5
}

# Find the closest country match
closest_country = None
smallest_diff = float('inf')

for country, emissions in country_total_emissions.items():
    diff = abs(emissions - company_emissions)
    if diff < smallest_diff:
        smallest_diff = diff
        closest_country = country

if closest_country:
    st.markdown(f"Your organization's annual emissions ({company_emissions:.2f} tCO2e) are approximately equivalent to:")
    
    if company_emissions >= 1e9:
        pct_of_us = (company_emissions / country_total_emissions["United States"]) * 100
        st.markdown(f"- **{pct_of_us:.2f}%** of the United States' annual emissions")
    elif company_emissions >= 1e6:
        comparable_country = closest_country
        st.markdown(f"- The emissions of a small country like **{comparable_country}**")
    elif company_emissions >= 1e3:
        num_households = company_emissions / 10  # Average household ~10 tCO2e/year
        st.markdown(f"- The annual emissions of approximately **{num_households:,.0f}** average households")
    else:
        num_flights = company_emissions / 2  # ~2 tCO2e per transatlantic flight
        st.markdown(f"- Approximately **{num_flights:.0f}** transatlantic flights")

# Additional context
st.markdown("### Global Emissions Reductions Needed")

# Global emissions reduction targets visualization
reduction_years = [2020, 2025, 2030, 2035, 2040, 2045, 2050]
current_global_emissions = 51e9  # 51 billion tonnes CO2e
emissions_15c_pathway = [
    current_global_emissions,
    current_global_emissions * 0.80,  # 20% reduction by 2025
    current_global_emissions * 0.55,  # 45% reduction by 2030
    current_global_emissions * 0.30,  # 70% reduction by 2035
    current_global_emissions * 0.15,  # 85% reduction by 2040
    current_global_emissions * 0.05,  # 95% reduction by 2045
    0  # Net zero by 2050
]

emissions_2c_pathway = [
    current_global_emissions,
    current_global_emissions * 0.90,  # 10% reduction by 2025
    current_global_emissions * 0.75,  # 25% reduction by 2030
    current_global_emissions * 0.60,  # 40% reduction by 2035
    current_global_emissions * 0.45,  # 55% reduction by 2040
    current_global_emissions * 0.25,  # 75% reduction by 2045
    current_global_emissions * 0.10   # 90% reduction by 2050
]

# Create dataframe for plotting
pathway_df = pd.DataFrame({
    "Year": reduction_years + reduction_years,
    "Annual Emissions (Gt CO2e)": emissions_15c_pathway + emissions_2c_pathway,
    "Pathway": ["1.5°C Pathway"] * len(reduction_years) + ["2°C Pathway"] * len(reduction_years)
})

# Create line chart
fig_pathway = px.line(
    pathway_df,
    x="Year",
    y="Annual Emissions (Gt CO2e)",
    color="Pathway",
    title="Global Emissions Reduction Pathways",
    markers=True
)

fig_pathway.update_layout(
    xaxis_title="Year",
    yaxis_title="Annual Emissions (Gt CO2e)",
    plot_bgcolor="white"
)

st.plotly_chart(fig_pathway, use_container_width=True)

st.markdown("""
### Global Context for Your Emissions Targets

The above chart shows the global emissions reduction pathways needed to limit warming to 1.5°C or 2°C, 
according to climate science. When setting your organization's targets, consider:

- The 1.5°C pathway requires net zero emissions by 2050
- This translates to ~50% global emissions reduction by 2030
- Your organization should aim to reduce emissions at least in line with these global pathways
- Science-based targets often require faster reductions from organizations in developed economies

Your targets on the Reduction Targets page should be evaluated against these global requirements.
""")
