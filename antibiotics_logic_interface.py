import pandas as pd
import streamlit as st
from excel_interface import process_spectrum_info, load_info_text

def get_antibiotic_info(first_line_antibiotics, other_antibiotics, info_antibiotics):
    antibiotics_df = pd.read_excel('antibiotics.xlsx')
    if other_antibiotics and info_antibiotics:
        for antibiotic in info_antibiotics:
            display_info_text(antibiotic)
    if first_line_antibiotics:
        st.markdown("## First-Line Antibiotics")
        for antibiotic in first_line_antibiotics:
            display_antibiotic_info(antibiotics_df, antibiotic, 'first_line')
    if other_antibiotics:
        for antibiotic in other_antibiotics:
            if antibiotic == "No antibiotics":
                st.error("No antibiotics indicated.")
            else:
                display_antibiotic_info(antibiotics_df, antibiotic, 'no')




def display_antibiotic_info(antibiotics_df, antibiotic, kind):
    display_df = antibiotics_df[antibiotics_df['advice'].str.lower() == antibiotic.lower()]
    for _, row in display_df.iterrows():

        spectrum_info_str = process_spectrum_info(row)


        info_content = f"""
        ## {row['advice']}  ({row['application']})  \n
        **Application**: {row['dosage']} {row['application']} {row['frequency']}    \n
        **Spectrum**: {spectrum_info_str}    \n
        **Warning**: {row['warnings']}
        """
        if kind == "first_line":
          st.success(info_content)
        else:
          st.info(info_content)

def display_info_text(antibiotic_name):
    # Fetch the info text for the given antibiotic name
    info_text = load_info_text(antibiotic_name)

    # Display the info text in a Streamlit warning widget
    if info_text:
        st.warning(f"## {antibiotic_name}    \n {info_text}")


