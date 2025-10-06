from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Serve static files from /app/static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html for root and frontend routes
@app.get("/{full_path:path}")
def serve_frontend(full_path: str):
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend build not found. Please redeploy after building frontend."}
