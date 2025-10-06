# ---------- Base image ----------
FROM python:3.11-slim

# ---------- System dependencies ----------
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 curl nodejs npm \
 && rm -rf /var/lib/apt/lists/*

# ---------- Set working directory ----------
WORKDIR /app

# ---------- Copy and install backend ----------
COPY ./backend /app/backend
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# ---------- Copy and build frontend ----------
COPY ./frontend /app/frontend
WORKDIR /app/frontend
RUN npm install && npm run build

# ---------- Move build to static folder ----------
WORKDIR /app
RUN mkdir -p /app/static && cp -r /app/frontend/dist/* /app/static/

# (Optional) List static files for debugging
RUN ls -R /app/static

# ---------- Environment variables ----------
ENV DATA_DIR=/app/data \
    OPENAI_MODEL=gpt-4o-mini \
    OPENAI_AUDIO_MODEL=whisper-1

# ---------- Expose port ----------
EXPOSE 10000

# ---------- Start FastAPI server ----------
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "10000"]
