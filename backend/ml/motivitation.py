import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Read the csv file that contains the answers to the motivation survey
df = pd.read_csv('motivation_answers.csv')

# Define a function that calculates the score based on the question scores and types
def calculate_score(row):
    # Use Q1 value to determine the question type
    if row['Q1'] == 1:
        # The higher the Q3 score, the higher the score
        score = row['Q3'] / max(df['Q3'])
    else:
        # The lower the Q2, Q5, Q6 scores, and the higher the Q3, Q4 scores, the higher the score
        max_q3_q4 = max(row['Q3'], row['Q4'])
        score = (max_q3_q4 - row['Q2'] - row['Q5'] - row['Q6']) / (max_q3_q4 * 3)
    return score

# Calculate the score for each user
df['Score'] = df.apply(calculate_score, axis=1)

# Create a new dataframe that only includes the ID and score columns
new_df = df[['ID', 'Score']]

# Output the new dataframe to a csv file
new_df.to_csv('scores.csv', index=False)
