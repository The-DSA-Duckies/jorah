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