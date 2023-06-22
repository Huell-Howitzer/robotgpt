# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Change working directory to 'notes'
WORKDIR /app/notes

# Specify the command to run when the container starts
CMD [ "python", "howto.py" ]
