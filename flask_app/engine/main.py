import os
import openai
import re
from dotenv import load_dotenv
from difflib import SequenceMatcher
import black
import requests

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


class Engine:
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
        return SequenceMatcher(None, a, b).ratio()

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

    def handle_request(self, request):
        """
        Handle request
        """
        print("Handling the request...")
        try:
            response = requests.post(
                "https://api.openai.com/v1/engines/davinci-codex/completions",
                json={
                    "prompt": request,
                    "max_tokens": 1000,
                    "temperature": 1,
                    "top_p": 1,
                    "frequency_penalty": 0,
                    "presence_penalty": 0,
                    "stop": ["\n"]
                }
            )
            print(f"Response: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Error while handling the request: {str(e)}")
            return None

    def extract_code_from_chat_model(self, prompt_file):
        """
        Extract code from chat model response
        """
        print("Extracting code from chat model response...")
        model = "gpt-3.5-turbo"
        prompt = self.read_file(prompt_file)

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

    def execute_engine_logic(self, prompt_file):
        try:
            code = self.extract_code_from_chat_model(prompt_file)
            formatted_code = self.format_code(code)

            print("Executing the code...")
            output = None
            exec(formatted_code, {'__builtins__': {}}, locals())
            if 'output' in locals():
                return str(output)
            else:
                return ""  # If no output variable defined in the code
        except Exception as e:
            # Handle any errors that occur during execution
            error_message = str(e)
            return f"An error occurred during execution: {error_message}"
