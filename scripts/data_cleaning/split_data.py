import pandas as pd

# Read the large CSV file into a DataFrame
large_df = pd.read_csv('../data/dataset_single/dataset_single.csv')

# Optional: Shuffle the DataFrame
large_df = large_df.sample(frac=1).reset_index(drop=True)

# Decide on the split ratio (e.g., 80% training, 20% testing)
train_ratio = 0.8
test_ratio = 1 - train_ratio

# Calculate the number of rows for training and testing
train_size = int(train_ratio * len(large_df))
test_size = len(large_df) - train_size

# Split the DataFrame into training and testing sets
train_df = large_df.iloc[:train_size]
test_df = large_df.iloc[train_size:]

# Write the training and testing sets to CSV files
train_df.to_csv('../data/dataset_single/dataset_single_training.csv', index=False)
test_df.to_csv('../data/dataset_single/dataset_single_test.csv', index=False)
