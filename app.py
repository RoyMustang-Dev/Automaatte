import streamlit as st
import requests

# Webhook URL from your Make scenario
WEBHOOK_URL = "https://hook.eu2.make.com/6it1v4q73it8nwoncysmiw1qpf48pe4h"

# Set up the page configuration for wide layout
st.set_page_config(page_title="Automaatte", page_icon="🌐", layout="wide")

# CSS styles file
with open("main.css") as f:
    st.write(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Custom CSS to override Streamlit's default padding and margins for full-width layout
st.markdown(
    """
    <style>
        /* Ensure that the app content takes up the full screen width */
        .block-container {
            padding-left: 0;
            padding-right: 0;
            padding-top: 0;
            padding-bottom: 0;
            margin-top:-50px;
        }

        /* Optional: to remove the default margin at the top */
        .main {
            padding-top: 0;
        }

        /* Adjust iframe and other components to take full width */
        iframe {
            width: 100%;
            height: 100%;
        }

        /* Ensure the content inside the divs is stretched to fit the width */
        .spline-container {
            width: 100%;
            height: 100vh;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to fetch country names dynamically from the REST Countries API
def fetch_countries():
    try:
        response = requests.get("https://restcountries.com/v3.1/all")
        response.raise_for_status()  # Raise an exception for HTTP errors
        countries_data = response.json()
        return sorted([country['name']['common'] for country in countries_data])
    except Exception as e:
        st.error(f"Failed to fetch countries: {e}")
        return []

# Function to fetch states for a given country
def fetch_states(country_name):
    try:
        response = requests.post(
            "https://countriesnow.space/api/v0.1/countries/states",
            json={"country": country_name}
        )
        response.raise_for_status()
        states_data = response.json()
        if "data" in states_data and "states" in states_data["data"]:
            return [state["name"] for state in states_data["data"]["states"]]
        else:
            st.error(f"Invalid response format for {country_name}")
            return []
    except Exception as e:
        st.error(f"Failed to fetch states for {country_name}: {e}")
        return []

# Function to fetch cities for a given state
def fetch_cities(country_name, state_name):
    try:
        response = requests.post(
            "https://countriesnow.space/api/v0.1/countries/state/cities",
            json={"country": country_name, "state": state_name}  # Include country in payload
        )
        response.raise_for_status()
        cities_data = response.json()
        if "data" in cities_data:
            return cities_data["data"]
        else:
            st.error(f"Invalid response format for {state_name}")
            return []
    except Exception as e:
        st.error(f"Failed to fetch cities for {state_name}: {e}")
        return []

# Fetch countries
COUNTRIES = fetch_countries()

# Initialize session state for showing content
if 'show_content' not in st.session_state:
    st.session_state.show_content = False

# Title and description with Spline background
st.markdown("""
<style>
    .spline-container {
        position: relative;
        height: 100vh;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Embed Spline using iframe
st.markdown("""
<div class="spline-container">
    <iframe src='https://my.spline.design/cybernetwork-ace4bd63302a1ed48cb50826fa110d63/' frameborder='0' width='100%' height='100%'></iframe>
    <h1 style="position:absolute; top:100px; left:225px; transform:translate(-50%, -50%); color:white; text-align: center;font-size:4rem;">Automaatte</h1>
    <h5 style="position:absolute; top:150px; left:240px; transform:translate(-50%, -50%); color:white; text-align: center;font-size:2rem;">Transforming Tomorrow, Today</h5>
    <p style="position:absolute; top:320px; left:300px; transform:translate(-50%, -50%); color:white; text-align: left; font-size:1.1rem;">
            Welcome to Automaatte, where AI meets ambition to turn today's<br>ideas into tomorrow's achievements. We offer a suite 
            of intelligent, automated<br> Planning and Research solutions designed to streamline and elevate your<br> personal and 
            business endeavors across various industries. <br><br>With Automaatte, time-consuming tasks become a breeze, letting you 
            focus<br> on what truly matters while we handle the details.</p>
</div>
<div id="content" style="display:none;">
""",unsafe_allow_html=True)

# Show content based on button click
if st.button("Explore", key="explore_button", icon=":material/expand_circle_down:"):
    st.session_state.show_content = True

if st.session_state.show_content:
    st.markdown("</div> <!-- Close content div -->", unsafe_allow_html=True)
    
    # Core Services (initially hidden)
    st.markdown("### Core Services")
    st.markdown("""
    - **AI Researchers**:
        - Personalized vacation itineraries for individuals and corporate retreats.
        - Let us handle the details so you can focus on what truly matters.
    """)

    # Input Form
    st.markdown("---")
    st.markdown("### Vacation Researcher Form")

    # Country selection with placeholder
    country = st.selectbox("Country", options=["Select a Country"] + COUNTRIES, index=0)

    # Dynamically fetch and display states based on selected country
    if country != "Select a Country":
        states = fetch_states(country)
        state = st.selectbox("State", options=["Select a State"] + states)
    else:
        state = st.selectbox("State", options=["Select a State"])

    # Dynamically fetch and display cities based on selected state
    if state != "Select a State":
        cities = fetch_cities(country, state)
        city = st.selectbox("City", options=["Select a City"] + cities)
    else:
        city = st.selectbox("City", options=["Select a City"])

    # Specific Place input field
    specific_place = st.text_input("Specific Place", placeholder="Enter a specific place or landmark")

    # Button to trigger the scenario
    if st.button("Send Data to Make"):
        if country == "Select a Country":
            st.error("Please select a valid country!")
        elif state == "Select a State":
            st.error("Please select a valid state!")
        elif city == "Select a City":
            st.error("Please select a valid city!")
        else:
            # Data to send to the webhook
            payload = {
                "country": country,
                "state": state,
                "city": city,
                "specific_place": specific_place
            }
            try:
                # Sending POST request to the webhook
                response = requests.post(WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    try:
                        st.success("Data successfully compiled!")
                        st.markdown("#### Generated Itinerary:")
                        response_content = response.text
                        st.write("Response Content:\n", response_content)
                    except Exception as parse_error:
                        st.error(f"Failed to parse response: {parse_error}")
                else:
                    st.error(f"Failed to send data. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.markdown("*Powered by Automaatte*")
