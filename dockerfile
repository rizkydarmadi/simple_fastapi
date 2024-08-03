# Use the official Python image.
FROM python:3.11-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements file into the container.
COPY requirements.txt .

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container.
COPY . .

# Specify the command to run the FastAPI application.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
