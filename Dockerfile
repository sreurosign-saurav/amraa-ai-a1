# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first (for faster caching)
COPY requirements.txt .

# Install OS deps, Rust & Python build tools, then Python packages
RUN apt-get update && \
    apt-get install -y build-essential curl gcc rustc cargo && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port (Railway uses dynamic $PORT)
EXPOSE 8000

# Start command (string format, not list) using Railway dynamic port
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
