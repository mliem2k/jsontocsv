import os
import json
import csv
import re
import nltk
from nltk.corpus import words

# Define the folder containing the JSON files
# folder_path = "./KKTA-CLO GLTF/KKTA-CLO GLTF"
folder_path = "./all"

# Define the CSV file path
csv_file_path = "./frontier.csv"
all_keys = set()

# List to store the extracted data
extracted_data = []

# Download the 'words' corpus if needed
nltk.download("words")

# Create a set of valid English words for quick lookup
english_words = set(words.words())

def keep_only_english_words(text):
    # Find all sequences of alphabetic characters (potential words)
    potential_words = re.findall(r'\b[a-zA-Z]+\b', text)
    
    # Keep only those that are in the English dictionary
    filtered_words = [word for word in potential_words if word.lower() in english_words]
    
    # Join the words with spaces
    cleaned_text = ' '.join(filtered_words)
    return cleaned_text

def replace_non_alpha_with_space(text):
    # Replace all non-alphabetic characters with a space
    text_with_spaces = re.sub(r'[^a-zA-Z]', ' ', text)
    
    # Normalize spaces (replace multiple spaces with a single space)
    # normalized_text = re.sub(r'\s+', ' ', text_with_spaces).strip()  # Strip leading/trailing spaces
    
    return text_with_spaces

# Loop through the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):  # Check if the file is a JSON file
        json_file_path = os.path.join(folder_path, filename)
        # filename_no_extension = os.path.splitext(filename)[0]
        # filename_no_extension = replace_non_alpha_with_space(filename_no_extension)
        # filename_no_extension = keep_only_english_words(filename_no_extension)
        #remove numbers and special chars
        # print(json_file_path)

        # Open and read the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            # print(json_file)
            json_data = json.load(json_file)  # Load the JSON data
            
            for materials in json_data.get("materials", None):
                material_name = materials["name"]
                material_name = replace_non_alpha_with_space(material_name)
                material_name = keep_only_english_words(material_name)
                material_name = ' '.join([word for word in material_name.split() if len(word) > 1])

                if material_name:

                    physical_properties = materials["extensions"]["CLO_materials_fabric_property"]["physicalProperty"]  # Use None if key is not found
                    
                
                    data_entry = {
                        "name": material_name
                    }
                # Extract the physicalProperty value
            
                    all_keys.update(physical_properties.keys())
                    # Append the extracted data to the list
                    # Fill in data for each key found in physicalProperty
                    for key in all_keys:
                        data_entry[key] = physical_properties.get(key, None)  # Fill with None if the key is missing

                    extracted_data.append(data_entry)

# Write the extracted data to a CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Write the header
    # Write the header, with "filename" and all keys found
    headers = ["name"] + list(all_keys)
    csv_writer.writerow(headers)

    # Write the data rows
    for data in extracted_data:
        row = [data.get(header, None) for header in headers]
        csv_writer.writerow(row)
