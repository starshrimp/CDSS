import pandas as pd
import streamlit as st
from excel_interface import process_spectrum_info, load_info_text

def get_antibiotic_info(first_line_antibiotics, other_antibiotics, info_antibiotics):
    antibiotics_df = pd.read_excel('antibiotics.xlsx')
    # Check for no antibiotics indicated in other antibiotics list
    if other_antibiotics == ["No antibiotics"]:
        st.error("No antibiotics indicated.")
        return

    if first_line_antibiotics or other_antibiotics:
        st.markdown("## Results")
        st.write("Antibiotics are prioritized: in green boxes are first-line recommendations, in blue boxes are alternative recommendations.    \n If there is no first-line recommendation for your selection, try the application method “any.” If there is still none, this is due to your patient's exclusion criteria. Please choose one of the alternative recommendations.")

    if info_antibiotics:
        for antibiotic in info_antibiotics:
            display_info_text(antibiotic)
    if first_line_antibiotics:
        st.markdown("## First-Line Antibiotics")
        for antibiotic in first_line_antibiotics:
            display_antibiotic_info(antibiotics_df, antibiotic, 'first_line')

    if other_antibiotics:
        st.markdown("## Alternatives")
        for antibiotic in other_antibiotics:
            display_antibiotic_info(antibiotics_df, antibiotic, 'no')



def display_antibiotic_info(antibiotics_df, antibiotic, kind):
    display_df = antibiotics_df[antibiotics_df['advice'].str.lower() == antibiotic.lower()]
    for _, row in display_df.iterrows():
        spectrum_info_str = process_spectrum_info(row)
        info_content = f"""
        ### {row['advice']}  ({row['application']})  \n
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
        st.warning(f"### {antibiotic_name}    \n {info_text}")


