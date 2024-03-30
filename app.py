import streamlit as st
import pandas as pd

# Title of the web app
st.title('Customer Data Input')

# Input for a specific customerID code
customer_id = st.text_input('Customer ID', 'Enter Customer ID here')

# Multiple selection for Region
regions = ['North', 'South', 'East', 'West']
selected_regions = st.multiselect('Select Region(s)', regions)

# Specific input for Zipcode
zipcode = st.text_input('Zipcode', 'Enter Zipcode here')

# Multiple selection for Gender
genders = ['Male', 'Female', 'Other']
selected_genders = st.multiselect('Select Gender(s)', genders)

# Multiple selection for Health Plan Type
health_plans = ['HMO', 'PPO', 'EPO']
selected_plans = st.multiselect('Select Health Plan Type(s)', health_plans)

# Multiple selection for Disease
diseases = ['Diabetes', 'Hypertension', 'Heart Disease', 'Cancer']
selected_diseases = st.multiselect('Select Disease(s)', diseases)

# Button to confirm the input and selection
if st.button('Submit'):
    st.write('Customer ID:', customer_id)
    st.write('Selected Regions:', selected_regions)
    st.write('Zipcode:', zipcode)
    st.write('Selected Genders:', selected_genders)
    st.write('Selected Health Plan Types:', selected_plans)
    st.write('Selected Diseases:', selected_diseases)
