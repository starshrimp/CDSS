"""
main_app.py

This script is the main entry point for the Streamlit application. It orchestrates the loading
of rule data, setting up the initial Streamlit interface, filtering applications based on 
user-selected conditions, and conditionally updating the Streamlit interface with the 
filtered results.

Functions:
- main(): Executes the main workflow of the Streamlit app, including loading rules, setting up the 
interface, and filtering applications.

Modules:
- streamlit: Used to create the web application interface.
- streamlit_setup: Contains functions for initial and conditional setup of the Streamlit interface.
- excel_interface: Handles loading and filtering of rules from an Excel file.
"""


import streamlit as st
from streamlit_setup import initial_setup_streamlit, conditional_setup_streamlit
from excel_interface import load_rules, filter_applications

def main():
    rules_df = load_rules()
    selected_condition = initial_setup_streamlit(rules_df)
    if selected_condition:
        applications_list = filter_applications(rules_df, selected_condition)
        conditional_setup_streamlit(rules_df, selected_condition, applications_list)


if __name__ == "__main__":
    main()
