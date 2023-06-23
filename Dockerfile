# Use the base Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the necessary files
COPY requirements.txt .
COPY docs/build /app/templates/docs
COPY flask_app/engine /app/engine
COPY flask_app /app/flask_app
COPY flask_app/robot_framework/data /app/data
COPY flask_app/.env .
COPY flask_app/config.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the necessary port
EXPOSE 5000

# Set the entry point and command to start the Flask app
CMD ["python", "-m", "flask_app.app"]