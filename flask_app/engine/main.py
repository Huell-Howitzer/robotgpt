import os
import openai
import nltk
import re
from io import StringIO
import sys
from dotenv import load_dotenv
from difflib import SequenceMatcher
import black
import requests
from werkzeug.utils import secure_filename

load_dotenv()

class Engine:
    def __init__(self, api_key):
        self.api_key = api_key
        self.prompt_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'input', 'prompt.txt'))
        openai.api_key = self.api_key

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
            with open(file_path, 'r') as file:
                data = file.read().replace('\n', '')
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
            with open(file_path, 'w') as file:
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

    def handle_request(self, prompt, expected_output):
        """
        Handle request
        """
        print("Handling the request...")

        # Download the required NLTK resource
        nltk.download('punkt')

        # Calculate the token count of the input prompt using NLTK
        prompt_tokens = len(nltk.word_tokenize(prompt))

        # Calculate the remaining tokens by subtracting the prompt tokens from the maximum allowed tokens
        remaining_tokens = 16384 - prompt_tokens

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type" : "application/json"
            }

            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
                {"role": "user", "content": f"Here is the expected output of the program: {expected_output}"}
            ]

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json={
                    "model"      : "gpt-3.5-turbo-16k-0613",
                    "messages"   : messages,
                    "max_tokens" : 8242,
                    "temperature": 1.0
                }
            )

            print(f"Response: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Error while handling the request: {str(e)}")
            return None

    def extract_code_from_chat_model(self, prompt, expected_output):
        """
        Extract code from chat model response
        """
        print("Extracting code from chat model response...")
        model = "gpt-3.5-turbo-16k-0613"
        file_path = self.write_file(self.prompt_file, prompt)

        if file_path:
            response = self.handle_request(prompt, expected_output)
            content = response['choices'][0]['message']['content']

            # Extract Python code using regular expression
            code_match = re.search(r'```python([\s\S]*?)```', content)
            if code_match:
                code = code_match.group(1).strip()  # Get the code
                print(f"Extracted code:\n{code}")
                return code
            else:
                print(f"Code could not be extracted from the response: {content}")
                return None
        else:
            return None

    def execute_engine_logic(self, prompt_file, expected_output):
        try:
            code = self.extract_code_from_chat_model(prompt_file, expected_output)
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
            exec(formatted_code, {'__builtins__': {}}, locals_dict)

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

    def generate_code(self, prompt, expected_output):
        """
        Generate Python code using ChatGPT
        """
        print("Generating code...")
        try:
            response = self.handle_request(prompt, expected_output)

            if response:
                code = self.extract_code_from_chat_model(prompt, expected_output)
                print("Generated code:\n", code)
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
            captured_output = StringIO()
            sys.stdout = captured_output

            # Execute the code
            exec(code)

            # Get the captured output
            output = captured_output.getvalue()

            print("[execute_code] Output of the code:")
            print(output)
            return output
        except Exception as e:
            # Handle any errors that occur during execution
            error_message = str(e)
            error_info = sys.exc_info()
            error_line = error_info[2].tb_lineno
            print(f"[execute_code] Error while executing code:")
            print(f"Line {error_line}: {error_message}")
            return f"An error occurred during execution: Line {error_line}, {error_message}"
