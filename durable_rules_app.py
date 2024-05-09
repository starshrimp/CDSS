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

def get_medical_advice(condition, foal_status, pet_status, abscess, application, rules_df):
    # Filter the DataFrame based on the provided conditions
    filtered_rules = rules_df[
        (rules_df['condition'].str.lower() == condition.lower()) &
        (rules_df['foal_status'].str.lower() == foal_status.lower()) &
        (rules_df['pet_status'].str.lower() == pet_status.lower()) &
        (rules_df['abscess'].str.lower() == abscess.lower()) &
        (rules_df['application'].str.lower() == application.lower())
    ]
    print(condition, foal_status, pet_status, abscess, application)
    print(filtered_rules)
    # Assuming that the filtered results will always have one matching row
    if not filtered_rules.empty:
        return filtered_rules.iloc[0]['advice']
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

    if st.button("Get Advice"):
        advice = get_medical_advice("Non-complicated Wounds", "abc", "abc", "abc", "abc", rules_df)
        st.write(f"Advice: {advice}")

if __name__ == "__main__":
    main()
