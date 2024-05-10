import streamlit as st
from streamlit_setup import initial_setup_streamlit, conditional_setup_streamlit
from excel_interface import load_rules, filter_applications

def main():
    rules_df = load_rules()
    selected_condition = initial_setup_streamlit(rules_df)
    applications_list, has_foal_status, has_pet_status, has_abscess = filter_applications(rules_df, selected_condition)

    conditional_setup_streamlit(rules_df, selected_condition, applications_list, has_foal_status, has_pet_status, has_abscess)


if __name__ == "__main__":
    main()