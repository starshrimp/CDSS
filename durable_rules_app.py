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

    unique_applications = filtered_df['application'].dropna().unique()
    
    # Convert the numpy array to a list
    applications_list = unique_applications.tolist()

    if applications_list:
        print(applications_list)
        return applications_list
    else:
        return [] 
    
def setup_streamlit(rules_df):
    st.title('Equine Antibiotics CDSS')
    manager = DiseaseManager(pd.read_excel('diseases.xlsx', sheet_name='Diseases'),
                             pd.read_excel('conditions.xlsx', sheet_name='Conditions'))

    selected_system_label = st.selectbox("Select the organ system or disease type:", manager.organ_systems_labels)
    conditions = manager.get_conditions(selected_system_label)
    selected_condition = st.selectbox("Select the specific condition you are treating:", conditions)
    foal_status = st.selectbox("Is your patient a foal < 1 month of age?", ["Yes, Foal < 1 Month", "No, older than 1 Month"]) 
    pet_status = st.selectbox("Is the patient a pet or a farm animal?", ["Pet", "Farm Animal"]) 

    applications_list = filter_applications(rules_df, selected_condition)

    if applications_list:
      applications_list.append("any")
      application = st.selectbox("Which method of application do you prefer?", applications_list) 
    else:
      application = ""

    if st.button("Get Advice"):
        antibiotic_list = get_possible_antibiotics(selected_condition, foal_status, pet_status, "", application, rules_df)
        get_antibiotic_info(antibiotic_list)


# Streamlit interface
def main():
    rules_df = load_rules()

    setup_streamlit(rules_df)

if __name__ == "__main__":
    main()
