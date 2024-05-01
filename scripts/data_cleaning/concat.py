import pandas as pd
import glob

# Prompt for the directory where the CSV files are located
# Change this to suit your needs
directory = "data/data_pcb"

# Find all CSV files in the directory
csv_files = glob.glob(directory + '/*.csv')

# Read all CSV files into a list of Pandas DataFrames
dfs = [pd.read_csv(file) for file in csv_files]

# Concatenate all DataFrames vertically
combined_df = pd.concat(dfs, ignore_index=True)

# Write the combined DataFrame to a new CSV file
# Change this to suit your needs
combined_df.to_csv('data/data_pcb/rr_compv3.csv', index=False)

print("CSV files combined successfully!")
