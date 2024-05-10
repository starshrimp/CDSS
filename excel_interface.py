import pandas as pd


def load_rules():
    return pd.read_excel('rules.xlsx')

def load_conditional_questions():
    df = pd.read_excel('conditional_questions.xlsx')
    # Delimiter is ";"
    df['possible_answers'] = df['possible_answers'].apply(lambda x: x.split(';'))
    return df

def load_info_text(antibiotic_name):
    antibiotics_info_df = pd.read_excel('info_texts.xlsx')

    antibiotic_name = antibiotic_name.strip().lower()
    info_text_row = antibiotics_info_df[antibiotics_info_df['advice'].str.lower().str.strip() == antibiotic_name]

    # Check if there is an info text available and return it
    if not info_text_row.empty and info_text_row['info_text'].values[0]:
        return info_text_row['info_text'].values[0]


def filter_applications(rules_df, selected_condition):
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


# def check_for_entries_in_column(filtered_df):
#     has_foal_status = 'foal_status' in filtered_df.columns and not filtered_df['foal_status'].isnull().all()
#     has_pet_status = 'pet_status' in filtered_df.columns and not filtered_df['pet_status'].isnull().all()
#     has_abscess = 'abscess' in filtered_df.columns and not filtered_df['abscess'].isnull().all()
#     return has_foal_status, has_pet_status, has_abscess


def process_spectrum_info(row):
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