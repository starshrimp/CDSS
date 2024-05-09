from durable.lang import *
import pandas as pd
import streamlit as st

class DiseaseManager:
    def __init__(self, disease_dataframe, condition_dataframe):
        self.disease_data = disease_dataframe
        self.condition_data = condition_dataframe
        # Creating a dictionary to map labels to names for display purposes
        self.label_to_name = dict(zip(self.disease_data['label'], self.disease_data['name']))
        self.organ_systems_labels = self.disease_data['label'].unique()  # Use labels for display
        self.conditions_map = self._map_conditions()

    def _map_conditions(self):
        conditions_map = {}
        # Mapping conditions using the 'name' from diseases_df for internal processing
        for name in self.label_to_name.values():
            system_conditions = self.condition_data[self.condition_data['selected_disease'].str.lower() == name.lower()]
            conditions_map[name] = system_conditions['label'].tolist()
        return conditions_map

    def get_conditions(self, system_label):
        # Use the mapping to get the correct name for internal processing
        system_name = self.label_to_name[system_label]
        return self.conditions_map.get(system_name, [])


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


def get_medical_advice(condition, foal_status, pet_status, abscess, application, rules_df):
    # Apply filters dynamically based on provided arguments
    conditions = []
    if condition:
        conditions.append(rules_df['condition'].str.lower() == condition.lower())
    if foal_status:
      conditions.append(
          (rules_df['foal_status'].fillna('').str.lower() == foal_status.lower()) | 
          (rules_df['foal_status'].fillna('') == '')
      )
    if pet_status:
        conditions.append(
            (rules_df['pet_status'].fillna('').str.lower() == pet_status.lower()) | 
            (rules_df['pet_status'].fillna('') == '')
        )

    if abscess:
        conditions.append(
            (rules_df['abscess'].fillna('').str.lower() == abscess.lower()) | 
            (rules_df['abscess'].fillna('') == '')
        )

    if application:
        conditions.append(
            (rules_df['application'].fillna('').str.lower() == application.lower()) | 
            (rules_df['application'].fillna('') == '')
        )

    # Combine conditions with logical AND
    if conditions:
        filtered_rules = rules_df[conditions[0]]
        for condition in conditions[1:]:
            filtered_rules = filtered_rules[condition]
    else:
        # If no filters are provided, return the full dataset
        filtered_rules = rules_df


    # Check if any rules were found
    if not filtered_rules.empty:
        # Concatenate all advices into a single string separated by newline
        advices = '\n'.join(filtered_rules['advice'].drop_duplicates())
        return advices
    else:
        return "No advice found for the given conditions."



# Streamlit interface
def main():
    rules_df = load_rules()
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
        advice = get_medical_advice(selected_condition, foal_status, pet_status, "", application, rules_df)
        st.write(f"Advice: {advice}")

if __name__ == "__main__":
    main()
