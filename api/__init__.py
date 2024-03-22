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

COLLECTION_NAME = "newCollection"
collection = db[COLLECTION_NAME]

documents = [
    {
        "student_id": 1,
        "code": 'cout << "helloWorld" << endl;',
        "feedback": "wow, amazing code. well done",
        "report": "look at my beautiful code, and please give me a good score",
        "tests": 'should print "hello world"',
        "embedding": "wtf is this",
    },
    {
        "student_id": 2,
        "code": 'cout << "helloWorld" << endl;',
        "feedback": "wow, amazing code. well done",
        "report": "look at my beautiful code, and please give me a good score",
        "tests": 'should print "hello world"',
        "embedding": "wtf is this",
    },
    {
        "student_id": 3,
        "code": 'cout << "helloWorld" << endl;',
        "feedback": "wow, amazing code. well done",
        "report": "look at my beautiful code, and please give me a good score",
        "tests": 'should print "hello world"',
        "embedding": "wtf is this",
    },
]


@app.route("/")
def ping():
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return "My First API !!"


@app.route("/dbtest")
def insert_record():
    try:
        result = collection.insert_many(documents)
        print(f"Resulting ids from insertion: {result.inserted_ids}")
    except Exception as e:
        print(e)
    return "Documents inserted into db"


# DB_NAME = 'test_database'

# Select the database
# db = client[DB_NAME]

# Define the collection (table) name
# collection_name = 'newCollection'

# Select the collection. If it doesn't exist, it will be created when the first document is inserted.
# collection = db[collection_name]

# Data points to insert
# data_points = [
#     {"name": "John Doe", "age": 30, "city": "New York"},
#     {"name": "Jane Doe", "age": 25, "city": "Chicago"},
#     {"name": "Jim Beam", "age": 35, "city": "San Francisco"}
# ]

# Insert data points into the collection
# result = collection.insert_many(data_points)

# Print the IDs of the inserted documents
# print('IDs of the inserted documents:', result.inserted_ids)
# for data_point in data_points:
#     print(data_point["name"])
