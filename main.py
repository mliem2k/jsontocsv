import json
import pandas as pd

#load json file
with open('sisa_fix.json') as f:
    data = json.load(f)

# print(len(data["materials"]))

# print(data)

# res = {}
# res["materials"] = data

# print(res)

# store into new json file
# with open('res.json', 'w') as f:
#     json.dump(res, f, indent=4)

# Normalizing the JSON data to flatten nested structures with merged parent keys
df = pd.json_normalize(
    data["materials"],
    sep="/"
)


# Exporting the DataFrame to a CSV file
csv_file = "materials_sisa.csv"
df.to_csv(csv_file, index=False)

# Output the file name
print("CSV file generated:", csv_file)