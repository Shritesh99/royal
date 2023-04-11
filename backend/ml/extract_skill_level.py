import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

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


# Read csv file containing answers to GRE math questions
df = pd.read_csv('gre_answers.csv')

# Clean and preprocess data
# ...

# Get a list of all topics
topics = df['Topic'].unique()

# Calculate score for each user on each topic
scores = []
for index, row in df.iterrows():
    user_id = row['User_id']
    topic = row['Topic']
    time = row['Time']
    difficulty = row['Diffculty']
    correct = row['Correct']

    score = calculate_score(topic, time, difficulty, correct)
    scores.append((user_id, topic, score))

# Group scores by user_id and topic, and calculate average score for each user on each topic
scores_df = pd.DataFrame(scores, columns=['User_id', 'Topic', 'Score'])
scores_mean = scores_df.groupby(['User_id', 'Topic']).mean().reset_index()

# Calculate skill level for each user on each topic
skill_levels = []
for user_id, group in scores_mean.groupby('User_id'):
    row = {'User_id': user_id}
    for topic in topics:
        if topic in group['Topic'].values:
            score = group[group['Topic'] == topic]['Score'].iloc[0]
        else:
            score = np.mean(group['Score'])
        skill_level = (score - np.mean(group['Score'])) / np.std(group['Score'])
        row['Topic{}'.format(topic)] = skill_level
    skill_levels.append(row)

# Convert skill levels for each user on each topic to a new dataframe
new_df = pd.DataFrame(skill_levels, columns=['User_id'] + ['Topic{}'.format(topic) for topic in topics])

# Sort topics in ascending order
topics = ['Topic{}'.format(i) for i in range(1, 18)]
new_df = new_df[['User_id'] + topics]

# Fill all 0 values with mean value of the row (excluding User_id)
for topic in topics:
    new_df[topic] = new_df[topic].apply(lambda x: np.mean(new_df.loc[new_df[topic] != 0, topic]) if x == 0 else x)

# Normalize scores for each row to 0-10
scaler = MinMaxScaler(feature_range=(0, 10))
new_df[topics] = scaler.fit_transform(new_df[topics])

# Save new dataframe as a csv file
new_df.to_csv('topic_skill_level.csv', index=False)
