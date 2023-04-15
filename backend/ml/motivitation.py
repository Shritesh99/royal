import pandas as pd
import csv
import numpy as np
from sklearn.preprocessing import MinMaxScaler



def whetherFindCertainId(user_id, score):
    # Open the CSV file and read the contents
    with open('static/motivation_level.csv', mode='r') as file:
        reader = csv.reader(file)

        # Create an empty list to store all rows of data
        all_rows = []

        # Iterate through each row and look for a specific ID
        found_id = False
        for row in reader:
            if row[0] == 'ID':
                continue
            if int(row[0]) == user_id:
                # Perform an update operation when a specific ID is found
                row[1] = score
                found_id = True
            # Add each row to the all_rows list
            all_rows.append(row)
    file.close()
    # Now open the file to write the new data
    with open('static/motivation_level.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Motivation Score'])
        for row in all_rows:
            writer.writerow(row)

    # close csv
    file.close()
    return found_id

# Six Questions:
# Question1:  Has user taken GRE before? 1 - yes 0 - no
# Question2:  What has the user scored?
# Question3:  What score do you want to achieve next?
# Question4:  When are planning to take GRE?
# Question5:  How long was it taken?
# Question6:  How many times has he taken it overall?

#example
row =  {'Q1': 1, 'Q2': 139, 'Q3': 155, 'Q4': 1, 'Q5': 3, 'Q6':9}


# Define a function that calculates the score based on the question scores and types
def calculate_score(user_id, row):
    # Use Q1 value to determine the question type
    if row['Q1'] == 0:
        # The higher the Q3 score, the highest the score
        score = row['Q3'] / 170
    else:
        # The lower the Q4, Q5, Q6 scores, and the higher the Q3, Q4 scores, the higher the score
        max_q3_q2 = max(row['Q3'], row['Q2'])
        score = (max_q3_q2 - row['Q4'] - row['Q5'] - row['Q6']) / max_q3_q2
    if not whetherFindCertainId(user_id, score):
        with open('static/motivation_level.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_id, score])

        file.close()
    return score

# calculate_score(1001, row)
