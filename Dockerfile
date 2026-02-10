# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy your code
COPY . .

# Install OS dependencies + Rust + build tools + Python packages
RUN apt-get update && \
    apt-get install -y build-essential curl gcc rustc cargo && \
    python -m pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
