import openai
import yaml
import pandas as pd
import random
import json


# Load the configuration from the YAML file
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

api_key = config['api_key']
num_questions = config['num_questions']
temperature = config['temperature']
top_p = config['top_p']
frequency_penalty = config['frequency_penalty']
presence_penalty = config['presence_penalty']
max_token = config['max_token']

df = pd.read_excel("faq.xlsx",sheet_name="FAQ Helpdesk (Eng)(Update)")
answers = df['Ans (ENG)']
# cat = df['sub sub cat']

openai.api_key = api_key

def generate_example(num_questions, answer, prev_examples, temperature=0, top_p=0.5, max_token=500, presence_penalty=0.8, frequency_penalty=0.6):
    messages=[
        {
            "role": "system",
            "content": f"Generate {num_questions} questions that can be answered with the following answer: {answer}."
    }
    ]

    if len(prev_examples) > 0:
        if len(prev_examples) > 10:
            prev_examples = random.sample(prev_examples, 10)
        for example in prev_examples:
            messages.append({
                "role": "assistant",
                "content": example
            })

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
        temperature=temperature,
        top_p = top_p,
        max_tokens=max_token,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    return response.choices[0].message['content']

# Generate examples
data = {}
prev_examples = []
for i in range(len(answers)):
    print(f'Generating {num_questions} questions for answer #{i}...')
    example = generate_example(num_questions, answers[i], prev_examples, temperature=temperature, top_p=top_p, max_token=max_token, presence_penalty=presence_penalty, frequency_penalty=frequency_penalty)
    prev_examples.append(example)

# Export the DataFrame to an Excel file
data = {
    "answer": answers,
    "questions": prev_examples
}
df = pd.DataFrame(data)
excel_file_name = "output.xlsx"
df.to_excel(excel_file_name, index=False)

print('questions moved to excel file successfully')

