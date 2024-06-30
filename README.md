# CDSS
## Step-by-Step Installation Guide

### Prerequisites
Ensure you have the following installed on your system:
- Python (version 3.7 or higher)
- pip (Python package installer)

### Step 1: Clone the Repository
First, clone the repository containing the project files. Open your terminal or command prompt and run:
```git clone <repository_url>```

### Step 2: Navigate to the Project Directory
Change your directory to the project folder:
```cd <project_directory>```

Replace <project_directory> with the name of the folder where the project files are located.

### Step 3: Install Required Packages
Install the required Python packages listed in the requirements.txt file:

``` pip install -r requirements.txt``` 

## How to Run the Application
The application is live at https://equine-antibiotic-cdss.streamlit.app/ ; if you'd still like to run the streamlit application locally on your computer, here is a short guide on how to execute it.

### Step 1: Start the Streamlit Application
Run the main application script using Streamlit:

```streamlit run main_app.py```  

### Step 2: Open the Application in Your Browser
After running the above command, Streamlit will automatically open your default web browser with the application. If it doesn't, you can manually open your browser and navigate to:

```http://localhost:8501```



## Modules
### main_app.py
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

### streamlit_setup.py
streamlit_setup.py

This module sets up the Streamlit interface for the Equine Antibiotics Clinical Decision Support 
System (CDSS). It includes functions to initialize the interface, manage disease and condition 
questions, handle conditional setups, and interact with other modules to fetch and display 
antibiotic recommendations.

Functions:
- initial_setup_streamlit(rules_df): Initializes the Streamlit interface, sets up the disease
question, and returns the selected condition.
- conditional_setup_streamlit(rules_df, selected_condition, applications_list): Sets up conditional
 questions based on the selected condition and displays antibiotic recommendations.
- binary_question(possible_answers): Determines if a question is binary based on possible answers.
- setup_disease_question(manager): Sets up the initial question regarding the organ system or 
disease type.
- setup_condition_question(manager, selected_system_label): Sets up the subsequent question 
regarding the specific condition being treated.

Modules:
- pandas: Used to read Excel files containing disease and condition data.
- streamlit: Used to create the web application interface and display various UI components.
- disease_manager: Manages disease and condition data.
- rule_logic_interface: Provides logic to fetch possible antibiotic recommendations.
- antibiotics_logic_interface: Provides functions to display detailed antibiotic information.
- excel_interface: Contains utility functions to load conditional questions from an Excel file.

### excel_interface.py

This module handles the loading and processing of data from various Excel files. It includes functions to load rules, conditional questions, information texts, filter applications based on selected conditions, and process spectrum information for antibiotics.

Functions:
- load_rules(): Loads the rules from the 'rules.xlsx' file.
- load_conditional_questions(): Loads and processes conditional questions from the 'conditional_questions.xlsx' file.
- load_info_text(advice): Loads and returns the information text for a given antibiotic advice from the 'info_texts.xlsx' file.
- filter_applications(rules_df, selected_condition): Filters the available application methods for a selected condition.
- check_for_application_methods(filtered_df): Checks and returns unique application methods from the filtered DataFrame.
- process_spectrum_info(row): Processes and returns the spectrum information for an antibiotic.

Modules:
- pandas: Used to handle data operations, particularly reading and processing Excel files.

### antibiotics_logic_interface.py

This module provides functionality to display detailed antibiotic information within a 
Streamlit application. It includes functions to fetch and display first-line and alternative
antibiotics, process spectrum information, and present additional textual information for 
selected antibiotics.

Functions:
- get_antibiotic_info(first_line_antibiotics, other_antibiotics, info_antibiotics): Main function 
to display antibiotic recommendations and detailed information.
- display_antibiotic_info(antibiotics_df, antibiotic, kind): Displays detailed information for a
specific antibiotic.
- display_info_text(antibiotic_name): Fetches and displays additional information text for a 
specific antibiotic.

Modules:
- pandas: Used to handle data operations, particularly reading the Excel file containing 
antibiotic data.
- streamlit: Used to create the web application interface and display various types of messages
and content.
- excel_interface: Contains utility functions to process spectrum information and load additional
text information.

### disease_manager.py

This module defines the DiseaseManager class, which manages disease and condition data for the 
Equine Antibiotics CDSS. It provides methods to initialize the data, map conditions to diseases, 
and fetch conditions based on the selected disease.

Classes:
- DiseaseManager: Manages disease and condition data, including mapping and retrieval of conditions.

Methods:
- __init__(self, disease_dataframe, condition_dataframe): Initializes the DiseaseManager with 
disease and condition data.
- _map_conditions(self): Creates a mapping of conditions to their respective diseases.
- get_conditions(self, system_label): Retrieves a list of conditions for the given system label.

Modules:
- pandas: Used to handle data operations, particularly reading and processing Excel files.

