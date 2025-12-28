from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Adventure Site Simulator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AdventureIn(BaseModel):
    title: str
    master_name: str
    master_telegram: Optional[str] = None
    discord: Optional[str] = None
    system: Optional[str] = None
    type_game: Optional[str] = None
    setting_genre: Optional[str] = None
    level: Optional[str] = None
    cost: Optional[str] = None
    date: str
    time: str
    duration: Optional[str] = None
    age_limit: Optional[str] = None
    warnings: Optional[str] = None
    tags: Optional[str] = None
    description: Optional[str] = None
    filled: Optional[str] = None

class Adventure(AdventureIn):
    id: int

# simple in-memory store
_adventures: List[Adventure] = []
_next_id = 1

@app.post("/adventures", response_model=Adventure)
def create_adventure(ad: AdventureIn):
    global _next_id
    adv = Adventure(id=_next_id, **ad.dict())
    _adventures.append(adv)
    _next_id += 1
    return adv

@app.get("/adventures/latest", response_model=Adventure)
def get_latest_adventure():
    if not _adventures:
        raise HTTPException(status_code=404, detail="No adventures")
    return _adventures[-1]

@app.get("/adventures", response_model=List[Adventure])
def list_adventures():
    return _adventures
