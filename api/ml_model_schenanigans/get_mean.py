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
                score = row['2: Report/Test Cases (25.0 pts)'] # OK so note to self, I need to go back and check if the grader said test was or wasn't there, and compare to if test.cpp was NOT FOUND and remove those. Then, see only that data

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

def read_csv_for_conditions(csv_filename):
    conditions = set()
    try:
        with open(csv_filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Assume we have a column 'Submission ID' and 'Catch tests: 5 catch test cases are provided'
                submission_id = row['Assignment Submission ID']
                catch_tests_provided = row['**Catch tests**: 5 catch test cases **are provided**']

                if catch_tests_provided == 'TRUE':
                    conditions.add(submission_id)
    except FileNotFoundError:
        print(f"CSV file {csv_filename} was not found.")
    except Exception as e:
        print(f"An error occurred while reading {csv_filename}: {e}")
    return conditions


def clean_submission_files(directory):
    file_ids = set()
    for direc in os.listdir(directory):
        for filename in os.listdir(os.path.join(directory, direc)):
            if filename.endswith("_feedback.txt"):
                path = os.path.join(directory, direc, filename)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if "Bonus catch tests: 5/5 pts deducted" in content or "(bonus points not earned)" in content or "[Missing Bonus Points]" in content or "did not submit Catch test cases" in content or "Include test case" in content or "Bonus catch tests [5 pts deducted]" in content or "5 points are deducted for not providing functioning Catch2 tests" in content or "commented out" in content or "No test cases" in content or "no bonus points" in content or "did not provide the" in content or "The student provided catch test cases, but could not be evaluated due to submission formatting" in content or "**Bonus catch tests [5/5 pts deducted]:**" in content or "Bonus catch tests [5/5 pts deducted]" in content:
                        file_ids.add(filename.split('_')[0])
    return file_ids


def test_case_failures():
    set_1 = clean_submission_files('./cleaned_stuff')
    set_2 = read_csv_for_conditions('2_Report_Test_Cases.csv')
    set_3 = set()
    for element in set_2:
        if element in set_1:
            set_3.add(element)
    return set_3

def filter_keys_from_first_map(map1, map2):
    # Create a list of keys to remove from map1
    keys_to_remove = [key for key in map1 if key not in map2]
    
    # Remove these keys from map1
    for key in keys_to_remove:
        del map1[key]
    
    for key in test_case_failures():
        if key in map1:
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

def filter_and_align(scores, grades):
    paired_data = []

    # Ensure only common keys are retained and sorted for direct comparison
    common_keys = scores.keys() & grades.keys()

    for key in common_keys:
        if scores[key] is not None and grades[key] is not None:
            paired_data.append((key, float(scores[key]), float(grades[key])))

    return paired_data

paired_data = filter_and_align(scores, grades)

# Sort the data by TA grades (2nd element in each tuple), descending
sorted_paired_data = sorted(paired_data, key=lambda x: x[1], reverse=True)

# Unzip the sorted data
_, filtered_ta_reports, filtered_autograder_normalized = zip(*sorted_paired_data)


import matplotlib.pyplot as plt

# Assuming you have the following data lists:
# predicted_grades = list(resulting_map.values())

_, ta_reports, autograder_normalized = zip(*sorted_paired_data)
# ta_reports = [float(score) for score in scores.values() if score != None]
# autograder_normalized = [float(grade) for grade in grades.values() if grade != None] 

data = [ta_reports, autograder_normalized]

plt.figure(figsize=(10, 6))
plt.boxplot(data, labels=['TA Grades', 'Autograder Grades (Normalized)'])

plt.title('Distribution of Grades Over Methods')
plt.ylabel('Grade Value')
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

plt.show()

# Data
# ta_reports = [float(score) for score in scores.values() if score is not None]
# autograder_normalized = [float(grade) for grade in grades.values() if grade is not None]

# Plot
plt.figure(figsize=(12, 6))
plt.hist([ta_reports, autograder_normalized], bins=20, alpha=0.7, label=['TA Grades', 'Autograder Grades (Normalized)'])
plt.title('Histogram of Grades')
plt.xlabel('Grade Value')
plt.ylabel('Frequency')
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.show()


min_length = min(len(ta_reports), len(autograder_normalized))
paired_ta_reports = ta_reports[:min_length]
paired_autograder_normalized = autograder_normalized[:min_length]

# Plot


# Assuming that both lists are of the same length or have been adjusted to match
# If they are not, you would need to align them by some criterion (e.g., student ID).
min_length = min(len(ta_reports), len(autograder_normalized))
paired_ta_reports = ta_reports[:min_length]
paired_autograder_normalized = autograder_normalized[:min_length]

# Plot
min_length = min(len(ta_reports), len(autograder_normalized))
paired_ta_reports = ta_reports[:min_length]
paired_autograder_normalized = autograder_normalized[:min_length]

# Data points
x = list(range(min_length))  # Just a range of indices for positioning on the x-axis

paired_ta_reports = ta_reports
paired_autograder_normalized = autograder_normalized

# paired_ta_reports.sort()

# autograde_matching_students = []

#for student in paired_ta_reports:
#    autograde_matching_students = paired_autograder_normalized[student]
#paired_autograder_normalized.sort()
# Plot
plt.figure(figsize=(10, 6))
plt.scatter(x, paired_ta_reports, color='red', label='TA Grades', alpha=0.7)
plt.scatter(x, paired_autograder_normalized, color='blue', label='Autograder Grades (Normalized)', alpha=0.7)
plt.title('Comparison of TA Grades vs. Autograder Grades')
plt.xlabel('Lowest to highest graded student by TA')
plt.ylabel('Grades')
plt.legend()
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.show()
