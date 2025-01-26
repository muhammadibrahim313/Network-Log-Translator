import os
import streamlit as st
import speech_recognition as sr
from dotenv import load_dotenv
import pyperclip

# Fix Groq import
try:
    from groq import Groq
except ImportError:
    from groq.client import Groq

# Load environment variables
load_dotenv()

# Custom CSS for Premium Look
def set_custom_style():
    st.markdown("""
    <style>
    /* Global Styling */
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        background-color: #f4f6f9;
        color: #2c3e50;
    }

    /* Header Styling */
    .stApp > header {
        background-color: transparent;
    }

    /* Container Styling */
    .stContainer {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Button Styling */
    .stButton > button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #2980b9;
        transform: scale(1.05);
    }

    /* Input Styling */
    .stTextArea > div > textarea {
        border-radius: 10px;
        border: 1.5px solid #e0e4e8;
        background-color: #f8f9fa;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Sidebar Styling */
    .css-1aumxhk {
        background-color: #2c3e50;
        color: white;
    }

    .css-1aumxhk .stRadio > label {
        color: white !important;
    }

    /* Team Member Cards */
    .team-card {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 15px;
        text-align: center;
        transition: transform 0.3s ease;
    }

    .team-card:hover {
        transform: translateY(-10px);
    }

    /* Expander Styling */
    .stExpander {
        border-radius: 10px;
        border: 1.5px solid #e0e4e8;
    }
    </style>
    """, unsafe_allow_html=True)

# Predefined Common Network Errors
COMMON_ERRORS = {
    "DNS_PROBE_FINISHED_NO_INTERNET": "DNS resolution failed. Unable to connect to internet.",
    "Connection Timed Out": "Network connection could not be established within expected timeframe.",
    "No Route to Host": "Network path to destination is unavailable.",
    "Connection Refused": "Remote server rejected connection attempt.",
    "SSL Handshake Failed": "Secure connection could not be established.",
}

# Language to BCP-47 Code Mapping for Speech Recognition
LANGUAGE_CODES = {
    'English': 'en-US', 'Urdu': 'ur-PK', 'Spanish': 'es-ES',
    'French': 'fr-FR', 'Arabic': 'ar-SA', 'Afrikaans': 'af-ZA',
    'Zulu': 'zu-ZA', 'Xhosa': 'xh-ZA', 'Sotho': 'st-ZA',
    'Tswana': 'tn-ZA'
}

# All other functions remain the same as in the previous implementation
# (initialize_groq_client, classify_error, get_severity, generate_explanation, speech_to_text)

# Landing Page with Enhanced Styling
def landing_page():
    set_custom_style()
    st.title("🌐 Network Log Translator")
    st.markdown("""
    ### Simplify Complex Network Errors with AI-Powered Troubleshooting

    **Cutting-edge solutions for network diagnostics:**
    - 🛠️ Instant Error Analysis
    - 🌍 Multilingual Support
    - 🎤 Voice & Text Inputs
    - 📋 Quick Diagnostic Commands
    """)
    
    cols = st.columns([1, 1, 1])
    with cols[1]:
        st.image("https://ideogram.ai/assets/image/lossless/response/fjemlPTxRSagPZPIt9w44Q", 
                 use_column_width=True, 
                 caption="AI-Powered Network Diagnostics")

# About Us Page with Team Card Styling
def about_us_page():
    set_custom_style()
    st.title("👥 Network Solutions Team")
    
    team_members = [
        {"name": "Humam", "role": "Backend Developer", "image": "https://via.placeholder.com/150.png?text=Humam"},
        {"name": "Muhammad Ibrahim Qasmi", "role": "Data Scientist", "image": "https://media.licdn.com/dms/image/v2/D4D03AQFCNX1cJg9J8w/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1732156800150?e=1743638400&v=beta&t=5nk_TRhQGlSX-I0tp0cf9ZHwJzFOLrLWWkxTdTrn6EU"},
        {"name": "Ahmad Fakhar", "role": "AI Engineer", "image": "https://media.licdn.com/dms/image/v2/D4D03AQFrxTgmUio4Mw/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1732197610882?e=1743638400&v=beta&t=we1bOWBoC3ZrXcus979HRY1yT9tRUsKa3dc7-JWZSXI"},
        {"name": "Muhammad Zia", "role": "UI/UX Designer", "image": "https://via.placeholder.com/150.png?text=Zia"},
        {"name": "Tayyab Sajjad", "role": "Data Scientist", "image": "https://media.licdn.com/dms/image/v2/D4E03AQELdwDpn2a9Bg/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1732042661073?e=1743638400&v=beta&t=6vX_f7IeZETm70ZZ8x-h6_vH6uDJ9f-2S6SGPVcHIOU"},
        {"name": "Frank", "role": "Project Manager", "image": "https://via.placeholder.com/150.png?text=Frank"}
    ]

    st.markdown("### Our Dedicated Team of Network Experts")
    
    rows = [team_members[i:i+3] for i in range(0, len(team_members), 3)]
    for row in rows:
        cols = st.columns(3)
        for col, member in zip(cols, row):
            with col:
                with st.container():
                    st.image(member['image'], width=150, use_column_width=False)
                    st.markdown(f"**{member['name']}**")
                    st.caption(member['role'])

# Translator Page with Enhanced Interactions
def translator_page():
    set_custom_style()
    st.title("🌐 Smart Network Troubleshooter")
    
    # Rest of the translator_page implementation remains the same
    # (Include all previous logic for input, processing, and display)

def main():
    st.set_page_config(
        page_title="Network Log Translator", 
        page_icon="🌐", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar Navigation with Enhanced Styling
    st.sidebar.title("🔍 Network Diagnostics")
    page = st.sidebar.radio(
        "Navigation", 
        ["🏠 Landing Page", "🌐 Translator", "👥 About Us"],
        label_visibility="collapsed"
    )

    # Page Routing
    if page == "🏠 Landing Page":
        landing_page()
    elif page == "🌐 Translator":
        translator_page()
    elif page == "👥 About Us":
        about_us_page()

if __name__ == "__main__":
    main()
