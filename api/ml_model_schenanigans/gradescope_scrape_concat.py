import os
from docx import Document
import fitz
import re
import csv


def main():
    pass

submission_pattern = r"\\submission_\d+\\"


def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def read_pdf(file_path):
    doc = fitz.open(file_path)
    full_text = ''
    for page in doc:
        full_text += page.get_text()
    return full_text

def write_to_student_folders(base_output_path, id_map, test_map, code_map, name_map):
    # Ensure the base output path exists
    os.makedirs(base_output_path, exist_ok=True)

    # Iterate through each submission ID
    for submission_id in set(id_map) | set(test_map) | set(code_map) | set(name_map):
        # Create a specific folder for the submission ID
        student_folder = os.path.join(base_output_path, submission_id)
        os.makedirs(student_folder, exist_ok=True)

        # Write report/document if exists
        if submission_id in id_map:
            with open(os.path.join(student_folder, f"{submission_id}_report.txt"), "w", encoding="utf-8") as f:
                f.write(id_map[submission_id])
        else:
            with open(os.path.join(student_folder, f"{submission_id}_report.txt"), "w", encoding="utf-8") as f:
                f.write("NO REPORT FOUND")

        # Write test data if exists
        if submission_id in test_map:
            with open(os.path.join(student_folder, f"{submission_id}_tests.txt"), "w", encoding="utf-8") as f:
                f.write(test_map[submission_id])
        else:
            with open(os.path.join(student_folder, f"{submission_id}_tests.txt"), "w", encoding="utf-8") as f:
                f.write("NO TESTS FOUND")
            
        name_file_path = os.path.join(student_folder, f"{submission_id}_name.txt")
        with open(name_file_path, "w", encoding="utf-8") as f:
            if submission_id in name_map:
                f.write(f"{name_map[submission_id]['First Name']} {name_map[submission_id]['Last Name']}")
            else:
                f.write("NO NAME FOUND")

        # Write code if exists
        if submission_id in code_map:
            with open(os.path.join(student_folder, f"{submission_id}_code.txt"), "w", encoding="utf-8") as f:
                f.write(code_map[submission_id])
        else:
            with open(os.path.join(student_folder, f"{submission_id}_code.txt"), "w", encoding="utf-8") as f:
                f.write("NO CODE FOUND")

def read_files_in_folder(start_path):

    id_map_to_submission = dict()

    code_map_to_submission = dict()

    test_map_to_submission = dict()

    for root, dirs, files in os.walk(start_path):
        for file in files:
                file_path = os.path.join(root, file)

                submission_match = re.search(submission_pattern, file_path)

                if submission_match:
                    cur_submission_name = submission_match.group(0)
                    just_id_match = re.search("\d+", cur_submission_name[1:len(cur_submission_name) - 1])
                    
                    submission_id = just_id_match.group(0)

                    # print(submission_id)
                else:
                    submission_id = None
                if file_path.endswith('.docx') and '__MACOSX' not in file_path and ('report' in file.lower() or 'documentation' in file.lower()) and '__MACOSX' not in file.lower():
                    # print(f'Reading DOCX file: {file_path}')
                    content = read_docx(file_path)

                    if submission_id is not None:
                        id_map_to_submission[submission_id] = content

                elif file_path.endswith('.pdf') and '__MACOSX' not in file_path and ('report' in file.lower() or 'documentation' in file.lower()) and '__MACOSX' not in file.lower():
                    # print(f'Reading PDF file: {file_path}')
                    content = read_pdf(file_path)
                    
                    if submission_id is not None:
                        id_map_to_submission[submission_id] = content

                elif file_path.find('test.cpp') != -1 and '__MACOSX' not in file_path:


                    if submission_id is not None:
                        
                        test = open(file_path, "rb").read()

                        try:
                            test_map_to_submission[submission_id] = test.decode()
                        except Exception as e:
                            if file_path.endswith('.pdf'):
                                test = read_pdf(file_path)
                                test_map_to_submission[submission_id] = test
                            else:
                                print(file_path)

                elif (file_path.endswith('.cpp') or file_path.endswith('.h')) and '__MACOSX' not in file_path:

                    if submission_id is not None:

                        code = open(file_path, "rb").read()

                        local_file_name = os.path.basename(file_path)


                        if submission_id not in code_map_to_submission:
                            try: 
                                code_map_to_submission[submission_id] = "CUR FILE == " + local_file_name + "\n" + code.decode() + "\n"
                            except:
                                print(file_path)
                        else:
                            try:
                                code_map_to_submission[submission_id] += "CUR FILE == " + local_file_name + "\n" + code.decode() + "\n"
                            except:
                                print(file_path)

    # print(test_map_to_submission)

    return id_map_to_submission, test_map_to_submission, code_map_to_submission

def process_report_names(filename='2_Report_Test_Cases.csv'):
    # Open the CSV file for reading
    with open(filename, mode='r', encoding='utf-8') as file:
        # Use csv.DictReader to read the file
        reader = csv.DictReader(file)
        
        # Initialize a dictionary to hold our processed data
        processed_data = {}
        
        # Iterate over each row in the CSV
        for row in reader:
            # Use Assignment Submission ID as the unique identifier for each report
            submission_id = row['Assignment Submission ID']
            
            # Initialize a dictionary for this submission if not already present
            if submission_id not in processed_data:
                processed_data[submission_id] = {
                    'First Name': row['First Name'],
                    'Last Name': row['Last Name']
                }
                
        return processed_data


def process_report_test_cases(filename='2_Report_Test_Cases.csv'):
    # Open the CSV file for reading
    with open(filename, mode='r', encoding='utf-8') as file:
        # Use csv.DictReader to read the file
        reader = csv.DictReader(file)
        
        # Initialize a dictionary to hold our processed data
        processed_data = {}
        
        # Iterate over each row in the CSV
        for row in reader:
            # Use Assignment Submission ID as the unique identifier for each report
            submission_id = row['Assignment Submission ID']
            
            # Initialize a dictionary for this submission if not already present
            if submission_id not in processed_data:
                processed_data[submission_id] = {'TRUE': [], 'FALSE': [], 'Score': row['Score']}
            
            # Iterate through each column in the row to find TRUE/FALSE values
            for column, value in row.items():
                # Check if the column is related to a TRUE/FALSE value
                if value == 'true':
                    processed_data[submission_id]['TRUE'].append(column)
                elif value == 'false':
                    processed_data[submission_id]['FALSE'].append(column)
                # Note: This assumes that the TRUE/FALSE values are exactly 'true'/'false'
                # Adjust the condition based on the actual content of your CSV file

    return processed_data

# Example usage
#report_data = process_report_test_cases()
#for submission_id, details in report_data.items():
#    print(f"Submission ID: {submission_id}, Details: {details}")
#    break

report_names = process_report_names('2_Report_Test_Cases.csv')

id_map, test_map, code_map = read_files_in_folder('submissions/assignment_3866728_export')
write_to_student_folders("./cleaned_stuff", id_map, test_map, code_map, report_names)