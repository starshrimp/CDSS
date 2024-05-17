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

    selected_system_label = setup_disease_question(manager)
    if selected_system_label:
      selected_condition = setup_condition_question(manager, selected_system_label)
      return selected_condition

def conditional_setup_streamlit(rules_df, selected_condition, applications_list):
    # Load conditional questions
    conditional_questions = load_conditional_questions()

    # Filter rules DataFrame for the selected condition
    condition_filtered_rules = rules_df[rules_df['condition'].str.lower() == selected_condition.lower()]

    responses = {}
    for idx, row in conditional_questions.iterrows():
        feature_key = row['feature_key']
        question = row['question']
        possible_answers = row['possible_answers']

        # Check if the feature column exists and has non-empty values for the selected condition
        if feature_key in condition_filtered_rules.columns and not condition_filtered_rules[feature_key].isnull().all():
            if binary_question(possible_answers) == True:
                # radiobuttons for binary questions
                response = st.radio(question, ["Yes", "No"], key=f"{feature_key}_binary_{idx}")
                responses[feature_key] = response
            else:
                # dropdowns for non-binary questions
                user_response = st.selectbox(question, ["Select an option"] + possible_answers, key=f"{feature_key}_{idx}")
                if user_response == "Select an option":
                    st.warning(f"Please select an answer for: {question}")
                    return None
                responses[feature_key] = user_response
        else:
            responses[feature_key] = None
        

    if applications_list:
        applications_list.append("any")
        default_option_index = applications_list.index("any")
        application = st.selectbox("Which method of application do you prefer?", applications_list, default_option_index)
        responses['application'] = application
    else:
        responses['application'] = ""

    if st.button("Get Advice"):
        first_line_antibiotics, other_antibiotics, info_antibiotics = get_possible_antibiotics(selected_condition, responses, rules_df)
        get_antibiotic_info(first_line_antibiotics, other_antibiotics, info_antibiotics)

def binary_question(possible_answers):
    for item in possible_answers:
      if item == 'binary':
        return True
        
    else:
        return False
    

def setup_disease_question(manager):
    disease_options = manager.organ_systems_labels.tolist()
    disease_options.insert(0,"Select an option")
    selected_system_label = st.selectbox("Select an organ system or disease type.", disease_options)
    if selected_system_label == "Select an option":
        st.warning("Please select an organ system or disease type.")
        return None
    else:
        return selected_system_label
    
def setup_condition_question(manager, selected_system_label):
    conditions = manager.get_conditions(selected_system_label)
    selected_condition = st.selectbox("Select the specific condition you are treating.", ["Select an option "] + conditions)
    if selected_condition == "Select an option":
        st.warning("Please select a specific condition.")
        return None
    else:
        return selected_condition