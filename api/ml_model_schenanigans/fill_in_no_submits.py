import os
import pandas as pd

# Path to your CSV file
csv_file_path = './2_Report_Test_Cases.csv'  # Replace with the actual path to your CSV file

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

root_folder_qs = './cleaned_stuff'

# Ensure the root folder exists
os.makedirs(root_folder_qs, exist_ok=True)

# Process each row in the DataFrame, using 'Question Submission ID' this time
for index, row in df.dropna(subset=['Assignment Submission ID']).iterrows():
    # Extract Question Submission ID, first name, and last name
    question_submission_id = str(row['Assignment Submission ID']).strip()  # Ensure it's a string and strip spaces
    first_name = row['First Name']
    last_name = row['Last Name']
    
    # Define the folder name for each Question Submission ID
    student_folder_qs = os.path.join(root_folder_qs, question_submission_id)
    
    # Ensure the student's folder exists
    os.makedirs(student_folder_qs, exist_ok=True)
    
    # Define the file name using Question Submission ID
    file_name_qs = f"{question_submission_id}_name.txt"
    file_path_qs = os.path.join(student_folder_qs, file_name_qs)

    if os.path.exists(file_path_qs):
        os.remove(file_path_qs)
    
    # Check if the file does not exist and then create it
    if not os.path.exists(file_path_qs):
        with open(file_path_qs, 'w') as file:
            # Write the student's first and last name to the file
            file.write(f"{first_name} {last_name}")