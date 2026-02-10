# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt .

# Install OS dependencies + Rust + build tools + Python packages
RUN apt-get update && \
    apt-get install -y build-essential curl gcc rustc cargo && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port (for local testing, optional in Railway)
EXPOSE 8000

# Start command using Railway dynamic PORT
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"

