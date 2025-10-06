from pydantic import BaseModel
from typing import List, Optional

class ProcessRequest(BaseModel):
    file_id: str
    target_ratios: List[str] = ["9:16", "1:1", "16:9"]
    max_clips: int = 5
    clip_min_seconds: int = 20
    clip_max_seconds: int = 60
    burn_captions: bool = True
    style: str = "dynamic"

class StatusResponse(BaseModel):
    job_id: str
    status: str
    progress: float
    message: Optional[str] = None

class ClipMeta(BaseModel):
    id: str
    title: str
    ratio: str
    duration: float
    url: str
    transcript_excerpt: str
    hashtags: List[str]
