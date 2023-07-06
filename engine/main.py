import json
import types
import os
import re
import sys
from difflib import SequenceMatcher
from io import StringIO
import traceback
import black
import nltk
import openai
import requests
from dotenv import load_dotenv

from database.db import Database

load_dotenv()

class Engine(Database):
    def __init__(self):
        load_dotenv()
        super().__init__()
        self.prompt_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "prompt.txt"))
        self.database = Database()
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key
        print(f"API Key: {self.api_key}")

    def format_code(self, code):
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

    def calculate_similarity(self, a, b):
        """
        Calculate similarity between two strings
        """
        return SequenceMatcher(None, a, b).ratio() * 100

    def read_file(self, file_path):
        """
        Read file content
        """
        print(f"Reading the file: {file_path}...")
        try:
            with open(file_path, "r") as file:
                data = file.read().replace("\n", "")
            print(f"File content: {data}")
            return data
        except Exception as e:
            print(f"Error while reading the file: {str(e)}")
            return None

    def write_file(self, file_path, data):
        """
        Write file content
        """
        print(f"Writing the file: {file_path}...")
        try:
            with open(file_path, "w") as file:
                file.write(data)
            print(f"File content: {data}")
            return True
        except Exception as e:
            print(f"Error while writing the file: {str(e)}")
            return False

    def process_speech_to_text(self, file_path):
        """
        Process speech to text
        """
        print(f"Processing speech to text...")
        audio_file = open(file_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        print(transcript)
        return transcript

    def handle_request(self, prompt, expected_output, similarity_threshold, max_attempts=10):
        print("Handling the request...")

        # Download the required NLTK resource
        nltk.download("punkt")

        # Calculate the token count of the input prompt using NLTK
        prompt_tokens = len(nltk.word_tokenize(prompt))

        # Calculate the remaining tokens by subtracting the prompt tokens from the maximum allowed tokens
        remaining_tokens = 16384 - 8000

        similarity_score = 0
        attempts = 0
        while similarity_score < int(similarity_threshold) and attempts < max_attempts:
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }

                messages = [
                    {"role": "system", "content": "You are a helpful assistant and a master of Regular Expressions."},
                    {"role": "user",
                     "content": f"Create a Python Regex that will convert: {prompt} into: {expected_output}"}
                ]
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": "gpt-3.5-turbo-16k-0613",
                        "messages": messages,
                        "max_tokens": 7044,
                        "temperature": 0.8,
                    },
                )

                # Parse the response as JSON
                response_data = response.json()

                # Check if 'choices' is in the response
                if "choices" in response_data:
                    # Extract the required fields from the response
                    response_id = response_data["id"]
                    object_type = response_data["object"]
                    created_at = response_data["created"]
                    model_used = response_data["model"]
                    chatgpt_response = response_data["choices"][0]["message"]["content"]
                    chatgpt_finish_reason = response_data["choices"][0]["finish_reason"]
                    usage_info = response_data["usage"]
                    prompt_tokens = usage_info["prompt_tokens"]
                    completion_tokens = usage_info["completion_tokens"]
                    total_tokens = usage_info["total_tokens"]

                    print(f"Response: {chatgpt_response}")
                    return response_data
                else:
                    if "error" in response_data:
                        error_message = response_data["error"]["message"]
                    else:
                        error_message = "Unknown error occurred"
                    print(f"Error: {error_message}")
                    return None

            except Exception as e:
                print(f"Error occurred during request handling: {str(e)}")
                return None

    def extract_code_from_chat_model(self, response_json):
        print("Extracting code from chat model response...")
        print(response_json)
        response_data = json.dumps(response_json)
        print(response_data)
        # Extract Python code using regular expression
        code_matches = re.findall(r"```(?s)(.*?)```(?s)", response_data, re.DOTALL)
        print(f"code_matches: {code_matches}")
        code = code_matches
        if code[0][:6] == 'python':
            code = code[0][6:]
            code = code.replace('\\n', '\n')
            code = code.replace('\\', '')
            blackened_code = black.format_str(code, mode=black.FileMode())
            print(f"code: {blackened_code}")
            return blackened_code

    def execute_engine_logic(self, prompt, expected_output, similarity_threshold):
        print("Executing the engine logic...")
        try:
            code = self.generate_code(prompt, expected_output, similarity_threshold)
            if code is None:
                return "Failed to generate code"

            formatted_code = self.format_code(code)

            print("Executing the code...")
            output = None

            # Create a StringIO object to capture the output
            captured_output = StringIO()

            # Replace sys.stdout with the StringIO object
            sys.stdout = captured_output

            # Create a dictionary to capture the local variables
            locals_dict = {}

            # Execute the code in the given dictionary
            exec(formatted_code, {"__builtins__": {}}, locals_dict)

            # Retrieve the captured output
            output = captured_output.getvalue()

            # Restore sys.stdout
            sys.stdout = sys.__stdout__

            if output.strip():
                return output
            else:
                return ""  # If no output captured
        except Exception as e:
            # Handle any errors that occur during execution
            error_message = str(e)
            return f"An error occurred during execution: {error_message}"

    def generate_code(self, prompt, expected_output, similarity_threshold):
        """
        Generate Python code using ChatGPT
        """
        print("Generating code...")
        print(f"similarity_threshold: {similarity_threshold}")
        try:
            x = self.handle_request(
                prompt, expected_output, float(similarity_threshold)
            )

            if x:
                code = self.extract_code_from_chat_model(x)
                print("Generated code:\n", code)

                # Save the generated code to the database
                return code
            else:
                return None
        except Exception as e:
            print(f"Error while generating code: {str(e)}")
            return None

    def execute_code(self, code):
        """
        Execute the generated Python code and return its output
        """
        print("[execute_code] Executing the code...")
        try:
            # Redirect stdout to a StringIO object
            original_stdout = sys.stdout
            captured_output = StringIO()
            sys.stdout = captured_output

            # Check if the code is a string or a compiled code object
            if isinstance(code, str):
                exec(code)
            elif isinstance(code, types.CodeType):
                exec(code, globals())

            # Get the captured output
            output = captured_output.getvalue()
            print("[execute_code] Output of the code:")
            print(output)
        except Exception as e:
            # Handle any errors that occur during execution
            error_message = str(e)
            error_info = sys.exc_info()
            error_line = error_info[2].tb_lineno
            print(f"[execute_code] Error while executing code:")
            print(f"Line {error_line}: {error_message}")
            output = f"An error occurred during execution: Line {error_line}, {error_message}"
        finally:
            # Reset stdout to its original state
            sys.stdout = original_stdout
        return output


