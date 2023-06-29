import ast
import os
import subprocess
import sys
from io import StringIO

import astunparse
import black
import nltk
from dotenv import load_dotenv
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import send_file
from flask import send_from_directory
from main import Engine
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates')

# Get the absolute path to the prompt.txt file
load_dotenv()
prompt_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'prompt.txt'))
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: {api_key}")
engine = Engine()
database = engine.database


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run', methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        # Handle POST request
        # Get the prompt and expected output from the form
        prompt = request.form.get('prompt')
        expected_output = request.form.get('expected_output')

        # Save the prompt and expected output to the database
        prompt_tokens = len(nltk.word_tokenize(prompt))

        # Generate the code using the prompt and expected output
        generated_code = engine.generate_code(prompt, expected_output)

        # Calculate the number of completion tokens
        try:
            completion_tokens = len(nltk.word_tokenize(generated_code)) - prompt_tokens
        except Exception as e:
            return jsonify({'error': 'Failed to generate code. Please try again.'})

        # Calculate the total number of tokens
        total_tokens = prompt_tokens + completion_tokens

        # Get the response from the OpenAI API
        response = engine.handle_request(prompt, expected_output)

        if response:
            # Print the entire JSON response
            print("Response from OpenAI API:")
            print(response)

            # Extract relevant data from the JSON response
            response_id = response['id']
            chatgpt_finish_reason = response['choices'][0]['finish_reason']
            chatgpt_output = response['choices'][0]['message']['content']

            # Save the data to the database
            engine.save_to_db(
                prompt,
                expected_output,
                None,
                None,
                prompt_tokens,
                completion_tokens,
                total_tokens,
                response_id,
                chatgpt_finish_reason,
                chatgpt_output,
                response
            )

            # Render the run.html template with the updated data
            return render_template('run.html', prompt=prompt, expected_output=expected_output, generated_code=generated_code, api_key=engine.api_key)
        else:
            return jsonify({'error': 'Failed to generate code. Please try again.'})

    elif request.method == 'GET':
        # Handle GET request
        return render_template('run.html', api_key=engine.api_key)

def get_formatted_code():
    try:
        # Run the engine/main.py script and capture the output
        output = subprocess.check_output(['python', 'engine/main.py', prompt_file, expected_output])

        # Extract the code from the output
        code = engine.extract_code_from_chat_model(output, expected_output)

        # Format the code
        formatted_code = engine.format_code(code)

        # Return the formatted code
        return formatted_code
    except Exception as e:
        # Handle any errors that occur during execution
        error_message = str(e)
        return f"An error occurred during execution: {error_message}"

@app.route('/robot_framework/reports/report')
def serve_report():
    reports_dir = os.path.join(app.root_path, 'flask_app/robot_framework', 'reports')
    filename = "report.html"
    file_path = os.path.join(reports_dir, filename)

    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "Report file not found."

@app.route('/robot_framework/reports/logs')
def serve_logs():
    logs_dir = os.path.join(app.root_path, 'flask_app/robot_framework', 'reports')
    filename = "logs.html"
    file_path = os.path.join(logs_dir, filename)

    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "Log file not found."

@app.route('/docs/<path:filename>')
def serve_docs(filename):
    docs_dir = os.path.join(app.root_path, 'templates', 'docs', 'html')
    return send_from_directory(docs_dir, filename)

@app.route('/about')
def about():
    return "About Page"
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/tts', methods=['GET'])
def tts_page():
    # Code to render the TTS page
    return render_template('tts.html')

@app.route('/tts', methods=['POST'])
def process_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file in the request'})

    _file = request.files['file']

    if _file.filename == '':
        return jsonify({'error': 'No file selected'})

    if _file and allowed_file(_file.filename):
        filename = secure_filename(_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        _file.save(filepath)

        try:
            transcript = engine.process_speech_to_text(filepath)
            if transcript:
                return jsonify({'filename': filename, 'output': transcript})
            else:
                return jsonify({'error': 'Audio processing failed'})
        except Exception as e:
            return jsonify({'error': str(e)})

    return jsonify({'error': 'Invalid file'})

if __name__ == '__main__':
    database.init_db()
    app.run(host='0.0.0.0', port=5000)


