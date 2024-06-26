from flask import Flask
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
import re

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
print(MONGO_USERNAME, " AH ", MONGO_PASSWORD)

uri = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@autograder.4e6iu9n.mongodb.net/?retryWrites=true&w=majority&appName=Autograder"

client = MongoClient(uri)

DB_NAME = "test_database"
db = client[DB_NAME]

COLLECTION_NAME = "project_2_prod_feedback"
collection = db[COLLECTION_NAME]

collection.delete_many({})

documents = []

with open('rubric.txt', 'r') as rubric_file:
    rubric_content = rubric_file.read()
with open('assignment.txt', 'r') as assignment_file:
    assignment_content = assignment_file.read()

student_folders_path = './cleaned_stuff'

for student_folder in os.listdir(student_folders_path):
    folder_path = os.path.join(student_folders_path, student_folder)
    if os.path.isdir(folder_path):
        # Initialize a document for the student
        document = {
            "student_id": int(student_folder),  # Assuming folder names are student IDs
            "assignment": assignment_content,
            "rubric": rubric_content
        }

        # Iterate through each file in the student's folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # Determine the type of file and assign the content appropriately
                if 'code' in file_name:
                    document['code'] = content
                elif 'test' in file_name:
                    document['tests'] = content
                elif 'feedback' in file_name:
                    document['feedback'] = content
                    start = content.find("Score: ") + 7  # +7 to skip the length of "Score: "
                    try:
                        match = re.search(r"Score: (\d+(\.\d+)?)", content)
                        original_score = match.group(1)
                        document['grade'] = float(original_score)
                    except:
                        try:
                            match = re.search(r"score: (\d+(\.\d+)?)", content)
                            original_score = match.group(1)
                            document['grade'] = float(original_score)
                        except: 
                            end = content.rfind("//")  # Assuming the score is always followed by a semicolon
                            original_score = content[start:end]
                            try:
                                points = float(original_score)
                                document['grade'] = points
                            except:
                                try:
                                    end = len(content) - 1
                                    original_score = content[start:end]
                                    original_score = ''.join(original_score.split())
                                    points = float(original_score)
                                    document['grade'] = points
                                except:
                                    document['grade'] = None
                    if document['grade'] != None:
                        with open(student_folder + "_grade.txt", 'w') as file:
                            file.write(str(document['grade']))
                    

                elif 'report' in file_name:
                    document['report'] = content
                elif 'embedding' in file_name:
                    embeddings = content.strip().split(',')
                    # Convert each embedding from string to float (or the appropriate data type)
                    document['embedding'] = [float(e) for e in embeddings]
                elif 'studentid_ta' in file_name:
                    document['studentid_ta'] = content
                # Add more conditions as needed for other file types

        student_id = int(student_folder)
        # The $set operator replaces the value of a field with the specified value
        update_document = {"$set": document}
        
        # Update the document for the given student_id, or insert if it doesn't exist
        # result = collection.update_one({"student_id": student_id}, update_document, upsert=True)
        
        # Optional: print information about the update result
        #if result.matched_count:
        #    pass
        #elif result.upserted_id:
        #    print(f"Inserted new document with _id {result.upserted_id} for student_id {student_id}.")
