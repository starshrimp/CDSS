from durable.lang import *
import pandas as pd
import streamlit as st
from disease_manager import DiseaseManager
from rule_logic_interface import get_possible_antibiotics
from antibiotics_logic_interface import get_antibiotic_info
from excel_interface import load_conditional_questions


def initial_setup_streamlit(rules_df):
    st.title('Equine Antibiotics CDSS')
    manager = DiseaseManager(pd.read_excel('diseases.xlsx', sheet_name='Diseases'),
                             pd.read_excel('conditions.xlsx', sheet_name='Conditions'))

    selected_system_label = st.selectbox("Select the organ system or disease type:", manager.organ_systems_labels)
    conditions = manager.get_conditions(selected_system_label)
    selected_condition = st.selectbox("Select the specific condition you are treating:", conditions)

    return selected_condition

def conditional_setup_streamlit(rules_df, selected_condition, applications_list):
    # Load conditional questions
    conditional_questions = load_conditional_questions()

    # Filter rules DataFrame for the selected condition
    condition_filtered_rules = rules_df[rules_df['condition'].str.lower() == selected_condition.lower()]

    responses = {}
    for _, row in conditional_questions.iterrows():
        feature_key = row['feature_key']
        question = row['question']
        possible_answers = row['possible_answers']

        # Check if the feature column exists and has non-empty values for the selected condition
        if feature_key in condition_filtered_rules.columns and not condition_filtered_rules[feature_key].isnull().all():
            user_response = st.selectbox(question, possible_answers)
            responses[feature_key] = user_response
        else:
            responses[feature_key] = None

    if applications_list:
        applications_list.append("any")
        application = st.selectbox("Which method of application do you prefer?", applications_list)
        responses['application'] = application
    else:
        responses['application'] = ""

    if st.button("Get Advice"):
        first_line_antibiotics, other_antibiotics, info_antibiotics = get_possible_antibiotics(selected_condition, responses, rules_df)
        get_antibiotic_info(first_line_antibiotics, other_antibiotics, info_antibiotics)
