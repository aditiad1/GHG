import streamlit as st
import streamlit.components.v1 as components
import re
from typing import List, Dict, Optional, Union

def is_url_safe(url: str) -> bool:
    """
    Check if a URL is potentially safe to embed
    
    Args:
        url (str): The URL to check
        
    Returns:
        bool: True if the URL seems safe, False otherwise
    """
    # Check if URL is using http or https
    if not (url.startswith('http://') or url.startswith('https://')):
        return False
    
    # Basic pattern check for a valid URL
    url_pattern = re.compile(
        r'^(?:http|https)://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url))

def safe_embed(url: str, height: int = 600, width: Optional[int] = None, scrolling: bool = True) -> None:
    """
    Safely embed an external website with error handling
    
    Args:
        url (str): URL to embed
        height (int): Height of the iframe in pixels
        width (Optional[int]): Width of the iframe in pixels (None for full width)
        scrolling (bool): Whether to enable scrolling
    """
    if not is_url_safe(url):
        st.error(f"URL validation failed: {url}. The URL format is invalid or potentially unsafe.")
        return
    
    try:
        # Add some styling to make the iframe look nicer
        if width is None:
            components.iframe(url, height=height, scrolling=scrolling)
        else:
            components.iframe(url, height=height, width=width, scrolling=scrolling)
    except Exception as e:
        st.error(f"Error embedding {url}: {str(e)}")

def embed_with_fallback(url: str, fallback_message: str, height: int = 600) -> None:
    """
    Embed content with a fallback message if embedding fails
    
    Args:
        url (str): URL to embed
        fallback_message (str): Message to display if embedding fails
        height (int): Height of the iframe in pixels
    """
    if not is_url_safe(url):
        st.warning(fallback_message)
        st.code(url, language="text")
        return
    
    try:
        components.iframe(url, height=height, scrolling=True)
    except Exception:
        st.warning(fallback_message)
        st.code(url, language="text")

def embed_html_content(html_content: str, height: int = 600) -> None:
    """
    Embed custom HTML content
    
    Args:
        html_content (str): HTML content to embed
        height (int): Height of the component in pixels
    """
    try:
        components.html(html_content, height=height)
    except Exception as e:
        st.error(f"Error embedding HTML content: {str(e)}")
        st.code(html_content[:100] + "..." if len(html_content) > 100 else html_content, language="html")

def get_embed_code(url: str, width: str = "100%", height: str = "600px") -> str:
    """
    Generate HTML embed code for a URL that users can copy
    
    Args:
        url (str): URL to generate embed code for
        width (str): Width of the iframe
        height (str): Height of the iframe
        
    Returns:
        str: HTML embed code
    """
    return f'<iframe src="{url}" width="{width}" height="{height}" frameborder="0" scrolling="yes"></iframe>'

def create_embed_library() -> Dict[str, Dict[str, Union[str, List[Dict[str, str]]]]]:
    """
    Create a library of useful embeddable resources for emissions and sustainability
    
    Returns:
        dict: Dictionary of categorized embeddable resources
    """
    return {
        "Carbon Calculators": {
            "description": "Tools for calculating carbon footprints",
            "resources": [
                {
                    "name": "EPA Carbon Footprint Calculator",
                    "url": "https://www3.epa.gov/carbon-footprint-calculator/",
                    "description": "Calculate your household carbon footprint"
                },
                {
                    "name": "Carbon Fund Calculator",
                    "url": "https://carbonfund.org/calculation-methods/",
                    "description": "Calculate and offset your carbon footprint"
                },
                {
                    "name": "Carbon Footprint Calculator",
                    "url": "https://www.carbonfootprint.com/calculator.aspx",
                    "description": "Comprehensive carbon footprint calculator"
                }
            ]
        },
        "Climate Data": {
            "description": "Sources of climate data and statistics",
            "resources": [
                {
                    "name": "Our World in Data - CO2 Emissions",
                    "url": "https://ourworldindata.org/co2-emissions",
                    "description": "Global CO2 emissions data and visualizations"
                },
                {
                    "name": "Climate Action Tracker",
                    "url": "https://climateactiontracker.org/",
                    "description": "Track countries' climate action"
                },
                {
                    "name": "Global Carbon Atlas",
                    "url": "http://www.globalcarbonatlas.org/en/CO2-emissions",
                    "description": "Explore CO2 emissions by country and sector"
                }
            ]
        },
        "Sustainability Tools": {
            "description": "Tools for sustainability planning",
            "resources": [
                {
                    "name": "Science Based Targets Initiative",
                    "url": "https://sciencebasedtargets.org/",
                    "description": "Set science-based emissions reduction targets"
                },
                {
                    "name": "CDP Disclosure Platform",
                    "url": "https://www.cdp.net/en",
                    "description": "Environmental disclosure system"
                },
                {
                    "name": "GHG Protocol",
                    "url": "https://ghgprotocol.org/",
                    "description": "GHG accounting and reporting standards"
                }
            ]
        },
        "Reporting Standards": {
            "description": "Frameworks for emissions reporting",
            "resources": [
                {
                    "name": "GRI Standards",
                    "url": "https://www.globalreporting.org/standards/",
                    "description": "Global Reporting Initiative standards"
                },
                {
                    "name": "TCFD Recommendations",
                    "url": "https://www.fsb-tcfd.org/",
                    "description": "Climate-related financial disclosures"
                },
                {
                    "name": "SASB Standards",
                    "url": "https://www.sasb.org/",
                    "description": "Industry-specific sustainability standards"
                }
            ]
        }
    }