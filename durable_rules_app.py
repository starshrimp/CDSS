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


diseases_df = pd.read_excel('diseases.xlsx', sheet_name='Diseases')
conditions_df = pd.read_excel('conditions.xlsx', sheet_name='Conditions')

manager = DiseaseManager(diseases_df, conditions_df)

# Streamlit user interface
st.title('Disease and Condition Selector')

# Select box for organ systems
selected_system_label = st.selectbox("What organ system or disease type are you treating in the horse?", manager.organ_systems_labels)

# Get conditions based on the selected label, mapping it to the name
conditions = manager.get_conditions(selected_system_label)

# Select box for conditions
selected_condition = st.selectbox("What specific condition are you treating?", conditions)

st.write(f"You selected the system: {selected_system_label} and the condition: {selected_condition}")
