import os

names_list = [

]

# Base folder for creating new folders
base_folder = "./cleaned_stuff"

# Start from label 100
folder_label = 100

# For demonstration purposes, we'll just simulate the creation and show the paths and file contents
# that would be generated.

# Create a list to hold the paths and contents for demonstration
created_files_info = []

for name in names_list:
    folder_path = os.path.join(base_folder, str(folder_label))
    os.makedirs(folder_path, exist_ok=True)  # Create the folder
    
    file_path = os.path.join(folder_path, f"{folder_label}_name.txt")
    with open(file_path, 'w') as file:
        file.write(name)  # Write the name to the file
    
    folder_label += 1 
