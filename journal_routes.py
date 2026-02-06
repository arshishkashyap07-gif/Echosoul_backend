
from fastapi import APIRouter, Depends, HTTPException
from auth.auth_utils import get_current_user
from emotion.hybrid import analyze_text
from database import journals_collection
from datetime import datetime

router = APIRouter(prefix="/journal", tags=["Journal"])

@router.post("/add")
def add_journal(data: dict, user=Depends(get_current_user)):
    if len(data.get("text", "").strip()) < 5:
        raise HTTPException(status_code=400, detail="Journal too short")

    analysis = analyze_text(data["text"])

    entry = {
        "user_id": user["user_id"],
        "text": data["text"],
        "emotion": analysis["emotion"],
        "confidence": analysis["confidence"],
        "created_at": datetime.utcnow()
    }

    journals_collection.insert_one(entry)
    return entry

@router.get("/all")
def get_journals(user=Depends(get_current_user)):
    journals = list(journals_collection.find(
        {"user_id": user["user_id"]},
        {"_id": 0}
    ))
    return journals
