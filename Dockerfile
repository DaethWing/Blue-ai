FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 curl nodejs npm && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY ./backend /app/backend
RUN pip install --no-cache-dir -r /app/backend/requirements.txt
COPY ./frontend /app/frontend
WORKDIR /app/frontend
RUN npm install && npm run build
WORKDIR /app
RUN mkdir -p static && cp -r /app/frontend/dist/* /app/static/
ENV DATA_DIR=/app/data OPENAI_MODEL=gpt-4o-mini OPENAI_AUDIO_MODEL=whisper-1
EXPOSE 10000
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "10000"]
