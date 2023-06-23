import os
import json
import openai
import re
from dotenv import load_dotenv
from RestrictedPython import compile_restricted_function, safe_builtins
from difflib import SequenceMatcher
from termcolor import colored
import ast
import logging

import os
import openai
import black
import ast
import difflib
from nltk import sent_tokenize

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def format_code(code):
    """
    Format code using black
    """
    print("Formatting the code...")
    try:
        formatted_code = black.format_str(code, mode=black.FileMode())
        print("Formatted code:\n", formatted_code)
        return formatted_code
    except Exception as e:
        print(f"Error while formatting code: {str(e)}")
        return None


def calculate_similarity(a, b):
    """
    Calculate similarity between two strings
    """
    return difflib.SequenceMatcher(None, a, b).ratio()


def read_file(file_path):
    """
    Read file content
    """
    print(f"Reading the file: {file_path}...")
    try:
        with open(file_path, 'r') as file:
            data = file.read().replace('\n', '')
        print(f"File content: {data}")
        return data
    except Exception as e:
        print(f"Error while reading the file: {str(e)}")
        return None


def write_file(file_path, content):
    """
    Write content to file
    """
    print(f"Writing content to the file: {file_path}...")
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Content written to the file: {file_path}")
        return True
    except Exception as e:
        print(f"Error while writing the file: {str(e)}")
        return False


def extract_code_from_chat_model(prompt_file):
    """
    Extract code from chat model response
    """
    print("Extracting code from chat model response...")
    model = "gpt-3.5-turbo"
    prompt = read_file(prompt_file)

    response = openai.ChatCompletion.create(model=model, messages=[
                                            {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}])

    content = response['choices'][0]['message']['content']

    # Extract Python code using regular expression
    code_match = re.search(r'```python([\s\S]*?)```', content)
    if code_match:
        code = code_match.group(1).strip()  # Get the code
    else:
        code_match = re.search(r'```([\s\S]*?)```', content)
        if code_match:
            code = code_match.group(1).strip()  # Get the code

    print(f"Extracted code:\n{code}")
    return code


def main():
    prompt_file = "./data/input/prompt.txt"
    code = extract_code_from_chat_model(prompt_file)

    formatted_code = format_code(code)

    print("Executing the code...")

    exec(formatted_code)


if __name__ == "__main__":
    main()

