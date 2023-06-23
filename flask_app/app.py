import os
from flask import Flask, render_template, request, send_from_directory
from flask import send_file

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run', methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        # Handle the form submission and execute the engine here
        # You can access form data using request.form['input_name']
        # Perform the necessary logic to run the engine
        # Return the results or redirect to a results page

        # Example code to run the engine and return a result
        input_data = request.form['input_data']
        # Perform the engine execution logic with the input data
        result = "Program executed successfully!"

        return render_template('results.html', result=result)

    # If the method is GET, render the form to input data
    return render_template('run.html')


@app.route('/reports')
def serve_report():
    reports_dir = os.path.join(app.root_path, 'reports')
    filename = "report.html"
    file_path = os.path.join(reports_dir, filename)

    print("File Path:", file_path)  # Debug statement

    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "Report file not found."

# Serve Sphinx documentation
# Serve Sphinx documentation
# Serve Sphinx documentation
@app.route('/docs/<path:filename>')
def serve_docs(filename):
    docs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'docs', 'html')
    return send_from_directory(docs_dir, filename)

@app.route('/about')
def about():
    return "About Page"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
