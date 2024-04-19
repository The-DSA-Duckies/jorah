import os

import csv

from statistics import mean

def map_submission_scores(filename):
    # Dictionary to store the mapping of Submission ID to Report/Test Cases score
    submission_scores = {}

    # Try to open and read the CSV file
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            # Iterate over each row in the CSV file
            for row in reader:
                # Get the Submission ID and Report/Test Cases score
                submission_id = row['Submission ID']
                score = row['2: Report/Test Cases (25.0 pts)']
                # Map the Submission ID to the score
                submission_scores[submission_id] = score
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return submission_scores

def map_grades_in_directory():
    # Dictionary to store the mapping of student names to grades
    grade_mapping = {}
    
    # Get the current working directory
    current_directory = os.getcwd()
    
    # Loop through each file in the directory
    for filename in os.listdir(current_directory): # + "/with_no_report"
        # Check if the file ends with '_grade.txt'
        if filename.endswith("_grade.txt"):
            # Extract the student name from the filename
            student_name = filename[:-10]  # Removes '_grade.txt' from the end
            
            # Try to open the file and read the grade
            try:
                with open(os.path.join(current_directory, filename), 'r') as file: #+ "/with_no_report"
                    # Read the grade from the file
                    grade = file.read().strip()
                    # Map the student name to the grade
                    grade_mapping[student_name] = grade
            except Exception as e:
                print(f"Error reading from {filename}: {e}")
    
    return grade_mapping

# Call the function and print the resulting mapping
grades = map_grades_in_directory()
# print(grades)

# Example usage
filename = 'Project_2_scores.csv'
scores = map_submission_scores(filename)
# print(scores)

def subtract_maps(map1, map2):
    # Dictionary to store the result of subtraction when keys are present in both
    result = {}

    # Iterate over keys in the first dictionary
    for key in map1:
        if key in map2:
            # Subtract the value in the second dictionary from the first
            result[key] = float(map1[key]) - float(map2[key])

    return result

def filter_keys_from_first_map(map1, map2):
    # Create a list of keys to remove from map1
    keys_to_remove = [key for key in map1 if key not in map2]
    
    # Remove these keys from map1
    for key in keys_to_remove:
        del map1[key]

for key, val in grades.items():
    grades[key] = 5/6 * float(val)

# print(grades)

filter_keys_from_first_map(scores, grades)

filter_keys_from_first_map(grades, scores)

resulting_map = subtract_maps(scores, grades)
print(mean(resulting_map.values()))
print(mean( [float(score) for score in scores.values() if score != None] ))
print(mean(grades.values()))

print(len(resulting_map.values()))


import matplotlib.pyplot as plt

# Assuming you have the following data lists:
# predicted_grades = list(resulting_map.values())
ta_reports = [float(score) for score in scores.values() if score != None]
autograder_normalized = [float(grade) for grade in grades.values() if grade != None] 

data = [ta_reports, autograder_normalized]

plt.figure(figsize=(10, 6))
plt.boxplot(data, labels=['TA Grades', 'Autograder Grades (Normalized)'])

plt.title('Distribution of Grades Over Methods')
plt.ylabel('Grade Value')
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

plt.show()
