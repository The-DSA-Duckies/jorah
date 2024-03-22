
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import torch
from torch import Tensor
from transformers import AutoTokenizer, AutoModel
import torch.nn.functional as F

load_dotenv()

DB_NAME = 'test_database'

def last_token_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
    if left_padding:
        return last_hidden_states[:, -1]
    else:
        sequence_lengths = attention_mask.sum(dim=1) - 1
        batch_size = last_hidden_states.shape[0]
        return last_hidden_states[torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths]

tokenizer = AutoTokenizer.from_pretrained('Salesforce/SFR-Embedding-Mistral')
model = AutoModel.from_pretrained('Salesforce/SFR-Embedding-Mistral')
def get_embedding(text):
    # Load model and tokenizer

    # Prepare the text for the model
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=4096)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Extract and normalize the embedding of the last token
    embedding = last_token_pool(outputs.last_hidden_state, inputs['attention_mask'])
    embedding = F.normalize(embedding, p=2, dim=1)
    
    return embedding.squeeze().cpu().numpy()



def extract_student_data(base_path):
    # Dictionary to hold all extracted information
    extracted_info = {}
    
    # Check if the path exists to avoid errors
    if not os.path.exists(base_path):
        print(f"The specified path does not exist: {base_path}")
        return
    
    # Iterate over each folder in the base directory
    for folder_name in os.listdir(base_path):
        student_folder_path = os.path.join(base_path, folder_name)
        
        # Skip any files to ensure we're only dealing with directories
        if not os.path.isdir(student_folder_path):
            continue
        
        # Initialize a dictionary for this student's data
        student_data = {'feedback': '', 'code': '', 'report': '', 'tests': ''}
        
        # Iterate over files within the student's folder
        for file_name in os.listdir(student_folder_path):
            file_path = os.path.join(student_folder_path, file_name)
            
            # Determine the type of file and read its content
            if file_name.endswith('_feedback.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    student_data['feedback'] = file.read()
            elif file_name.endswith('_code.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    student_data['code'] = file.read()
            elif file_name.endswith('_report.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    student_data['report'] = file.read()
            elif file_name.endswith('_tests.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    student_data['tests'] = file.read()
        
        # Use the folder name as the student ID and add to extracted_info
        extracted_info[folder_name] = student_data
    
    return extracted_info

def save_embedding_to_file(base_path, student_id, embedding):
    # Construct the path to the student's folder
    student_folder_path = os.path.join(base_path, student_id)
    
    # Ensure the folder exists
    if not os.path.isdir(student_folder_path):
        print(f"Folder for student ID {student_id} does not exist.")
        return
    
    # Construct the full path for the embedding file
    embedding_file_path = os.path.join(student_folder_path, f"{student_id}_embedding.txt")
    
    # Convert the embedding to a string format (e.g., comma-separated values)
    embedding_str = ", ".join(map(str, embedding))
    
    # Write the embedding to a file
    with open(embedding_file_path, 'w', encoding='utf-8') as file:
        file.write(embedding_str)
    print(f"Saved embedding for student ID {student_id} at {embedding_file_path}")

# Example usage
if __name__ == "__main__":
    base_path = './cleaned_stuff'  # Update this path to your directory's path
    data = extract_student_data(base_path)
    with open("./rubric.txt", 'r', encoding='utf-8') as file:
        rubric = file.read()
    
    for student_id, student_data in data.items():
        # Concatenate the text components for each student
        student_folder_path = os.path.join(base_path, student_id)
        embedding_file_path = os.path.join(student_folder_path, f"{student_id}_embedding.txt")

        if not os.path.exists(embedding_file_path):
            text_to_embed = rubric + "\n" + student_data['report'] + "\n" + student_data['tests'] + "\n" + student_data['code']
            try:
                embedding = get_embedding(text_to_embed)
                print("not weird")
            except Exception as e:
                print("weird")
        

        save_embedding_to_file(base_path, student_id, embedding)    


