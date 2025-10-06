import os, subprocess, tempfile
from typing import List, Dict
from .storage import save_clip

FFMPEG = os.environ.get("FFMPEG_BIN", "ffmpeg")

def run_ffmpeg(args: List[str]):
    cmd = [FFMPEG, "-y", *args]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="ignore"))

def convert_ratio(in_path: str, ratio: str) -> str:
    w, h = probe_resolution(in_path)
    tw, th = map(int, ratio.split(":"))
    target = tw / th
    src = w / h
    if src > target:
        new_w = int(h * target)
        x = (w - new_w) // 2
        vf = f"crop={new_w}:{h}:{x}:0,scale={new_w}:{h}"
    else:
        new_h = int(w / target)
        y = (h - new_h) // 2
        vf = f"crop={w}:{new_h}:0:{y},scale={w}:{new_h}"
    tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    run_ffmpeg(["-i", in_path, "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-c:a", "aac", tmp])
    return tmp

def probe_resolution(path: str):
    import json, subprocess
    p = subprocess.run([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=width,height", "-of", "json", path
    ], stdout=subprocess.PIPE)
    j = json.loads(p.stdout.decode())
    w = j["streams"][0]["width"]
    h = j["streams"][0]["height"]
    return w, h

def cut_segment(src: str, start: float, end: float) -> str:
    duration = max(0.1, end - start)
    tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    run_ffmpeg(["-ss", str(start), "-i", src, "-t", str(duration), "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-c:a", "aac", tmp])
    return tmp

def burn_captions(in_path: str, srt_path: str) -> str:
    tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    run_ffmpeg(["-i", in_path, "-vf", f"subtitles='{srt_path}':force_style='Fontsize=24,PrimaryColour=&H00FFFFFF&'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-c:a", "aac", tmp])
    return tmp

def build_srt(transcript_segments: List[Dict], start: float, end: float) -> str:
    def fmt(t):
        ms = int((t - int(t)) * 1000)
        s = int(t) % 60
        m = (int(t) // 60) % 60
        h = int(t) // 3600
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    lines = []
    idx = 1
    for seg in transcript_segments or []:
        s0, s1 = seg.get("start", 0), seg.get("end", 0)
        if s1 < start or s0 > end:
            continue
        rs = max(0, s0 - start)
        re = max(rs + 0.4, min(end - start, s1 - start))
        text = seg.get("text", "").replace("\n", " ").strip()
        if not text:
            continue
        lines.append(f"{idx}\n{fmt(rs)} --> {fmt(re)}\n{text}\n\n")
        idx += 1
    tmp = tempfile.NamedTemporaryFile(suffix=".srt", delete=False, mode="w", encoding="utf-8")
    tmp.write("".join(lines) or "1\n00:00:00,000 --> 00:00:02,000\n\n")
    tmp.close()
    return tmp.name
