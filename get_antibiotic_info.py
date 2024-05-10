import pandas as pd
import streamlit as st
from excel_interface import process_spectrum_info

def get_antibiotic_info(first_line_antibiotics, other_antibiotics):
    antibiotics_df = pd.read_excel('antibiotics.xlsx')
    if first_line_antibiotics:
        st.markdown("## First-Line Antibiotics")
        for antibiotic in first_line_antibiotics:
            display_antibiotic_info(antibiotics_df, antibiotic, 'yes')
    if other_antibiotics:
        for antibiotic in other_antibiotics:
            print(antibiotic)
            if antibiotic == "No antibiotics":
                st.write("No antibiotics indicated.")
            else:
                display_antibiotic_info(antibiotics_df, antibiotic, 'no')
        



def display_antibiotic_info(antibiotics_df, antibiotic, first_line):
    display_df = antibiotics_df[antibiotics_df['advice'].str.lower() == antibiotic.lower()]
    for _, row in display_df.iterrows():

        spectrum_info_str = process_spectrum_info(row)


        info_content = f"""
        ## {row['advice']}   \n
        **Application**: {row['dosage']} {row['application']} {row['frequency']}    \n
        **Spectrum**: {spectrum_info_str}    \n
        **Warning**: {row['warnings']}
        """
        if first_line == "yes":
          st.success(info_content)
        else:
          st.info(info_content)

