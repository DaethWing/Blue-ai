import os, uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from typing import Dict
from .models import ProcessRequest, StatusResponse, ClipMeta
from .storage import save_upload, save_clip, list_clips
from . import ai
from . import processing as fx

app = FastAPI(title="Opus-Style Auto Clips (Dark Blue)")

origins = [os.environ.get("FRONTEND_URL", "*"), "http://localhost:5173", "http://localhost:4173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = "/app/static"
if os.path.isdir(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

JOBS: Dict[str, Dict] = {}
CLIP_INDEX: Dict[str, ClipMeta] = {}

@app.post("/api/upload")
def upload(file: UploadFile = File(...)):
    sf = save_upload(file.file, file.filename)
    return {"file_id": sf.id, "filename": sf.name}

@app.post("/api/process", response_model=StatusResponse)
def process(req: ProcessRequest):
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"status": "queued", "progress": 0.0, "message": "Starting"}

    import threading
    def work():
        try:
            from .storage import UPLOAD_DIR, CLIPS_DIR
            path = None
            for f in os.listdir(UPLOAD_DIR):
                if f.startswith(req.file_id + "_"):
                    path = os.path.join(UPLOAD_DIR, f)
                    break
            if not path:
                raise FileNotFoundError("file not found")
            JOBS[job_id].update(status="transcribing", progress=0.1, message="Transcribing audio")
            transcript = ai.transcribe(path)

            JOBS[job_id].update(status="selecting", progress=0.35, message="Selecting highlights")
            segs = ai.select_highlights(transcript, req.max_clips, req.clip_min_seconds, req.clip_max_seconds)

            made = []
            for i, seg in enumerate(segs):
                s, e = float(seg.get("start", 0)), float(seg.get("end", 0))
                title = seg.get("title", f"Clip {i+1}")
                clip_tmp = fx.cut_segment(path, s, e)

                if req.burn_captions:
                    srt = fx.build_srt(transcript.get("segments", []), s, e)
                    clip_tmp = fx.burn_captions(clip_tmp, srt)

                for ratio in req.target_ratios:
                    ar_tmp = fx.convert_ratio(clip_tmp, ratio)
                    out_path = save_clip(ar_tmp, f"clip_{i+1}_{ratio.replace(':','x')}.mp4")
                    meta = ai.suggest_metadata(title + "\n" + seg.get("reason", ""))
                    clip_id = os.path.basename(out_path).split("_")[0]
                    url = f"/api/clip/{os.path.basename(out_path)}"
                    cm = ClipMeta(
                        id=clip_id,
                        title=meta.get("title", title),
                        ratio=ratio,
                        duration=max(0.1, e - s),
                        url=url,
                        transcript_excerpt=seg.get("reason", ""),
                        hashtags=meta.get("hashtags", [])
                    )
                    CLIP_INDEX[clip_id] = cm
                    made.append(cm)
                JOBS[job_id].update(progress=0.35 + 0.6 * ((i+1)/max(1,len(segs))))

            JOBS[job_id].update(status="done", progress=1.0, message=f"Generated {len(made)} clips")
        except Exception as e:
            JOBS[job_id].update(status="error", message=str(e))

    threading.Thread(target=work, daemon=True).start()
    return StatusResponse(job_id=job_id, status="queued", progress=0.0)

@app.get("/api/status/{job_id}", response_model=StatusResponse)
def status(job_id: str):
    j = JOBS.get(job_id)
    if not j:
        return JSONResponse(status_code=404, content={"error":"unknown job"})
    return StatusResponse(job_id=job_id, status=j["status"], progress=j.get("progress",0.0), message=j.get("message"))

@app.get("/api/clips")
def clips():
    from .storage import CLIPS_DIR
    out = []
    for f in os.listdir(CLIPS_DIR):
        if not f.lower().endswith((".mp4",".mov",".m4v")):
            continue
        clip_id = f.split("_")[0]
        meta = CLIP_INDEX.get(clip_id)
        url = f"/api/clip/{f}"
        out.append({"id": clip_id, "meta": meta.model_dump() if meta else None, "url": url})
    return out

@app.get("/api/clip/{filename}")
async def get_clip(filename: str):
    from .storage import CLIPS_DIR
    path = os.path.join(CLIPS_DIR, filename)
    if not os.path.isfile(path):
        return JSONResponse(status_code=404, content={"error":"not found"})
    return FileResponse(path, media_type="video/mp4")
