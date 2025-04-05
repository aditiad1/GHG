import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Carbon Credits Marketplace",
    page_icon="💰",
    layout="wide"
)

st.title("Carbon Credits Marketplace")

if not st.session_state.company_data['name']:
    st.warning("Please enter your organization information on the home page first.")
    st.stop()

if not st.session_state.calculation_complete:
    st.warning("Please complete your emissions calculation before exploring carbon credits.")
    st.stop()

# Introduction to carbon credits
st.markdown("""
### Understanding Carbon Credits

Carbon credits represent one metric ton of carbon dioxide equivalent (tCO2e) that is either removed from the atmosphere 
or prevented from being emitted. Organizations can purchase carbon credits to offset emissions they cannot eliminate.

While reducing emissions directly should be the priority, carbon credits can help:
- Offset hard-to-abate emissions
- Support the transition to a low-carbon economy
- Fund climate mitigation projects worldwide
- Complement your emissions reduction strategy
""")

# Carbon credit calculator
st.markdown("### Carbon Offset Calculator")

total_emissions = st.session_state.total_emissions
offset_percentage = st.slider("Percentage of Emissions to Offset", 0, 100, 30)
offset_amount = total_emissions * offset_percentage / 100

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Emissions", f"{total_emissions:.2f} tCO2e")
with col2:
    st.metric("Offset Target", f"{offset_percentage}%")
with col3:
    st.metric("Credits Needed", f"{offset_amount:.2f} tCO2e")

# Carbon credit price estimator
st.markdown("### Estimated Costs")

# Define different credit types and price ranges
credit_types = {
    "Renewable Energy": {"min_price": 3, "max_price": 15, "avg_price": 8},
    "Forestry & Conservation": {"min_price": 5, "max_price": 25, "avg_price": 12},
    "Methane Capture": {"min_price": 6, "max_price": 20, "avg_price": 10},
    "Energy Efficiency": {"min_price": 4, "max_price": 18, "avg_price": 9},
    "Direct Air Capture": {"min_price": 50, "max_price": 500, "avg_price": 100}
}

credit_selection = st.radio(
    "Select Carbon Credit Type",
    list(credit_types.keys())
)

selected_credit = credit_types[credit_selection]
price_per_credit = st.slider(
    "Price per Credit (USD)",
    selected_credit["min_price"],
    selected_credit["max_price"],
    selected_credit["avg_price"]
)

total_cost = offset_amount * price_per_credit

st.metric("Estimated Total Cost", f"${total_cost:,.2f}")

# Create cost breakdown visualization
st.markdown("### Cost Comparison Across Credit Types")

# Prepare data for cost comparison
comparison_data = []
for credit_type, prices in credit_types.items():
    comparison_data.append({
        "Credit Type": credit_type,
        "Minimum Cost": offset_amount * prices["min_price"],
        "Average Cost": offset_amount * prices["avg_price"],
        "Maximum Cost": offset_amount * prices["max_price"]
    })

comparison_df = pd.DataFrame(comparison_data)
comparison_df_melted = pd.melt(
    comparison_df,
    id_vars=["Credit Type"],
    value_vars=["Minimum Cost", "Average Cost", "Maximum Cost"],
    var_name="Cost Scenario",
    value_name="Total Cost (USD)"
)

# Create bar chart
fig = px.bar(
    comparison_df_melted,
    x="Credit Type",
    y="Total Cost (USD)",
    color="Cost Scenario",
    title=f"Cost to Offset {offset_percentage}% of Emissions ({offset_amount:.2f} tCO2e)",
    barmode="group",
    color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c"]
)

fig.update_layout(
    xaxis_title="Carbon Credit Type",
    yaxis_title="Cost (USD)",
    plot_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

# Sample carbon credit projects
st.markdown("### Featured Carbon Credit Projects")

# Sample project data - in a real app, this would come from an API
projects = [
    {
        "name": "Amazon Rainforest Conservation",
        "type": "Forestry & Conservation",
        "location": "Brazil",
        "price_per_credit": 15,
        "available_credits": 50000,
        "certification": "Verified Carbon Standard (VCS)",
        "description": "This project protects critical Amazon rainforest areas from deforestation, preserving biodiversity and carbon stocks.",
        "co_benefits": ["Biodiversity protection", "Indigenous community support", "Water conservation"]
    },
    {
        "name": "Wind Farm Development",
        "type": "Renewable Energy",
        "location": "India",
        "price_per_credit": 7,
        "available_credits": 75000,
        "certification": "Gold Standard",
        "description": "Large-scale wind farm project that displaces fossil fuel-based electricity generation.",
        "co_benefits": ["Energy access", "Local employment", "Air quality improvement"]
    },
    {
        "name": "Landfill Methane Capture",
        "type": "Methane Capture",
        "location": "United States",
        "price_per_credit": 10,
        "available_credits": 30000,
        "certification": "Climate Action Reserve",
        "description": "Captures methane emissions from landfills and converts them into electricity.",
        "co_benefits": ["Reduced odor", "Local energy generation", "Improved waste management"]
    },
    {
        "name": "Efficient Cookstoves Distribution",
        "type": "Energy Efficiency",
        "location": "Kenya",
        "price_per_credit": 9,
        "available_credits": 25000,
        "certification": "Gold Standard",
        "description": "Distributes efficient cookstoves to rural communities, reducing fuel wood consumption and indoor air pollution.",
        "co_benefits": ["Health improvements", "Reduced deforestation", "Time savings for women and children"]
    },
    {
        "name": "Direct Air Carbon Capture",
        "type": "Direct Air Capture",
        "location": "Iceland",
        "price_per_credit": 95,
        "available_credits": 5000,
        "certification": "PURO Standard",
        "description": "Cutting-edge technology that directly removes CO2 from the atmosphere and stores it permanently underground.",
        "co_benefits": ["Technological innovation", "Permanent carbon removal", "Scalable climate solution"]
    }
]

# Filter projects based on selected credit type
filtered_projects = [p for p in projects if p["type"] == credit_selection]

# Display projects as cards
if filtered_projects:
    cols = st.columns(min(len(filtered_projects), 3))
    for i, project in enumerate(filtered_projects):
        with cols[i % 3]:
            st.markdown(f"#### {project['name']}")
            st.markdown(f"**Location**: {project['location']}")
            st.markdown(f"**Price**: ${project['price_per_credit']} per tCO2e")
            st.markdown(f"**Available Credits**: {project['available_credits']:,} tCO2e")
            st.markdown(f"**Certification**: {project['certification']}")
            st.markdown(f"**Description**: {project['description']}")
            
            st.markdown("**Co-benefits**:")
            for benefit in project['co_benefits']:
                st.markdown(f"- {benefit}")
            
            if st.button(f"Select Project: {project['name']}", key=f"select_{i}"):
                st.session_state.selected_project = project
                st.success(f"Selected {project['name']} for carbon offsetting")
else:
    st.info(f"No projects currently available for {credit_selection} credits. Try selecting a different credit type.")

# Purchase simulation
st.markdown("### Offset Purchase Simulation")

# Check if a project has been selected
if 'selected_project' in st.session_state:
    selected_project = st.session_state.selected_project
    
    st.markdown(f"**Selected Project**: {selected_project['name']}")
    st.markdown(f"**Credit Type**: {selected_project['type']}")
    st.markdown(f"**Price per Credit**: ${selected_project['price_per_credit']}")
    
    # Credit purchase form
    purchase_amount = st.number_input(
        "Number of Credits to Purchase (tCO2e)",
        min_value=1.0,
        max_value=min(selected_project['available_credits'], offset_amount),
        value=min(100.0, offset_amount)
    )
    
    purchase_cost = purchase_amount * selected_project['price_per_credit']
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Purchase Amount", f"{purchase_amount:.2f} tCO2e")
    with col2:
        st.metric("Total Cost", f"${purchase_cost:,.2f}")
    
    offset_percentage_achieved = (purchase_amount / total_emissions) * 100
    
    st.progress(min(offset_percentage_achieved / offset_percentage, 1.0))
    st.markdown(f"This purchase will offset **{offset_percentage_achieved:.1f}%** of your total emissions")
    
    if st.button("Confirm Purchase (Simulation)"):
        st.success(f"Simulation: Successfully purchased {purchase_amount:.2f} tCO2e of carbon credits from {selected_project['name']}")
        st.balloons()
else:
    st.info("Please select a project from the Featured Carbon Credit Projects section above")

# Education on high-quality carbon credits
st.markdown("### Ensuring High-Quality Carbon Credits")
st.markdown("""
When purchasing carbon credits, look for these key quality indicators:

1. **Additionality**: The project wouldn't have happened without carbon credit funding
2. **Permanence**: Carbon reductions or removals will last for a significant time
3. **Leakage Prevention**: Emissions aren't simply shifted elsewhere
4. **Verification**: Credits are verified by reputable third-party standards
5. **Co-benefits**: Projects provide additional social and environmental benefits

**Reputable Carbon Credit Standards**:
- Verified Carbon Standard (VCS/Verra)
- Gold Standard
- American Carbon Registry
- Climate Action Reserve
- Plan Vivo
- Clean Development Mechanism (CDM)
""")

# Strategic advice on carbon offsetting
st.markdown("### Carbon Offsetting Strategy")
st.markdown("""
**Best Practices for Incorporating Carbon Credits:**

1. **Follow the mitigation hierarchy**:
   - First, avoid and reduce emissions where possible
   - Second, offset remaining unavoidable emissions

2. **Develop a balanced portfolio**:
   - Mix of project types (renewable energy, forestry, direct air capture)
   - Mix of locations and co-benefits
   - Combination of near-term and long-term removals

3. **Set clear offsetting goals**:
   - Align with your organization's climate targets
   - Communicate transparently about use of offsets
   - Increase ambition over time

4. **Budget considerations**:
   - Allocate funds for both reduction initiatives and offsetting
   - Anticipate rising carbon credit prices over time
   - Consider forward purchasing agreements for price stability
""")

# Disclaimer
st.markdown("---")
st.markdown("""
**Disclaimer**: This marketplace simulation is for educational purposes only. In a real implementation, 
this would connect to actual carbon credit registries and marketplaces. Prices and projects shown are 
representative examples and may not reflect current market conditions.
""")
