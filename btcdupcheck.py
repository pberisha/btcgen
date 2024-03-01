#!/usr/bin/env python3
import pandas as pd
import sys

from datetime import datetime

startTime = datetime.now()
print("Starting Dupplicate Checking of index " + sys.argv[3])

csv_dir = sys.argv[1]
real_csv_filename = 'balance.csv'
generated_csv_filename = sys.argv[2]
column_to_check = int(sys.argv[3])

real_csv_path = csv_dir + real_csv_filename
generated_csv_path = generated_csv_filename

output_csv_path = csv_dir + "m" + str(column_to_check) + "_" + generated_csv_filename

# Read the CSV files into pandas DataFrames
df_real = pd.read_csv(real_csv_path)
df_generated = pd.read_csv(generated_csv_path)

# Assuming you're comparing the first column from both CSVs, adjust as needed
r_column_to_compare = df_real.columns[0]
g_column_to_compare = df_generated.columns[column_to_check]

# Perform the string comparison to find matches
# This checks if each element in the generated DataFrame's column is present in the real DataFrame's column
matches = df_generated[g_column_to_compare].isin(df_real[r_column_to_compare])


# Filter the generated DataFrame to only include matched rows
df_matched = df_generated[matches]
print(df_matched)

# Save the matched DataFrame to a new CSV file
df_matched.to_csv(output_csv_path, index=False)

print(f"Matched rows have been saved to: {output_csv_path}")
print(datetime.now() - startTime)

