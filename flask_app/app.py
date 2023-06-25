import os
import subprocess

from flask import jsonify

from flask_app.engine.database import init_db
import dotenv
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_from_directory, send_file
from engine.main import Engine
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates')

# Get the absolute path to the prompt.txt file
load_dotenv()
prompt_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'input', 'prompt.txt'))
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: {api_key}")
engine = Engine(api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['GET', 'POST'])
def run():
    # Set default values
    prompt = ""
    expected_output = ""
    generated_code = ""
    code_output = ""
    similarity = None
    api_key = engine.api_key

    if request.method == 'POST':
        prompt = request.form.get('prompt')
        expected_output = request.form.get('expected_output')

        # Generate code using ChatGPT
        generated_code = engine.generate_code(prompt, expected_output)

        # Check if generated_code is not None
        if generated_code is not None:
            # Execute the generated code and capture its output
            code_output = engine.execute_code(generated_code)

            # Check if code_output is not None
            if code_output is not None:
                similarity = engine.calculate_similarity(expected_output, code_output)

    return render_template('run.html', prompt=prompt, expected_output=expected_output, similarity=similarity, generated_code=generated_code, code_output=code_output, api_key=api_key)

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
    reports_dir = os.path.join(app.root_path, 'robot_framework', 'reports')
    filename = "report.html"
    file_path = os.path.join(reports_dir, filename)

    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "Report file not found."

@app.route('/robot_framework/reports/logs')
def serve_logs():
    logs_dir = os.path.join(app.root_path, 'robot_framework', 'reports')
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
    init_db()
    app.run(host='0.0.0.0', port=5000)



