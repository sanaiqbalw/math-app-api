
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Copy the entire project
COPY . /app/

# Run the FastAPI app using python app.py, using the PORT environment variable if set
CMD ["python", "app.py"]

