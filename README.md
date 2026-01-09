# 🎬 AI-Powered Video Editor MVP

**An intelligent automated video editing system that uses AI to analyze talking-head videos, understand context, and automatically insert relevant B-roll footage with reasoning.**

---

## 🎯 Project Overview

This MVP demonstrates an AI-powered video editing pipeline that:

1. **Analyzes A-roll** (talking head video) using OpenAI Whisper for precise transcription with timestamps
2. **Analyzes B-roll** (stock clips) using GPT to generate semantic descriptions
3. **Semantic Matching** using embeddings and cosine similarity to find contextually relevant clips
4. **Intelligent Planning** that applies professional editor rules to decide when and where to insert B-roll
5. **Generates EDL** (Edit Decision List) in JSON format with **AI-generated reasoning** for every decision

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                      │
│  - A-roll upload                                             │
│  - B-roll multi-upload                                       │
│  - Parameter controls                                        │
│  - EDL viewer with reasoning                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST API
┌──────────────────────▼──────────────────────────────────────┐
│                   BACKEND (FastAPI)                          │
│                                                               │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │Transcription│  │   B-roll     │  │  Semantic       │    │
│  │   Service   │  │  Analysis    │  │  Matcher        │    │
│  │  (Whisper)  │  │   (GPT)      │  │ (Embeddings)    │    │
│  └─────────────┘  └──────────────┘  └─────────────────┘    │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         Edit Planner (Rule Engine)                   │    │
│  │  - Minimum gap enforcement                           │    │
│  │  - Duration constraints                              │    │
│  │  - Similarity threshold filtering                    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         EDL Generator with Reasoning                 │    │
│  │  - JSON output with timestamps                       │    │
│  │  - AI-generated explanations                         │    │
│  └─────────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │  OpenAI API    │
              │  - Whisper     │
              │  - GPT-3.5     │
              │  - Embeddings  │
              └────────────────┘
```

---

## 🧠 AI Reasoning Logic

### Why JSON EDL is the Core Output

The Edit Decision List (EDL) is the **single source of truth** for video editing decisions. Instead of directly rendering video (which is expensive and inflexible), the system outputs a **machine-readable, human-interpretable JSON document** that:

1. **Explains** every decision with AI-generated reasoning
2. Can be **reviewed** by human editors before rendering
3. Can be **modified** or **regenerated** with different parameters
4. Serves as **documentation** for the editing process
5. Can be **consumed** by any video editing software (Final Cut, Premiere, DaVinci Resolve)

### How AI Decisions Are Made

#### 1. **Transcription Phase**
```python
A-roll → Whisper API → Timestamped Segments
[
  {"start": 0.0, "end": 5.2, "text": "Today we're talking about space exploration"},
  {"start": 5.2, "end": 10.5, "text": "The Mars rover discovered something incredible"},
  ...
]
```

#### 2. **B-roll Analysis Phase**
```python
B-roll Filename → GPT Enhancement → Rich Description
"mars_rover_landscape.mp4" → "A sweeping panoramic view of the Martian 
landscape showing the rover traversing red rocky terrain under a dusty 
pink sky, conveying isolation and exploration."
```

#### 3. **Semantic Matching Phase**
```python
Segment Text → Embedding Vector (1536 dimensions)
B-roll Description → Embedding Vector (1536 dimensions)

Cosine Similarity = dot(vec1, vec2) / (||vec1|| * ||vec2||)

If similarity >= threshold (0.7):
  → GPT generates reasoning
  → "This B-roll of the Mars landscape perfectly complements the 
     spoken narrative about the rover's discoveries, providing 
     visual context to the space exploration theme."
```

#### 4. **Rule-Based Planning**

**Professional editor rules implemented:**

| Rule | Implementation | Why It Matters |
|------|---------------|----------------|
| **Minimum Gap** | 8 seconds between edits | Prevents jarring, too-frequent cuts |
| **Duration Constraint** | B-roll ≤ 80% of segment length | Ensures sync with narration |
| **Similarity Threshold** | Only insert if score ≥ 0.7 | Avoids irrelevant footage |
| **Breathing Room** | Leave space around edits | Natural pacing |

---

## 📋 EDL Output Format

```json
{
  "metadata": {
    "total_segments": 15,
    "total_broll_clips": 8,
    "edits_applied": 5,
    "similarity_threshold": 0.7,
    "min_gap_seconds": 8.0
  },
  "edits": [
    {
      "start_time": 5.2,
      "duration": 4.16,
      "b_roll_clip": "mars_rover_landscape.mp4",
      "reason": "This B-roll of the Mars landscape perfectly complements the spoken narrative about the rover's discoveries, providing visual context to the space exploration theme. (Similarity: 0.876)",
      "transcript_text": "The Mars rover discovered something incredible",
      "similarity_score": 0.876
    },
    ...
  ]
}
```

**Each edit entry contains:**
- `start_time`: When to begin B-roll overlay (seconds)
- `duration`: How long to show B-roll (seconds)
- `b_roll_clip`: Which clip to use
- `reason`: **AI-generated explanation** of why this match makes sense
- `transcript_text`: What was being said (for context)
- `similarity_score`: Confidence metric (0-1)

---

## 🚀 How to Run Locally

### Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **ffmpeg** (optional, for video rendering)

### Setup Instructions

#### 1. Clone and Navigate
```bash
cd flona-ai-editor
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-...
```

#### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

#### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```
Backend will run on `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
Frontend will run on `http://localhost:3000`

#### 5. Use the System

1. Open `http://localhost:3000` in your browser
2. Upload an A-roll video (talking head footage)
3. Upload B-roll clips (stock footage)
4. Adjust similarity threshold and gap settings if needed
5. Click **"Generate Edit Plan"**
6. Review the JSON EDL with AI reasoning

---

## 📁 Project Structure

```
flona-ai-editor/
├── backend/
│   ├── main.py               # FastAPI application
│   ├── transcription.py      # Whisper transcription service
│   ├── broll_analysis.py     # B-roll description generator
│   ├── matcher.py            # Semantic matching engine
│   ├── planner.py            # Edit planning with rules
│   ├── renderer.py           # Optional ffmpeg rendering
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example          # Environment template
│   └── uploads/              # Uploaded files (auto-created)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Minimal styling
│   ├── index.html           # HTML template
│   ├── vite.config.js       # Vite configuration
│   └── package.json         # Node dependencies
│
└── README.md                # This file
```

---

## 🎓 Key Technical Decisions

### 1. **Why Whisper for Transcription?**
- **Timestamp precision**: Returns segment-level timing data
- **Accuracy**: State-of-the-art speech recognition
- **Multi-language**: Works with various accents and languages

### 2. **Why Embeddings over Simple Keywords?**
- **Semantic understanding**: Matches concepts, not just words
- **Example**: "ocean waves" matches "beach sunset" semantically
- **Robustness**: Works even if exact words aren't spoken

### 3. **Why GPT for Reasoning?**
- **Human interpretability**: Clear explanations for stakeholders
- **Trust building**: Users understand WHY decisions were made
- **Debugging**: Easy to identify when matching goes wrong

### 4. **Why JSON EDL?**
- **Non-destructive**: Original files unchanged
- **Flexible**: Can regenerate with different parameters instantly
- **Portable**: Works with professional editing software
- **Debuggable**: Human-readable output

---

## 🔧 Configuration Options

Edit `.env` file to customize:

```bash
# OpenAI API Key (REQUIRED)
OPENAI_API_KEY=sk-your-key-here

# Server Settings
HOST=0.0.0.0
PORT=8000

# Matching Parameters
SIMILARITY_THRESHOLD=0.7      # Higher = stricter (0.0 - 1.0)
MIN_GAP_BETWEEN_EDITS=8.0     # Minimum seconds between B-rolls
```

---

## 🎯 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/upload-aroll` | POST | Upload A-roll, get transcript |
| `/api/upload-broll` | POST | Upload B-roll clips, get analyses |
| `/api/generate-edl` | POST | Generate Edit Decision List |
| `/api/status` | GET | Check processing status |
| `/api/reset` | POST | Clear cache and uploads |
| `/health` | GET | System health check |

---

## ⚡ Optional: Video Rendering

The system includes an **optional** ffmpeg-based renderer. To use it:

1. Install ffmpeg: `https://ffmpeg.org/download.html`
2. Use the `renderer.py` module to apply EDL to video files
3. This is NOT required for the MVP - EDL is the primary deliverable

---

## 🏆 Why This Architecture for an Internship

### Demonstrates:
1. **Full-stack skills**: Python backend + React frontend
2. **AI integration**: Practical use of OpenAI APIs
3. **System design**: Clean separation of concerns
4. **Product thinking**: EDL-first approach shows understanding of real workflows
5. **Code quality**: Modular, documented, testable

### Shows Understanding Of:
- **Video editing workflows**: Why editors need reasoning, not just automation
- **AI limitations**: Uses thresholds and rules to ensure quality
- **Scalability**: JSON EDL can be cached, shared, versioned
- **Production readiness**: Includes validation, error handling, status endpoints

---

## 🐛 Troubleshooting

**"OpenAI API key not configured"**
- Edit `.env` file with valid API key

**"Transcription failed"**
- Ensure video file is valid format (mp4, mov, wav)
- Check file size (Whisper API has 25MB limit)

**"No matches above threshold"**
- Lower `SIMILARITY_THRESHOLD` in .env
- Use more descriptive B-roll filenames
- Try different B-roll clips

**"CORS errors"**
- Ensure backend is running on port 8000
- Check Vite proxy configuration

---

## 📚 Future Enhancements

- [ ] Add video preview player
- [ ] Support for custom B-roll descriptions
- [ ] Real-time progress tracking
- [ ] Export to Final Cut Pro XML
- [ ] Batch processing multiple A-roll videos
- [ ] Visual similarity matching (using CLIP)
- [ ] Audio ducking for A-roll when B-roll plays
- [ ] User feedback loop to improve matching

---

## 📄 License

MIT License - Free for educational and commercial use

---

## 👨‍💻 Author

Built as an internship assignment demonstrating AI-powered video editing capabilities.

**Tech Stack**: Python • FastAPI • OpenAI API • React • Vite

---

## 🙏 Acknowledgments

- OpenAI for Whisper and GPT APIs
- FastAPI for elegant Python web framework
- React team for frontend framework
- ffmpeg for video processing capabilities

---

**🎬 Happy Editing!**
