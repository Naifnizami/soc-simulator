# Use Python
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire source code folder
COPY src/ ./src/

# Set Python Path so it finds the modules
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Command to run (overridden by compose, but good default)
CMD ["python", "src/main.py"]