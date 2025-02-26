import streamlit as st # type: ignore
from google import genai
import pyttsx3 



# creating a genai client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


st.title("⚖ Advanced Unit Converter 🧠")

st.write("This app converts between different units of measurement.")

select_unit, convert_unit = st.columns(2)

# Define unit hierarchies (from largest to smallest)
unit_hierarchies = {
    "Length": ["Kilometer", "Meter", "Centimeter", "Millimeter"],
    "Weight": ["Kilogram", "Gram", "Milligram"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Volume": ["Kiloliter", "Liter", "Milliliter"]
}

# fisrt column

with select_unit:
    st.write("## Select the unit you want to convert from")
    unit_from = st.selectbox("Select the unit", ["Length", "Weight", "Temperature", "Volume"], key="unit_from")

# second column
with convert_unit:
    st.write("## Select the unit you want to convert to")
    unit_to = st.selectbox("Select the unit", ["Length", "Weight", "Temperature", "Volume"], key="unit_to")

# add a comparison of both the selected parent units must be same, different units can't be converted
if unit_from != unit_to:
    st.write("## Please select the same unit")
else:
    st.subheader("Select the sub units")
    
    # Get the available sub units for the selected unit type
    available_sub_units = unit_hierarchies[unit_from]
    
    sub_unit_from = st.selectbox("Select the sub unit", available_sub_units, key="sub_unit_from")
    
    # Get index of selected sub_unit_from in the hierarchy
    from_index = available_sub_units.index(sub_unit_from)
    # Filter to only show smaller units (units that come after the selected unit in the hierarchy)
    smaller_units = available_sub_units[from_index + 1:]
    
    if smaller_units:
        sub_unit_to = st.selectbox("Select the sub unit", smaller_units, key="sub_unit_to")
    else:
        st.write("No smaller units available for conversion")


   
    # get values for both the sub units

    
    st.subheader(f"Enter the value in {sub_unit_from}")
    sub_unit_from_value = st.number_input("Enter the value", key="sub_unit_from_value")

response = client.models.generate_content(
model="gemini-2.0-flash",
contents=f"Convert {sub_unit_from_value} {sub_unit_from} to {sub_unit_to},for the conversion part just give answer like this: this value in this unit is equal to this value in this unit, and end the response with a little dark humor or funny sentence at last, but keep it short (the funny or dark humor should be at the end of the response and be of around maximum 10 words)",
)



engine = pyttsx3.init()
engine.say(response.text)
engine.runAndWait()







