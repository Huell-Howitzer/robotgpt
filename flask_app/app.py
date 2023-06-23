import os
import subprocess
import openai

from config import OPENAI_API_KEY
from flask import Flask, render_template, request, send_from_directory, send_file

app = Flask(__name__, template_folder='templates')

# Get the absolute path to the prompt.txt file
prompt_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'input', 'prompt.txt'))

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run', methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        input_data = request.form['input_data']

        # Save the input data to the file
        with open(prompt_file, 'w') as file:
            file.write(input_data)

        # Execute the engine logic with the updated input data
        result = execute_engine_logic()

        # Return the results or redirect to a results page
        return render_template('results.html', result=result)
    else:
        return render_template('run.html')


def execute_engine_logic():
    try:
        # Run the engine/main.py script and capture the output
        result = subprocess.check_output(['python', 'engine/main.py']).decode().strip()

        # Print the entire output to stdout
        print(result)

        return "Hello, world!"  # Replace with the desired output text
    except Exception as e:
        # Handle any errors that occur during execution
        error_message = str(e)
        return f"An error occurred during execution: {error_message}"



@app.route('/robot_framework/reports')
def serve_report():
    reports_dir = os.path.join(app.root_path, 'robot_framework', 'reports')
    filename = "report.html"
    file_path = os.path.join(reports_dir, filename)

    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "Report file not found."




@app.route('/docs/<path:filename>')
def serve_docs(filename):
    docs_dir = os.path.join(app.root_path, 'templates', 'docs', 'html')
    return send_from_directory(docs_dir, filename)


@app.route('/about')
def about():
    return "About Page"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

