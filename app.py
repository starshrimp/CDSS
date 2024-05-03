import streamlit as st
import requests

# Title of the app
st.title("Horse Treatment Decision Support System")

# Using a form for input collection
with st.form("input_form"):
    # Text input for disease treatment
    disease = st.selectbox(
        "Which disease are you treating the horse for?",
        ["Colic", "Laminitis", "Respiratory Infection", "Other"]
    )

    # Numeric input for horse age
    age = st.number_input("How old is the horse?", min_value=0)

    # Radio buttons for choosing between farm-animal or pet
    horse_type = st.radio(
        "Is the horse a farm-animal or pet?",
        ["Farm-Animal", "Pet"]
    )

    # Select box for type of application
    application_type = st.selectbox(
        "What type of application do you prefer?",
        ["Intravenous (IV)", "Intramuscular (IM)", "Oral (PO)"]
    )

    # Submit button for the form
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success("Form Submitted Successfully!")

def send_data_to_make(data):
    try:
        MAKE_URL = "https://hook.eu2.make.com/fjdjieu50c6puq59we54mbvn3bg6zuky"
        response = requests.post(MAKE_URL, json=data)
        # Check if the response was successful
        if response.status_code == 200:
            # Try to decode the response as JSON
            return response.json()
        else:
            # Return a custom error message or the status code
            return {'error': 'Received unexpected status code: {}'.format(response.status_code)}
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the request
        return {'error': str(e)}
    except ValueError as e:
        # Handle JSON decode error
        return {'error': 'Error decoding JSON: {}'.format(str(e))}

# Displaying the collected information
if submitted:
    # Collect all the data in a dictionary
    data = {
        "disease": disease,
        "age": age,
        "horse_type": horse_type,
        "application_type": application_type
    }

    # Send data to MAKE and get the result
    result = send_data_to_make(data)
    
    # Display the response
    st.success("Form Submitted Successfully!")
    st.write("### Decision Result")
    st.json(result)  # Display the JSON response directly
