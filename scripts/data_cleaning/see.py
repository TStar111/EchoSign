import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("data/data_pcb/rr_comp.csv")

# Count the occurrences of each unique value in the "Letter" column
letter_counts = df["Letter"].value_counts().sort_index()

print(letter_counts)
