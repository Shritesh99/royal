import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

# Read the data from CSV files
learning_style_df = pd.read_csv("learning_style.csv")
skill_level_df = pd.read_csv("skill_level.csv")
motivation_level_df = pd.read_csv("motivation_level.csv")

# Merge the DataFrames
data_df = learning_style_df.merge(skill_level_df, on="ID").merge(motivation_level_df, on="ID")

# Generate random difficulty labels
difficulty_labels = ["Easy", "Medium", "Hard"]
data_df["Difficulty"] = [random.choice(difficulty_labels) for _ in range(len(data_df))]

# Convert categorical features to numerical values
data_df = pd.get_dummies(data_df, columns=["SI", "VV", "AR", "SG"])

# Split the data into training and testing sets
X = data_df.drop(["ID", "Difficulty"], axis=1)
y = data_df["Difficulty"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a decision tree classifier
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Test the classifier
y_pred = clf.predict(X_test)

print(y_pred)

# Print the classification report
print(classification_report(y_test, y_pred))

def select_top_topics(skill_levels, num_topics):
    sorted_skills = sorted(skill_levels.items(), key=lambda x: x[1], reverse=True)
    return [topic for topic, _ in sorted_skills[:num_topics]]
    

def generate_question_request(difficulty_level, topics, learning_style):
    request = f"Can you give me a {difficulty_level} question in GRE quantitative reasoning about {', '.join(topics)}?"

    if learning_style['VV'] == 'Visual':
        request += " Please include figures in the question."

    if learning_style['SI'] == 'Sensing':
        request += " The question should involve real-world examples and practical applications."
    else:
        request += " The question should involve abstract concepts and theoretical reasoning."

    if learning_style['AR'] == 'Active':
        request += " Please provide opportunities for hands-on problem-solving."
    else:
        request += " Please provide opportunities for individual reflection and analysis."

    if learning_style['SG'] == 'Sequential':
        request += " The question should be broken down into a series of smaller, well-organized steps."
    else:
        request += " The question should involve a holistic approach and require understanding of the bigger picture."

    return request

# The rest of the script remains the same

# Select a random student from the dataset
student = data_df.sample()

# Get the difficulty level for the selected student
difficulty = student["Difficulty"].values[0]

# Get the skill levels for the selected student (excluding learning style and motivation level columns)
skill_levels = student.drop(["ID", "Difficulty", "Motivation Score", "SI_Intuitive", "SI_Sensing", "VV_Verbal", "VV_Visual", "AR_Active", "AR_Reflective", "SG_Global", "SG_Sequential"], axis=1).to_dict(orient="records")[0]

# Get the learning style for the selected student
learning_style = {
    "SI": "Intuitive" if student["SI_Intuitive"].values[0] else "Sensing",
    "VV": "Visual" if student["VV_Visual"].values[0] else "Verbal",
    "AR": "Active" if student["AR_Active"].values[0] else "Reflective",
    "SG": "Global" if student["SG_Global"].values[0] else "Sequential"
}

# Select the top 3 topics based on the student's skill levels
top_topics = select_top_topics(skill_levels, 3)

# Generate a question request based on the difficulty level, top topics, and learning style
question_request = generate_question_request(difficulty, top_topics, learning_style)

print("Student ID:", student["ID"].values[0])
print("Question Request:", question_request)
