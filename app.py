import os
from pathlib import Path
import streamlit as st
import pandas as pd
from joblib import load

# Set page configuration
st.set_page_config(
    page_title='Raphael Health',
    page_icon='🩺',
    layout='centered',
    initial_sidebar_state='auto'
)

model_path = Path('/home/gmartin/code/GeorgeDavisonMartin/raphhealth_frontend/raphhealth/GradientBost_model.joblib')

st.write(os.getcwd())
model = load(model_path)

# Function to check login credentials
def login_user(username, password):
    return username == "user" and password == "password"

# Function to display the login form
def login_form():
    st.title("Login to Raphael Health 🩺")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            if login_user(username, password):
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("Incorrect username or password. Please try again.")

# Define page functions
def landing_page():
    st.title("Welcome to Raphael Health 🩺")

    # Create three columns
    col1, col2, col3 = st.columns([1,2,1])  # The middle column has twice the width of the side columns

    with col2:
        st.image('RaphaelHealthLogo.png', width=300)
    st.write("""
        ## Empowering Your Health Decisions
        Raphael Health is dedicated to bringing you advanced predictive insights into healthcare.
        Explore our predictive models, dive into the data, or learn more about our mission on the About Us page.

        Use the sidebar to navigate through the application. Start by exploring our Predictions to understand
         potential health outcomes based on various factors or head over to our Data Analysis for in-depth
        insights. Our About Us page will tell you more about our mission, the technology behind Raphael Health,
        and the people making it all possible.
        """)
    st.markdown("""
        ### Quick Links:
    """)

    # Buttons for navigation
    if st.button('Show Predictions'):
        prediction()
    elif st.button('Show Data Analysis'):
        eda()
    elif st.button('Show About Us'):
        about_us()

def prediction():
    st.markdown("<h1 style='text-align: center; color: black;'>Input Customer Data:</h1>", unsafe_allow_html=True)
    #df = pd.read_csv('data/grouped_ver_1.csv')


    # Define the mapping of regions to their corresponding numerical codes
    region_codes = {
        'North Central': 0,
        'Northeast': 1,
        'South': 2,
        'West': 3
    }

    # List of regions to display in the multiselect
    regions = list(region_codes.keys())

    # Streamlit multiselect widget for selecting regions
    selected_regions = st.multiselect('Select Address Region', regions)

    # Check if any regions have been selected
    if selected_regions:
        # Retrieve the codes for the selected regions using a list comprehension
        selected_codes = [region_codes[region] for region in selected_regions]
        region_lst = [0,0,0,0]
        region_lst[int(selected_codes[0])] = 1


    # User inputs an age
    age_input = st.text_input('Select Age', placeholder='Enter Age In Years (0-65)')


    # Define the mapping of genders to their corresponding numerical codes
    gender_codes = {
        'Male': 1,
        'Female': 2
    }

    # Streamlit multiselect widget for selecting genders
    selected_genders = st.multiselect('Select Gender(s)', list(gender_codes.keys()))

    # Check if any regions have been selected
    if selected_genders:
        # Retrieve the codes for the selected genders using a list comprehension
        selected_codes = [gender_codes[gender] for gender in selected_genders]
        gender_1st = [0,0]
        gender_1st[int(selected_codes[0])] = 1

    # Define the mapping of readable relationship names to their corresponding numerical codes
    relationship_codes = {
        'Plan Holder': 1,
        'Spouse': 2,
        'Child/Other Dependent': 3,
        'Unknown': 4
    }

    # Streamlit multiselect widget for selecting relationships
    selected_relationship_names = st.multiselect('Select Relationship to Plan Holder', list(relationship_codes.keys()))


    # Check if any regions have been selected
    if selected_relationship_names:
        # Retrieve the codes for the selected regions using a list comprehension
        selected_codes = [relationship_codes[name] for name in selected_relationship_names]
        relationship_lst = [0,0,0,0]
        relationship_lst[int(selected_codes[0])] = 1


    # Define the mapping of previously admitted to their corresponding numerical codes
    hosp_codes = {
        'Yes': 1,
        'No': 0,
    }

    # List of regions to display in the multiselect
    hosped = list(hosp_codes.keys())

    # Streamlit multiselect widget for selecting previously admitted
    selected_hosped = st.multiselect('Has Patient Previously been Hospitalised?', hosped)

    # Check if any values have been selected
    if selected_hosped:
        # Retrieve the codes for the selected values using a list comprehension
        selected_hosped = [hosp_codes[hosp] for hosp in selected_hosped]
        hosped_1st = [0,0]
        hosped_1st[int(selected_hosped[0])] = 1

    # User inputs number of previous days in hospital
    days_input = st.text_input('Lifetime Days In Hospital', placeholder='Enter Lifetime Number of Days Spent In Hospital')


    # Mapping of dataframe columns to readable disease names
    disease_name_mapping = {
        'respiratory_d': 'Respiratory Disease',
        'hypertension': 'Hypertension',
        'diabetes_melitus': 'Diabetes Melitus',
        'dementia': 'Dementia',
        'kidney_disease': 'Kidney Disease',
        'liver_disease': 'Liver Disease',
        'diarrheal_disease': 'Diarrheal Disease',
        'myocardial_infarction': 'Myocardial Infarction',
        'cardiovascular_d': 'Cardiovascular Disease',
        'chf': 'Heart Failure',
        'pvd': 'Peripherial Vascular Disease',
        'cancer': 'Non-Metastatic Cancer',
        'metastasis': 'Metastatic Cancer',
        'connective_tissue_disease': 'Autoimmune Disease',
        'puc': 'Peptic Ulcer',
        'hemiplegia': 'Stroke',
        'lymphoma': 'Lymphoma',
        'aids': 'AIDS',
        'trauma': 'Previous Fracture'
    }

    # List of readable disease names for the multiselect widget
    readable_disease_names = list(disease_name_mapping.values())

    # Create a multiselect box for selecting diseases with readable names
    selected_readable_names = st.multiselect('Select Positive Diseases', readable_disease_names)
    selected_disease_list=[]
    # Map the readable names back to the dataframe's column names
    for key, value in disease_name_mapping.items():
        if value in selected_readable_names:
            selected_disease_list.append(1)
        else:
            selected_disease_list.append(0)

    if st.button('Submit'):
# DataFrame should match the exact format (order and number of columns) expected by model
        initial_list_wo_dis = pd.DataFrame({
            'age_years': [float(age_input)],
            'relationship_to_primary_beneficiary': [float(relationship_lst[0])],
            'clinic_visits': [float(days_input)],
            'clinic_inpatient': [float(hosped_1st[0])],
            'region_mod_northcentral': [float(region_lst[0])],
            'region_mod_northeast': [float(region_lst[1])],
            'region_mod_south': [float(region_lst[2])],
            'region_mod_west': [float(region_lst[3])],
            'gender_female': [float(gender_1st[0])],
            'gender_male': [float(gender_1st[1])],
            'both_clinic': [float(0)],
            'cci': [int(0)]
        })
        initial_list_wo_dis.extend(selected_disease_list)
        # Make prediction
        predicted_cost = model.predict(initial_list_wo_dis)

        # Display the prediction
        st.title(f"Expected Cost: ${round(predicted_cost[0], 2)} USD")

'''
get input variables
preprocess so input data matches data types/columns, etc
input variables into model.predict
'''

#     if st.button('Submit'):
# # DataFrame should match the exact format (order and number of columns) expected by model
#         df = pd.DataFrame({
#             'age_years': [float(age_years)],
#             'relationship_to_primary_beneficiary': [float(relationship_to_primary_beneficiary)],
#             'clinic_visits': [float(clinic_visits)],
#             'myocardial_infarction': [float(myocardial_infarction)],
#             'chf': [float(chf)],
#             'pvd': [float(pvd)],
#             'cardiovascular_d': [float(cardiovascular_d)],
#             'respiratory_d': [float(respiratory_d)],
#             'hypertension': [float(hypertension)],
#             'diabetes_melitus': [float(diabetes_melitus)],
#             'dementia': [float(dementia)],
#             'kidney_disease': [float(kidney_disease)],
#             'liver_disease': [float(liver_disease)],
#             'diarrheal_disease': [float(diarrheal_disease)],
#             'cancer': [float(cancer)],
#             'connective_tissue_disease': [float(connective_tissue_disease)],
#             'puc': [float(puc)],
#             'hemiplegia': [float(hemiplegia)],
#             'lymphoma': [float(lymphoma)],
#             'clinic_inpatient': [float(clinic_inpatient)],
#             'region_mod_northcentral': [float(region_mod_northcentral)],
#             'region_mod_northeast': [float(region_mod_northeast)],
#             'region_mod_south': [float(region_mod_south)],
#             'region_mod_west': [float(region_mod_west)],
#             'gender_female': [float(gender_female)],
#             'gender_male': [float(gender_male)],
#             'trauma': [float(trauma)],
#             'both_clinic': [float(both_clinic)],
#             'cci': [int(cci)]
#         })
#         # Make prediction
#         predicted_cost = model.predict(input_data)

#         # Display the prediction
#         st.title(f"Expected Cost: ${round(predicted_cost[0], 2)} USD")


def eda():
    st.title('EDA Page')

def about_us():
    st.title("About Us")

    # Introduction to the idea
    st.header("Our Idea")
    st.write("""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """)

    # About the company
    st.header("About Raphael Health")
    st.write("""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """)

    # About the company
    st.header("The Model")
    st.write("""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """)

    # Founders
    st.header("Meet the Founders")

    # Amer Mujkanovik
    st.subheader("Amer Mujkanovik: Data & Modelling")

    # Add an image of Amer
    st.image("AmerProfile.jpg", width=200)

    st.write("""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """)

    # Panwen Chen
    st.subheader("Panwen Chen: Modelling")

    # Add an image of Panwen
    st.image("PanwenProfile.png", width=200)

    st.write("""
    Panwen is an experienced insurance broker for many years.
    In his distinguished career, he mainly dealt with health insurance. Every time when he sees a potential candidate for health insurance,
    he always asks himself, how can I best help maximise my shareholder’s interest by preventing potential big pay outs?
    This is his motivation to build Raphael Health - to quickly valuate a candidate’s likely cost to avoid high risk insurance policies.
    """)

    # George Martin
    st.subheader("George Martin: Data & Front End")

    # Add an image of George
    st.image("GeorgeProfile.JPG", width=200)

    st.write("""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """)


    # Closing
    st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit")

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Display login form if not logged in, else display the app
if not st.session_state.logged_in:
    login_form()
else:
    # Setup navigation
    page_names_to_funcs = {
        "Home": landing_page,
        "Predictions": prediction,
        "Data Analysis": eda,
        "About Us": about_us
    }

    selected_page = st.sidebar.selectbox("Choose a page", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()
