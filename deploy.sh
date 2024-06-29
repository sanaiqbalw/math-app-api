#!/bin/bash

# Build the Docker image
docker build -t math-app-api:latest .

# Set port from input argument or environment variable, or default to 8000
if [ -n "$1" ]; then
  PORT=$1
elif [ -n "$PORT" ]; then
  PORT=$PORT
else
  PORT=8000
fi

# Run the Docker container with dynamic port mapping
docker run -d -p $PORT:$PORT --name math-app-api-con -e PORT=$PORT math-app-api

echo "Math app API is now running on http://localhost:$PORT/pvalue/"

# Check if the API is running
sleep 5 
curl -X 'GET' "http://localhost:$PORT/" -H 'accept: application/json'