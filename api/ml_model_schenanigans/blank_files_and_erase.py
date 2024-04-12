import os

def replace_files_with_studentid(base_path):
    # Iterate through all items in base_path
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        
        # Check if the item is a directory
        if os.path.isdir(folder_path):
            # Paths for existing files to be removed
            scores_file_path = os.path.join(folder_path, '_scores.txt')
            feedback_file_path = os.path.join(folder_path, '_feedback.txt')
            
            # Remove _scores.txt if it exists
            if os.path.exists(scores_file_path):
                os.remove(scores_file_path)
            
            # Remove _feedback.txt if it exists
            if os.path.exists(feedback_file_path):
                os.remove(feedback_file_path)
            
            # Create new files with studentid prefix
            new_scores_file_path = os.path.join(folder_path, f'{folder_name}_scores.txt')
            new_feedback_file_path = os.path.join(folder_path, f'{folder_name}_feedback.txt')
            
            # Creating new files
            with open(new_scores_file_path, 'w') as _:
                pass  # Creates an empty file
            with open(new_feedback_file_path, 'w') as _:
                pass  # Creates an empty file

# Specify the path to the directory containing all the folders
base_path = "./cleaned_stuff"
replace_files_with_studentid(base_path)

print("Old files removed, new files created with student IDs.")