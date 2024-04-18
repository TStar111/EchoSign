import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('data/dataset_double_word/somya-what.csv')

# Create a new DataFrame to store the combined data
combined_df = pd.DataFrame()

# Iterate over the rows of the original DataFrame
for i in range(4, len(df)):
    # Combine the current row, the previous row, and the row two steps back into one row
    combined_row = pd.concat([df.iloc[i-4][:-1], df.iloc[i-3][:-1], df.iloc[i-2][:-1], df.iloc[i-1][:-1], df.iloc[i]], ignore_index=True)
    # Append the combined row to the new DataFrame
    combined_df = combined_df._append(combined_row, ignore_index=True)

# Save the new dataset to a CSV file
combined_df.iloc[:, -1] = combined_df.iloc[:, -1].astype(int)
combined_df.to_csv('data/data_double_time/somya-what.csv', index=False)
