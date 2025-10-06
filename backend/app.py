from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Serve static frontend build
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/api/health")
def health():
    return {"status": "ok"}
