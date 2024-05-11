from durable.lang import *
import pandas as pd
import streamlit as st
from disease_manager import DiseaseManager
from rule_logic_interface import get_possible_antibiotics
from antibiotics_logic_interface import get_antibiotic_info
from excel_interface import load_conditional_questions


def initial_setup_streamlit(rules_df):
    st.title('Equine Antibiotics CDSS')
    st.write('This Clinical Decision Support System is based upon the Antibiotika Leitfaden of the Schweizerische Vereinigung für Pferdemedizin.    \n It is intended to provide the user with an aid in selecting appropriate antibiotic therapy for each indication. The correct selection of antibiotics is critical to ensure optimal treatment outcomes, prevent the development of resistance, and minimize adverse effects.   \n  By integrating the latest research and guidelines, this system supports clinicians in making evidence-based decisions that are tailored to the specific health needs of each patient. This not only enhances the efficacy of treatment but also contributes to the broader effort to curb antibiotic resistance, a growing concern in veterinary as well as human medicine.')
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
