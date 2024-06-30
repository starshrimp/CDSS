"""
excel_interface.py

This module handles the loading and processing of data from various Excel files. 
It includes functions to load rules, conditional questions, information texts, filter 
applications based on selected conditions, and process spectrum information for antibiotics.

Functions:
- load_rules(): Loads the rules from the 'rules.xlsx' file.
- load_conditional_questions(): Loads and processes conditional questions from the 
'conditional_questions.xlsx' file.
- load_info_text(advice): Loads and returns the information text for a given antibiotic advice 
from the 'info_texts.xlsx' file.
- filter_applications(rules_df, selected_condition): Filters the available application methods 
for a selected condition.
- check_for_application_methods(filtered_df): Checks and returns unique application methods from
 the filtered DataFrame.
- process_spectrum_info(row): Processes and returns the spectrum information for an antibiotic.

Modules:
- pandas: Used to handle data operations, particularly reading and processing Excel files.
"""


import pandas as pd


def load_rules():
    # loads the rules
    return pd.read_excel('rules.xlsx')

def load_conditional_questions():
    # loads & processes conditional questions (= additional questions that can be added for antibiotic selection)
    df = pd.read_excel('conditional_questions.xlsx')
    # Delimiter is ";"
    df['possible_answers'] = df['possible_answers'].apply(lambda x: x.split(';'))
    return df

def load_info_text(advice):
    # loads the info_text for an advice and returns the corresponding info text 
    antibiotics_info_df = pd.read_excel('info_texts.xlsx')

    advice = advice.strip().lower()
    info_text_row = antibiotics_info_df[antibiotics_info_df['advice'].str.lower().str.strip() == advice]

    # Check if there is an info text available and return it
    if not info_text_row.empty and info_text_row['info_text'].values[0]:
        return info_text_row['info_text'].values[0]


def filter_applications(rules_df, selected_condition):
    # Checks for which methods of application are available for the selected condition and returns them

    # Filter the DataFrame for a specific condition
    filtered_df = rules_df[rules_df['condition'] == selected_condition]

    # Checking for application methods and dropping NaN values
    unique_applications = check_for_application_methods(filtered_df)

    applications_list = list(unique_applications)

    return applications_list
    

def check_for_application_methods(filtered_df):
    if 'application' in filtered_df.columns:
        unique_applications = filtered_df['application'].dropna().unique()
    else:
        unique_applications = []
    return unique_applications


def process_spectrum_info(row):
    # gets spectrum info for the antibiotic and processes it 
    spectrum_info = []
    if not pd.isna(row['gram-positives']):
        spectrum_info.append(f"Gram-positives: {row['gram-positives'].replace('*', '+')}")
    if not pd.isna(row['gram-negatives']):
        spectrum_info.append(f"Gram-negatives: {row['gram-negatives'].replace('*', '+')}")
    if not pd.isna(row['anaerobics']) and row['anaerobics'] != 'nan':
        spectrum_info.append(f"Anaerobics: {row['anaerobics'].replace('*', '+')}")

    # Join all valid spectrum info with commas
    spectrum_info_str = ', '.join(spectrum_info)
    return spectrum_info_str