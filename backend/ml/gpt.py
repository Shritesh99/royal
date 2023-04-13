import openai
import re
import environ

env = environ.Env()

# Set the API key
openai.api_key = env("OPENAI_KEY")


def get_chatgpt_question(prompt):
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
    return parse_generated_text(response["choices"][0]["text"])


def parse_generated_text(text):
    question_match = re.search("^(Question: .+)", text, re.MULTILINE)
    question = question_match.group(1).strip() if question_match else ""
    
    options_match = re.findall("([A-D]\)[^A-D]+)", question_match)
    options = [option.strip()
               for option in options_match] if options_match else []

    answer_match = re.search(
        "^([A-D])\.", answer_match.strip(), re.MULTILINE)
    answer_index = ord(answer_match.group(1)) - \
        ord('A') if answer_match else None

    explanation_match = re.search(
        "Explanation:(.+)", answer_section, re.IGNORECASE)
    explanation = explanation_match.group(
        1).strip() if explanation_match else ""

    ontology_tags_match = re.search("Ontology Tag[s]?: (.+)", answer_section, re.IGNORECASE)
    ontology_tags = ontology_tags_match.group(1).split(", ") if ontology_tags_match else []

    return question, options, answer_index, explanation, ontology_tags

print("Prompt is: ")
print("Q:",question)
print("O1:",options[0])  # Access option A
print("O2:",options[1])  # Access option B
print("O3:",options[2])  # Access option C
print("O4:",options[3])  # Access option D
print("Oright:",options[answer_index])  # Access the correct answer
print("Onto:",ontology_tags)
