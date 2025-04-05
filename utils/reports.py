import streamlit as st
from datetime import datetime
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import numpy as np
import io
import plotly.io as pio
import base64

def generate_report(company_data, total_emissions, emissions_by_scope, scope1_breakdown, scope2_breakdown, scope3_breakdown, targets):
    """
    Generate a PDF report of emissions calculation results
    
    Args:
        company_data (dict): Dictionary containing company information
        total_emissions (float): Total emissions in tCO2e
        emissions_by_scope (dict): Dictionary containing emissions by scope
        scope1_breakdown (dict): Dictionary containing scope 1 emissions breakdown
        scope2_breakdown (dict): Dictionary containing scope 2 emissions breakdown
        scope3_breakdown (dict): Dictionary containing scope 3 emissions breakdown
        targets (dict): Dictionary containing emissions reduction targets
    
    Returns:
        str: Path to the generated PDF file
    """
    # In a real app, this would create a PDF file
    # For this example, we'll just print the report details to the console
    
    # Create report data for display
    report_data = {
        "Company Information": {
            "Name": company_data['name'],
            "Industry": company_data['industry'],
            "Employees": company_data['employees'],
            "Revenue": f"${company_data['revenue']} million",
            "Reporting Year": company_data['year']
        },
        "Emissions Summary": {
            "Total Emissions": f"{total_emissions:.2f} tCO2e",
            "Scope 1 Emissions": f"{emissions_by_scope['scope1']:.2f} tCO2e ({emissions_by_scope['scope1']/total_emissions*100:.1f}%)",
            "Scope 2 Emissions": f"{emissions_by_scope['scope2']:.2f} tCO2e ({emissions_by_scope['scope2']/total_emissions*100:.1f}%)",
            "Scope 3 Emissions": f"{emissions_by_scope['scope3']:.2f} tCO2e ({emissions_by_scope['scope3']/total_emissions*100:.1f}%)",
            "Emissions per Employee": f"{total_emissions/company_data['employees']:.2f} tCO2e",
            "Emissions Intensity": f"{total_emissions/company_data['revenue']:.2f} tCO2e per million USD"
        },
        "Reduction Targets": {
            "2030 Target": f"{targets['2030']:.2f} tCO2e",
            "Required Annual Reduction": f"{targets['annual_reduction']:.2f} tCO2e"
        },
        "Scope 1 Breakdown": scope1_breakdown,
        "Scope 2 Breakdown": scope2_breakdown,
        "Scope 3 Breakdown": scope3_breakdown
    }
    
    # In a real app, we would generate a PDF using a library like ReportLab
    # But for this example, we'll just simulate the report generation
    
    print("\n=== GHG EMISSIONS REPORT ===")
    print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n--- COMPANY INFORMATION ---")
    for key, value in report_data["Company Information"].items():
        print(f"{key}: {value}")
    
    print("\n--- EMISSIONS SUMMARY ---")
    for key, value in report_data["Emissions Summary"].items():
        print(f"{key}: {value}")
    
    print("\n--- REDUCTION TARGETS ---")
    for key, value in report_data["Reduction Targets"].items():
        print(f"{key}: {value}")
    
    print("\n--- SCOPE 1 BREAKDOWN ---")
    for category, value in report_data["Scope 1 Breakdown"].items():
        print(f"{category}: {value:.2f} tCO2e")
    
    print("\n--- SCOPE 2 BREAKDOWN ---")
    for category, value in report_data["Scope 2 Breakdown"].items():
        print(f"{category}: {value:.2f} tCO2e")
    
    print("\n--- SCOPE 3 BREAKDOWN ---")
    for category, value in report_data["Scope 3 Breakdown"].items():
        print(f"{category}: {value:.2f} tCO2e")
    
    print("\n=== END OF REPORT ===")
    
    # In a real app, we would return the path to the generated PDF
    return "emissions_report.pdf"

def create_pdf_report(company_data, total_emissions, emissions_by_scope, scope1_breakdown, scope2_breakdown, scope3_breakdown, targets):
    """
    Create a PDF report using ReportLab
    
    Args:
        company_data (dict): Dictionary containing company information
        total_emissions (float): Total emissions in tCO2e
        emissions_by_scope (dict): Dictionary containing emissions by scope
        scope1_breakdown (dict): Dictionary containing scope 1 emissions breakdown
        scope2_breakdown (dict): Dictionary containing scope 2 emissions breakdown
        scope3_breakdown (dict): Dictionary containing scope 3 emissions breakdown
        targets (dict): Dictionary containing emissions reduction targets
    
    Returns:
        BytesIO: PDF file as bytes
    """
    # In a real application, this would create an actual PDF file
    # For this demo, we'll create a simple structure of what would be included
    
    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()
    
    # Create the PDF object
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    subheading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Add title
    elements.append(Paragraph(f"GHG Emissions Report: {company_data['name']}", title_style))
    elements.append(Paragraph(f"Reporting Year: {company_data['year']}", subheading_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Company Information
    elements.append(Paragraph("Company Information", heading_style))
    company_info = [
        ["Company Name:", company_data['name']],
        ["Industry:", company_data['industry']],
        ["Employees:", str(company_data['employees'])],
        ["Revenue:", f"${company_data['revenue']} million"],
        ["Reporting Year:", str(company_data['year'])]
    ]
    company_table = Table(company_info, colWidths=[2*inch, 4*inch])
    company_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(company_table)
    elements.append(Spacer(1, 0.25*inch))
    
    # Emissions Summary
    elements.append(Paragraph("Emissions Summary", heading_style))
    emissions_info = [
        ["Total Emissions:", f"{total_emissions:.2f} tCO2e"],
        ["Scope 1 Emissions:", f"{emissions_by_scope['scope1']:.2f} tCO2e ({emissions_by_scope['scope1']/total_emissions*100:.1f}%)"],
        ["Scope 2 Emissions:", f"{emissions_by_scope['scope2']:.2f} tCO2e ({emissions_by_scope['scope2']/total_emissions*100:.1f}%)"],
        ["Scope 3 Emissions:", f"{emissions_by_scope['scope3']:.2f} tCO2e ({emissions_by_scope['scope3']/total_emissions*100:.1f}%)"],
        ["Emissions per Employee:", f"{total_emissions/company_data['employees']:.2f} tCO2e"],
        ["Emissions Intensity:", f"{total_emissions/company_data['revenue']:.2f} tCO2e per million USD"]
    ]
    emissions_table = Table(emissions_info, colWidths=[2*inch, 4*inch])
    emissions_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(emissions_table)
    elements.append(Spacer(1, 0.25*inch))
    
    # Reduction Targets
    elements.append(Paragraph("Reduction Targets", heading_style))
    targets_info = [
        ["2030 Target:", f"{targets['2030']:.2f} tCO2e"],
        ["Required Annual Reduction:", f"{targets['annual_reduction']:.2f} tCO2e"]
    ]
    targets_table = Table(targets_info, colWidths=[2*inch, 4*inch])
    targets_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(targets_table)
    elements.append(Spacer(1, 0.25*inch))
    
    # Scope Breakdowns
    # Scope 1
    if scope1_breakdown:
        elements.append(Paragraph("Scope 1 Emissions Breakdown", heading_style))
        scope1_data = [["Category", "Emissions (tCO2e)"]]
        for category, value in scope1_breakdown.items():
            scope1_data.append([category, f"{value:.2f}"])
        scope1_table = Table(scope1_data, colWidths=[3*inch, 3*inch])
        scope1_table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(scope1_table)
        elements.append(Spacer(1, 0.25*inch))
    
    # Scope 2
    if scope2_breakdown:
        elements.append(Paragraph("Scope 2 Emissions Breakdown", heading_style))
        scope2_data = [["Category", "Emissions (tCO2e)"]]
        for category, value in scope2_breakdown.items():
            scope2_data.append([category, f"{value:.2f}"])
        scope2_table = Table(scope2_data, colWidths=[3*inch, 3*inch])
        scope2_table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(scope2_table)
        elements.append(Spacer(1, 0.25*inch))
    
    # Scope 3
    if scope3_breakdown:
        elements.append(Paragraph("Scope 3 Emissions Breakdown", heading_style))
        scope3_data = [["Category", "Emissions (tCO2e)"]]
        for category, value in scope3_breakdown.items():
            scope3_data.append([category, f"{value:.2f}"])
        scope3_table = Table(scope3_data, colWidths=[3*inch, 3*inch])
        scope3_table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(scope3_table)
        elements.append(Spacer(1, 0.25*inch))
    
    # Recommendations
    elements.append(Paragraph("Recommendations for Emissions Reduction", heading_style))
    elements.append(Paragraph("Based on your emissions profile, consider these recommended actions:", normal_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Add recommendations based on dominant scope
    scope_values = [
        ("Scope 1", emissions_by_scope['scope1']),
        ("Scope 2", emissions_by_scope['scope2']),
        ("Scope 3", emissions_by_scope['scope3'])
    ]
    dominant_scope = max(scope_values, key=lambda x: x[1])[0]
    
    if dominant_scope == "Scope 1":
        recommendations = [
            "Implement energy efficiency improvements in facilities",
            "Consider switching to low-carbon fuels where possible",
            "Optimize HVAC systems and building controls",
            "Electrify vehicle fleet and other equipment",
            "Implement a refrigerant management program"
        ]
    elif dominant_scope == "Scope 2":
        recommendations = [
            "Purchase renewable energy through PPAs or RECs",
            "Install on-site renewable energy generation",
            "Implement comprehensive energy efficiency program",
            "Optimize building management systems",
            "Consider green building certification for facilities"
        ]
    else:  # Scope 3
        recommendations = [
            "Engage with key suppliers on emissions reduction",
            "Develop a sustainable procurement policy",
            "Optimize product design to reduce lifecycle emissions",
            "Implement circular economy initiatives",
            "Reduce business travel and optimize logistics"
        ]
    
    for i, recommendation in enumerate(recommendations, 1):
        elements.append(Paragraph(f"{i}. {recommendation}", normal_style))
        elements.append(Spacer(1, 0.05*inch))
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(f"Report generated on: {datetime.now().strftime('%Y-%m-%d')}", normal_style))
    elements.append(Paragraph("GHG Emissions Calculator", normal_style))
    
    # Build the PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and return it
    buffer.seek(0)
    return buffer

def get_download_link(pdf_bytes, filename="emissions_report.pdf", text="Download Report"):
    """
    Generate a download link for a PDF file
    
    Args:
        pdf_bytes (BytesIO): PDF file as bytes
        filename (str): Name of the file to download
        text (str): Text to display for the download link
        
    Returns:
        str: HTML for download link
    """
    # Encode the PDF bytes to base64
    b64 = base64.b64encode(pdf_bytes.getvalue()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">{text}</a>'
    return href

def export_plots_for_report(company_data, total_emissions, emissions_by_scope, scope1_breakdown, scope2_breakdown, scope3_breakdown, targets):
    """
    Export plotly figures as images for inclusion in reports
    
    Args:
        company_data (dict): Dictionary containing company information
        total_emissions (float): Total emissions in tCO2e
        emissions_by_scope (dict): Dictionary containing emissions by scope
        scope1_breakdown (dict): Dictionary containing scope 1 emissions breakdown
        scope2_breakdown (dict): Dictionary containing scope 2 emissions breakdown
        scope3_breakdown (dict): Dictionary containing scope 3 emissions breakdown
        targets (dict): Dictionary containing emissions reduction targets
        
    Returns:
        dict: Dictionary containing image bytes for each plot
    """
    # In a real application, this would export the actual plots
    # For this demo, we'll just return placeholder data
    
    # Create placeholder images
    plot_bytes = {}
    
    # In a real application, we would use Plotly's export functionality, e.g.:
    # from utils.visualization import create_emissions_pie_chart
    # scope_values = [emissions_by_scope['scope1'], emissions_by_scope['scope2'], emissions_by_scope['scope3']]
    # scope_labels = ["Scope 1", "Scope 2", "Scope 3"]
    # fig = create_emissions_pie_chart(scope_values, scope_labels)
    # img_bytes = pio.to_image(fig, format="png")
    # plot_bytes["emissions_by_scope"] = img_bytes
    
    return plot_bytes
