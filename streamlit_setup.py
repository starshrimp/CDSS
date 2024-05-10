from durable.lang import *
import pandas as pd
import streamlit as st
from disease_manager import DiseaseManager
from get_possible_antibiotics import get_possible_antibiotics
from get_antibiotic_info import get_antibiotic_info


def initial_setup_streamlit(rules_df):
    st.title('Equine Antibiotics CDSS')
    manager = DiseaseManager(pd.read_excel('diseases.xlsx', sheet_name='Diseases'),
                             pd.read_excel('conditions.xlsx', sheet_name='Conditions'))

    selected_system_label = st.selectbox("Select the organ system or disease type:", manager.organ_systems_labels)
    conditions = manager.get_conditions(selected_system_label)
    selected_condition = st.selectbox("Select the specific condition you are treating:", conditions)

    return selected_condition

def conditional_setup_streamlit(rules_df, selected_condition, applications_list, has_foal_status, has_pet_status, has_abscess):
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
        first_line_antibiotics, other_antibiotics = get_possible_antibiotics(selected_condition, foal_status, pet_status, abscess, application, rules_df)
        get_antibiotic_info(first_line_antibiotics, other_antibiotics)
