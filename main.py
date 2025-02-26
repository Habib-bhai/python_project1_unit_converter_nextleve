import streamlit as st
from google import genai
from gtts import gTTS  # Import gTTS
import os

# Custom CSS with dark theme and animations (keeping all original styles)
st.markdown("""
<style>
    /* Main container and global styles */
    .main {
        background-color: #0D0D0D;
        color: #F5F5F5;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Animated gradient background */
    .stApp {
        background: linear-gradient(
            45deg,
            #0D0D0D,
            #1A1A1A,
            #262626,
            #1A1A1A,
            #0D0D0D
        );
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Title styling with animated gradient */
    .title {
        text-align: center;
        font-size: 3rem !important;
        font-weight: bold;
        background: linear-gradient(
            45deg,
            #FF4D00,
            #FF6B00,
            #FF8C00,
            #FF6B00,
            #FF4D00
        );
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientText 5s ease infinite;
        margin-bottom: 2rem;
        text-shadow: 0 0 20px rgba(255, 77, 0, 0.3);
    }
    
    @keyframes gradientText {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating animation for cards */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* Glow effect */
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(255, 77, 0, 0.2); }
        50% { box-shadow: 0 0 20px rgba(255, 77, 0, 0.4); }
        100% { box-shadow: 0 0 5px rgba(255, 77, 0, 0.2); }
    }
    
    /* Card styling */
    .column-container {
        background: linear-gradient(145deg, #1A1A1A, #262626);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 77, 0, 0.1);
        animation: float 6s ease-in-out infinite;
        transition: all 0.3s ease;
    }
    
    .column-container:hover {
        transform: translateY(-5px);
        animation: glow 1.5s ease-in-out infinite;
        border: 1px solid rgba(255, 77, 0, 0.3);
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background-color: #262626 !important;
        border: 1px solid rgba(255, 77, 0, 0.2) !important;
        color: #F5F5F5 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #FF4D00 !important;
        box-shadow: 0 0 15px rgba(255, 77, 0, 0.2);
    }
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        background-color: #262626 !important;
        border: 1px solid rgba(255, 77, 0, 0.2) !important;
        color: #F5F5F5 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #FF4D00 !important;
        box-shadow: 0 0 15px rgba(255, 77, 0, 0.2);
    }
    
    /* Subheader styling */
    .subheader {
        color: #F5F5F5;
        font-size: 1.5rem;
        margin: 1.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(255, 77, 0, 0.3);
        text-shadow: 0 0 10px rgba(255, 77, 0, 0.2);
    }
    
    /* Error message styling */
    .error-message {
        background: linear-gradient(145deg, #8B0000, #FF4D00);
        color: #F5F5F5;
        padding: 1rem;
        border-radius: 10px;
        animation: pulse 2s infinite;
        text-align: center;
        margin: 1rem 0;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    /* Audio player styling */
    .stAudio > audio {
        width: 100%;
        border-radius: 10px;
        background-color: #262626;
        border: 1px solid rgba(255, 77, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .stAudio > audio:hover {
        border-color: #FF4D00;
        box-shadow: 0 0 15px rgba(255, 77, 0, 0.2);
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #FF4D00 !important;
        animation: spinner 0.8s linear infinite !important;
    }
    
    @keyframes spinner {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Result text animation */
    .result-text {
        opacity: 0;
        transform: translateY(20px);
        animation: fadeInUp 0.5s ease forwards;
    }
    
    @keyframes fadeInUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1A1A1A;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #FF4D00;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #FF6B00;
    }
    
    /* Form button styling */
    .stButton > button {
        background: linear-gradient(145deg, #FF4D00, #FF8C00) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.3s ease !important;
        font-weight: bold !important;
        box-shadow: 0 4px 10px rgba(255, 77, 0, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(255, 77, 0, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(1px) !important;
        box-shadow: 0 2px 5px rgba(255, 77, 0, 0.3) !important;
    }
    
    /* Form styling */
    .stForm {
        background: transparent !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Creating a genai client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Custom title with animated gradient
st.markdown('<h1 class="title">⚖ Advanced Unit Converter 🧠</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #F5F5F5; opacity: 0.8;">Transform your units with AI-powered precision</p>', unsafe_allow_html=True)

# Create columns
select_unit, convert_unit = st.columns(2)

# Define unit hierarchies
unit_hierarchies = {
    "Length": ["Kilometer", "Meter", "Centimeter", "Millimeter"],
    "Weight": ["Kilogram", "Gram", "Milligram"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Volume": ["Kiloliter", "Liter", "Milliliter"]
}

# First column
with select_unit:
    st.markdown('<div class="column-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #F5F5F5; font-size: 1.2rem;">From Unit</h2>', unsafe_allow_html=True)
    unit_from = st.selectbox("Select the unit type", ["Length", "Weight", "Temperature", "Volume"], key="unit_from")
    st.markdown('</div>', unsafe_allow_html=True)

# Second column
with convert_unit:
    st.markdown('<div class="column-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #F5F5F5; font-size: 1.2rem;">To Unit</h2>', unsafe_allow_html=True)
    unit_to = st.selectbox("Select the unit type", ["Length", "Weight", "Temperature", "Volume"], key="unit_to")
    st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state variables
if "previous_value" not in st.session_state:
    st.session_state["previous_value"] = 0

if "conversion_in_progress" not in st.session_state:
    st.session_state["conversion_in_progress"] = False

if "conversion_result" not in st.session_state:
    st.session_state["conversion_result"] = None

if "audio_path" not in st.session_state:
    st.session_state["audio_path"] = None

# Check if different units are selected
if unit_from != unit_to:
    st.markdown('<div class="error-message">Please select the same unit type for conversion</div>', unsafe_allow_html=True)
else:
    st.markdown('<h3 class="subheader">Select Sub Units</h3>', unsafe_allow_html=True)
    
    available_sub_units = unit_hierarchies[unit_from]
    
    # Create columns for sub units
    sub_from_col, sub_to_col = st.columns(2)
    
    with sub_from_col:
        st.markdown('<div class="column-container">', unsafe_allow_html=True)
        sub_unit_from = st.selectbox("From", available_sub_units, key="sub_unit_from")
        st.markdown('</div>', unsafe_allow_html=True)
    
    from_index = available_sub_units.index(sub_unit_from)
    smaller_units = available_sub_units[from_index + 1:]
    
    if smaller_units:
        with sub_to_col:
            st.markdown('<div class="column-container">', unsafe_allow_html=True)
            sub_unit_to = st.selectbox("To", smaller_units, key="sub_unit_to")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'<h3 class="subheader">Enter value in {sub_unit_from}</h3>', unsafe_allow_html=True)
        
        st.markdown('<div class="column-container">', unsafe_allow_html=True)
        
        # Use a form to control when the value is submitted
        with st.form(key="conversion_form"):
            sub_unit_from_value = st.number_input("Value", min_value=0.0, step=0.1, key="sub_unit_from_value")
            submit_button = st.form_submit_button(label="Convert")
        
        # Only process when form is submitted and not already in progress
        if submit_button and not st.session_state["conversion_in_progress"] and sub_unit_from_value > 0:
            if st.session_state["previous_value"] != sub_unit_from_value:
                st.session_state["previous_value"] = sub_unit_from_value
                st.session_state["conversion_in_progress"] = True
                
                try:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=f"Convert {sub_unit_from_value} {sub_unit_from} to {sub_unit_to}, for the conversion part just give answer like this: this value in this unit is equal to this value in this unit, and end the response with a little dark humor or funny sentence at last, but keep it short (the funny or dark humor should be at the end of the response and be of around maximum 10 words)",
                    )
                    st.session_state["conversion_result"] = response.text
                    
                    if not os.path.exists('./temp'):
                        os.makedirs('./temp')
                    
                    output_path = './temp/output.mp3'
                    
                    # Generate audio using gTTS
                    tts = gTTS(text=st.session_state["conversion_result"], lang='en')
                    tts.save(output_path)
                    
                    st.session_state["audio_path"] = output_path
                    
                finally:
                    st.session_state["conversion_in_progress"] = False
                    
        
        # Display results if available
        
        if st.session_state["audio_path"] and os.path.exists(st.session_state["audio_path"]):
            with open(st.session_state["audio_path"], 'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-message">No smaller units available for conversion</div>', unsafe_allow_html=True)