import ast
import os
import re
import sys
import dotenv
import openai
from dotenv import load_dotenv
from RestrictedPython import compile_restricted, safe_builtins
from RestrictedPython.PrintCollector import PrintCollector
from utilities.file_utils import FileUtils

def _print_(message):
    print(message)

def transformation(text):
    return text.title()

class TransformationScriptGenerator:
    def __init__(self):
        dotenv.load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.DEBUG_MODE = os.getenv("DEBUG_MODE") == 'True'
        self.file_utils = FileUtils()

    def chat_with_agent(self, agent, message):
        print(f"Chatting with agent: {agent}, message: {message}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an intelligent machine that produces source code."},
                {"role": agent, "content": message},
            ],
        )
        response_content = response['choices'][0]['message']['content']
        print(f"Response content: {response_content}")

        # Find all occurrences of code blocks using backticks
        code_blocks = re.findall(r"```([\s\S]*?)```", response_content, re.MULTILINE)
        print(f"Code blocks: {code_blocks}")

        python_code = ""

        # Extract the Python code from the code blocks
        for code_block in code_blocks:
            if "python" in code_block.lower():
                # Remove the leading "python" line and leading/trailing whitespace
                code_lines = code_block.split("\n")
                code_lines = [line for line in code_lines if line.strip() != "python"]
                code_block = "\n".join(code_lines).strip()
                python_code += code_block + "\n"

        if not python_code:
            raise ValueError("The assistant's response does not contain any Python code")

        return python_code

    def process_agent_output(self):
        agent = "assistant"
        message = "Create a Python script that transforms 'hello world' into 'Hello World'."
        python_code = self.chat_with_agent(agent, message)
        print(f"Python code: {python_code}")

        # Format and process the extracted Python code
        formatted_code = self.format_python_code(python_code)
        print(f"Formatted code: {formatted_code}")
        self.process_python_code(formatted_code)

    def format_python_code(self, python_code):
        # Remove leading/trailing whitespace
        formatted_code = python_code.strip()
        return formatted_code

    def process_python_code(self, python_code):
        # Check if the code is valid Python
        try:
            ast.parse(python_code)
        except SyntaxError:
            raise ValueError("The extracted Python code is not valid")

    def run_untrusted_code(self, code, local_vars):
        # Define a policy for the restricted execution environment
        class MyPolicy(safe_builtins):
            def __init__(self):
                super().__init__()
                self._print_ = PrintCollector
                self.__import__ = __import__

        # Create a restricted globals dictionary with the policy
        restricted_globals = dict(__builtins__=MyPolicy())

        # Compile and execute the code
        byte_code = compile_restricted(code, "<inline>", "exec")
        exec(byte_code, restricted_globals, local_vars)

    def create_and_test_transform(self, sample_text_filename, expected_output_filename, attempts_allowed=5,
                                  max_invalid_code_attempts=3):
        self.file_utils.create_directories()
        sample_text = selfThe error message "name 'SafeBuiltins' is not defined" is likely due to the line where you define `MyPolicy` class. In this line:
class MyPolicy(SafeBuiltins):







