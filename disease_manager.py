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
