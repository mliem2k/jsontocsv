import json
import csv

# Define the JSON and CSV file paths
json_file_path = "./sisa_fix.json"  # Path to the JSON file with nested data
csv_file_path = "./sisa_flat.csv"  # Output CSV file path

# Function to flatten nested structures (dictionaries and arrays)
def flatten(value, parent_key='', sep='_'):
    """Flatten nested structures into a single level."""
    items = {}
    if isinstance(value, dict):
        for key, sub_value in value.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            items.update(flatten(sub_value, new_key, sep))
    elif isinstance(value, list):
        # Flatten lists by creating index-based keys
        for idx, item in enumerate(value):
            new_key = f"{parent_key}{sep}{idx}" if parent_key else str(idx)
            items.update(flatten(item, new_key, sep))
    else:
        # If not a dict or list, return the current value with its key
        key = parent_key if parent_key else 'value'
        items[key] = value
    return items

# Collect all unique keys for CSV headers
all_keys = set()

# Load and process the JSON data
extracted_data = []
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

    for material in json_data["materials"]:
        name = material["name"]
        physical_property = material["extensions"]["CLO_materials_fabric_property"]["physicalProperty"]

        # Flatten the physical properties
        flattened_physical_property = flatten(physical_property)
        all_keys.update(flattened_physical_property.keys())
        
        # Add the flattened data and the material name to the list
        data = {'name': name, **flattened_physical_property}
        extracted_data.append(data)

# Write the extracted data to a CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Write the headers
    headers = ["name"] + list(sorted(all_keys))  # "name" is the first column, followed by unique property keys
    csv_writer.writerow(headers)
    
    # Write the data rows
    for data in extracted_data:
        row = [data.get(header, None) for header in headers]  # Fill in data for each header, or None if not present
        csv_writer.writerow(row)

print("CSV file generated:", csv_file_path)
