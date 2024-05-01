import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('data/data_pcb/data_pcb_three/rr_three.csv')

# Define the column you want to modify
column_name1 = 'Letter'
# column_name2 = 'Index1'
# column_name3 = 'Middle1'
# column_name4 = 'Ring1'
# column_name5 = 'Pinky1'

# Replace values above 0.8 with 0.25 in the specified column
# df[column_name1] = df[column_name1].apply(lambda x: 0.25 if x > 0.8 else x)
# df[column_name2] = df[column_name2].apply(lambda x: 0.5 if x > 0.8 else x)
# df[column_name3] = df[column_name3].apply(lambda x: 0.25 if x > 0.8 else x)
# df[column_name4] = df[column_name4].apply(lambda x: 0.25 if x > 0.8 else x)
# df[column_name5] = df[column_name5].apply(lambda x: 0.25 if x > 0.8 else x)
df['Letter'] = df['Letter'].replace(10, 2)

# Save the modified DataFrame to a new CSV file
df.to_csv('data/data_pcb/data_pcb_three/rr_three.csv', index=False)
