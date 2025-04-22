import streamlit as st
import subprocess
from app import display_dashboard

st.set_page_config(page_title="📘 Web Scraper App", page_icon="🌐", layout="centered")

st.title("🌐 Web Scraper & Book Analyzer")
st.markdown("---")

page = st.sidebar.selectbox("Navigation", ["🏠 Home", "🔍 Run Web Scraper", "📊 Analyze Data", "📈 Dashboard"])

if page == "🏠 Home":
    st.subheader("Welcome!")
    st.write("Use this app to scrape book data, analyze prices, and visualize insights.")

elif page == "🔍 Run Web Scraper":
    st.subheader("Running Web Scraper...")
    result = subprocess.run(["python", "scraper.py"], capture_output=True, text=True)
    st.code(result.stdout)
    if result.stderr:
        st.error(result.stderr)
    else:
        st.success("Scraping completed successfully.")

elif page == "📊 Analyze Data":
    st.subheader("Analyzing Data...")
    result = subprocess.run(["python", "analyze_data.py"], capture_output=True, text=True)
    st.code(result.stdout)
    if result.stderr:
        st.error(result.stderr)
    else:
        st.success("Analysis completed.")

elif page == "📈 Dashboard":
    st.subheader("Interactive Dashboard")
    display_dashboard()
