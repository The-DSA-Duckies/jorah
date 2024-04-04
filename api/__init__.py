from flask import Flask
from flask import request
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from bson.json_util import dumps
import os
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
# print(MONGO_USERNAME, " AH ", MONGO_PASSWORD)

uri = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@autograder.4e6iu9n.mongodb.net/?retryWrites=true&w=majority&appName=Autograder"

client = MongoClient(uri)

DB_NAME = "test_database"
db = client[DB_NAME]

COLLECTION_NAME = "project_2_rag_collection"
# COLLECTION_NAME = "newCollection"
collection = db[COLLECTION_NAME]


@app.route("/")
def ping():
    try:
        client.admin.command("ping")
        print("Pinged deployment, heartbeat is alive")
    except Exception as e:
        print(e)

    return {"message": "API is healthy"}


@app.route("/assignments", methods=["GET", "POST"])
def assignments():
    # TODO: Get request needs method to get single assignment

    if request.method == "GET":
        """Find all assignment documents"""
        query = {"assignment_name": {"$exists": True}}
        results = collection.find(query)
        return dumps(results)

    if request.method == "POST":
        """insert new assignment"""

        # form document to insert
        # TODO: This should also have information such as mean/median/num students/min/max/std deviation
        document = {
            "assignment_id": 1,
            "assignment_name": request.form["assignment_name"],
            "assignment": "Here is where assignment description will go",
            "student_names": ["Jeremy Roach", "Jack May"],
        }

        result = collection.insert(document)
        print(result)
        return dumps(document)


@app.route("/submissions", methods=["GET", "PUT"])
def submissions():
    if request.method == "GET":
        """Find single document with request student id"""
        query = {"student_id": int(request.args["student_id"])}
        results = collection.find(query)
        return dumps(results)

    if request.method == "PUT":
        """Update student submission with new feedback and grade"""
        query = {"student_id": int(request.args["student_id"])}
        update = {
            "$set": {
                "editedFeedback": request.json["feedback"],
                "editedGrade": request.json["grade"],
            }
        }
        results = collection.update(query, update)
        return {"message": "API Received PUT request"}
