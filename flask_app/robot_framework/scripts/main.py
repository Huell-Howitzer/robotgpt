import ast
import os
import dotenv
import openai
from difflib import SequenceMatcher
from RestrictedPython import compile_restricted, safe_builtins

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
DEBUG_MODE = os.getenv("DEBUG_MODE") == 'True'


def chat_with_agent(agent, message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an intelligent machine that produces source code."},
            {"role": agent, "content": message},
        ],
    )
    response_content = response['choices'][0]['message']['content']

    if DEBUG_MODE:
        print(f"Assistant's response: {response_content}")

    # Split the response by newline
    response_parts = response_content.split("\n")

    # Check if the response contains more than one line
    if len(response_parts) > 1:
        # Return only the second part (which is assumed to be the Python code)
        python_code = response_parts[1]
    else:
        raise ValueError("The assistant's response does not contain any Python code")

    # Check if the generated code is valid Python
    try:
        ast.parse(python_code)
    except SyntaxError:
        raise ValueError("The assistant's response is not valid Python code")

    return python_code



def run_untrusted_code(code, local_vars):
    byte_code = compile_restricted(code, '<inline>', 'exec')
    global_vars = {"__builtins__": safe_builtins}
    exec(byte_code, global_vars, local_vars)


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read().strip()


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def write_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)


def create_directories():
    if not os.path.exists("../data"):
        os.mkdir("../data")
    if not os.path.exists("../data/output"):
        os.mkdir("../data/output")
    if not os.path.exists("data/script"):
        os.mkdir("data/script")


def create_and_test_transform(sample_text_filename, expected_output_filename, attempts_allowed=5,
                              max_invalid_code_attempts=3):
    sample_text = read_file("data/input/" + sample_text_filename)
    expected_output = read_file("data/output/" + expected_output_filename)
    user_message = f"Create a Python script that transforms '{sample_text}' into '{expected_output}'."

    best_similarity = 0
    best_script = ""
    invalid_code_attempts = 0

    for attempt in range(attempts_allowed):
        try:
            while True:
                try:
                    transformation_script = chat_with_agent("user", user_message)
                    local_vars = {"sample_text": sample_text, "transformed_text": None}
                    untrusted_code = transformation_script + "\ntransformed_text = transformation(sample_text)"
                    run_untrusted_code(untrusted_code, local_vars)
                    break
                except ValueError as ve:
                    invalid_code_attempts += 1
                    if invalid_code_attempts >= max_invalid_code_attempts:
                        raise RuntimeError("The assistant has produced invalid Python code too many times.")
                    user_message = f"The transformation script was incorrect: {str(ve)}. Please try again."

            current_similarity = similarity(local_vars["transformed_text"], expected_output)

            if DEBUG_MODE:
                print(f"Iteration {attempt + 1} started with a similarity of {best_similarity * 100:.2f}%")
                print(f"Script:\n{best_script}")
                print(f"Result of this iteration is {current_similarity * 100:.2f}%")

            if current_similarity >= best_similarity:
                best_similarity = current_similarity
                best_script = transformation_script
                write_to_file(f"data/script/iteration_{attempt + 1}.py", best_script)
                write_to_file(f"data/output/iteration_{attempt + 1}.txt", local_vars["transformed_text"])

            if local_vars["transformed_text"] == expected_output:
                break
        except Exception as e:
            user_message = f"The transformation script was incorrect: {str(e)}. Please try again."
    else:
        raise RuntimeError(f"Failed to generate a correct transformation script after {attempts_allowed} attempts.")

    return best_script


if __name__ == "__main__":
    create_directories()
    sample_text_filename = "sample_text_1.lores"
    expected_output_filename = "expected_output_1.html"
    transformation_script = create_and_test_transform(sample_text_filename, expected_output_filename, 10)
    print(f"Successful transformation script: {transformation_script}")
