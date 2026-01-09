from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

# Import our working modules
try:
    from transcription import transcribe_video
    from broll_analysis import analyze_multiple_broll
    from planner import generate_edit_plan
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from transcription import transcribe_video
    from broll_analysis import analyze_multiple_broll
    from planner import generate_edit_plan


# Load environment variables
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
async def health():
    return {"status": "online", "mode": "REAL AI"}

@app.post("/process")
async def process_video(
    a_roll: UploadFile = File(...),
    b_rolls: List[UploadFile] = File(...),
    similarity_threshold: float = 0.4,
    min_gap: float = 8.0
):
    try:
        # Save A-roll
        a_roll_path = UPLOAD_DIR / f"aroll_{a_roll.filename}"
        with open(a_roll_path, "wb") as f:
            shutil.copyfileobj(a_roll.file, f)

        # Save B-rolls
        broll_paths = []
        for clip in b_rolls:
            broll_path = UPLOAD_DIR / f"broll_{clip.filename}"
            with open(broll_path, "wb") as f:
                shutil.copyfileobj(clip.file, f)
            broll_paths.append(str(broll_path))

        # REAL AI MODE
        print("🤖 RUNNING IN REAL AI MODE")
        print(f"DEBUG: Processing A-roll: {a_roll.filename}, B-rolls: {[b.filename for b in b_rolls]}")
        transcript = transcribe_video(str(a_roll_path))
        print(f"DEBUG: Transcription complete. Got {len(transcript)} segments.")
        
        broll_desc = analyze_multiple_broll(broll_paths)
        print(f"DEBUG: B-roll analysis complete. Analyzed {len(broll_desc)} clips.")
        
        edl = generate_edit_plan(
            transcript, 
            broll_desc, 
            similarity_threshold=similarity_threshold, 
            min_gap=min_gap
        )
        print(f"DEBUG: EDL generation complete. {len(edl.get('edits', []))} edits found.")
        return edl

    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
