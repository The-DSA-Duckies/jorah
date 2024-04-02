import pandas as pd
import os
import regex as re

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('2_Report_Test_Cases.csv')

# Define the path to the cleaned_stuff folder
cleaned_stuff_path = 'cleaned_stuff'

# Function to remove the names and SID from the content of a file
def clean_file_content(file_path, first_name, last_name, sid):
    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    first_name_pattern = re.compile(re.escape(str(first_name)), re.IGNORECASE)
    last_name_pattern = re.compile(re.escape(str(last_name)), re.IGNORECASE)
    
    # Remove the occurrences of the first name, last name, and SID
    content = content.replace(str(first_name), '').replace(str(last_name), '').replace(str(sid), '')

    ufid_pattern = re.compile("[0-9]{8}")

    content = ufid_pattern.sub('', content)

    content = first_name_pattern.sub('', content)
    content = last_name_pattern.sub('', content)
    
    # Write the cleaned content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    assignment_id = row['Assignment Submission ID']
    first_name = row['First Name']
    last_name = row['Last Name']
    sid = row['SID']
    
    # Construct the path to the folder for the current Assignment Submission ID
    folder_path = os.path.join(cleaned_stuff_path, str(assignment_id))
    
    # Check if the folder exists
    if os.path.isdir(folder_path):
        # Iterate over each file in the directory
        for file_name in os.listdir(folder_path):
            # Construct the path to the file
            file_path = os.path.join(folder_path, file_name)
            
            # Check if it is a text file
            if file_path.endswith('.txt'):
                # Clean the file content
                clean_file_content(file_path, first_name, last_name, sid)

print("Cleaning complete.")
