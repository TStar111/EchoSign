import pandas as pd

# Load the CSV file
data = pd.read_csv('../data/dataset_single/dataset_single_test.csv')

# Replace all occurrences of label 10 in the final column with 9
data['Letter'] = data['Letter'].replace(10, 9)

# Save the modified DataFrame back to a CSV file
data.to_csv('../data/dataset_single/dataset_single_test.csv', index=False)
