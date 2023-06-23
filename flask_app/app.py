import os
from flask import Flask, render_template, request, send_from_directory


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    # Handle the form submission and execute the engine here
    # You can access form data using request.form['input_name']
    # Perform the necessary logic to run the engine
    # Return the results or redirect to a results page

    # Example code to run the engine and return a result
    input_data = request.form['input_data']
    # Perform the engine execution logic with the input data
    result = "Program executed successfully!"

    return render_template('results.html', result=result)

@app.route('/reports/report.html')
def serve_report():
    filename = "report.html"
    reports_dir = os.path.abspath(os.path.join(os.getcwd(), '..', 'reports'))
    return send_from_directory(reports_dir, filename)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



