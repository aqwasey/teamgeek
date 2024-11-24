# Use a lightweight Python image as the base
FROM python:3.11-alpine

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port on which the app will run
EXPOSE 5000

# Command to run the Flask app
CMD ["gunicorn", "serve:app", "-w", "4", "-b", "0.0.0.0:5000"]