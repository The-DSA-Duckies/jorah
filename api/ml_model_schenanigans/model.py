import os
import time

import modal
import csv

from modal import Image, Stub, wsgi_app

from concurrent.futures import ThreadPoolExecutor


bot_image = modal.Image.debian_slim().pip_install("openai")
bot_image = bot_image.pip_install("numpy")
bot_image = bot_image.pip_install("pandas")
bot_image = bot_image.pip_install("youtube_transcript_api")
bot_image = bot_image.pip_install("flask")
bot_image = bot_image.pip_install("flask_cors")
bot_image = bot_image.pip_install("anthropic")
bot_image = bot_image.pip_install("pymongo")
bot_image = bot_image.pip_install("python-dotenv")



stub = modal.Stub("GPT wins 😔", image=bot_image)

@stub.function(secret=modal.Secret.from_name("my-openai-secret"))
def complete_text_gpt(prompt):
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613", # note, test this with gpt-4 for quality improvements
        messages=[
            {"role": "system", "content": "You are an instructor who is very good at grading."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content

@stub.function(secret=modal.Secret.from_name("my-openai-secret"))
def complete_text_gpt_4(prompt):
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-0125-preview", # note, this should be completely deprecated in the future for anthropic haiku, but they day limited me
        messages=[
            {"role": "system", "content": "You are an instructor who is very good at grading."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content


@stub.function(secret=modal.Secret.from_name("my-anthropic-secret"))
def complete_text_anthropic(prompt):
    import anthropic
    
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=4096,
        temperature=0.0,
        system="You are an instructor who is very good at grading.",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )

    return message.content[0].text

def perform_operations():
    pass

def database_sync():
    pass


def iterate_through_all_submissions_in_a_batch(base_path):
    data = {}
    
    # Iterate through each folder in the base_path
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            # Initialize dictionary to hold the content of code, report, and tests
            student_data = {'code': None, 'report': None, 'tests': None, 'embedding': None}
            
            # Iterate through files in the folder
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    if file_name.endswith('_code.txt'):
                        with open(file_path, 'r', encoding='utf-8') as file:
                            student_data['code'] = file.read()
                    elif file_name.endswith('_report.txt'):
                        with open(file_path, 'r', encoding='utf-8') as file:
                            student_data['report'] = file.read()
                    elif file_name.endswith('_tests.txt'):
                        with open(file_path, 'r', encoding='utf-8') as file:
                            print("here")
                            student_data['tests'] = file.read()
                    elif file_name.endswith('_embedding.txt'):
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.read()
                            embeddings = content.strip().split(',')
                            embedding = [float(e) for e in embeddings]
                            student_data['embedding'] = embedding
            
            # Store the read data in the main dictionary with the folder name as key
            data[folder_name] = student_data

    return data

# iterate_through_all_submissions_in_a_batch("./cleaned_stuff")

def get_feedback_from_file(client, db_name, collection_name, embedding):
    db = client[db_name]
    collection = db[collection_name]


    response = collection.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": embedding,
                "numCandidates": 540,
                "limit": 1
            }
        }
    ])

    # Extract feedback
    feedback = [doc['feedback'] for doc in response if 'feedback' in doc]

    return feedback




def massive_data_mapping(file_name):

    student_feedback = {}

    rubric_mapping = {
    "**Graph representation**: Graph represented as a Adjacency List": "Graph representation: Graph represented as an Adjacency List - 0 pts",
    "**Graph representation**: Graph represented as an Adjacency Matrix": "Graph representation: Graph represented as an Adjacency Matrix - 25 pts",
    "**Describe the data structure** you used to implement the graph and **why**? : described and justified": "Describe the data structure you used to implement the graph and why?: Described and justified - 0 pts",
    "**Describe the data structure** you used to implement the graph and **why**? : missing description and justification": "Describe the data structure you used to implement the graph and why?: Missing description and justification - 2.5 pts",
    "**Describe the data structure** you used to implement the graph and **why**? : missing justification": "Describe the data structure you used to implement the graph and why?: Missing justification - 1.5 pts",
    "**Describe the data structure** you used to implement the graph and **why**? : Incorrect information in justification": "Describe the data structure you used to implement the graph and why?: Incorrect information in justification - 1.5 pts",
    "**Describe the data structure** you used to implement the graph and **why**? : Vague justification": "Describe the data structure you used to implement the graph and why?: Vague justification - 0.5 pts",
    "**Describe the data structure** you used to implement the graph and **why**? : Vague description": "Describe the data structure you used to implement the graph and why?: Vague description - 0.5 pts",
    "**Describe the data structure** you used to implement the graph and **why**? : Vague justification and description": "Describe the data structure you used to implement the graph and why?: Vague justification and description - 1 pt",
    "**Describe the data structure** you used to implement the graph and **why**? : Missing description": "Describe the data structure you used to implement the graph and why?: Missing description - 1.5 pts",
   "**Time complexity analysis** - **Functions** - What is the computational complexity of each method in the worst case? - 1.67 points for correct complexity, 1.67 for describing variables and 1.67 for justification.: Time complexity analysis meets expectations": "Time complexity analysis - Functions: Time complexity analysis meets expectations - 0 pts",
    "**Time complexity analysis** - **Functions** - What is the computational complexity of each method in the worst case? - 1.67 points for correct complexity, 1.67 for describing variables and 1.67 for justification.: missing variables descriptions": "Time complexity analysis - Functions: Missing variables descriptions - 1.67 pts",
    "**Time complexity analysis** - **Functions** - What is the computational complexity of each method in the worst case? - 1.67 points for correct complexity, 1.67 for describing variables and 1.67 for justification.: missing justification": "Time complexity analysis - Functions: Missing justification - 1.67 pts",
    "**Time complexity analysis** - **Functions** - What is the computational complexity of each method in the worst case? - 1.67 points for correct complexity, 1.67 for describing variables and 1.67 for justification.: all complexities missing or incorrect": "Time complexity analysis - Functions: All complexities missing or incorrect - 5 pts",
    "**Time complexity analysis** - **Functions** - What is the computational complexity of each method in the worst case? - 1.67 points for correct complexity, 1.67 for describing variables and 1.67 for justification.: 1 wrong time complexity": "Time complexity analysis - Functions: 1 wrong time complexity - 1.67 pts",
    "**Time complexity analysis** - **Functions** - What is the computational complexity of each method in the worst case? - 1.67 points for correct complexity, 1.67 for describing variables and 1.67 for justification.: 2 wrong time complexities": "Time complexity analysis - Functions: 2 wrong time complexities - 3.34 pts",
    "**Time complexity analysis** - **Functions** - What is the computational complexity of each method in the worst case? - 1.67 points for correct complexity, 1.67 for describing variables and 1.67 for justification.: Complexities can be further simplified": "Time complexity analysis - Functions: Complexities can be further simplified - 1 pt",
    "**Time complexity analysis** - **Main** method - What is the computational complexity of each method in the worst case? - 1.67 points for correct complexity, 1.67 for describing variables and 1.67 for justification. Note that the theoretical minimum is $$ \Omega(pV^2)  $$ or $$ \Omega(pE)  $$: Time complexity analysis meets expectations": "Time complexity analysis meets expectations - 0 pts",
    "**Time complexity analysis** - **Main** method - What is the computational complexity of each method in the worst case? - 1.67 points for correct complexity, 1.67 for describing variables and 1.67 for justification. Note that the theoretical minimum is $$ \Omega(pV^2)  $$ or $$ \Omega(pE)  $$: missing variables descriptions": "Missing variables descriptions - 1.67 pts",
    "**Time complexity analysis** - **Main** method - What is the computational complexity of each method in the worst case? - 1.67 points for correct complexity, 1.67 for describing variables and 1.67 for justification. Note that the theoretical minimum is $$ \Omega(pV^2)  $$ or $$ \Omega(pE)  $$: missing justification": "Missing justification - 1.67 pts",
    "**Time complexity analysis** - **Main** method - What is the computational complexity of each method in the worst case? - 1.67 points for correct complexity, 1.67 for describing variables and 1.67 for justification. Note that the theoretical minimum is $$ \Omega(pV^2)  $$ or $$ \Omega(pE)  $$: complexity incorrect": "Complexity incorrect - 5 pts",
    "**Time complexity analysis** - **Main** method - What is the computational complexity of each method in the worst case? - 1.67 points for correct complexity, 1.67 for describing variables and 1.67 for justification. Note that the theoretical minimum is $$ \Omega(pV^2)  $$ or $$ \Omega(pE)  $$: can be further simplified": "Complexity can be further simplified - 1 pt",
    "**Time complexity analysis** - **Main** method - What is the computational complexity of each method in the worst case? - 1.67 points for correct complexity, 1.67 for describing variables and 1.67 for justification. Note that the theoretical minimum is $$ \Omega(pV^2)  $$ or $$ \Omega(pE)  $$: complexity stated is less than theoretical minimum or does not match the code logic": "Complexity stated is less than theoretical minimum or does not match the code logic - 5 pts",
    "**Time complexity analysis** - **Main** method - What is the computational complexity of each method in the worst case? - 1.67 points for correct complexity, 1.67 for describing variables and 1.67 for justification. Note that the theoretical minimum is $$ \Omega(pV^2)  $$ or $$ \Omega(pE)  $$: Missing main function complexity analysis ": "Missing main function complexity analysis - 5 pts",
    "**Reflection on learning: **What did you learn from this assignment and what would you do differently if you had to start over?: Reflection meets expectations": "Reflection on learning: What did you learn from this assignment and what would you do differently if you had to start over?: Reflection meets expectations - 0 pts",
    "**Reflection on learning: **What did you learn from this assignment and what would you do differently if you had to start over?: Missing reflection ": "Reflection on learning: What did you learn from this assignment and what would you do differently if you had to start over?: Missing reflection - 2.5 pts",
    "**Reflection on learning: **What did you learn from this assignment and what would you do differently if you had to start over?: Reflection too shallow or less than 2 sentences": "Reflection on learning: What did you learn from this assignment and what would you do differently if you had to start over?: Reflection too shallow or less than 2 sentences - 1 pt",
    "**Code Style and Design **: Code quality meets expectations": "Code Style and Design : Code quality meets expectations - 0 pts",
    "**Code Style and Design **: Too few comments": "Code Style and Design: Too few comments - 1 pt",
    "**Code Style and Design **: Program still contains commented out code, could be cleaned up": "Code Style and Design: Program still contains commented out code, could be cleaned up - 1 pt",
    "**Code Style and Design **: inadequate commenting or no comments present in the code": "Code Style and Design: Inadequate commenting or no comments present in the code - 2 pts",
    "**Code Style and Design **: inconsistent whitespace": "Code Style and Design: Inconsistent whitespace - 1 pt",
    "**Code Style and Design **: naming conventions have some room for improvement": "Code Style and Design: Naming conventions have some room for improvement - 1 pt",
    "**Code Style and Design **: naming conventions are inconsistent": "Code Style and Design: Naming conventions are inconsistent - 2 pts",
    "**Code Style and Design **: Code could be slightly more modular": "Code Style and Design: Code could be slightly more modular - 1 pt",
    "**Code Style and Design **: code modularity has room for improvement": "Code Style and Design: Code modularity has room for improvement - 2.5 pts",
    "**Code Style and Design **: No modularization at all. The entire project is completed in the main method.": "Code Style and Design: No modularization at all. The entire project is completed in the main method - 5 pts",
    "**Code Style and Design **: Missing code submission": "Code Style and Design: Missing code submission - 5 pts",
    "**Code Style and Design **: Memory leaks": "Code Style and Design: Memory leaks - 2 pts",
    "**Bonus catch tests**: 5 catch test cases **are provided**": "Bonus catch tests: 5 catch test cases are provided - 0 pts",
    "**Bonus catch tests**: 5 catch test cases **are not provided** ": "Bonus catch tests: 5 catch test cases are not provided - 5 pts",
    "**Bonus catch tests**: only 1 test case provided": "Bonus catch tests: Only 1 test case provided - 4 pts",
    "**Bonus catch tests**: only 2 test cases provided": "Bonus catch tests: Only 2 test cases provided - 3 pts",
    "**Bonus catch tests**: only 3 test cases provided": "Bonus catch tests: Only 3 test cases provided - 2 pts",
    "**Bonus catch tests**: only 4 test cases provided": "Bonus catch tests: Only 4 test cases provided - 1 pt"
}
    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            feedback_list = []
            for key, description in rubric_mapping.items():
                # Ensure the key exists in the row and the value is not None
                if key in row and row[key] is not None:
                    cell_value = row[key].strip().upper()
                    if cell_value == 'TRUE':
                        feedback = description
                    else:
                        # Optionally handle unexpected values
                        continue
                    feedback_list.append(feedback)
            student_feedback[row["Assignment Submission ID"]] = feedback_list

    return student_feedback

def handle_student_submission(assignment, rubric, student_report, student_code, student_test, student_id, embedding, client, DB_NAME, COLLECTION_NAME):
        feedback_file_path = os.path.join("./cleaned_stuff", student_id, student_id + "_" + "feedback.txt")

        if os.path.exists(feedback_file_path):
            return

        student_feedback_similar = get_feedback_from_file(client, DB_NAME, COLLECTION_NAME, embedding)
        rag_feedback_1 = student_feedback_similar[0]
        example_feedback = open("204884010_feedback2.txt", "r").read()
        os.makedirs(os.path.dirname(feedback_file_path), exist_ok=True)


        question = f"""
            Act as a very dilligent teacher's assistant grading a given assignment from the rubric provided. Explain for each decision you make why you
            made it, and why it checks off certain boxes on the rubric.

            Do the grading step by step by going through each part of the ASSIGNMENT, STUDENT REPORT SUBMISSION, STUDENT CODE SUBMISSION, and STUDENT TEST CASES SUBMISSION. The STUDENT REPORT SUBMISSION contains student explanations. The STUDENT CODE SUBMISSION contains the student's code for their project. The STUDENT TEST CASES SUBMISSION contains the test cases the student submitted. Compare your grading step by step to the grading criteria. Use the RUBRIC for each bullet to grade upon. The answer should be formatted as follows in a single text block:

            CRITERIA: [go through each criteria and explain if the student has completed it]

            FEEDBACK: [what did the student do well and what could be improved (but isn't wrong) in plain text]

            FIXING: [Anything that is missing, incorrect or incomplete from the ASSIGNMENT]

            GRADE: [Each breakdown of points lost for missing parts of the rubric with explanation and use EVERY part of the rubric with points shown like x/y where x is points earned, y is points possible for each rubric item.]

            Here follows the assignment, grading criteria and student report submission, student code submission, and student test cases submission. I will also be providing example feedback used for a different student, please read it from EXAMPLE_FORMATTING_FEEDBACK and use the same style of formatting. I also have a 1 previous versions of student feedback provided for this assignment to a student who had a similar submissions labeled EXAMPLE_FEEDBACK. Format everything the same way EXAMPLE_FORMATTING_FEEDBACK and EXAMPLE_FEEDBACK are formatted.

            ASSIGNMENT:
            \"\"\"
            {assignment}
            \"\"\"

            GRADING:
            \"\"\"
            {rubric}
            \"\"\"

            EXAMPLE_FORMATTING_FEEDBACK:
            \"\"\"
            {example_feedback}
            \"\"\"

            EXAMPLE_FEEDBACK:
            \"\"\"
            {rag_feedback_1}
            \"\"\"

            STUDENT REPORT SUBMISSION:
            \"\"\"
            {student_report}
            \"\"\"

            STUDENT CODE SUBMISSION:
            \"\"\"
            {student_code}
            \"\"\"

            STUDENT TEST CASES SUBMISSION:
            \"\"\"
            {student_test}
            \"\"\"


            Please use the deducations from GRADING when appropriate and explain why you are deducting for each of them, also DO NOT MENTION THIS FILE WHEN EXPLAINING. 
            Also remember the score is out of 30 points and if it's negative, please cap it at 0. Also you are not allowed to deduct points for the graph being an adjacency matrix instead of an adjacency list because you are wrong if you see that. Every student submitted an adjacency list representation, and should not lose points on that. 
        """
        try:
            feedback = complete_text_gpt_4.remote(question)
        except Exception as e: 
            try:
                feedback = complete_text_gpt_4.remote(question)
            except:
                try:
                    feedback = complete_text_gpt_4.remote(question)
                except:
                    feedback = "Student did something crazy and overloaded the max tokens, please grade this yourself and apologies."

        os.makedirs(os.path.dirname(feedback_file_path), exist_ok=True)
        with open(feedback_file_path, 'w', encoding='utf-8') as feedback_file:
            feedback_file.write(feedback)
        
            



@stub.local_entrypoint()
def main():
    import time
    from pymongo.mongo_client import MongoClient
    from dotenv import load_dotenv
    import os

    load_dotenv()

    MONGO_USERNAME = os.getenv("MONGO_USERNAME")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    print(MONGO_USERNAME, " AH ", MONGO_PASSWORD)

    uri = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@autograder.4e6iu9n.mongodb.net/?retryWrites=true&w=majority&appName=Autograder"

    client = MongoClient(uri)

    DB_NAME = "test_database"
    COLLECTION_NAME = "project_2_rag_collection"

    assignment = open("assignment.txt", "r").read()
    rubric = open("rubric.txt", "r").read()
    # my_data = massive_data_mapping("2_Report_Test_Cases.csv")

    student_submissions = iterate_through_all_submissions_in_a_batch("./cleaned_stuff")

    # Use ThreadPoolExecutor to handle submissions in parallel
    for student_id, submission in student_submissions.items():
        student_report = submission['report']
        student_code = submission['code']
        student_test = submission['tests']
        embedding = submission['embedding']  # Assuming an embedding key exists or defaulting to an empty list
            # Scheduling the execution and storing the future

        handle_student_submission(assignment, rubric, student_report, student_code, student_test, 
                student_id, embedding, client, DB_NAME, COLLECTION_NAME)
        
        time.sleep(15)