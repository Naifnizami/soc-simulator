FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src folder hierarchy
COPY src/ ./src/

# CRITICAL: This allows python to find 'utils', 'simulators'
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Run main.py which now lives in src/
CMD ["python", "src/main.py"]