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
def set_custom_styling():
    st.markdown("""
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Poppins', sans-serif;
    }

    /* Header Styling */
    h1 {
        font-weight: 700;
        color: #2c3e50;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        letter-spacing: -1px;
    }

    /* Sidebar Styling */
    .css-1aumxhk {
        background: linear-gradient(145deg, #3494e6, #2c3e50);
        color: white !important;
    }

    .css-1aumxhk .stRadio > label {
        color: white !important;
    }

    /* Button Styling */
    .stButton > button {
        background-color: #3494e6 !important;
        color: white !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }

    .stButton > button:hover {
        background-color: #2c3e50 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 8px rgba(0,0,0,0.2) !important;
    }

    /* Card and Expander Styling */
    .stExpander {
        border-radius: 15px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        background-color: white !important;
    }

    /* Input Styling */
    .stTextArea > div > textarea {
        border-radius: 15px !important;
        border: 2px solid #3494e6 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Status Update Styling */
    .stStatus {
        background-color: rgba(52, 148, 230, 0.1) !important;
        border-radius: 15px !important;
    }

    /* Team Member Cards */
    .team-card {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 15px;
        text-align: center;
        transition: transform 0.3s ease;
    }

    .team-card:hover {
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Configuration
st.set_page_config(page_title="Network Log Translator", page_icon="🌐", layout="wide")

# Rest of your previous code remains the same...
# [Keep all the previous functions: COMMON_ERRORS, LANGUAGE_CODES, etc.]

# Updated Landing Page with Premium Design
def landing_page():
    set_custom_styling()
    st.title("🌐 Network Log Translator")
    st.markdown("""
    ### Intelligent Network Troubleshooting, Simplified
    Revolutionize your network problem-solving with AI-powered insights.
    """)
    
    # Feature Highlights
    cols = st.columns(3)
    features = [
        ("🚀 Instant Diagnosis", "Identify network issues in seconds"),
        ("🌍 Multilingual Support", "10+ language translations"),
        ("🤖 AI-Powered Solutions", "Intelligent troubleshooting")
    ]
    
    for col, (title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="team-card">
                <h3 style="color:#3494e6;">{title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Background Image or Illustration
    st.image("https://ideogram.ai/assets/image/lossless/response/fjemlPTxRSagPZPIt9w44Q", 
             use_column_width=True, 
             caption="AI-Powered Network Troubleshooting")

# Updated About Us Page
def about_us_page():
    set_custom_styling()
    st.title("👥 Our Innovative Team")
    st.markdown("""
    ### Passionate Developers Transforming Network Troubleshooting
    We combine expertise in AI, data science, and user experience to solve complex network challenges.
    """)

    # Team Members Grid
    team_members = [
        {"name": "Humam", "role": "Backend Developer", "image": "https://via.placeholder.com/150.png?text=Humam"},
        {"name": "Muhammad Ibrahim Qasmi", "role": "Data Scientist", "image": "https://media.licdn.com/dms/image/v2/D4D03AQFCNX1cJg9J8w/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1732156800150?e=1743638400&v=beta&t=5nk_TRhQGlSX-I0tp0cf9ZHwJzFOLrLWWkxTdTrn6EU"},
        {"name": "Ahmad Fakhar", "role": "AI Engineer", "image": "https://media.licdn.com/dms/image/v2/D4D03AQFrxTgmUio4Mw/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1732197610882?e=1743638400&v=beta&t=we1bOWBoC3ZrXcus979HRY1yT9tRUsKa3dc7-JWZSXI"},
        {"name": "Muhammad Zia", "role": "UI/UX Designer", "image": "https://via.placeholder.com/150.png?text=Zia"},
        {"name": "Tayyab Sajjad", "role": "Data Scientist", "image": "https://media.licdn.com/dms/image/v2/D4E03AQELdwDpn2a9Bg/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1732042661073?e=1743638400&v=beta&t=6vX_f7IeZETm70ZZ8x-h6_vH6uDJ9f-2S6SGPVcHIOU"},
        {"name": "Frank", "role": "Project Manager", "image": "https://via.placeholder.com/150.png?text=Frank"}
    ]

    cols = st.columns(3)
    for idx, member in enumerate(team_members):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="team-card">
                <img src="{member['image']}" style="width:150px; border-radius:50%; margin-bottom:10px;">
                <h4 style="color:#2c3e50;">{member['name']}</h4>
                <p style="color:#3494e6;">{member['role']}</p>
            </div>
            """, unsafe_allow_html=True)

# Translator Page (Keep existing implementation, just add set_custom_styling())
def translator_page():
    set_custom_styling()
    # Rest of your existing translator_page implementation...

# Sidebar Navigation
def main():
    set_custom_styling()
    st.sidebar.title("Network Log Translator")
    st.sidebar.markdown("### Navigate with Ease")
    
    page = st.sidebar.radio("Choose a Section", [
        "🏠 Landing Page", 
        "🌐 Translator", 
        "👥 About Us"
    ])

    if page == "🏠 Landing Page":
        landing_page()
    elif page == "🌐 Translator":
        translator_page()
    elif page == "👥 About Us":
        about_us_page()

# Main Execution
if __name__ == "__main__":
    main()
