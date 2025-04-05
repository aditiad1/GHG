import streamlit as st
import streamlit.components.v1 as components

def main():
    st.title("External Resources")
    st.subheader("Access helpful third-party tools and resources")
    
    # Create tabs for different categories of external resources
    tab1, tab2, tab3, tab4 = st.tabs(["Carbon Calculators", "Climate Data", "Sustainability Tools", "Reporting Standards"])
    
    with tab1:
        st.header("Carbon Calculators")
        st.write("These tools can help you calculate emissions for specific activities or compare with your existing calculations.")
        
        calculator_option = st.selectbox(
            "Select a calculator to embed:",
            ["EPA Carbon Footprint Calculator", "Carbon Fund Calculator", "Carbon Footprint Calculator", "Custom URL"]
        )
        
        if calculator_option == "EPA Carbon Footprint Calculator":
            st.write("EPA's Carbon Footprint Calculator helps you estimate your household's annual carbon footprint.")
            components.iframe("https://www3.epa.gov/carbon-footprint-calculator/", height=600, scrolling=True)
        
        elif calculator_option == "Carbon Fund Calculator":
            st.write("Calculate and offset your carbon footprint with Carbon Fund's calculator.")
            components.iframe("https://carbonfund.org/calculation-methods/", height=600, scrolling=True)
        
        elif calculator_option == "Carbon Footprint Calculator":
            st.write("A comprehensive carbon footprint calculator for individuals and businesses.")
            components.iframe("https://www.carbonfootprint.com/calculator.aspx", height=600, scrolling=True)
        
        elif calculator_option == "Custom URL":
            custom_url = st.text_input("Enter the URL of the calculator you want to embed:")
            if custom_url:
                try:
                    components.iframe(custom_url, height=600, scrolling=True)
                except Exception as e:
                    st.error(f"Error embedding the URL: {e}")
    
    with tab2:
        st.header("Climate Data")
        st.write("Access the latest climate data and emissions statistics.")
        
        data_option = st.selectbox(
            "Select a data source:",
            ["Our World in Data - CO2 Emissions", "Climate Action Tracker", "Global Carbon Atlas", "Custom URL"]
        )
        
        if data_option == "Our World in Data - CO2 Emissions":
            st.write("Explore CO2 and greenhouse gas emissions data worldwide.")
            components.iframe("https://ourworldindata.org/co2-emissions", height=600, scrolling=True)
        
        elif data_option == "Climate Action Tracker":
            st.write("Track countries' climate action and global efforts to tackle climate change.")
            components.iframe("https://climateactiontracker.org/", height=600, scrolling=True)
        
        elif data_option == "Global Carbon Atlas":
            st.write("Explore CO2 emissions by country and sector using interactive visualizations.")
            components.iframe("http://www.globalcarbonatlas.org/en/CO2-emissions", height=600, scrolling=True)
        
        elif data_option == "Custom URL":
            custom_url = st.text_input("Enter the URL of the climate data source you want to embed:", key="climate_data_url")
            if custom_url:
                try:
                    components.iframe(custom_url, height=600, scrolling=True)
                except Exception as e:
                    st.error(f"Error embedding the URL: {e}")
    
    with tab3:
        st.header("Sustainability Tools")
        st.write("Tools to help with sustainability planning and emissions reduction strategies.")
        
        tool_option = st.selectbox(
            "Select a sustainability tool:",
            ["Science Based Targets Initiative", "CDP Disclosure Platform", "GHG Protocol", "Custom URL"]
        )
        
        if tool_option == "Science Based Targets Initiative":
            st.write("Learn how to set science-based emissions reduction targets.")
            components.iframe("https://sciencebasedtargets.org/", height=600, scrolling=True)
        
        elif tool_option == "CDP Disclosure Platform":
            st.write("Information about CDP's environmental disclosure system.")
            components.iframe("https://www.cdp.net/en", height=600, scrolling=True)
        
        elif tool_option == "GHG Protocol":
            st.write("Resources and standards for greenhouse gas accounting and reporting.")
            components.iframe("https://ghgprotocol.org/", height=600, scrolling=True)
        
        elif tool_option == "Custom URL":
            custom_url = st.text_input("Enter the URL of the sustainability tool you want to embed:", key="sustainability_url")
            if custom_url:
                try:
                    components.iframe(custom_url, height=600, scrolling=True)
                except Exception as e:
                    st.error(f"Error embedding the URL: {e}")
    
    with tab4:
        st.header("Reporting Standards")
        st.write("Learn about different frameworks and standards for emissions reporting.")
        
        standard_option = st.selectbox(
            "Select a reporting standard:",
            ["GRI Standards", "TCFD Recommendations", "SASB Standards", "Custom URL"]
        )
        
        if standard_option == "GRI Standards":
            st.write("Global Reporting Initiative's sustainability reporting standards.")
            components.iframe("https://www.globalreporting.org/standards/", height=600, scrolling=True)
        
        elif standard_option == "TCFD Recommendations":
            st.write("Task Force on Climate-related Financial Disclosures framework.")
            components.iframe("https://www.fsb-tcfd.org/", height=600, scrolling=True)
        
        elif standard_option == "SASB Standards":
            st.write("Sustainability Accounting Standards Board industry-specific standards.")
            components.iframe("https://www.sasb.org/", height=600, scrolling=True)
        
        elif standard_option == "Custom URL":
            custom_url = st.text_input("Enter the URL of the reporting standard you want to embed:", key="standard_url")
            if custom_url:
                try:
                    components.iframe(custom_url, height=600, scrolling=True)
                except Exception as e:
                    st.error(f"Error embedding the URL: {e}")
    
    # Add disclaimer
    st.divider()
    st.caption("Disclaimer: External websites are embedded for reference only. We do not own or control the content of these websites. "
              "Please review the privacy policy and terms of use of each website before providing any personal information.")

if __name__ == "__main__":
    main()