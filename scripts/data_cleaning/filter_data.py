import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('../data/ricky-big.csv')

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
filtered_df.to_csv('../data/ricky-big.csv', index=False)

# import glob
# import pandas as pd

# # Prompt for the directory where the CSV files are located
# directory = "../../data/"

# # Find all CSV files in the directory
# csv_files = glob.glob(directory + '/*.csv')

# # Read all CSV files into a list of Pandas DataFrames
# dfs = [pd.read_csv(file) for file in csv_files]

# for df in dfs:
#     # Apply the filter
#     filtered_df = df[(df.iloc[:, 0] < 2) & (df.iloc[:, 0] > -1) &
#                         (df.iloc[:, 1] < 2) & (df.iloc[:, 1] > -1) &
#                         (df.iloc[:, 2] < 2) & (df.iloc[:, 2] > -1) &
#                         (df.iloc[:, 3] < 2) & (df.iloc[:, 3] > -1) &
#                         (df.iloc[:, 4] < 2) & (df.iloc[:, 4] > -1) &
#                         (df.iloc[:, 14] < 2) & (df.iloc[:, 14] > -1) &
#                         (df.iloc[:, 15] < 2) & (df.iloc[:, 15] > -1) &
#                         (df.iloc[:, 16] < 2) & (df.iloc[:, 16] > -1) &
#                         (df.iloc[:, 17] < 2) & (df.iloc[:, 17] > -1) &
#                         (df.iloc[:, 18] < 2) & (df.iloc[:, 18] > -1)]

#     # Save the filtered DataFrame to a new CSV file
#     filtered_filepath = os.path.join(directory, f"{os.path.splitext(filename)[0]}_filtered.csv")
#     filtered_df.to_csv(filtered_filepath, index=False)
