import os

import csv

from statistics import mean

import nltk
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
 
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


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

        words = {word for word in words if word not in stop_words}

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

        words_llm = {word for word in words_llm if word not in stop_words}

        words_gradescope = {word for word in words_gradescope if word not in stop_words}


        # Count how many words in map_gradescope are present in map_llm
        common_words = words_gradescope & words_llm
        common_word_count[key] = len(common_words)

    return common_word_count


def result_map(map_llm, map_gradescope):
    resulting_map = dict()
    for key in map_llm.keys() & map_gradescope.keys():

        words_llm = map_llm[key].lower()

        words_gradescope = map_gradescope[key].lower()

        for word in common_words:
            words_llm = words_llm.replace(word, "")
            words_gradescope = words_gradescope.replace(word, "")

        resulting_map[key] = my_cosine_similarity(words_llm, words_gradescope)

    return resulting_map

def my_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    # Convert the text to vectors
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Calculate the cosine similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return similarity

    # print(f"Cosine similarity: {similarity[0][0]}")



common_words = count_common_words(map_llm, map_gradescope)

unique_words_in_gradescope = count_unique_words_per_key(map_gradescope)

percentage_map = dict()

for key in common_words.keys():
    percentage_map[key] = common_words[key] / unique_words_in_gradescope[key]

print(mean(percentage_map.values()))


result_map = result_map(map_llm, map_gradescope)
for key in result_map:
    result_map[key] = float(result_map[key])
    
print(mean(result_map.values()))


