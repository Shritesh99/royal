import openai
import re
import environ
from question_generate import generate_question
from difficulty_ml import difficulty_train
from difficulty_ml import make_prediction
env = environ.Env()

# Set the API key
openai.api_key = env("OPENAI_KEY")

def get_chatgpt_question(prompt):

    # openai.api_key = "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"
    # Set the parameters for the completion
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2500,
        n=1,
        stop=None,
        temperature=0.8,
    )

    # Return the generated text
    return response["choices"][0]["text"]


def parse_generated_text(text):
    question_match = re.search("^Question: (.+)", text, re.MULTILINE)
    question = question_match.group(1).strip() if question_match else ""

    options_match = re.findall("([A-D]\) [^A-D]+)", text)
    options = [option.strip()
               for option in options_match] if options_match else []

    answer_section = text.split("Answer:")[1]
    answer_match = re.search("([A-D])", answer_section.strip())
    answer_index = ord(answer_match.group(1)) - \
        ord('A') if answer_match else None

    explanation_match = re.search(
        "Explanation:(.+)", answer_section, re.IGNORECASE)
    explanation = explanation_match.group(
        1).strip() if explanation_match else ""

    ontology_tags_match = re.search(
        "(Tag|Ontology Tag[s]?): (.+)", answer_section, re.IGNORECASE)
    ontology_tags = ontology_tags_match.group(
        2).split(", ") if ontology_tags_match else []

    return question, options, answer_index, explanation, ontology_tags


difficulty_train()

get_difficulty = make_prediction(188)
# 123 - easy
# 188 - hard
get_question_part1 = generate_question(188, get_difficulty)

prompt = get_question_part1 + """. Structure your response in the following format:

Question: [Your question here]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

Answer: [Correct answer option, e.g., 'A', 'B', 'C', or 'D']
Ontology Tag: [Choose one from the list: 'Properties of integers, Fractions, decimals, and percents, Ratio, proportion, and variation, Exponents and roots, Descriptive statistics, Operations with algebraic expressions, Equations and inequalities, Functions and graphs, Quadratic equations and functions, Sequences and series, Lines and angles, Triangles and polygons, Circles, Three-dimensional geometry, Geometric transformations, Probability, Counting methods and combinatorics, Data interpretation']

Explanation:
1. [Step 1 of the explanation]
2. [Step 2 of the explanation]
..."""


#
generated_text = get_chatgpt_question(prompt)
# Parse the generated text
question , options, answer_index, explanation, ontology_tags = parse_generated_text(generated_text)

# Print the generated question
print(generated_text)

# Parse the generated text
question , options, answer_index, explanation, ontology_tags = parse_generated_text(generated_text)

print("Prompt is: ")
print(question)
print(options[0])  # Access option A
print(options[1])  # Access option B
print(options[2])  # Access option C
print(options[3])  # Access option D
if answer_index is not None:
    print(options[answer_index])  # Access the correct answer
else:
    print("No correct answer found.")
print(ontology_tags)
