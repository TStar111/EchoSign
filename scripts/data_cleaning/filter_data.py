import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('../../data/dataset_double/somya-m.csv')

# Filter the DataFrame based on the condition
filtered_df = df[df.iloc[:, 0] < 2]
filtered_df = filtered_df[df.iloc[:, 0] > -1]

filtered_df = filtered_df[df.iloc[:, 1] < 2]
filtered_df = filtered_df[df.iloc[:, 1] > -1]

filtered_df = filtered_df[df.iloc[:, 2] < 2]
filtered_df = filtered_df[df.iloc[:, 2] > -1]

filtered_df = filtered_df[df.iloc[:, 3] < 2]
filtered_df = filtered_df[df.iloc[:, 3] > -1]

filtered_df = filtered_df[df.iloc[:, 4] < 2]
filtered_df = filtered_df[df.iloc[:, 4] > -1]

filtered_df = filtered_df[df.iloc[:, 14] < 2]
filtered_df = filtered_df[df.iloc[:, 14] > -1]

filtered_df = filtered_df[df.iloc[:, 15] < 2]
filtered_df = filtered_df[df.iloc[:, 15] > -1]

filtered_df = filtered_df[df.iloc[:, 16] < 2]
filtered_df = filtered_df[df.iloc[:, 16] > -1]

filtered_df = filtered_df[df.iloc[:, 17] < 2]
filtered_df = filtered_df[df.iloc[:, 17] > -1]

filtered_df = filtered_df[df.iloc[:, 18] < 2]
filtered_df = filtered_df[df.iloc[:, 18] > -1]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('../../data/dataset_double/somya-m.csv', index=False)
