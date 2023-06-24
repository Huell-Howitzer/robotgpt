import os
import subprocess
from flask import Flask, render_template, request, send_from_directory, send_file
from engine.main import Engine

app = Flask(__name__, template_folder='templates')

# Get the absolute path to the prompt.txt file
prompt_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'input', 'prompt.txt'))

engine = Engine()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run', methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        prompt = request.form['input_data']
        expected_output = request.form['expected_output']
        actual_output = engine.execute_engine_logic(prompt)

        similarity = engine.calculate_similarity(expected_output, actual_output)
        return render_template('run.html', prompt=prompt, expected_output=expected_output, similarity=similarity)
    else:
        return render_template('run.html')


def get_formatted_code():
    try:
        # Run the engine/main.py script and capture the output
        output = subprocess.check_output(['python', 'engine/main.py', prompt_file])

        # Extract the code from the output
        code = engine.extract_code_from_chat_model(output)

        # Format the code
        formatted_code = engine.format_code(code)

        # Return the formatted code
        return formatted_code
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


