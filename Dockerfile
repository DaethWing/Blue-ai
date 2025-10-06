FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    curl \
    nodejs \
    npm \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend and install dependencies
COPY backend/ ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy and build frontend
COPY frontend/ ./frontend/
WORKDIR /app/frontend
RUN npm install && npm run build

# Collect static frontend build into /app/static
WORKDIR /app
RUN mkdir -p static && cp -r frontend/dist/* static/

# Environment variables
ENV DATA_DIR=/app/data \
    OPENAI_MODEL=gpt-4o-mini \
    OPENAI_AUDIO_MODEL=whisper-1

EXPOSE 10000

# Start FastAPI backend
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "10000"]
