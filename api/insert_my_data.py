from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = 'test_database'

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uri = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@autograder.4e6iu9n.mongodb.net/?retryWrites=true&w=majority&appName=Autograder"

client = MongoClient(uri)

openai.api_key = OPENAI_API_KEY

def generate_embedding(text):
    response = openai.Embedding.create(
      input=text,
      model="text-embedding-3-large"
    )
    return response['data'][0]['embedding']

def insert_document(student_id, code, feedback, report, tests):
    embedding = generate_embedding(feedback)  # Generate embedding for the feedback text
    document = {
        "student_id": student_id,
        "code": code,
        "feedback": feedback,
        "report": report,
        "tests": tests,
        "embedding": embedding
    }
    result = collection.insert_one(document)
    print(f"Inserted document with ID: {result.inserted_id}")

def process_files(folder_path):
    for file_path in glob.glob(f"{folder_path}/*_filetype.txt"):
        student_id = os.path.basename(file_path).split('_')[0]
        # Read the file content and split it into parts
        # This is a placeholder, adjust the logic based on your file format
        with open(file_path, 'r') as file:
            content = file.read()
            code, feedback, report, tests = content.split('\n\n')  # Example split, adjust as needed
        insert_document(student_id, code, feedback, report, tests)

if __name__ == "__main__":
    folder_path = 'cleaned_stuff'
    process_files(folder_path)


# Select the database
db = client[DB_NAME]

# Define the collection (table) name
collection_name = 'newCollection'

# Select the collection. If it doesn't exist, it will be created when the first document is inserted.
collection = db[collection_name]

# Data points to insert
data_points = [
    {"name": "John Doe", "age": 30, "city": "New York"},
    {"name": "Jane Doe", "age": 25, "city": "Chicago"},
    {"name": "Jim Beam", "age": 35, "city": "San Francisco"}
]

# Insert data points into the collection
# result = collection.insert_many(data_points)

# Print the IDs of the inserted documents
# print('IDs of the inserted documents:', result.inserted_ids)
for data_point in data_points:
    print(data_point["name"])
