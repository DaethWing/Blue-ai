import os, json
from typing import List, Dict
from openai import OpenAI

OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_AUDIO_MODEL = os.environ.get("OPENAI_AUDIO_MODEL", "whisper-1")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def transcribe(filepath: str) -> Dict:
    with open(filepath, "rb") as f:
        tr = client.audio.transcriptions.create(model=OPENAI_AUDIO_MODEL, file=f)
    text = tr.text
    segments = []
    if hasattr(tr, "segments") and tr.segments:
        segments = [{"start": s["start"], "end": s["end"], "text": s["text"]} for s in tr.segments]
    return {"text": text, "segments": segments}

def select_highlights(transcript: Dict, max_clips: int, min_len: int, max_len: int) -> List[Dict]:
    sys = "You pick the most viral moments for short social clips. Return JSON list of segments with start,end,title,reason."
    usr = {
        "instruction": {"max_clips": max_clips, "min_seconds": min_len, "max_seconds": max_len},
        "transcript": transcript
    }
    msg = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role":"system","content":sys},{"role":"user","content":json.dumps(usr)}],
        response_format={"type":"json_object"}
    )
    content = msg.choices[0].message.content
    try:
        data = json.loads(content)
        return data.get("segments", [])
    except Exception:
        total_dur = transcript.get("segments", [])[-1]["end"] if transcript.get("segments") else 120
        end = min(total_dur, max_len)
        return [{"start":0,"end":end,"title":"Clip","reason":"fallback"}]

def suggest_metadata(segment_text: str) -> Dict:
    sys = "You write catchy video titles and hashtags for shorts. Return JSON: {title, hashtags} (5-10 hashtags)."
    msg = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role":"system","content":sys},{"role":"user","content":segment_text}],
        response_format={"type":"json_object"}
    )
    return json.loads(msg.choices[0].message.content)
