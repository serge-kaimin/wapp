# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY backend/ .

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the application
CMD ["sh", "-c", "/app/app.sh"]