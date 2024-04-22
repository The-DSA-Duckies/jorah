import os

import csv

from statistics import mean

def read_csv_for_comments(csv_filename):
    comments = dict()
    try:
        with open(csv_filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Assume we have a column 'Submission ID' and 'Catch tests: 5 catch test cases are provided'
                submission_id = row['Assignment Submission ID']
                comment = row['Comments']
                if len(comment.split(" ")) >= 5:
                    comments[submission_id] = comment
    except FileNotFoundError:
        print(f"CSV file {csv_filename} was not found.")
    except Exception as e:
        print(f"An error occurred while reading {csv_filename}: {e}")
    return comments


def clean_submission_files(directory):
    file_contents = dict()
    for direc in os.listdir(directory):
        for filename in os.listdir(os.path.join(directory, direc)):
            if filename.endswith("_feedback.txt"):
                path = os.path.join(directory, direc, filename)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    file_contents[filename.split('_')[0]] = content

    return file_contents



map_gradescope = read_csv_for_comments('2_Report_Test_Cases.csv')

map_llm = clean_submission_files('./cleaned_stuff')

my_union = set()
for element in map_gradescope.values():
    if element in map_llm.values():
        my_union.add(element)


def filter_keys_from_first_map(map1, map2, union_set):
    # Create a list of keys to remove from map1
    keys_to_remove = [key for key in map1 if key not in map2]
    
    # Remove these keys from map1
    for key in keys_to_remove:
        del map1[key]
    
    for key in union_set:
        if key in map1:
            del map1[key]

filter_keys_from_first_map(map_gradescope, map_llm, my_union)
filter_keys_from_first_map(map_llm, map_gradescope, my_union)

def count_unique_words_per_key(input_map):
    unique_word_count = {}
    
    for key, text in input_map.items():
        # Convert the text to lowercase and split into words
        words = set(text.lower().split())
        # Count the unique words and store it in the dictionary
        unique_word_count[key] = len(words)
    
    return unique_word_count

def count_common_words(map_llm, map_gradescope):
    # Dictionary to store the results
    common_word_count = {}

    # Iterate over the common keys in both dictionaries
    for key in map_llm.keys() & map_gradescope.keys():
        # Split the strings into sets of words
        words_llm = set(map_llm[key].lower().split())
        words_gradescope = set(map_gradescope[key].lower().split())

        # Count how many words in map_gradescope are present in map_llm
        common_words = words_gradescope & words_llm
        common_word_count[key] = len(common_words)

    return common_word_count

common_words = count_common_words(map_llm, map_gradescope)

unique_words_in_gradescope = count_unique_words_per_key(map_gradescope)

percentage_map = dict()

for key in common_words.keys():
    percentage_map[key] = common_words[key] / unique_words_in_gradescope[key]

print(mean(percentage_map.values()))




