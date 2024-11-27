# Use the official Python image from the Docker Hub
FROM python:3.12-slim AS python-base

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY backend/ .

# Install Node.js to build the React application
FROM node:20.18 AS node-base

# Set the working directory for the React app
WORKDIR /frontend

# Copy the React app source code
COPY frontend/ .

# Install dependencies and build the React app
RUN npm install && npm run build

# Use the Python base image to create the final image
FROM python-base

# Copy the built React app to the Django static files directory
COPY --from=node-base /frontend/build /app/public

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the application
CMD ["sh", "-c", "/app/app.sh"]