# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first (caching layer)
COPY requirements.txt .

# Install OS dependencies + Rust + build tools + Python packages
RUN apt-get update && \
    apt-get install -y build-essential curl gcc rustc cargo && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the default port (not mandatory, but good practice)
EXPOSE 8000

# Start command using Railway dynamic $PORT
# Note: string format, not list format, to expand $PORT
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
