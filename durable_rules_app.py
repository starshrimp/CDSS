from durable.lang import *
import pandas as pd
import streamlit as st
from disease_manager import DiseaseManager
from get_antibiotic_advice import get_antibiotic_advice


def load_rules():
    return pd.read_excel('rules.xlsx')

def filter_applications(rules_df, selected_condition):
    # Filter the DataFrame for a specific condition
    filtered_df = rules_df[rules_df['condition'] == selected_condition]

    unique_applications = filtered_df['application'].dropna().unique()
    
    # Convert the numpy array to a list
    applications_list = unique_applications.tolist()

    if applications_list:  # This check will now work as expected
        print(applications_list)
        return applications_list
    else:
        return [] 
    
def setup_streamlit(rules_df):
    st.title('Disease and Condition Selector')
    manager = DiseaseManager(pd.read_excel('diseases.xlsx', sheet_name='Diseases'),
                             pd.read_excel('conditions.xlsx', sheet_name='Conditions'))

    selected_system_label = st.selectbox("Select the organ system or disease type:", manager.organ_systems_labels)
    conditions = manager.get_conditions(selected_system_label)
    selected_condition = st.selectbox("Select the specific condition you are treating:", conditions)
    foal_status = st.selectbox("Is your patient a foal < 1 month of age?", ["Yes, Foal < 1 Month", "No, older than 1 Month"]) 
    pet_status = st.selectbox("Is the patient a pet or a farm animal?", ["Pet", "Farm Animal"]) 

    applications_list = filter_applications(rules_df, selected_condition)
    print(applications_list)
    if applications_list:
      application = st.selectbox("Which method of application do you prefer?", applications_list) 
      print(application)
    else:
      application = ""

    if st.button("Get Advice"):
        advice = get_antibiotic_advice(selected_condition, foal_status, pet_status, "", application, rules_df)
        st.write(f"Advice: {advice}")

# Streamlit interface
def main():
    rules_df = load_rules()

    setup_streamlit(rules_df)

if __name__ == "__main__":
    main()
