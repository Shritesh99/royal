import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import joblib

global data_df

def preprocess_data():
    # Read the data from CSV files
    learning_style_df = pd.read_csv("../static/learning_style.csv")
    skill_level_df = pd.read_csv("../static/skill_level.csv")
    motivation_level_df = pd.read_csv("../static/motivation_level.csv")

    # Merge the DataFrames
    data_df = learning_style_df.merge(skill_level_df, on="ID").merge(motivation_level_df, on="ID")

    # Generate random difficulty labels
    difficulty_labels = ["Easy", "Medium", "Hard"]
    data_df["Difficulty"] = [random.choice(difficulty_labels) for _ in range(len(data_df))]

    # Convert categorical features to numerical values
    data_df = pd.get_dummies(data_df, columns=["SI", "VV", "AR", "SG"])

    return data_df

def train_and_evaluate(data_df):
    # Split the data into training and testing sets
    X = data_df.drop(["ID", "Difficulty"], axis=1)
    y = data_df["Difficulty"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a decision tree classifier
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)

    # Test the classifier
    y_pred = clf.predict(X_test)

    # Print the classification report
    print(classification_report(y_test, y_pred))

    return clf

def save_model(clf, filename):
    # Save the trained model
    joblib.dump(clf, filename)

def load_model(filename):
    # Load the saved model
    return joblib.load(filename)

#2nd api
#external module can call this api to predict the dificulty level by given a student_id
def make_prediction(student_id):
    global data_df
    student_data = data_df.loc[data_df["ID"] == student_id].drop(["ID", "Difficulty"], axis=1).iloc[0].values.reshape(1, -1)
    loaded_clf = load_model("../static/decision_tree_model.pkl")
    # Predict using the loaded model
    y_pred = loaded_clf.predict(student_data)
    print(y_pred)

#1st api
#external module can call this api to train the model
def difficulty_train():
    global data_df
    data_df = preprocess_data()
    clf = train_and_evaluate(data_df)
    save_model(clf, "../static/decision_tree_model.pkl")
    return data_df

    
if __name__ == "__main__":
    difficulty_train()
    student_id = 123
    make_prediction(student_id)