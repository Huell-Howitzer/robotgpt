# Use the base Ubuntu image
FROM ubuntu:20.04

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory
WORKDIR /app

# Install Python and pip
RUN apt-get update && apt-get install -y python3.10 python3-pip sqlite3 libsqlite3-dev

# Create a symbolic link for Python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Copy the necessary files
COPY requirements.txt .
COPY docs/build /app/templates/docs
COPY flask_app/engine /app/engine
COPY flask_app /app/flask_app
COPY flask_app/robot_framework/data /app/data
COPY flask_app/.env .
COPY flask_app/config.py .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the necessary port
EXPOSE 5000

# Set up the volume for live code reloading
VOLUME /app

# Set the entry point and command to start the Flask app
CMD ["python", "-m", "flask_app.app"]

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog
