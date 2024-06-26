import pandas as pd


def get_possible_antibiotics(condition, responses, rules_df):
    
    conditions = [rules_df['condition'].str.lower() == condition.lower()]
    for key, response in responses.items():
            if key != 'application':  
                if response:
                    conditions.append(
                        (rules_df[key].fillna('').str.lower() == response.lower()) | 
                        (rules_df[key].fillna('') == '')
                    )

        # Handle 'application' response specifically 
    application_response = responses.get('application')
    if application_response and application_response.lower() != 'any':
            conditions.append(
                (rules_df['application'].fillna('').str.lower() == application_response.lower()) | 
                (rules_df['application'].fillna('') == '')
            )
    filtered_rules = rules_df
    for cond in conditions:
        filtered_rules = filtered_rules[cond]

    first_line_antibiotics = filtered_rules[filtered_rules['first_line'] == 'yes']['advice'].drop_duplicates().tolist()
    info_antibiotics = filtered_rules[filtered_rules['info_text'] != ""]['advice'].drop_duplicates().tolist()
    other_antibiotics = filtered_rules[filtered_rules['first_line'] != 'yes']['advice'].drop_duplicates().tolist()

    return first_line_antibiotics, other_antibiotics, info_antibiotics

