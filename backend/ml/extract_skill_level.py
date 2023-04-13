import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import csv

# Define function to calculate score based on topic, time, difficulty, and correct
def calculate_score(topic, time, difficulty, correct):
    # Calculate weight for each factor
    if (topic < 8):
        topic_weight = 0.6
    elif (topic < 13):
        topic_weight = 0.5
    else:
        topic_weight = 0.7
    time_weight = 0.2  # can be adjusted based on actual situation
    diff_weight = 0.2  # can be adjusted based on actual situation
    correct_weight = 0.1  # can be adjusted based on actual situation

    # Calculate score
    score = (topic_weight +
             time_weight / time -
             diff_weight * difficulty +
             correct_weight * (1 if correct else 0))

    return score

# example
# gre_answers = {
#     1: {
#         'Topic': 1,
#         'time': 360,
#         'difficulty': 3,
#         'correct': 1
#     },
#     2: {
#         'Topic': 2,
#         'time': 180,
#         'difficulty': 2,
#         'correct': 0
#     },
#     3: {
#         'Topic': 4,
#         'time': 230,
#         'difficulty': 2,
#         'correct': 0
#     },
#     4: {
#         'Topic': 18,
#         'time': 180,
#         'difficulty': 2,
#         'correct': 0
#     },
#     5: {
#         'Topic': 10,
#         'time': 300,
#         'difficulty': 3,
#         'correct': 0
#     },
#     6: {
#         'Topic': 6,
#         'time': 360,
#         'difficulty': 3,
#         'correct': 1
#     },
#     7: {
#         'Topic': 14,
#         'time': 180,
#         'difficulty': 2,
#         'correct': 0
#     },
#     8: {
#         'Topic': 16,
#         'time': 180,
#         'difficulty': 2,
#         'correct': 0
#     },
#     9: {
#         'Topic': 13,
#         'time': 180,
#         'difficulty': 1,
#         'correct': 0
#     },
#     10: {
#         'Topic':5,
#         'time': 660,
#         'difficulty': 3,
#         'correct': 1
#     },


# }

def whetherFindCertainId(user_id, append_row):
    # Open the CSV file and read the contents
    with open('static/skill_level.csv', mode='r') as file:
        reader = csv.reader(file)

        # Create an empty list to store all rows of data
        all_rows = []

        # Iterate through each row and look for a specific ID
        found_id = False
        for row in reader:
            if row[0] == 'ID':
                continue
            if int(row[0]) == user_id:
                found_id = True
                row = append_row
            # Add each row to the all_rows list
            all_rows.append(row)
    file.close()

    if found_id:
        # Now open the file to write the new data
        with open('static/skill_level.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID',  'Properties of integers',
                             'Fractions, decimals, and percents',
                             'Ratio, proportion, and variation',
                             'Exponents and roots',
                             'Descriptive statistics',
                             'Operations with algebraic expressions',
                             'Equations and inequalities',
                             'Functions and graphs',
                             'Quadratic equations and functions',
                             'Sequences and series',
                             'Lines and angles',
                             'Triangles and polygons',
                             'Circles',
                             'Three-dimensional geometry',
                             'Geometric transformations',
                             'Probability',
                             'Counting methods and combinatorics',
                             'Data interpretation'])
            for row in all_rows:
                writer.writerow(row)

    # close csv
    file.close()
    return found_id

def extra_skill_level(user_id, gre_answers):
    # new extra skill level row
    row = [user_id, 0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0, 0 ,0]
    # count & total_scroe for calculate the average score
    count = 0
    total_score = 0

    # Iterate over all key values in the dictionary
    for key in gre_answers:
        # from key get value
        value = gre_answers[key]
        # get info from value
        topic = value['Topic']
        time = value['time']
        difficulty = value['difficulty']
        correct = value['correct']
        # calculate score
        score = calculate_score(topic, time, difficulty, correct)
        count += 1
        # save the score into row
        row[topic] = score
        total_score += score

    mean_score = total_score / count
    for i in range(1, len(row)):
        if row[i] == 0:
            row[i] = mean_score

    # transfer the list ot an array
    row = np.array(row)
    # Normalize scores for each row to 0-10
    scaler = MinMaxScaler(feature_range=(0, 10))
    row[1:] = scaler.fit_transform(row[1:].reshape(-1, 1)).flatten()
    new_row = []
    for r in row:
        new_row.append(int(r))
    print(new_row)
    if not whetherFindCertainId(user_id, new_row):
        with open('static/skill_level.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_row)

        file.close()

# extra_skill_level(1, gre_answers)

