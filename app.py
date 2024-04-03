import os
from pathlib import Path
import streamlit as st
import pandas as pd
from joblib import load
import numpy as np
import pickle

# Set page configuration
st.set_page_config(
    page_title='Raphael Health',
    page_icon='🩺',
    layout='centered',
    initial_sidebar_state='auto'
)

model_path = Path('model.pkl')

model = load(model_path)


#####################################################
################  LOGIN PAGE  ######################
#####################################################


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


#####################################################
################  HOME PAGE  ######################
#####################################################


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


#####################################################
################  PREDICTIONS  ######################
#####################################################


def prediction():
    st.markdown("<h1 style='text-align: center; color: black;'>Input Customer Data</h1>", unsafe_allow_html=True)
    #df = pd.read_csv('data/grouped_ver_1.csv')

################  REGION  ########################

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
        selected_region_codes = [region_codes[region] for region in selected_regions]
        region_lst = [0,0,0,0]
        region_lst[int(selected_region_codes[0])] = 1

################  AGE  ########################

    # User inputs an age
    age_input = st.text_input('Select Age', placeholder='Enter Age In Years (0-65)')

################  number of clinic visits ########################
    clinic_vistis_input = st.text_input('Enter the number of clinic visits last year',
                                        placeholder='Enter number of clinic visits')

################  GENDER  ########################

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
        selected_gender_codes = [gender_codes[gender] for gender in selected_genders]
        gender_1st = [0,0]
        gender_1st[int(selected_gender_codes[0])] = 1

################  RELATIONSHIP TO PRIMARY  ########################

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
        selected_relationship_codes = [relationship_codes[name] for name in selected_relationship_names]
        relationship_lst = [0,0,0,0]
        relationship_lst[int(selected_relationship_codes[0])] = 1

################  PREVIOUSLY HOPITALISED  ########################

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

################  DISEASES  ########################

    # Define the mapping of readable disease names to their corresponding logical names
    disease_name_mapping = {
        'Respiratory Disease': 'respiratory_d',
        'Hypertension': 'hypertension',
        'Diabetes Melitus': 'diabetes_melitus',
        'Dementia': 'dementia',
        'Kidney Disease': 'kidney_disease',
        'Liver Disease': 'liver_disease',
        'Diarrheal Disease': 'diarrheal_disease',
        'Myocardial Infarction': 'myocardial_infarction',
        'Cardiovascular Disease': 'cardiovascular_d',
        'Heart Failure': 'chf',
        'Peripherial Vascular Disease': 'pvd',
        'Non-Metastatic Cancer': 'cancer',
        'Metastatic Cancer': 'metastasis',
        'Autoimmune Disease': 'connective_tissue_disease',
        'Peptic Ulcer': 'puc',
        'Stroke': 'hemiplegia',
        'Lymphoma': 'lymphoma',
        'AIDS': 'aids',
        'Previous Fracture': 'trauma'
    }

    # Streamlit multiselect widget for selecting diseases
    selected_disease_names = st.multiselect(
        'Select Diseases Diagnosed to Patient',
        list(disease_name_mapping.keys()),
        key='disease_selection'  # Providing a unique key
    )

    # Initialize disease_lst with zeros for all diseases
    disease_lst = [0] * len(disease_name_mapping)

    # Update disease_lst based on selected diseases
    if selected_disease_names:
        for name in selected_disease_names:
            # Find the index for each selected disease from disease_name_mapping
            index = list(disease_name_mapping.keys()).index(name)
            # Set the corresponding position in disease_lst to 1
            disease_lst[index] = 1


    if st.button('Submit'):
        # Validate age_input before using it in the model
        try:
        # Convert age_input to float, but use np.nan if age_input is empty or invalid
            age_input_value = float(age_input) if age_input and age_input.replace('.','',1).isdigit() else np.nan
        except ValueError:
            st.error("Please enter a valid age in years.")
            return  # Stop execution if age_input is invalid

        # Validate days_input before using it in the model
        try:
        # Convert days_input to float, but use np.nan if days_input is empty or invalid
            days_input_value = float(days_input) if days_input and days_input.replace('.','',1).isdigit() else np.nan
        except ValueError:
            st.error("Please enter a valid age in years.")
            return

        try:
           clinic_vistis_input = float(clinic_vistis_input) if clinic_vistis_input and clinic_vistis_input.replace('.','',1).isdigit() else np.nan
        except ValueError:
            st.error("Please enter a valid number of clinic visits")
            return  # Stop execution if age_input is invalid

# DataFrame should match the exact format (order and number of columns) expected by model
        initial_list_wo_dis = pd.DataFrame({
            'gender_male': [float(gender_1st[1])],
            'relationship_to_primary_beneficiary': [float(relationship_lst[0])],
            'age_years': [float(age_input_value)],
            'clinic_visits': [float(clinic_vistis_input)], # need to have this on the input page for clinic visits
            'myocardial_infarction': [int(disease_lst[7])],
            'chf': [int(disease_lst[9])],
            'pvd': [int(disease_lst[10])],
            'cardiovascular_d': [int(disease_lst[8])],
            'respiratory_d': [int(disease_lst[0])],
            'hypertension': [int(disease_lst[1])],
            'diabetes_melitus': [int(disease_lst[2])],
            'dementia': [int(disease_lst[3])],
            'kidney_disease': [int(disease_lst[4])],
            'liver_disease': [int(disease_lst[5])],
            'diarrheal_disease': [int(disease_lst[6])],
            'cancer': [int(disease_lst[11])],
            'metastasis': [int(disease_lst[12])],
            'connective_tissue_disease': [int(disease_lst[13])],
            'puc': [int(disease_lst[14])],
            'hemiplegia': [int(disease_lst[15])],
            'lymphoma': [int(disease_lst[16])],
            'aids': [int(disease_lst[17])],
            'lohs': [float(days_input_value)],
            'clinic_inpatient': [float(hosped_1st[0])],
            'region_mod_northcentral': [float(region_lst[0])],
            'region_mod_northeast': [float(region_lst[1])],
            'region_mod_south': [float(region_lst[2])],
            'region_mod_west': [float(region_lst[3])],
            'gender_female': [float(gender_1st[0])],
            'trauma': [int(disease_lst[18])],
            'both_clinic': [float(0)],
            'cci': [int(0)]
            })
        # st.write(pd.DataFrame(selected_disease_list).T)
        # initial_list_wo_dis.extend(selected_disease_list)
        # Make prediction



        predicted_cost = model.predict(initial_list_wo_dis)


        # Display the prediction
        st.title(f"Expected Cost: ${round(predicted_cost[0], 2)} USD")


#####################################################
################  EDA PAGE  ######################
#####################################################


def eda():
    st.title('EDA Page')


#####################################################
################  ABOUT US PAGE  ######################
#####################################################


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
    """)

    # Panwen Chen
    st.subheader("Panwen Chen: Modelling")

    # Add an image of Panwen
    st.image("PanwenProfile.png", width=200)

    st.write("""
    Panwen is an experienced insurance broker for many years.
    In his distinguished career, he mainly dealt with health insurance.
    Every time when he sees a potential candidate for health insurance,
    he always asks himself, how can I best help maximise my shareholder`s interest by preventing potential big pay outs?
    This is his motivation to build Raphael Health - to quickly valuate a candidate`s likely cost to avoid high risk insurance policies.
    """)

    # George Martin
    st.subheader("George Martin: Data & Front End")

    # Add an image of George
    st.image("GeorgeProfile.JPG", width=200)

    st.write("""
    George is the Senior Data Engineer at the Royal Kennel Club,
    A non-profit organisation dedicated to the health and welfare of dogs.
    In his role he frequently wrangles and vizualises large datasets to turn data from a resource into
    a product that can be used for the betternment of his organisation and its objectives.
    His interest and belief in the ability to leverage big data for positive outcomes in the health space
    inspired him to join Amer and Panwen on the journey to create Raphael Health.
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
