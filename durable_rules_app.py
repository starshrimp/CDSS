from durable.lang import *
import pandas as pd
import streamlit as st
from disease_manager import DiseaseManager
from get_possible_antibiotics import get_possible_antibiotics
from get_antibiotic_info import get_antibiotic_info


def load_rules():
    return pd.read_excel('rules.xlsx')

def filter_applications(rules_df, selected_condition):
    # Filter the DataFrame for a specific condition
    filtered_df = rules_df[rules_df['condition'] == selected_condition]

    # Checking for application methods and dropping NaN values
    if 'application' in filtered_df.columns:
        unique_applications = filtered_df['application'].dropna().unique()
    else:
        unique_applications = []

    applications_list = list(unique_applications)

    # Check if 'foal_status', 'pet_status', and 'abscess' columns have any relevant entries
    has_foal_status = 'foal_status' in filtered_df.columns and not filtered_df['foal_status'].isnull().all()
    has_pet_status = 'pet_status' in filtered_df.columns and not filtered_df['pet_status'].isnull().all()
    has_abscess = 'abscess' in filtered_df.columns and not filtered_df['abscess'].isnull().all()

    if applications_list:
        print(applications_list)

    return applications_list, has_foal_status, has_pet_status, has_abscess
    
def setup_streamlit(rules_df):
    st.title('Equine Antibiotics CDSS')
    manager = DiseaseManager(pd.read_excel('diseases.xlsx', sheet_name='Diseases'),
                             pd.read_excel('conditions.xlsx', sheet_name='Conditions'))

    selected_system_label = st.selectbox("Select the organ system or disease type:", manager.organ_systems_labels)
    conditions = manager.get_conditions(selected_system_label)
    selected_condition = st.selectbox("Select the specific condition you are treating:", conditions)

    applications_list, has_foal_status, has_pet_status, has_abscess = filter_applications(rules_df, selected_condition)

    if has_foal_status:
        foal_status = st.selectbox("Is your patient a foal < 1 month of age?", ["Yes, Foal < 1 Month", "No, older than 1 Month"])
    else:
        foal_status = None 

    if has_pet_status:
        pet_status = st.selectbox("Is the patient a pet or a farm animal?", ["Pet", "Farm Animal"])
    else:
        pet_status = None 

    if has_abscess:
        abscess = st.selectbox("Is there an abscess present?", ["Yes, Abscess", "No, No Abscess"])
    else:
        abscess = None  

    if applications_list:
        applications_list.append("any")
        application = st.selectbox("Which method of application do you prefer?", applications_list)
    else:
        application = ""

    if st.button("Get Advice"):
        antibiotic_list = get_possible_antibiotics(selected_condition, foal_status, pet_status, abscess, application, rules_df)
        get_antibiotic_info(antibiotic_list)



# Streamlit interface
def main():
    rules_df = load_rules()
    setup_streamlit(rules_df)

if __name__ == "__main__":
    main()
