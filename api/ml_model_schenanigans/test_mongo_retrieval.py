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
db = client[DB_NAME]

COLLECTION_NAME = "project_2_rag_collection"
collection = db[COLLECTION_NAME]

student_id = 212408098  # Adjust based on your actual ID field and value
document = collection.find_one({"student_id": student_id})

if document and "embedding" in document:
    # Assuming 'embedding' is the field containing the vector
    query_vec = document["embedding"]
else:
    print(f"No document found with student_id {student_id}, or the document doesn't have an 'embedding' field.")
    query_vec = []  # Default to an empty vector if not found


response = db.project_2_rag_collection.aggregate([
  {
    "$vectorSearch": {
      "index": "vector_index",
      "path": "embedding",
      "queryVector": query_vec,
      "numCandidates": 540,
      "limit": 3
    }
  }
])

for document in response:
    print(document['feedback'])