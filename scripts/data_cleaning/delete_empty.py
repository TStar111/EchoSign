import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('../data/dataset_single/dataset_single.csv')

# Remove rows with NaN values (empty cells)
df = df.dropna()

# Write the cleaned DataFrame back to a CSV file
df.to_csv('../data/dataset_single/dataset_single.csv', index=False)
