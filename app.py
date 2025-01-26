import os
import streamlit as st
import speech_recognition as sr
from dotenv import load_dotenv
import pyperclip
import sounddevice as sd
import soundfile as sf
import numpy as np

# Fix Groq import
try:
    from groq import Groq
except ImportError:
    from groq.client import Groq

# Load environment variables
load_dotenv()

# Configuration
st.set_page_config(page_title="Network Log Translator", page_icon="🌐", layout="wide")

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
    'English': 'en-US',
    'Urdu': 'ur-PK',
    'Spanish': 'es-ES',
    'French': 'fr-FR',
    'Arabic': 'ar-SA',
    'Afrikaans': 'af-ZA',
    'Zulu': 'zu-ZA',
    'Xhosa': 'xh-ZA',
    'Sotho': 'st-ZA',
    'Tswana': 'tn-ZA'
}

# Initialize Groq client
def initialize_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY not found in .env file")
        return None
    return Groq(api_key=api_key)

# Error classification system
def classify_error(text):
    error_types = {
        "DNS": ["dns", "domain", "server"],
        "SSL": ["ssl", "certificate", "handshake"],
        "Connection": ["connection", "timeout", "refused", "route"]
    }
    text_lower = text.lower()
    for etype, keywords in error_types.items():
        if any(kw in text_lower for kw in keywords):
            return etype
    return "Network"

# Severity detection
def get_severity(text):
    text_lower = text.lower()
    if "critical" in text_lower: return "Critical"
    if "warning" in text_lower: return "Warning"
    if "severe" in text_lower: return "Critical"
    return "Info"

# Generate explanation using Groq API
def generate_explanation(client, log_text, language='en'):
    try:
        system_prompts = {
            'en': "You are a network troubleshooting assistant in English.",
            'es': "Eres un asistente de solución de problemas de red en español.",
            'fr': "Vous êtes un assistant de dépannage réseau en français.",
            'ur': "آپ اردو میں نیٹ ورک ٹروبل شوٹنگ اسسٹنٹ ہیں۔",
            'ar': "أنت مساعد استكشاف أخطاء الشبكة باللغة العربية.",
            'af': "Jy is 'n netwerk-probleemoplossingsassistent in Afrikaans.",
            'zu': "Ungusizo lokuxazulula amaproblem emseth-network ngesiZulu.",
            'xh': "Ungomnxeba wokusungula amaproblem emanyango ekuqhubekeni ngesiXhosa.",
            'st': "O moagi wa bothata ba network ka Sesotho.",
            'tn': "O thutapulamolemo ya network ka Setswana."
        }
        
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": f"{system_prompts.get(language, 'en')} Provide detailed analysis and step-by-step solutions."},
                {"role": "user", "content": f"Analyze this network error: {log_text}"}
            ],
            temperature=0.3,
            max_tokens=1200
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

# Speech-to-text conversion using sounddevice
def speech_to_text(language_code):
    r = sr.Recognizer()
    duration = 5  # seconds
    st.info("Listening... (5 second timeout)")
    
    try:
        # Record audio using sounddevice
        fs = 16000  # Sample rate
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()  # Wait until recording is finished
        
        # Save the recording to a temporary file
        temp_file = "temp.wav"
        sf.write(temp_file, recording, fs)
        
        # Recognize the audio using speech_recognition
        with sr.AudioFile(temp_file) as source:
            audio = r.record(source)
            return r.recognize_google(audio, language=language_code)
    except Exception as e:
        st.error(f"Recognition error: {str(e)}")
        return ""

# Check if running in Streamlit Cloud
def is_streamlit_cloud():
    return "STREAMLIT_CLOUD" in os.environ

# Landing Page
def landing_page():
    st.title("🌐 Welcome to Network Log Translator")
    st.markdown("""
    **Simplify Complex Network Errors with AI-Powered Troubleshooting**

    Our tool helps you:
    - 🛠️ Diagnose network issues in seconds
    - 🌍 Support for 10+ languages
    - 🎤 Voice and text input options
    - 📋 Quick fixes for common errors

    Get started by navigating to the **Translator** page from the sidebar.
    """)
    st.image("https://ideogram.ai/assets/image/lossless/response/fjemlPTxRSagPZPIt9w44Q", use_column_width=True)

# About Us Page
def about_us_page():
    st.title("👥 About Us")
    st.markdown("""
    We are a team of 6 passionate developers working to make network troubleshooting accessible to everyone.
    """)

    # Team Members
    st.subheader("Meet the Team")
    cols = st.columns(3)
    team_members = [
        {"name": "Humam", "role": "Backend Developer", "image": "https://via.placeholder.com/150.png?text=Alice"},
        {"name": "Muhammad Ibrahim Qasmi", "role": "Data Scientist", "image": "https://media.licdn.com/dms/image/v2/D4D03AQFCNX1cJg9J8w/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1732156800150?e=1743638400&v=beta&t=5nk_TRhQGlSX-I0tp0cf9ZHwJzFOLrLWWkxTdTrn6EU"},
        {"name": "Ahmad Fakhar", "role": "AI Engineer", "image": "https://media.licdn.com/dms/image/v2/D4D03AQFrxTgmUio4Mw/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1732197610882?e=1743638400&v=beta&t=we1bOWBoC3ZrXcus979HRY1yT9tRUsKa3dc7-JWZSXI"},
        {"name": "Muhammad Zia", "role": "UI/UX Designer", "image": "https://via.placeholder.com/150.png?text=Diana"},
        {"name": "Tayyab Sajjad", "role": "Data Scientist", "image": "https://media.licdn.com/dms/image/v2/D4E03AQELdwDpn2a9Bg/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1732042661073?e=1743638400&v=beta&t=6vX_f7IeZETm70ZZ8x-h6_vH6uDJ9f-2S6SGPVcHIOU"},
        {"name": "Frank", "role": "Project Manager", "image": "https://via.placeholder.com/150.png?text=Frank"}
    ]

    for idx, member in enumerate(team_members):
        with cols[idx % 3]:
            st.image(member["image"], width=150)
            st.markdown(f"**{member['name']}**")
            st.caption(member["role"])

# Main Translator Page
def translator_page():
    st.title("🌐 Smart Network Troubleshooter")
    
    # Initialize session state
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    # Initialize Groq client
    groq_client = initialize_groq_client()
    if not groq_client:
        return

    # Common Errors Grid
    st.subheader("Common Network Issues")
    cols = st.columns(3)
    for idx, (error, desc) in enumerate(COMMON_ERRORS.items()):
        with cols[idx % 3]:
            if st.button(error, help=desc, key=f"err_{idx}"):
                st.session_state.input_text = desc

    # Language Selection
    lang_col1, lang_col2 = st.columns([2, 1])
    with lang_col1:
        selected_lang = st.selectbox("Output Language", list(LANGUAGE_CODES.keys()))
    with lang_col2:
        input_method = st.radio("Input Method", ["Text", "Voice"])

    # Input Section
    input_text = ""
    if input_method == "Text":
        input_text = st.text_area("Network Error Details", 
                                value=st.session_state.get('input_text', ''),
                                height=100)
    else:
        if is_streamlit_cloud():
            st.warning("Voice input is not supported in Streamlit Cloud. Please use text input.")
        else:
            voice_lang = st.selectbox("Voice Input Language", list(LANGUAGE_CODES.keys()))
            if st.button("🎤 Start Recording"):
                input_text = speech_to_text(LANGUAGE_CODES[voice_lang])
                if input_text:
                    st.session_state.input_text = input_text

    # Main Processing
    if st.button("Analyze Error", type="primary"):
        if not input_text.strip():
            st.warning("Please enter error details")
            return

        with st.status("🔍 Analyzing Error...", expanded=True) as status:
            # Generate Explanation
            lang_code = next(
                (v[:2] for k, v in LANGUAGE_CODES.items() if k.lower().startswith(selected_lang[:2].lower())),
                'en'  # Default to English
            )
            explanation = generate_explanation(groq_client, input_text, lang_code)
            
            if not explanation:
                st.error("Failed to generate explanation")
                return

            # Error Classification
            error_category = classify_error(explanation)
            severity_level = get_severity(explanation)
            
            # Update History
            st.session_state.history.append({
                'error': input_text,
                'explanation': explanation,
                'category': error_category,
                'severity': severity_level
            })
            
            status.update(label="Analysis Complete", state="complete")

        # Display Results
        st.subheader(f"{severity_level} Issue", divider="rainbow")
        st.markdown(f"**Category:** :label: `{error_category}`")
        
        with st.expander("Detailed Analysis", expanded=True):
            st.markdown(explanation)

        # Quick Fixes
        QUICK_FIXES = {
            "DNS": "ipconfig /flushdns",
            "SSL": "sudo update-ca-certificates",
            "Connection": "ping 8.8.8.8",
            "Network": "netsh winsock reset"
        }
        
        if error_category in QUICK_FIXES:
            fix = QUICK_FIXES[error_category]
            st.code(fix, language="bash")
            if st.button("📋 Copy Command", key="copy_cmd"):
                pyperclip.copy(fix)
                st.toast("Command copied to clipboard!")

        # History Section
        st.subheader("Recent Analyses", divider="gray")
        for entry in reversed(st.session_state.history[-3:]):
            with st.expander(f"{entry['severity']} - {entry['error'][:30]}..."):
                st.caption(f"**Category:** {entry['category']}")
                st.write(entry['explanation'])
                
    # Feedback System
    st.divider()
    feedback = st.radio("Was this helpful?", [":thumbsup:", ":thumbsdown:"], 
                       index=None, horizontal=True)
    if feedback:
        st.success("Thank you for your feedback!")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Landing Page", "🌐 Translator", "👥 About Us"])

# Page Routing
if page == "🏠 Landing Page":
    landing_page()
elif page == "🌐 Translator":
    translator_page()
elif page == "👥 About Us":
    about_us_page()
