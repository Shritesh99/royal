import openai
import re

def get_chatgpt_question(prompt):
    # Set the API key
    openai.api_key = "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"

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
    question_match = re.search("^(Question: .+)", text, re.MULTILINE)
    question = question_match.group(1).strip() if question_match else ""

    options_match = re.findall("([A-D]\) [^A-D]+)", text)
    options = [option.strip() for option in options_match] if options_match else []

    answer_section = text.split("Answer:")[1]
    answer_match = re.search("^([A-D])\.", answer_section.strip(), re.MULTILINE)
    answer_index = ord(answer_match.group(1)) - ord('A') if answer_match else None

    explanation_match = re.search("Explanation:(.+)", answer_section, re.IGNORECASE)
    explanation = explanation_match.group(1).strip() if explanation_match else ""

    ontology_tags_match = re.search("Ontology Tag[s]?: (.+)", answer_section, re.IGNORECASE)
    ontology_tags = ontology_tags_match.group(1).split(", ") if ontology_tags_match else []

    return question, options, answer_index, explanation, ontology_tags



# Define the prompt
prompt = "Generate a challenging GRE quantitative reasoning question about Triangles and polygons. The question should involve real-world examples and practical applications. Provide 4 options in the format A), B), C), and D), with one correct option. Indicate the correct answer explicitly with the format 'Answer: X. Option_Text'. Provide a clear and well-organized explanation with a series of smaller steps. Include 1 ontology tag from the following list to store this question in a knowledge graph: 'Properties of integers, Fractions, decimals, and percents, Ratio, proportion, and variation, Exponents and roots, Descriptive statistics, Operations with algebraic expressions, Equations and inequalities, Functions and graphs, Quadratic equations and functions, Sequences and series, Lines and angles, Triangles and polygons, Circles, Three-dimensional geometry, Geometric transformations, Probability, Counting methods and combinatorics, Data interpretation'. Ensure that the response is easy to parse and well-structured."

# Call the API to generate the question
generated_text = get_chatgpt_question(prompt)

# Print the generated question
print(generated_text)

# Parse the generated text
question , options, answer_index, explanation, ontology_tags = parse_generated_text(generated_text)

print("Prompt is: ")
print("Q:",question)
print("O1:",options[0])  # Access option A
print("O2:",options[1])  # Access option B
print("O3:",options[2])  # Access option C
print("O4:",options[3])  # Access option D
print("Oright:",options[answer_index])  # Access the correct answer
print("Onto:",ontology_tags)