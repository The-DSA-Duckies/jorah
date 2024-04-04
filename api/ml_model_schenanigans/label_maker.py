import os

def load_ta_student_pairs(filename):
    ta_student_pairs = {}
    with open(filename, 'r') as file:
        for line in file:
            ta, students = line.strip().split(': ')
            students_list = students.split(', ')
            ta_student_pairs[ta] = students_list
    return ta_student_pairs

ta_student_pairs = load_ta_student_pairs('ta_student_mapping.txt')


ta_range_pairs = {ta: (students[0], students[-1]) for ta, students in ta_student_pairs.items()}

def which_ta(student_name):
    for ta, (start, end) in ta_range_pairs.items():
        if start <= student_name <= end:
            return ta
    return "Student's TA could not be determined based on the provided names."

    

print(which_ta("Bill Nye"))

def iterate_through_all_submissions_in_a_batch(base_path):
    data = {}
    
    # Iterate through each folder in the base_path
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            # Initialize dictionary to hold the content of code, report, and tests
            student_data = {'name': None}
            
            # Iterate through files in the folder
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    if file_name.endswith('_name.txt'):
                        with open(file_path, 'r', encoding='utf-8') as file:
                            student_data['name'] = file.read()

            data[folder_name] = student_data

    return data


            
student_submissions = iterate_through_all_submissions_in_a_batch("./cleaned_stuff")

# Group students by their TA based on the name range
ta_student_groups = {}
for student_id, folder_name in student_submissions.items():
    student_name = student_submissions[student_id]['name']
    ta = which_ta(student_name)
    if ta:
        if ta not in ta_student_groups:
            ta_student_groups[ta] = []
        ta_student_groups[ta].append(student_name)
    else:
        print(f"Could not determine TA for student: {student_name}")

# Sort students within each TA group and assign numbers
for ta, students in ta_student_groups.items():
    students.sort()
    for index, student_name in enumerate(students, start=1):
        print(f"{student_name} is assigned to {ta} as student number {index}.")