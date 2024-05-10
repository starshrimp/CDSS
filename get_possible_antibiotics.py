import pandas as pd


def get_possible_antibiotics(condition, responses, rules_df):
    conditions = [rules_df['condition'].str.lower() == condition.lower()]
    for key, response in responses.items():
            if key != 'application':  # Skip 'application' here; handle it separately below
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
    other_antibiotics = filtered_rules[filtered_rules['first_line'] != 'yes']['advice'].drop_duplicates().tolist()

    return first_line_antibiotics, other_antibiotics


    # # Combine conditions with logical AND
    # if conditions:
    #     filtered_rules = rules_df[conditions[0]]
    #     for condition in conditions[1:]:
    #         filtered_rules = filtered_rules[condition]
    # else:
    #     # If no filters are provided, return the full dataset
    #     filtered_rules = rules_df


    # # Check if any rules were found
    # if not filtered_rules.empty:
    #     # Return a list of unique antibiotics
    #     antibiotics = filtered_rules['advice'].drop_duplicates().tolist()
    #     return antibiotics
    # else:
    #     return []