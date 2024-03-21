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
print(MONGO_USERNAME , " AH " , MONGO_PASSWORD)

uri = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@autograder.4e6iu9n.mongodb.net/?retryWrites=true&w=majority&appName=Autograder"

client = MongoClient(uri)


@app.route("/")
def ping():
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return "My First API !!"
