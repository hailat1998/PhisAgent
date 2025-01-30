FROM python:3.10.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOST=0.0.0.0 \
    PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
    onnxruntime>=1.14.1 \
    -r requirements.txt

COPY . .

EXPOSE ${PORT}

# Use shell form to enable environment variable expansion
CMD uvicorn main:app --host ${HOST} --port ${PORT}