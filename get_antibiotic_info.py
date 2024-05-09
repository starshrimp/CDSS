import pandas as pd
import streamlit as st

def get_antibiotic_info(antibiotics_list):
    # Load the Excel file containing antibiotic details
    antibiotics_df = pd.read_excel('antibiotics.xlsx')

    if "No antibiotics" in antibiotics_list:
        st.write("No antibiotics are necessary for this condition.")
    else: 
        for antibiotic in antibiotics_list:
            display_df = antibiotics_df[antibiotics_df['advice'].str.lower() == antibiotic.lower()]
            if not display_df.empty:
                for _, row in display_df.iterrows():
                    st.markdown(f"## {row['advice']}")  # Title: Medication Name
                    st.markdown(f"### {row['medication_group']}")  # Title: Medication Name
                    # Application details
                    application_details = f"{row['dosage']} {row['application']} {row['frequency']}"
                    st.write(f"**Application**: {application_details}")
                    # Spectrum information
                    spectrum = f"**Gram-positives**: {row['gram-positives']}, **Gram-negatives**: {row['gram-negatives']}"
                    st.write(f"**Spectrum**: {spectrum}")
                    # Warning information with emphasis
                    st.markdown(f"**Warning**: <span style='color:red;'>{row['warnings']}</span>", unsafe_allow_html=True)
            else:
                st.write(f"No information found for {antibiotic}")
