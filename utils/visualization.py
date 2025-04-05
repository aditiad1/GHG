import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_emissions_pie_chart(values, labels):
    """
    Create a pie chart of emissions by scope
    
    Args:
        values (list): List of emission values
        labels (list): List of emission source labels
        
    Returns:
        plotly.graph_objects.Figure: Pie chart figure
    """
    fig = px.pie(
        names=labels,
        values=values,
        title="Emissions by Scope",
        color_discrete_sequence=px.colors.sequential.Greens_r
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hoverinfo='label+value+percent'
    )
    
    fig.update_layout(
        legend_title="Scopes",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=60, b=60, l=30, r=30)
    )
    
    return fig

def create_emissions_bar_chart(categories, values, scopes):
    """
    Create a bar chart of emissions by category
    
    Args:
        categories (list): List of emission categories
        values (list): List of emission values
        scopes (list): List of scopes for each category
        
    Returns:
        plotly.graph_objects.Figure: Bar chart figure
    """
    # Create dataframe for plotting
    df = pd.DataFrame({
        'Category': categories,
        'Emissions (tCO2e)': values,
        'Scope': scopes
    })
    
    # Filter out zero values for cleaner visualization
    df = df[df['Emissions (tCO2e)'] > 0]
    
    # Sort by emissions value in descending order
    df = df.sort_values('Emissions (tCO2e)', ascending=False)
    
    # Create the bar chart
    fig = px.bar(
        df,
        x='Category',
        y='Emissions (tCO2e)',
        color='Scope',
        title="Emissions by Category",
        color_discrete_map={
            "Scope 1": "#2E7D32",
            "Scope 2": "#4CAF50",
            "Scope 3": "#81C784"
        }
    )
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Emissions (tCO2e)",
        xaxis={'categoryorder': 'total descending'},
        plot_bgcolor="white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=60, b=100, l=60, r=30)
    )
    
    # Rotate x-axis labels for better readability
    fig.update_xaxes(tickangle=45)
    
    return fig

def create_reduction_pathway_chart(base_year, base_emissions, target_year, target_emissions):
    """
    Create a line chart showing the emissions reduction pathway
    
    Args:
        base_year (int): Base year
        base_emissions (float): Base year emissions
        target_year (int): Target year
        target_emissions (float): Target year emissions
        
    Returns:
        plotly.graph_objects.Figure: Line chart figure
    """
    # Generate years between base_year and target_year
    years = list(range(base_year, target_year + 1))
    
    # Calculate linear reduction pathway
    num_years = target_year - base_year
    annual_reduction = (base_emissions - target_emissions) / num_years
    
    # Linear pathway
    linear_emissions = [base_emissions - annual_reduction * i for i in range(len(years))]
    
    # Create dataframe for plotting
    df = pd.DataFrame({
        'Year': years,
        'Emissions (tCO2e)': linear_emissions
    })
    
    # Create line chart
    fig = px.line(
        df,
        x='Year',
        y='Emissions (tCO2e)',
        title=f"Emissions Reduction Pathway ({base_year}-{target_year})",
        markers=True
    )
    
    # Add markers for key points
    fig.add_trace(
        go.Scatter(
            x=[base_year, target_year],
            y=[base_emissions, target_emissions],
            mode='markers',
            marker=dict(size=12, color='red'),
            name='Key Milestones'
        )
    )
    
    # Add annotations
    fig.add_annotation(
        x=base_year,
        y=base_emissions,
        text=f"Base: {base_emissions:.1f} tCO2e",
        showarrow=True,
        arrowhead=1,
        ax=40,
        ay=-40
    )
    
    fig.add_annotation(
        x=target_year,
        y=target_emissions,
        text=f"Target: {target_emissions:.1f} tCO2e",
        showarrow=True,
        arrowhead=1,
        ax=-40,
        ay=-40
    )
    
    # Customize layout
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Emissions (tCO2e)",
        plot_bgcolor="white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="right",
            x=1
        ),
        margin=dict(t=60, b=60, l=60, r=30)
    )
    
    # Set axis properties
    fig.update_xaxes(
        tickmode='linear',
        tick0=base_year,
        dtick=max(1, (target_year - base_year) // 5)  # Set tick spacing based on time range
    )
    
    return fig

def create_scope_comparison_radar_chart(company_values, industry_values, labels):
    """
    Create a radar chart comparing company scope distribution with industry average
    
    Args:
        company_values (list): List of company percentages by scope
        industry_values (list): List of industry average percentages by scope
        labels (list): List of scope labels
        
    Returns:
        plotly.graph_objects.Figure: Radar chart figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=company_values,
        theta=labels,
        fill='toself',
        name='Your Organization'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=industry_values,
        theta=labels,
        fill='toself',
        name='Industry Average'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(company_values), max(industry_values)) * 1.1]
            )
        ),
        title="Scope Distribution Comparison",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=60, b=60, l=60, r=60)
    )
    
    return fig

def create_industry_comparison_chart(company_intensity, industry_data):
    """
    Create a bar chart comparing company emissions intensity with industry benchmarks
    
    Args:
        company_intensity (float): Company emissions intensity
        industry_data (dict): Dictionary containing industry benchmark data
        
    Returns:
        plotly.graph_objects.Figure: Bar chart figure
    """
    # Prepare data for comparison
    comparison_data = {
        "Category": ["Your Organization", "Industry Best", "Industry Average", "Industry Worst"],
        "Emissions Intensity": [
            company_intensity, 
            industry_data["best_performer"], 
            industry_data["avg_intensity"], 
            industry_data["worst_performer"]
        ]
    }
    
    df = pd.DataFrame(comparison_data)
    
    # Create bar chart
    fig = px.bar(
        df,
        x="Category",
        y="Emissions Intensity",
        title="Industry Emissions Intensity Comparison (tCO2e/$M revenue)",
        color="Category",
        color_discrete_map={
            "Your Organization": "#1f77b4",
            "Industry Best": "#2ca02c",
            "Industry Average": "#ff7f0e",
            "Industry Worst": "#d62728"
        }
    )
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Emissions Intensity (tCO2e/$M revenue)",
        plot_bgcolor="white",
        showlegend=False,
        margin=dict(t=60, b=40, l=60, r=30)
    )
    
    return fig

def create_carbon_credit_comparison_chart(offset_amount, credit_types, price_scenario="avg_price"):
    """
    Create a bar chart comparing costs across different carbon credit types
    
    Args:
        offset_amount (float): Amount of emissions to offset
        credit_types (dict): Dictionary of carbon credit types and prices
        price_scenario (str): Price scenario to use (min_price, avg_price, max_price)
        
    Returns:
        plotly.graph_objects.Figure: Bar chart figure
    """
    # Prepare data for comparison
    comparison_data = []
    
    for credit_type, prices in credit_types.items():
        comparison_data.append({
            "Credit Type": credit_type,
            "Minimum Cost": offset_amount * prices["min_price"],
            "Average Cost": offset_amount * prices["avg_price"],
            "Maximum Cost": offset_amount * prices["max_price"]
        })
    
    df = pd.DataFrame(comparison_data)
    
    # Melt dataframe for visualization
    df_melted = pd.melt(
        df,
        id_vars=["Credit Type"],
        value_vars=["Minimum Cost", "Average Cost", "Maximum Cost"],
        var_name="Cost Scenario",
        value_name="Total Cost (USD)"
    )
    
    # Create bar chart
    fig = px.bar(
        df_melted,
        x="Credit Type",
        y="Total Cost (USD)",
        color="Cost Scenario",
        title=f"Cost to Offset {offset_amount:.2f} tCO2e",
        barmode="group",
        color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c"]
    )
    
    fig.update_layout(
        xaxis_title="Carbon Credit Type",
        yaxis_title="Cost (USD)",
        plot_bgcolor="white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=60, b=100, l=60, r=30)
    )
    
    return fig
