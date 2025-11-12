# ===============================
# Stage 1 — Build environment
# ===============================
FROM python:3.12-slim AS builder

# Set working directory inside container
WORKDIR /app

# Install system dependencies (for building Python packages if needed)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ===============================
# Stage 2 — Runtime environment
# ===============================
FROM python:3.12-slim

# Working directory for the app
WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy all backend source code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Start FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

