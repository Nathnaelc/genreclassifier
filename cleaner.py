# Purpose: Clean the combined CSV file by removing duplicates and handling missing values.
import pandas as pd

# Load the combined CSV
df = pd.read_csv('combined_csv.csv')

# Remove duplicates based on trackId to ensure uniqueness
df = df.drop_duplicates(subset='trackId')

# Check for and handle missing values. Here I'm dropping rows with any missing information.
df = df.dropna()

# Save the cleaned CSV
df.to_csv('cleaned_combined_csv.csv',
          index=False)
