import os, uuid, shutil
from typing import List

DATA_DIR = os.environ.get("DATA_DIR", "/app/data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
CLIPS_DIR = os.path.join(DATA_DIR, "clips")
ASSETS_DIR = os.path.join(DATA_DIR, "assets")

for d in (DATA_DIR, UPLOAD_DIR, CLIPS_DIR, ASSETS_DIR):
    os.makedirs(d, exist_ok=True)

class StoredFile:
    def __init__(self, id: str, path: str, name: str):
        self.id = id
        self.path = path
        self.name = name

def save_upload(fileobj, filename: str) -> StoredFile:
    fid = str(uuid.uuid4())
    out_path = os.path.join(UPLOAD_DIR, f"{fid}_{filename}")
    with open(out_path, "wb") as f:
        shutil.copyfileobj(fileobj, f)
    return StoredFile(id=fid, path=out_path, name=filename)

def save_clip(tmp_path: str, basename: str) -> str:
    cid = str(uuid.uuid4())
    out = os.path.join(CLIPS_DIR, f"{cid}_{basename}")
    shutil.move(tmp_path, out)
    return out

def list_clips() -> List[str]:
    return [os.path.join(CLIPS_DIR, f) for f in os.listdir(CLIPS_DIR) if f.lower().endswith((".mp4",".mov",".m4v"))]
