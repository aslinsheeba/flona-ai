# Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Get Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Create a new API key
3. Copy it

### Step 2: Configure Backend
```bash
cd backend
copy .env.example .env
```

Edit `.env` and paste your API key:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 3: Install Dependencies

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate    # Windows
# OR
source venv/bin/activate # Mac/Linux

pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### Step 4: Run

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Step 5: Test

1. Open http://localhost:5173 (or the port Vite shows)
2. Upload a video with speech as A-roll
3. Upload 2-3 video clips as B-roll
4. Click "Generate Edit Plan"
5. See the JSON EDL with AI reasoning!

---

## 📝 Testing Tips

### Good A-roll Examples:
- Tutorial videos
- Product reviews
- Vlogs with narration
- Interview clips

### Good B-roll Examples:
Name files descriptively:
- `city_skyline_timelapse.mp4`
- `coffee_being_poured.mp4`
- `keyboard_typing_closeup.mp4`

The system uses filenames to understand content!

### Parameters to Try:

**Strict matching:**
- Similarity: 0.8
- Min Gap: 10s

**Relaxed matching:**
- Similarity: 0.6
- Min Gap: 5s

---

## ⚠️ Common Issues

**"Module not found"**
```bash
# Make sure virtual environment is activated
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

**"Port already in use"**
```bash
# Change port in .env
PORT=8001
```

**"No API key"**
- Double-check `.env` file has actual key
- Restart backend after editing .env

---

## 🎯 What Success Looks Like

After "Generate Edit Plan", you should see:

```json
{
  "metadata": {
    "edits_applied": 3,
    ...
  },
  "edits": [
    {
      "start_time": 5.2,
      "b_roll_clip": "coffee.mp4",
      "reason": "The B-roll of coffee being poured..."
    }
  ]
}
```

Each edit has:
- ✅ Timestamp
- ✅ B-roll filename
- ✅ **AI reasoning explanation**
- ✅ Similarity score

---

## 📊 Expected Performance

- **A-roll transcription**: ~10-20 seconds with Gemini 1.5 Flash
- **B-roll analysis**: ~3 seconds per clip
- **EDL generation**: ~5 seconds

**Cost estimate:**
- **Free** (within Gemini API free tier limits)
- Great for testing!

---

**Ready to Go? Start with Step 1! 🎬**
