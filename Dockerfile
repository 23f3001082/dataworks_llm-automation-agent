# Use official Python 3.10 slim image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Install Node.js, npm, and Prettier globally
RUN apt update && apt install -y nodejs npm && npm install -g prettier

# Copy the rest of the application code
COPY . .

# Expose FastAPI's default port
EXPOSE 8000

# Command to start the FastAPI server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]