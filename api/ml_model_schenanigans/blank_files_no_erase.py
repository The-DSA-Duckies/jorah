import os

base_folder = "./cleaned_stuff"  # Adjusted to a hypothetical path for demonstration

# Required file names and their default content if not found
required_files = {
    "_report.txt": "NO REPORT FOUND",
    "_code.txt": "NO CODE FOUND",
    "_tests.txt": "NO TESTS FOUND"
}

# List all directories in the base_folder
directories = [d for d in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, d))]

# Iterate through each directory
for directory in directories:
    folder_path = os.path.join(base_folder, directory)
    # Check and create required files if they do not exist
    for suffix, default_content in required_files.items():
        file_path = os.path.join(folder_path, f"{directory}{suffix}")
        if not os.path.isfile(file_path):  # Check if the file does not exist
            with open(file_path, 'w') as file:
                file.write(default_content) 