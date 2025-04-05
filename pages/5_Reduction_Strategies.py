import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Reduction Strategies",
    page_icon="💡",
    layout="wide"
)

st.title("Emissions Reduction Strategies")

if not st.session_state.company_data['name']:
    st.warning("Please enter your organization information on the home page first.")
    st.stop()

if not st.session_state.calculation_complete:
    st.warning("Please complete your emissions calculation before exploring reduction strategies.")
    st.stop()

# Introduction
st.markdown("""
### Implementing Effective Emissions Reduction Strategies

Reducing emissions requires a strategic approach that prioritizes high-impact initiatives. 
This page provides customized recommendations based on your emissions profile and industry.

Key principles for successful emissions reduction:
1. Focus on your largest emission sources first
2. Prioritize strategies with the best carbon return on investment
3. Consider both short-term wins and long-term transformational changes
4. Engage stakeholders across your value chain
""")

# Company data for context
company_name = st.session_state.company_data['name']
company_industry = st.session_state.company_data['industry']
total_emissions = st.session_state.total_emissions
scope1 = st.session_state.emissions_by_scope['scope1']
scope2 = st.session_state.emissions_by_scope['scope2']
scope3 = st.session_state.emissions_by_scope['scope3']

# Display company emissions profile
st.markdown("### Your Emissions Profile")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Scope 1 (Direct)", f"{scope1:.2f} tCO2e", f"{scope1/total_emissions*100:.1f}%")
with col2:
    st.metric("Scope 2 (Energy)", f"{scope2:.2f} tCO2e", f"{scope2/total_emissions*100:.1f}%")
with col3:
    st.metric("Scope 3 (Value Chain)", f"{scope3:.2f} tCO2e", f"{scope3/total_emissions*100:.1f}%")

# Determine dominant emission sources
if scope1 > max(scope2, scope3):
    dominant_scope = "Scope 1"
elif scope2 > max(scope1, scope3):
    dominant_scope = "Scope 2"
else:
    dominant_scope = "Scope 3"

st.markdown(f"Your largest emission source is **{dominant_scope}**, representing {max(scope1, scope2, scope3)/total_emissions*100:.1f}% of your total emissions.")

# Define strategy database
# Each strategy includes name, description, applicable_scope, reduction_potential, implementation_time, cost_level, and co-benefits
strategies = [
    # Scope 1 strategies
    {
        "name": "Electrify vehicle fleet",
        "description": "Replace conventional fuel vehicles with electric vehicles.",
        "applicable_scope": "Scope 1",
        "reduction_potential": "Medium-High",
        "implementation_time": "Medium",
        "cost_level": "High",
        "co_benefits": ["Air quality improvement", "Noise reduction", "Cost savings over vehicle lifetime"],
        "industries": ["All"]
    },
    {
        "name": "Upgrade to high-efficiency HVAC systems",
        "description": "Replace older heating, ventilation, and air conditioning systems with high-efficiency models.",
        "applicable_scope": "Scope 1",
        "reduction_potential": "Medium",
        "implementation_time": "Medium",
        "cost_level": "Medium",
        "co_benefits": ["Cost savings", "Improved comfort", "Extended equipment life"],
        "industries": ["All"]
    },
    {
        "name": "Optimize manufacturing processes",
        "description": "Identify and eliminate inefficiencies in manufacturing processes to reduce direct emissions.",
        "applicable_scope": "Scope 1",
        "reduction_potential": "Medium-High",
        "implementation_time": "Medium-Long",
        "cost_level": "Medium-High",
        "co_benefits": ["Productivity improvements", "Cost savings", "Waste reduction"],
        "industries": ["Manufacturing", "Chemical", "Food & Beverage", "Automotive", "Mining"]
    },
    {
        "name": "Switch to lower-carbon fuels",
        "description": "Replace high-carbon fuels like coal and oil with lower-carbon alternatives like natural gas or biofuels.",
        "applicable_scope": "Scope 1",
        "reduction_potential": "Medium-High",
        "implementation_time": "Short-Medium",
        "cost_level": "Low-Medium",
        "co_benefits": ["Reduced air pollutants", "Potential cost savings", "Improved public perception"],
        "industries": ["All"]
    },
    {
        "name": "Implement refrigerant management program",
        "description": "Monitor, maintain, and upgrade refrigeration systems to prevent leaks of high-GWP refrigerants.",
        "applicable_scope": "Scope 1",
        "reduction_potential": "Medium",
        "implementation_time": "Short",
        "cost_level": "Low",
        "co_benefits": ["Compliance with regulations", "Extended equipment life", "Cost savings"],
        "industries": ["Food & Beverage", "Retail", "Hospitality", "Healthcare"]
    },
    
    # Scope 2 strategies
    {
        "name": "Purchase renewable energy",
        "description": "Enter into power purchase agreements (PPAs) or buy renewable energy certificates (RECs).",
        "applicable_scope": "Scope 2",
        "reduction_potential": "High",
        "implementation_time": "Short",
        "cost_level": "Low-Medium",
        "co_benefits": ["Energy price stability", "Marketing opportunities", "Support for renewable industry"],
        "industries": ["All"]
    },
    {
        "name": "Install on-site renewable energy",
        "description": "Deploy solar panels, wind turbines, or other renewable energy systems at your facilities.",
        "applicable_scope": "Scope 2",
        "reduction_potential": "Medium-High",
        "implementation_time": "Medium",
        "cost_level": "High",
        "co_benefits": ["Energy independence", "Reduced operating costs", "Enhanced property value"],
        "industries": ["All"]
    },
    {
        "name": "Implement energy efficiency program",
        "description": "Conduct energy audits and implement efficiency upgrades for lighting, equipment, and building envelope.",
        "applicable_scope": "Scope 2",
        "reduction_potential": "Medium",
        "implementation_time": "Short-Medium",
        "cost_level": "Low-Medium",
        "co_benefits": ["Cost savings", "Improved workplace comfort", "Reduced maintenance"],
        "industries": ["All"]
    },
    {
        "name": "Smart building management systems",
        "description": "Install automated systems to optimize energy use in heating, cooling, and lighting.",
        "applicable_scope": "Scope 2",
        "reduction_potential": "Medium",
        "implementation_time": "Medium",
        "cost_level": "Medium",
        "co_benefits": ["Improved occupant comfort", "Detailed energy use data", "Remote management capabilities"],
        "industries": ["All"]
    },
    {
        "name": "Green building certification",
        "description": "Pursue LEED, BREEAM, or other green building certifications for new and existing buildings.",
        "applicable_scope": "Scope 2",
        "reduction_potential": "Medium",
        "implementation_time": "Medium-Long",
        "cost_level": "Medium-High",
        "co_benefits": ["Improved building value", "Enhanced reputation", "Healthier workspace"],
        "industries": ["All"]
    },
    
    # Scope 3 strategies
    {
        "name": "Supplier engagement program",
        "description": "Work with key suppliers to measure, report, and reduce their emissions.",
        "applicable_scope": "Scope 3",
        "reduction_potential": "Medium-High",
        "implementation_time": "Medium-Long",
        "cost_level": "Low-Medium",
        "co_benefits": ["Strengthened supplier relationships", "Supply chain resilience", "Knowledge sharing"],
        "industries": ["All"]
    },
    {
        "name": "Sustainable procurement policy",
        "description": "Integrate carbon footprint criteria into purchasing decisions and supplier selection.",
        "applicable_scope": "Scope 3",
        "reduction_potential": "Medium",
        "implementation_time": "Short-Medium",
        "cost_level": "Low",
        "co_benefits": ["Risk reduction", "Innovation encouragement", "Alignment with corporate values"],
        "industries": ["All"]
    },
    {
        "name": "Optimize product design",
        "description": "Redesign products to reduce material use, energy consumption during use, and end-of-life impacts.",
        "applicable_scope": "Scope 3",
        "reduction_potential": "Medium-High",
        "implementation_time": "Medium-Long",
        "cost_level": "Medium",
        "co_benefits": ["Cost savings", "Innovation opportunities", "Customer satisfaction"],
        "industries": ["Manufacturing", "Automotive", "Information Technology", "Retail", "Food & Beverage"]
    },
    {
        "name": "Implement circular economy initiatives",
        "description": "Develop take-back programs, use recycled materials, and design for reuse and recycling.",
        "applicable_scope": "Scope 3",
        "reduction_potential": "Medium",
        "implementation_time": "Medium-Long",
        "cost_level": "Medium",
        "co_benefits": ["Reduced waste", "New revenue streams", "Resource security"],
        "industries": ["All"]
    },
    {
        "name": "Logistics optimization",
        "description": "Optimize shipping routes, modes, and loading to reduce transportation emissions.",
        "applicable_scope": "Scope 3",
        "reduction_potential": "Medium",
        "implementation_time": "Short-Medium",
        "cost_level": "Low-Medium",
        "co_benefits": ["Cost savings", "Faster delivery times", "Reduced traffic congestion"],
        "industries": ["Retail", "Manufacturing", "Food & Beverage", "Transportation"]
    },
    {
        "name": "Remote work policy",
        "description": "Implement flexible work arrangements to reduce commuting emissions.",
        "applicable_scope": "Scope 3",
        "reduction_potential": "Low-Medium",
        "implementation_time": "Short",
        "cost_level": "Low",
        "co_benefits": ["Employee satisfaction", "Reduced office space needs", "Business continuity"],
        "industries": ["All"]
    },
    {
        "name": "Business travel reduction",
        "description": "Replace unnecessary business travel with virtual meetings and implement a sustainable travel policy.",
        "applicable_scope": "Scope 3",
        "reduction_potential": "Low-Medium",
        "implementation_time": "Short",
        "cost_level": "Low",
        "co_benefits": ["Cost savings", "Employee time savings", "Work-life balance"],
        "industries": ["All"]
    }
]

# Filter strategies by company's largest emission scope
dominant_strategies = [s for s in strategies if s["applicable_scope"] == dominant_scope]

# Filter by industry relevance (if industry is specified)
if company_industry and company_industry != "Other":
    industry_strategies = [
        s for s in strategies if "All" in s["industries"] or company_industry in s["industries"]
    ]
else:
    industry_strategies = strategies

# Prioritize strategies
top_dominant_strategies = dominant_strategies[:min(5, len(dominant_strategies))]
other_relevant_strategies = [s for s in industry_strategies if s not in top_dominant_strategies]

# Priority strategies section
st.markdown("### Priority Reduction Strategies")
st.markdown(f"Based on your emissions profile, these strategies targeting your largest source ({dominant_scope}) will have the greatest impact:")

for i, strategy in enumerate(top_dominant_strategies, 1):
    expander = st.expander(f"{i}. {strategy['name']} ({strategy['reduction_potential']} potential)")
    with expander:
        st.markdown(f"**Description**: {strategy['description']}")
        st.markdown(f"**Implementation Time**: {strategy['implementation_time']}")
        st.markdown(f"**Cost Level**: {strategy['cost_level']}")
        st.markdown("**Co-benefits**:")
        for benefit in strategy['co_benefits']:
            st.markdown(f"- {benefit}")

# Strategy explorer with filtering
st.markdown("### Strategy Explorer")
st.markdown("Explore all available reduction strategies with custom filtering:")

col1, col2 = st.columns(2)
with col1:
    scope_filter = st.multiselect(
        "Filter by Scope",
        ["Scope 1", "Scope 2", "Scope 3"],
        default=["Scope 1", "Scope 2", "Scope 3"]
    )

with col2:
    implementation_filter = st.multiselect(
        "Filter by Implementation Time",
        ["Short", "Short-Medium", "Medium", "Medium-Long", "Long"],
        default=["Short", "Short-Medium", "Medium"]
    )

# Apply filters
filtered_strategies = [
    s for s in industry_strategies 
    if s["applicable_scope"] in scope_filter 
    and any(time in s["implementation_time"] for time in implementation_filter)
]

# Display strategies in tabular format
if filtered_strategies:
    strategy_data = []
    for s in filtered_strategies:
        strategy_data.append({
            "Strategy": s["name"],
            "Scope": s["applicable_scope"],
            "Reduction Potential": s["reduction_potential"],
            "Implementation Time": s["implementation_time"],
            "Cost Level": s["cost_level"]
        })
    
    strategy_df = pd.DataFrame(strategy_data)
    st.dataframe(strategy_df, use_container_width=True)
    
    # Allow user to select a strategy for detailed view
    selected_strategy = st.selectbox(
        "Select a strategy for detailed information",
        [s["name"] for s in filtered_strategies]
    )
    
    # Find the selected strategy
    strategy_detail = next((s for s in filtered_strategies if s["name"] == selected_strategy), None)
    
    if strategy_detail:
        st.markdown(f"### {strategy_detail['name']}")
        st.markdown(f"**Description**: {strategy_detail['description']}")
        st.markdown(f"**Applicable Scope**: {strategy_detail['applicable_scope']}")
        st.markdown(f"**Reduction Potential**: {strategy_detail['reduction_potential']}")
        st.markdown(f"**Implementation Time**: {strategy_detail['implementation_time']}")
        st.markdown(f"**Cost Level**: {strategy_detail['cost_level']}")
        
        st.markdown("**Co-benefits**:")
        for benefit in strategy_detail['co_benefits']:
            st.markdown(f"- {benefit}")
        
        st.markdown("**Implementation Steps**:")
        # These steps would be customized in a real application
        st.markdown("1. Assess current situation and establish baseline")
        st.markdown("2. Set specific targets for this initiative")
        st.markdown("3. Develop detailed implementation plan")
        st.markdown("4. Allocate resources and responsibilities")
        st.markdown("5. Implement the strategy in phases")
        st.markdown("6. Monitor progress and measure results")
        st.markdown("7. Report outcomes and adjust approach as needed")
else:
    st.info("No strategies match your current filters. Try adjusting your selection.")

# Industry-specific recommendations
st.markdown("### Industry-Specific Recommendations")

industry_recommendations = {
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
    "Financial Services": [
        "Implement sustainable finance principles and products",
        "Reduce emissions from office operations and data centers",
        "Develop climate risk assessment tools",
        "Support clients' transition to low-carbon operations",
        "Shift investment portfolios toward low-carbon assets"
    ],
    "Food & Beverage": [
        "Optimize refrigeration systems and reduce leakage",
        "Implement energy efficiency in processing operations",
        "Source ingredients with lower carbon footprints",
        "Reduce food waste throughout operations",
        "Redesign packaging to reduce environmental impact"
    ],
    "Healthcare": [
        "Implement energy efficiency in hospitals and facilities",
        "Optimize medical waste management and recycling",
        "Reduce emissions from anesthetic gases",
        "Develop telemedicine to reduce patient travel",
        "Source sustainable medical supplies and pharmaceuticals"
    ],
    "Hospitality": [
        "Implement building energy management systems",
        "Reduce food waste in food service operations",
        "Optimize laundry operations and water use",
        "Install on-site renewable energy where possible",
        "Develop sustainable tourism offerings"
    ],
    "Information Technology": [
        "Increase data center energy efficiency",
        "Source renewable energy for operations",
        "Design energy-efficient hardware and software",
        "Implement circular economy principles for electronic waste",
        "Develop remote work tools to reduce commuting emissions"
    ],
    "Manufacturing": [
        "Optimize process energy efficiency",
        "Electrify manufacturing processes where possible",
        "Implement waste heat recovery systems",
        "Redesign products for lower lifecycle emissions",
        "Develop closed-loop material systems"
    ],
    "Mining": [
        "Electrify mining equipment and operations",
        "Implement energy efficiency in processing",
        "Optimize transportation logistics",
        "Develop renewable energy for remote operations",
        "Implement water conservation and land reclamation"
    ],
    "Real Estate": [
        "Retrofit existing buildings for energy efficiency",
        "Implement building automation systems",
        "Install on-site renewable energy generation",
        "Develop green leasing programs",
        "Design new buildings to net-zero energy standards"
    ],
    "Retail": [
        "Optimize store energy use and refrigeration",
        "Implement sustainable packaging initiatives",
        "Develop low-carbon logistics and delivery options",
        "Source sustainable products with lower emissions",
        "Implement efficient inventory management to reduce waste"
    ],
    "Telecommunications": [
        "Improve energy efficiency of network infrastructure",
        "Implement renewable energy for cell towers and data centers",
        "Extend equipment lifecycle and improve recycling",
        "Optimize field service operations to reduce travel",
        "Develop smart solutions that enable customer emission reductions"
    ],
    "Transportation": [
        "Transition fleet to electric or low-carbon vehicles",
        "Optimize routes and loading to maximize efficiency",
        "Implement driver training for fuel-efficient operations",
        "Develop intermodal solutions using lower-carbon transport modes",
        "Implement logistics optimization software"
    ],
    "Utilities": [
        "Accelerate transition to renewable energy generation",
        "Modernize grid infrastructure to support renewables",
        "Implement energy storage solutions",
        "Develop customer energy efficiency programs",
        "Reduce methane leakage from gas distribution"
    ],
    "Other": [
        "Implement organization-wide energy efficiency measures",
        "Transition to renewable energy through on-site generation or purchasing",
        "Develop a sustainable procurement policy",
        "Reduce business travel and support remote work",
        "Engage suppliers on emissions reduction initiatives"
    ]
}

if company_industry and company_industry in industry_recommendations:
    st.markdown(f"Based on your industry ({company_industry}), consider these specific recommendations:")
    
    for i, recommendation in enumerate(industry_recommendations[company_industry], 1):
        st.markdown(f"{i}. {recommendation}")
else:
    st.info("Select your industry on the home page to receive industry-specific recommendations.")

# Carbon reduction roadmap
st.markdown("### Developing Your Carbon Reduction Roadmap")
st.markdown("""
Creating an effective carbon reduction roadmap involves these key steps:

1. **Set science-based targets**: Establish clear, measurable reduction goals aligned with climate science
2. **Conduct detailed emissions analysis**: Identify hotspots and prioritize high-impact areas
3. **Develop initiative portfolio**: Create a balanced mix of short-term and long-term initiatives
4. **Create implementation timeline**: Sequence initiatives for optimal impact and resource use
5. **Assign responsibilities**: Define clear ownership for each initiative
6. **Establish monitoring system**: Implement regular measurement and reporting processes
7. **Engage stakeholders**: Communicate with and involve employees, suppliers, and customers
8. **Review and adapt**: Regularly assess progress and adjust strategies as needed
""")

# Emission reduction success factors
st.markdown("### Key Success Factors for Emissions Reduction")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Organizational Factors")
    st.markdown("""
    - **Executive leadership support**: Ensure sustainability is a strategic priority
    - **Cross-functional teams**: Break down silos between departments
    - **Clear governance structure**: Define responsibilities and decision-making processes
    - **Performance incentives**: Link compensation to emissions reduction targets
    - **Employee engagement**: Build a culture of sustainability across the organization
    """)
    
with col2:
    st.markdown("#### Technical Factors")
    st.markdown("""
    - **Robust data management**: Establish systems to collect accurate emissions data
    - **Regular progress monitoring**: Track initiatives against targets
    - **Technology assessment process**: Evaluate new low-carbon technologies
    - **Financial analysis tools**: Quantify costs and benefits of reduction initiatives
    - **Scenario planning**: Prepare for different possible future scenarios
    """)

# Case Studies
st.markdown("### Case Studies: Successful Emission Reduction")

case_studies = [
    {
        "company": "Microsoft",
        "industry": "Information Technology",
        "strategies": "Carbon neutrality since 2012; commitment to be carbon negative by 2030; $1B climate innovation fund; internal carbon fee",
        "results": "Reduced emissions by over 10M tCO2e; on track to reduce Scope 3 emissions by 55% by 2030"
    },
    {
        "company": "Unilever",
        "industry": "Food & Beverage / Consumer Goods",
        "strategies": "Transition to renewable energy; reformulation of products; supplier engagement; packaging redesign",
        "results": "70% reduction in manufacturing emissions since 2008; net zero emissions target by 2039"
    },
    {
        "company": "Ørsted",
        "industry": "Energy",
        "strategies": "Transformed from fossil fuel company to renewable energy; divested coal assets; invested in offshore wind",
        "results": "Reduced carbon intensity by 87% since 2006; on track for carbon neutrality in energy generation by 2025"
    },
    {
        "company": "IKEA",
        "industry": "Retail",
        "strategies": "Renewable energy investments; sustainable sourcing; circular product design; electric delivery vehicles",
        "results": "Reduced climate footprint by 17.3% relative to growth; committed to climate positive by 2030"
    }
]

# Display case studies
selected_case_study = st.selectbox(
    "Select a case study to learn more",
    [cs["company"] for cs in case_studies]
)

# Find the selected case study
case_study_detail = next((cs for cs in case_studies if cs["company"] == selected_case_study), None)

if case_study_detail:
    st.markdown(f"#### {case_study_detail['company']} ({case_study_detail['industry']})")
    st.markdown(f"**Key Strategies**: {case_study_detail['strategies']}")
    st.markdown(f"**Results**: {case_study_detail['results']}")

# Resources section
st.markdown("### Additional Resources")
st.markdown("""
#### Tools and Frameworks
- [Greenhouse Gas Protocol](https://ghgprotocol.org/) - Standard for GHG emissions accounting
- [Science Based Targets initiative](https://sciencebasedtargets.org/) - Framework for setting emissions reduction targets
- [CDP (Carbon Disclosure Project)](https://www.cdp.net/) - Global disclosure system for environmental reporting

#### Industry Associations
- [We Mean Business Coalition](https://www.wemeanbusinesscoalition.org/) - Coalition of businesses taking action on climate change
- [RE100](https://www.there100.org/) - Global initiative for 100% renewable electricity

#### Technical Guidance
- [Project Drawdown](https://drawdown.org/) - Comprehensive resource on climate solutions
- [EPA Center for Corporate Climate Leadership](https://www.epa.gov/climateleadership) - Resources for corporate emissions reduction
""")

# Disclaimer
st.markdown("---")
st.markdown("""
**Disclaimer**: The recommendations provided here are general in nature and based on your reported emissions profile. 
Detailed technical and financial analysis is recommended before implementing specific strategies. Regulatory requirements, 
technological options, and best practices may vary by location and over time.
""")
