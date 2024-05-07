import os

# Path to the folder containing your files
# folder_path = "./KKTA-CLO GLTF/KKTA-CLO GLTF"
folder_path = "./frontier"

# Iterate through each file in the folder
for filename in os.listdir(folder_path):
    # If the file has a .gltf extension
    if filename.endswith(".gltf"):
        # Get the new filename by replacing .gltf with .json
        new_filename = filename.replace(".gltf", ".json")
        
        # Get the full path for the old and new filenames
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)
        
        # Rename the file
        os.rename(old_file_path, new_file_path)

print("All .gltf files have been renamed to .json.")
