import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Reduction Targets",
    page_icon="📉",
    layout="wide"
)

st.title("Emissions Reduction Targets")

if not st.session_state.company_data['name']:
    st.warning("Please enter your organization information on the home page first.")
    st.stop()

if not st.session_state.calculation_complete:
    st.warning("Please complete your emissions calculation before setting reduction targets.")
    st.stop()

# Current year and base emissions
current_year = st.session_state.company_data['year']
base_emissions = st.session_state.total_emissions

# Science-based target frameworks
st.markdown("### Science-Based Targets")
st.markdown("""
Science-based targets provide companies with a clearly defined pathway to reduce greenhouse gas (GHG) 
emissions in line with the Paris Agreement goals. Targets are considered 'science-based' if they 
align with what the latest climate science deems necessary to meet the goals of the Paris Agreement – 
limiting global warming to well-below 2°C above pre-industrial levels and pursuing efforts to limit 
warming to 1.5°C.
""")

target_framework = st.radio(
    "Select Target Framework",
    ["Paris-Aligned (1.5°C)", "Well Below 2°C", "2°C", "Custom Target"],
    index=0
)

if target_framework == "Paris-Aligned (1.5°C)":
    reduction_by_2030 = 42  # 42% reduction by 2030 from base year
    annual_reduction = 4.2  # 4.2% annual reduction
    net_zero_year = 2050
elif target_framework == "Well Below 2°C":
    reduction_by_2030 = 35  # 35% reduction by 2030 from base year
    annual_reduction = 3.5  # 3.5% annual reduction
    net_zero_year = 2060
elif target_framework == "2°C":
    reduction_by_2030 = 25  # 25% reduction by 2030 from base year
    annual_reduction = 2.5  # 2.5% annual reduction
    net_zero_year = 2070
else:  # Custom
    col1, col2, col3 = st.columns(3)
    with col1:
        reduction_by_2030 = st.slider("Reduction by 2030 (%)", 0, 100, 42)
    with col2:
        annual_reduction = st.slider("Annual Reduction (%)", 0.0, 10.0, 4.2)
    with col3:
        net_zero_year = st.slider("Net Zero Target Year", 2030, 2100, 2050)

# Calculate targets
st.session_state.targets = {
    '2030': base_emissions * (100 - reduction_by_2030) / 100,
    'annual_reduction': base_emissions * annual_reduction / 100,
    'net_zero_year': net_zero_year
}

# Display target metrics
st.markdown("### Your Emissions Reduction Targets")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        f"Base Year ({current_year}) Emissions",
        f"{base_emissions:.2f} tCO2e"
    )
with col2:
    st.metric(
        f"2030 Target Emissions",
        f"{st.session_state.targets['2030']:.2f} tCO2e",
        f"-{reduction_by_2030}%"
    )
with col3:
    st.metric(
        f"Annual Reduction Needed",
        f"{st.session_state.targets['annual_reduction']:.2f} tCO2e/year"
    )

# Reduction trajectory
st.markdown("### Emissions Reduction Trajectory")

# Generate years from current to 2050
years = list(range(current_year, 2051))
emissions = []

# Calculate emissions for each year
for year in years:
    if year == current_year:
        emissions.append(base_emissions)
    else:
        # Linear reduction until net zero year
        if year < net_zero_year:
            years_passed = year - current_year
            reduction = min(years_passed * annual_reduction / 100 * base_emissions, base_emissions)
            emissions.append(max(base_emissions - reduction, 0))
        else:
            # Net zero after target year
            emissions.append(0)

# Create dataframe for plotting
df = pd.DataFrame({
    'Year': years,
    'Emissions (tCO2e)': emissions
})

# Create reduction trajectory plot
fig = px.line(
    df,
    x='Year',
    y='Emissions (tCO2e)',
    title=f"Emissions Reduction Trajectory ({current_year}-2050)",
    markers=True
)

# Add target line for 2030
fig.add_vline(
    x=2030,
    line_dash="dash",
    line_color="red",
    annotation_text="2030 Target",
    annotation_position="top right"
)

# Add net zero year line
fig.add_vline(
    x=net_zero_year,
    line_dash="dash",
    line_color="green",
    annotation_text=f"Net Zero ({net_zero_year})",
    annotation_position="top right"
)

# Customize layout
fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Emissions (tCO2e)",
    plot_bgcolor="white",
    xaxis=dict(
        tickmode='linear',
        tick0=current_year,
        dtick=5
    )
)

st.plotly_chart(fig, use_container_width=True)

# Scope-based targets
st.markdown("### Targets by Emission Scope")
st.markdown("""
Different emission scopes may require different reduction strategies:
- **Scope 1 (Direct Emissions)**: These are directly under your control and often the easiest to address
- **Scope 2 (Energy)**: Can be reduced through energy efficiency and renewable energy procurement
- **Scope 3 (Value Chain)**: Often the largest portion and requires collaboration with suppliers and customers
""")

# Current scope breakdown
scope1_emissions = st.session_state.emissions_by_scope['scope1']
scope2_emissions = st.session_state.emissions_by_scope['scope2']
scope3_emissions = st.session_state.emissions_by_scope['scope3']

# Calculate targets by scope (can be customized)
col1, col2, col3 = st.columns(3)
with col1:
    scope1_reduction = st.slider(
        "Scope 1 Reduction by 2030 (%)",
        0, 100, 
        int(reduction_by_2030 * 1.2) if scope1_emissions > 0 else 0,  # Higher target for direct emissions
        disabled=scope1_emissions == 0
    )
    scope1_target = scope1_emissions * (100 - scope1_reduction) / 100
    
with col2:
    scope2_reduction = st.slider(
        "Scope 2 Reduction by 2030 (%)",
        0, 100, 
        int(reduction_by_2030 * 1.5) if scope2_emissions > 0 else 0,  # Higher target for energy
        disabled=scope2_emissions == 0
    )
    scope2_target = scope2_emissions * (100 - scope2_reduction) / 100
    
with col3:
    scope3_reduction = st.slider(
        "Scope 3 Reduction by 2030 (%)",
        0, 100, 
        int(reduction_by_2030 * 0.8) if scope3_emissions > 0 else 0,  # Lower but still ambitious target
        disabled=scope3_emissions == 0
    )
    scope3_target = scope3_emissions * (100 - scope3_reduction) / 100

# Create a stacked bar chart for scope-based reductions
scope_data = {
    'Scope': ['Scope 1', 'Scope 2', 'Scope 3'],
    'Current Emissions': [scope1_emissions, scope2_emissions, scope3_emissions],
    '2030 Target': [scope1_target, scope2_target, scope3_target]
}

scope_df = pd.DataFrame(scope_data)
scope_df_melted = pd.melt(scope_df, id_vars=['Scope'], var_name='Year', value_name='Emissions (tCO2e)')

# Create stacked bar chart
fig_scope = px.bar(
    scope_df_melted,
    x='Scope',
    y='Emissions (tCO2e)',
    color='Year',
    title="Emissions Reduction Targets by Scope",
    barmode='group',
    color_discrete_sequence=["#1f77b4", "#2ca02c"]
)

fig_scope.update_layout(
    xaxis_title="Emission Scope",
    yaxis_title="Emissions (tCO2e)",
    plot_bgcolor="white"
)

st.plotly_chart(fig_scope, use_container_width=True)

# Recommendations based on targets
st.markdown("### Key Recommendations to Meet Targets")

# Calculate which scope has the highest absolute reduction requirement
scope1_reduction_abs = scope1_emissions - scope1_target
scope2_reduction_abs = scope2_emissions - scope2_target
scope3_reduction_abs = scope3_emissions - scope3_target

priority_scopes = [
    ("Scope 1", scope1_reduction_abs),
    ("Scope 2", scope2_reduction_abs),
    ("Scope 3", scope3_reduction_abs)
]
priority_scopes.sort(key=lambda x: x[1], reverse=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Priority Areas for Reduction")
    for i, (scope, reduction) in enumerate(priority_scopes, 1):
        if reduction > 0:
            st.markdown(f"{i}. **{scope}**: Reduce by {reduction:.2f} tCO2e")
    
    st.markdown("#### Key Milestones")
    st.markdown(f"- Achieve {annual_reduction}% reduction each year")
    st.markdown(f"- Reach {reduction_by_2030}% total reduction by 2030")
    st.markdown(f"- Achieve net zero emissions by {net_zero_year}")

with col2:
    st.markdown("#### Suggested Next Steps")
    st.markdown("""
    1. **Develop a detailed reduction roadmap**:
       - Set interim targets for each year
       - Assign responsibility for emission reduction initiatives
       - Establish monitoring and reporting procedures
       
    2. **Identify specific reduction projects**:
       - Conduct energy audits and efficiency improvements
       - Explore renewable energy procurement options
       - Evaluate sustainable transport alternatives
       - Engage with suppliers on Scope 3 emissions
       
    3. **Consider carbon offsetting for residual emissions**:
       - Research high-quality carbon offset projects
       - Develop a timeline for offsetting implementation
    """)

# Target alignment with industry benchmarks
st.markdown("### Target Alignment with Industry Benchmarks")

# Sample industry benchmarks (would be more accurate with real data)
industry_benchmarks = {
    "Agriculture": {"average_reduction": 30, "best_practice": 45},
    "Automotive": {"average_reduction": 35, "best_practice": 50},
    "Aviation": {"average_reduction": 25, "best_practice": 40},
    "Chemical": {"average_reduction": 30, "best_practice": 45},
    "Construction": {"average_reduction": 40, "best_practice": 55},
    "Education": {"average_reduction": 45, "best_practice": 60},
    "Energy": {"average_reduction": 35, "best_practice": 50},
    "Financial Services": {"average_reduction": 50, "best_practice": 65},
    "Food & Beverage": {"average_reduction": 35, "best_practice": 50},
    "Healthcare": {"average_reduction": 40, "best_practice": 55},
    "Hospitality": {"average_reduction": 35, "best_practice": 50},
    "Information Technology": {"average_reduction": 45, "best_practice": 60},
    "Manufacturing": {"average_reduction": 30, "best_practice": 45},
    "Mining": {"average_reduction": 25, "best_practice": 40},
    "Real Estate": {"average_reduction": 40, "best_practice": 55},
    "Retail": {"average_reduction": 35, "best_practice": 50},
    "Telecommunications": {"average_reduction": 40, "best_practice": 55},
    "Transportation": {"average_reduction": 30, "best_practice": 45},
    "Utilities": {"average_reduction": 35, "best_practice": 50},
    "Other": {"average_reduction": 35, "best_practice": 50}
}

# Get the industry of the company
industry = st.session_state.company_data['industry']
if industry and industry in industry_benchmarks:
    industry_avg = industry_benchmarks[industry]["average_reduction"]
    industry_best = industry_benchmarks[industry]["best_practice"]
    
    # Create a comparison chart
    benchmark_data = {
        'Benchmark': ['Your Target', f'{industry} Industry Average', f'{industry} Best Practice'],
        'Reduction by 2030 (%)': [reduction_by_2030, industry_avg, industry_best]
    }
    
    benchmark_df = pd.DataFrame(benchmark_data)
    
    fig_benchmark = px.bar(
        benchmark_df,
        x='Benchmark',
        y='Reduction by 2030 (%)',
        title=f"2030 Reduction Target Comparison - {industry} Industry",
        color='Benchmark',
        color_discrete_sequence=["#2ca02c", "#1f77b4", "#ff7f0e"]
    )
    
    fig_benchmark.update_layout(
        xaxis_title="",
        yaxis_title="Emission Reduction by 2030 (%)",
        plot_bgcolor="white",
        showlegend=False
    )
    
    st.plotly_chart(fig_benchmark, use_container_width=True)
    
    # Provide context based on comparison
    if reduction_by_2030 >= industry_best:
        st.success(f"Your target exceeds best practice standards for the {industry} industry. You're on a leadership pathway!")
    elif reduction_by_2030 >= industry_avg:
        st.info(f"Your target is above the average for the {industry} industry but below best practice standards.")
    else:
        st.warning(f"Your target is below the average for the {industry} industry. Consider setting more ambitious targets.")
else:
    st.info("Please select an industry on the home page to see industry benchmark comparisons.")
