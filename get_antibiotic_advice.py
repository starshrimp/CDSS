import pandas as pd


def get_antibiotic_advice(condition, foal_status, pet_status, abscess, application, rules_df):
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