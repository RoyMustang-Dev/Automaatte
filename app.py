import streamlit as st
import requests
import re
from streamlit_option_menu import option_menu

# Webhook URL from your Make scenario
WEBHOOK_GEMINI = "https://hook.eu2.make.com/y3gnzmgcnn9t38ze3ck5j6pxhayx6qwe"
WEBHOOK_GEMINI2 = "https://hook.eu2.make.com/e79m455b41ki8sgofv2rvuwdqgdpmo00"

# Set up the page configuration for wide layout
st.set_page_config(page_title="Automaatte: Transform Tomorrow, Today!!", page_icon="favicon.ico", layout="wide")

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
            padding-top: 0px;
            padding-bottom: 0;
            margin-top: 0px;
        }

        /* Optional: to remove the default margin at the top */
        .main {
            padding-top: 0;
            
        }

        /* Adjust iframe and other components to take full width */
        iframe {
            width: 100%;
            
        }

        /* Ensure the content inside the divs is stretched to fit the width */
        .spline-container {
            width: 100%;
            height: 100vh;
            padding-top: -10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to fetch country names dynamically from the REST Countries API
@st.cache_data
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
@st.cache_data
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
@st.cache_data
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

# Function to validate email
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def get_previous_level(level):
    """Returns the label for the previous level based on the selected level."""
    levels_hierarchy = {
        "9th": None,
        "10th": "Marks Obtained in 9th",
        "12th": "Marks Obtained in 10th",
        "Graduation": "Marks Obtained in 12th",
        "Post Graduation": "Marks Obtained in Graduation",
        "PhD": "Marks Obtained in Post Graduation"
    }
    return levels_hierarchy.get(level, None)

# Fetch countries
COUNTRIES = fetch_countries()

selected = option_menu(None, ["Home", "Services", "AI Researchers",  "AI Planners", "AI Free Services", "About Us", "Contact Us"], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background": "rgb(15 16 17)"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"width": "100%", "font-size": "25px", "text-align": "left", "margin-top":"0px", "--hover-color": "rgb(21 41 60)"},
        "nav-link-selected": {"background-color": "rgb(21 41 60)"},
    }
)

if selected == "Home":
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

if selected == "Services":    
    # Core Services (initially hidden)
    st.markdown("# Core Services")
    st.markdown("""
        ## AI Researchers:
            - Personalized vacation itineraries for individuals and corporate retreats.
            - Let us handle the details so you can focus on what truly matters.
            
        ### Our research tools provide data-backed insights for smarter decisions:
                
            1. Vacation Researching: Essential insights for individual and corporate travel planning.
            2. Education Researching: Data-driven recommendations for student career choices.
            3. Insurance Researching: Comprehensive insights into medical and vehicle insurance options.
            4. Investment Researching: In-depth data for crypto and stock market investments.
            5. Video Shoot Researching: Tailored content strategies for film, advertising, and social media.

        ## AI Planners:
            - Automaatte’s AI-driven planners transform complex planning into a seamless experience:
            
        ### Our planning tools provide comprehensive guidance in every step of the process making it easy to understand and saving your precious time.
                
            1. Vacation Planning: Personalized itineraries for individual travelers and corporate retreats in the Tourism industry.
            2. Education Planning: Career pathway guidance tailored to students after 10th and 12th grades, empowering the next generation in EdTech.
            3. Insurance Planning: Clear, informed decision-making support for medical and vehicle insurance in the Banking sector.
            4. Money Investment Planning: Actionable insights into crypto and stock markets, unlocking smarter investment strategies in FinTech.
            5. Video Shoot Planning: Thoughtful, customized shoot plans for short films, ads, and YouTube content in AdTech and Social Media.
                
        ## Additional AI-Powered Services
            1. Summarization: Instant, clear overviews of complex topics.
            2. Document QnA: Detailed answers to questions based on document content.
            3. Real-Time Language Translation: Breaks language barriers, enhancing planning and research experiences with seamless text and speech translations.

        ### At Automaatte, we redefine productivity, bringing clarity to complexity. Step into a future where planning and research are automated, empowering you to achieve more, with precision and confidence.       
        """)

if selected == "AI Researchers":
    # Input Form
    st.markdown("---")
    st.markdown("### Vacation Researcher Form")
    st.write("Vacation Researching: Personalized itineraries for individual travelers and corporate retreats in the Tourism industry.")

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
    if st.button("Generate Vacation Research"):
        if country == "Select a Country":
            st.error("Please select a valid country!")
        elif state == "Select a State":
            st.error("Please select a valid state!")
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
                response = requests.post(WEBHOOK_GEMINI, json=payload)
                if response.status_code == 200:
                    try:
                        st.success("Research Done!!")
                        
                        response_content = response.text
                        st.markdown("""
                                    <style>
                                        .response-content {
                                            background-color: rgb(15 16 17);
                                            padding: 20px;
                                            border-radius: 8px;
                                            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                                        }
                                    </style>
                                    """, unsafe_allow_html=True)

                                    # Applying the CSS class to the response content
                        st.markdown(f"""
                                    <div class="response-content">
                                        <pre>{response_content}</pre>
                                    </div>
                                    """, unsafe_allow_html=True)

                    except Exception as parse_error:
                        st.error(f"Failed to parse response: {parse_error}")
                else:
                    st.error(f"Failed to send data. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    
    
    # Input Form
    st.markdown("---")
    st.markdown("### Education Researcher Form")
    st.write("Higher Education Researching:")

    LEVELS = ["Select a Level", "10th", "12th", "Graduation", "Post Graduation", "PhD"]
    LEARNING_MODE = ["Select a Mode", "Online", "Offline", "Hybrid"]
    # Country selection with placeholder
    # Level selection
    level = st.selectbox("Select the Education Level you want to Research about", options=LEVELS)

    if level == "Select a Level":
        st.write("Please select a valid level to proceed.")
    else:
        st.markdown("---")

        # Dynamic field: Marks Obtained
        previous_level_label = get_previous_level(level)
        marks_obtained = None
        if previous_level_label:
            marks_obtained = st.text_input(previous_level_label, placeholder="Enter marks here")
        else:
            st.info("No previous level, Proceed with the next fields.")

        country_main = "India"
        # Dynamically fetch and display states based on selected country
        if country_main == "India":
            indian_states = fetch_states(country_main)
            istate = st.selectbox("State in which you want to Pursue the Education", options=["Select a State"] + indian_states)
        else:
            istate = st.selectbox("State in which you want to Pursue the Education", options=["Select a State"])

        # Dynamically fetch and display cities based on selected state
        if istate != "Select a State":
            indian_cities = fetch_cities(country_main, istate)
            icity = st.selectbox("Prefered City in which you want to Pursue the Education", options=["Select a City"] + indian_cities)

        mode = st.selectbox("Mode of Education", options= LEARNING_MODE)
        if mode == "Select a Mode":
            st.write("Please select a valid mode to proceed.")

        # Dynamic field: Interests & Hobbies
        interests_hobbies = st.text_area("Your Interests & Hobbies", placeholder="Describe your interests and hobbies here")

        # Dynamic field: Future Goals & Aspirations
        future_goals = st.text_area("Your Future Goals & Aspirations", placeholder="Share your future aspirations here")

    # Button to trigger the scenario
    if st.button("Generate Education Research"):
        if previous_level_label and not marks_obtained:
            st.error(f"Please enter {previous_level_label}.")
        elif istate == "Select a State":
            st.error("Please select a valid state!")
        else:
            # Data to send to the webhook
            payload = {
                "level": level,
                "interests": interests_hobbies,
                "future_goals": future_goals,
                "marks_obtained_label": previous_level_label,
                "marks_obtained_value": marks_obtained,
                "country": country_main,
                "state": istate,
                "city": icity,
                "mode": mode
            }
            try:
                # Sending POST request to the webhook
                response = requests.post(WEBHOOK_GEMINI2, json=payload)
                if response.status_code == 200:
                    try:
                        st.success("Research Done!!")
                        st.write("Your research is being processed. Please wait for a while.")
                        response_content = response.text
                        st.markdown("""
                                    <style>
                                        .response-content {
                                            background-color: rgb(15 16 17);
                                            padding: 20px;
                                            border-radius: 8px;
                                            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                                        }
                                    </style>
                                    """, unsafe_allow_html=True)

                                    # Applying the CSS class to the response content
                        st.markdown(f"""
                                    <div class="response-content">
                                        <pre>{response_content}</pre>
                                    </div>
                                    """, unsafe_allow_html=True)

                    except Exception as parse_error:
                        st.error(f"Failed to parse response: {parse_error}")
                else:
                    st.error(f"Failed to send data. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    # Input Form
    st.markdown("---")
    st.markdown("### Insurance Researcher Form")
    # Input Form
    st.markdown("---")
    st.markdown("### Investment Researcher Form")
    # Input Form
    st.markdown("---")
    st.markdown("### Video Shoot Researcher Form")
# Footer
st.markdown("---")
st.markdown("*Powered by Automaatte*")
