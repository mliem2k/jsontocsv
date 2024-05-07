import pandas as pd

# Load CSV files into DataFrames
df1 = pd.read_csv('b.csv')  # Replace with your first CSV file
df2 = pd.read_csv('merged_file.csv')  # Replace with your second CSV file

# Merge DataFrames with a full outer join
# This keeps all keys from both DataFrames
merged_df = pd.merge(df1, df2, how='outer', on='ITEM#')

# Use df1 values when keys (columns) are the same
# This overwrites values from df2 with those from df1 when there's a conflict
# for col in merged_df.columns:
#     if col in df1.columns:
#         if col in df2.columns:
#             merged_df[col] = df2[col].combine_first(df1[col])
#         else:
#             merged_df[col] = df1[col]
#     elif col in df2.columns:
#         merged_df[col] = df2[col]

# Save or return the merged DataFrame
merged_df.to_csv('merged_file.csv', index=False)
