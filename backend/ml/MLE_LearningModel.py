import numpy as np
import csv

# Define the dimensions and their associated questions


def getDimensions():
    dimensions = {
        "Sensing-Intuition": ["1"],
        "Visual-Verbal": ["2", "3", "10"],
        "Active-Reflective": ["6", "8", "9"],
        "Sequential-Global": ["4", "7"],
        "Sensitive-Resilient": ["5"]
    }
    return dimensions


# Define the answers for each question
answers = {
    # "1": "B",
    # "2": "B",
    # "3": "A",
    # "4": "A",
    # "5": "A",
    # "6": "B",
    # "7": "B",
    # "8": "A",
    # "9": "A",
    # "10": "B"

    "1": "B",
    "2": "A",
    "3": "A",
    "4": "A",
    "5": "A",
    "6": "B",
    "7": "B",
    "8": "B",
    "9": "A",
    "10": "B"

}

# Define the MLE function


def mle(data):
    input = []
    # for d in data:
    #     input.append(int(d))
    # Calculate the MLE estimate for each dimension
    estimates = np.apply_along_axis(lambda x: np.mean(x), 1, data)
    return estimates


def whetherFindCertainId(user_id, styleSI, styleVV, styleAR, styleSG):
    # Open the CSV file and read the contents
    with open('static/learning_style.csv', mode='r') as file:
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
                row[1] = styleSI
                row[2] = styleVV
                row[3] = styleAR
                row[4] = styleSG
                found_id = True
            # Add each row to the all_rows list
            all_rows.append(row)
    file.close()
    # Now open the file to write the new data
    with open('static/learning_style.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'SI', 'VV', 'AR', 'SG'])
        for row in all_rows:
            writer.writerow(row)

    # close csv
    file.close()
    return found_id

# Calculate the MLE estimates for each dimension


def determine_learning_style(user_id, answers):
    dimensions = getDimensions()

    # Define the number of questions and dimensions
    num_questions = 10
    num_dimensions = len(dimensions)
    # Define the responses
    responses = {
        "A": 1,
        "B": 0
    }

    # Initialize the data matrix with zeros
    data_matrix = np.zeros((num_dimensions, num_questions))

    # Loop through the dimensions and questions, and record the answers
    for i, (dimension, question_ids) in enumerate(dimensions.items()):
        for j, question_id in enumerate(question_ids):
            answer = answers[question_id]
            response = responses[answer]
            data_matrix[i, j] = response

    # Convert the responses to a numpy array
    data = np.array(data_matrix)

    # Calculate the MLE estimates for each dimension
    estimates = mle(data)

    # Determine the learning style based on the MLE estimates
    styleSI = ""
    styleVV = ""
    styleAR = ""
    styleSG = ""
    if estimates[0] > 0:
        styleSI += "Sensing"
    else:
        styleSI += "Intuitive"
    if estimates[1] > 0:
        styleVV += "Visual"
    else:
        styleVV += "Verbal"
    if estimates[2] > 0:
        styleAR += "Active"
    else:
        styleAR += "Reflective"
    if estimates[3] > 0:
        styleSG += "Sequential"
    else:
        styleSG += "Global"

    learning_style = {
        'SI': styleSI,
        'VV': styleVV,
        'AR': styleAR,
        'SG': styleSG
    }

    if not whetherFindCertainId(user_id, styleSI, styleVV, styleAR, styleSG):
        with open('static/learning_style.csv', mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write the row data to be added
            data = [user_id, styleSI, styleVV, styleAR, styleSG]
            writer.writerow(data)

        file.close()
    return "{0}-{1}-{2}-{3}".format(styleSI, styleVV, styleAR, styleSG)


determine_learning_style(1001, answers)
