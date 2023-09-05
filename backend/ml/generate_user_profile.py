import random

# Learning Style
learning_style_categories = {
    'SI': ['Sensing', 'Intuitive'],
    'VV': ['Visual', 'Verbal'],
    'AR': ['Active', 'Reflective'],
    'SG': ['Sequential', 'Global']
}

# Skill Level
skill_level_categories = [
    "Properties of integers",
    "Fractions, decimals, and percents",
    "Ratio, proportion, and variation",
    "Exponents and roots",
    "Descriptive statistics",
    "Operations with algebraic expressions",
    "Equations and inequalities",
    "Functions and graphs",
    "Quadratic equations and functions",
    "Sequences and series",
    "Lines and angles",
    "Triangles and polygons",
    "Circles",
    "Three-dimensional geometry",
    "Geometric transformations",
    "Probability",
    "Counting methods and combinatorics",
    "Data interpretation"
]

def generate_random_learning_style():
    learning_style = {}
    for key, values in learning_style_categories.items():
        learning_style[key] = random.choice(values)
    return learning_style

def generate_random_skill_level():
    skill_level = {}
    for category in skill_level_categories:
        skill_level[category] = random.randint(0, 10)
    return skill_level

def generate_random_motivation_level():
    return {"Motivation Score": round(random.uniform(0, 1), 2)}

def generate_random_data(num_samples):
    data = []
    for _ in range(num_samples):
        sample = {
            "Learning Style": generate_random_learning_style(),
            "Skill Level": generate_random_skill_level(),
            "Motivation Level": generate_random_motivation_level()
        }
        data.append(sample)
    return data

num_samples = 100
generated_data = generate_random_data(num_samples)
print(generated_data)


import pandas as pd

def generate_random_data_with_id(num_samples):
    data = []
    for i in range(num_samples):
        sample = {
            "ID": i + 1,
            "Learning Style": generate_random_learning_style(),
            "Skill Level": generate_random_skill_level(),
            "Motivation Level": generate_random_motivation_level()
        }
        data.append(sample)
    return data

num_samples = 1000
generated_data = generate_random_data_with_id(num_samples)

# Create separate DataFrames for Learning Style, Skill Level, and Motivation Level
learning_style_data = []
skill_level_data = []
motivation_level_data = []

for sample in generated_data:
    learning_style_data.append({"ID": sample["ID"], **sample["Learning Style"]})
    skill_level_data.append({"ID": sample["ID"], **sample["Skill Level"]})
    motivation_level_data.append({"ID": sample["ID"], **sample["Motivation Level"]})

learning_style_df = pd.DataFrame(learning_style_data)
skill_level_df = pd.DataFrame(skill_level_data)
motivation_level_df = pd.DataFrame(motivation_level_data)

# Save the DataFrames to CSV files
learning_style_df.to_csv("static/learning_style.csv", index=False)
skill_level_df.to_csv("static/skill_level.csv", index=False)
motivation_level_df.to_csv("static/motivation_level.csv", index=False)

