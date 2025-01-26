import streamlit as st
from groq import Groq
import speech_recognition as sr

# Configuration and API Setup
st.set_page_config(page_title="Network Log Translator", page_icon="🌐")

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
    # South African Languages
    'Afrikaans': 'af-ZA',
    'Zulu': 'zu-ZA',
    'Xhosa': 'xh-ZA',
    'Sotho': 'st-ZA',
    'Tswana': 'tn-ZA'
}

def initialize_groq_client():
    """Initialize Groq API client."""
    try:
        return Groq(api_key=st.secrets["GROQ_API_KEY"])
    except KeyError:
        st.error("Groq API key not found. Please set it in Streamlit secrets.")
        return None

def generate_explanation(client, log_text, language='en'):
    """Generate explanation using Groq API, optionally in specified language."""
    try:
        # Language-specific system prompts
        language_prompts = {
            'en': "You are a network troubleshooting assistant in English.",
            'es': "Eres un asistente de solución de problemas de red en español.",
            'fr': "Vous êtes un assistant de dépannage réseau en français.",
            'ur': "آپ اردو میں نیٹ ورک ٹروبل شوٹنگ اسسٹنٹ ہیں۔",
            'ar': "أنت مساعد استكشاف أخطاء الشبكة باللغة العربية.",
            # South African Languages
            'af': "Jy is 'n netwerk-probleemoplossingsassistent in Afrikaans.",
            'zu': "Ungusizo lokuxazulula amaproblem emseth-network ngesiZulu.",
            'xh': "Ungomnxeba wokusungula amaproblem emanyango ekuqhubekeni ngesiXhosa.",
            'st': "O moagi wa bothata ba network ka Sesotho.",
            'tn': "O thutapulamolemo ya network ka Setswana."
        }

        # Select the appropriate system prompt, default to English
        system_prompt = language_prompts.get(language, language_prompts['en'])

        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"{system_prompt} Provide clear, detailed explanations of network errors with comprehensive troubleshooting steps."},
                {"role": "user", "content": f"Provide a comprehensive explanation and detailed troubleshooting steps for this network error: {log_text}"}
            ],
            max_tokens=1500  # Increased max tokens
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error processing log: {e}")
        return "Unable to process the log. Please check the input."

def speech_to_text(language_code):
    """Convert speech to text for a specific language."""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        st.info(f"Listening... Please speak in {language_code}")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language=language_code)
            return text
        except sr.UnknownValueError:
            st.warning("Could not understand audio. Please try again.")
            return ""
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
            return ""
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return ""

def main():
    st.title("🌐 Network Log Translator")
    st.subheader("Simplify Complex Network Errors")

    # Groq Client Initialization
    groq_client = initialize_groq_client()
    if not groq_client:
        return

    # Common Error Buttons in Grid Layout
    st.write("**Quick Select Common Errors:**")
    
    # Create a 2x3 grid of buttons
    grid_rows = [
        st.columns(3),
        st.columns(3)
    ]
    
    # Flatten the list of common errors
    error_items = list(COMMON_ERRORS.items())
    
    # Populate buttons in grid
    for row_idx, row in enumerate(grid_rows):
        for col_idx, col in enumerate(row):
            # Calculate the index in the flattened error list
            list_idx = row_idx * 3 + col_idx
            
            # Check if we have an error for this position
            if list_idx < len(error_items):
                error, desc = error_items[list_idx]
                if col.button(error, key=f"error_{list_idx}", help=desc, use_container_width=True, type="secondary"):
                    st.session_state.input_text = desc

    # Language Selection (Including South African Languages)
    languages = {
        'English': 'en', 
        'Urdu': 'ur', 
        'Spanish': 'es', 
        'French': 'fr', 
        'Arabic': 'ar',
        # South African Languages
        'Afrikaans': 'af',
        'Zulu': 'zu',
        'Xhosa': 'xh',
        'Sotho': 'st',
        'Tswana': 'tn'
    }
    selected_lang = st.selectbox("Select Output Language", list(languages.keys()))

    # Input Method Selection
    input_method = st.radio("Choose Input Method", ["Text", "Voice"])

    # Input Area or Voice Input
    if input_method == "Text":
        st.session_state.input_text = st.text_area(
            "Enter network log or error details", 
            value=st.session_state.get('input_text', ''),
            placeholder='Enter network log or error details here.'
        )
    else:
        # Voice Input
        voice_lang = st.selectbox("Select Voice Input Language", list(LANGUAGE_CODES.keys()))
        
        if st.button("Start Voice Input"):
            # Perform speech-to-text conversion
            voice_input = speech_to_text(LANGUAGE_CODES[voice_lang])
            if voice_input:
                st.session_state.input_text = voice_input
                st.success(f"Recognized Text: {voice_input}")

    # Action Buttons
    col1, col2 = st.columns(2)
    translate_clicked = col1.button("Translate")
    clear_clicked = col2.button("Clear")

    # Clear functionality
    if clear_clicked:
        st.session_state.input_text = ''

    # Translation and Explanation Process
    if translate_clicked:
        if not st.session_state.input_text.strip():
            st.warning("Please enter a network log or error message.")
            return

        with st.spinner('Processing network log...'):
            # Generate Explanation in Selected Language
            lang_code = languages[selected_lang]
            explanation = generate_explanation(groq_client, st.session_state.input_text, lang_code)
            
            # Display Results with Expander to show full content
            with st.expander(f"Explanation ({selected_lang})", expanded=True):
                st.write(explanation)

if __name__ == "__main__":
    main()
