from flask import Flask
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

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

COLLECTION_NAME = "project_2_rag_collection"
collection = db[COLLECTION_NAME]

documents = [
    {
        "student_id": 1,
        "code": 'cout << "helloWorld" << endl;',
        "feedback": "wow, amazing code. well done",
        "report": "look at my beautiful code, and please give me a good score",
        "tests": 'should print "hello world"',
        "embedding": "wtf is this",
        "report": "myReport",
        "assignment": "The Assignment",
    },
    {
        "student_id": 2,
        "code": 'cout << "helloWorld" << endl;',
        "feedback": "wow, amazing code. well done",
        "report": "look at my beautiful code, and please give me a good score",
        "tests": 'should print "hello world"',
        "embedding": "wtf is this",
        "report": "myReport",
        "assignment": "The Assignment",
    },
    {
        "student_id": 3,
        "code": 'cout << "helloWorld" << endl;',
        "feedback": "wow, amazing code. well done",
        "report": "look at my beautiful code, and please give me a good score",
        "tests": 'should print "hello world"',
        "embedding": "wtf is this",
        "report": "myReport",
        "assignment": "The Assignment",
    },
]
# Insert data points into the collection
result = collection.insert_many(documents)

# Print the IDs of the inserted documents
print('IDs of the inserted documents:', result.inserted_ids)
for data_point in documents:
     print(data_point["name"])
