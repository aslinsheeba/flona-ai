# ✅ Setup and Testing Checklist

## Before Running the Application

### 1. Prerequisites Installed
- [ ] Python 3.9 or higher installed
  - Check: `python --version`
- [ ] Node.js 18 or higher installed
  - Check: `node --version`
- [ ] npm installed (comes with Node.js)
  - Check: `npm --version`
- [ ] Git installed (optional, for version control)
  - Check: `git --version`

### 2. OpenAI API Key
- [ ] Have OpenAI account
- [ ] Created API key at https://platform.openai.com/api-keys
- [ ] API key copied (starts with `sk-...`)
- [ ] Have billing set up (small amounts needed for testing)

### 3. Project Files
- [ ] All backend files present (9 files in `backend/`)
- [ ] All frontend files present (6 files in `frontend/`)
- [ ] Documentation files present (README, QUICKSTART, etc.)

---

## Backend Setup

### 4. Python Virtual Environment
- [ ] Navigated to `backend/` directory
  ```bash
  cd backend
  ```
- [ ] Created virtual environment
  ```bash
  python -m venv venv
  ```
- [ ] Activated virtual environment
  ```bash
  # Windows:
  venv\Scripts\activate
  
  # Mac/Linux:
  source venv/bin/activate
  ```
- [ ] See `(venv)` in terminal prompt

### 5. Install Python Dependencies
- [ ] Installed requirements
  ```bash
  pip install -r requirements.txt
  ```
- [ ] No error messages during installation
- [ ] All packages installed successfully

### 6. Environment Configuration
- [ ] Copied `.env.example` to `.env`
  ```bash
  copy .env.example .env
  ```
- [ ] Opened `.env` file in text editor
- [ ] Replaced `your_openai_api_key_here` with actual API key
  ```
  OPENAI_API_KEY=sk-your-actual-key-here
  ```
- [ ] Saved `.env` file

### 7. Test Backend (Optional)
- [ ] Run demo script without API calls
  ```bash
  python demo.py
  ```
- [ ] See formatted output with sample EDL
- [ ] No errors in output

---

## Frontend Setup

### 8. Install Node Dependencies
- [ ] Opened new terminal (keep backend terminal open)
- [ ] Navigated to `frontend/` directory
  ```bash
  cd frontend
  ```
- [ ] Installed npm packages
  ```bash
  npm install
  ```
- [ ] See `node_modules/` directory created
- [ ] No critical errors (warnings are OK)

---

## Running the Application

### 9. Start Backend Server
- [ ] In backend terminal (with venv active):
  ```bash
  python main.py
  ```
- [ ] See startup message:
  ```
  🚀 Starting AI Video Editor API on http://0.0.0.0:8000
  ```
- [ ] See Uvicorn running message
- [ ] No error about API key
- [ ] Server running on port 8000

### 10. Start Frontend Server
- [ ] In frontend terminal:
  ```bash
  npm run dev
  ```
- [ ] See Vite dev server message
- [ ] See URL: `http://localhost:3000`
- [ ] No port conflict errors

### 11. Open Application
- [ ] Opened browser (Chrome, Firefox, Edge)
- [ ] Navigated to `http://localhost:3000`
- [ ] See "AI Video Editor MVP" page
- [ ] See upload sections for A-roll and B-roll
- [ ] No console errors (F12 developer tools)

---

## Testing the Application

### 12. Prepare Test Files
- [ ] Have a video file with spoken audio (A-roll)
  - Supported: .mp4, .mov, .wav, .mp3
  - Duration: 30 seconds - 2 minutes (for testing)
  - Contains clear speech
- [ ] Have 2-5 video clips (B-roll)
  - Supported: .mp4, .mov, .avi
  - Named descriptively (e.g., `ocean_waves.mp4`)
  - Different subjects for variety

### 13. Upload A-roll
- [ ] Clicked "Choose File" under A-roll section
- [ ] Selected video file with speech
- [ ] Clicked "Upload & Transcribe" button
- [ ] See "Processing..." message
- [ ] Wait for completion (30-60 seconds)
- [ ] See success message: "✓ A-roll processed: X segments transcribed"
- [ ] No error messages

### 14. Upload B-roll
- [ ] Clicked "Choose Files" under B-roll section
- [ ] Selected multiple video clips (Ctrl/Cmd + click)
- [ ] Clicked "Upload & Analyze" button
- [ ] See "Analyzing..." message
- [ ] Wait for completion (10-30 seconds)
- [ ] See success message: "✓ B-roll analyzed: X clips processed"
- [ ] No error messages

### 15. Configure Parameters (Optional)
- [ ] Review similarity threshold (default: 0.7)
- [ ] Review minimum gap (default: 8.0 seconds)
- [ ] Adjust if desired (lower threshold = more matches)

### 16. Generate Edit Plan
- [ ] Clicked "🚀 Generate Edit Plan" button
- [ ] See "Generating EDL..." message
- [ ] Wait for completion (10-20 seconds)
- [ ] See "Edit Decision List (EDL)" section appear
- [ ] See summary with metadata
- [ ] See full JSON EDL
- [ ] See edit breakdown with individual edits
- [ ] Each edit has:
  - [ ] Start time and duration
  - [ ] B-roll clip name
  - [ ] Transcript excerpt
  - [ ] Reasoning explanation
  - [ ] Similarity score

### 17. Verify Results
- [ ] EDL has at least 1 edit (if not, lower threshold)
- [ ] Reasoning makes sense for each match
- [ ] Similarity scores are above threshold
- [ ] Timestamps look reasonable
- [ ] Can scroll through full JSON
- [ ] Edit breakdown is readable

---

## Troubleshooting

### 18. If Backend Fails to Start
- [ ] Check `.env` has valid OpenAI API key
- [ ] Verify virtual environment is activated
- [ ] Ensure port 8000 is not already in use
- [ ] Restart terminal and try again

### 19. If Frontend Fails to Start
- [ ] Check `node_modules/` exists
- [ ] Run `npm install` again if missing
- [ ] Ensure port 3000 is available
- [ ] Check backend is running first

### 20. If Upload Fails
- [ ] Check file format is supported
- [ ] Verify file size (Whisper has 25MB limit)
- [ ] Check backend terminal for error messages
- [ ] Ensure OpenAI API key is working

### 21. If No Edits Generated
- [ ] Lower similarity threshold to 0.5-0.6
- [ ] Check B-roll filenames are descriptive
- [ ] Verify A-roll has clear speech
- [ ] Try different B-roll clips
- [ ] Check backend logs for matching details

### 22. If API Errors Occur
- [ ] Verify API key is correct in `.env`
- [ ] Check OpenAI account has credits
- [ ] Restart backend server after `.env` changes
- [ ] Check internet connection

---

## Health Checks

### 23. Backend Health
- [ ] Visit `http://localhost:8000` in browser
- [ ] See JSON response with status: "online"
- [ ] Visit `http://localhost:8000/health`
- [ ] See `"openai_configured": true`

### 24. Frontend Health
- [ ] No console errors in browser (F12)
- [ ] Network tab shows successful API calls
- [ ] UI responds to button clicks
- [ ] File inputs work correctly

### 25. API Communication
- [ ] Backend terminal shows incoming requests
- [ ] Frontend network tab shows 200 status codes
- [ ] CORS errors are not present
- [ ] Responses contain expected data

---

## Final Validation

### 26. Complete Workflow Test
- [ ] Reset the application (click "Reset All")
- [ ] Upload new A-roll video
- [ ] Upload new B-roll clips
- [ ] Generate EDL with different parameters
- [ ] Verify consistent behavior
- [ ] All features work reliably

### 27. Documentation Review
- [ ] Read README.md for overview
- [ ] Review QUICKSTART.md for setup
- [ ] Check TECHNICAL.md for implementation details
- [ ] Understand WORKFLOW.md visualization
- [ ] Review PROJECT_SUMMARY.md for deliverables

### 28. Demo Preparation (Optional)
- [ ] Practice explaining the system
- [ ] Prepare sample videos for demonstration
- [ ] Understand AI reasoning process
- [ ] Can explain EDL output format
- [ ] Know how to troubleshoot common issues

---

## ✅ Ready for Submission!

If all items are checked, your AI Video Editor MVP is:
- ✅ Properly installed
- ✅ Configured correctly
- ✅ Running successfully
- ✅ Producing valid EDL outputs
- ✅ Ready for demonstration

---

## Quick Reference

### Start Servers
```bash
# Terminal 1 (Backend)
cd backend
venv\Scripts\activate  # Windows
python main.py

# Terminal 2 (Frontend)
cd frontend
npm run dev
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (FastAPI Swagger)
- **Health Check**: http://localhost:8000/health

### Common Commands
```bash
# Restart backend
Ctrl+C (stop)
python main.py (start)

# Restart frontend
Ctrl+C (stop)
npm run dev (start)

# Clear cache
Click "Reset All" button in UI
or
POST http://localhost:8000/api/reset
```

---

## Next Steps

After successful testing:
1. [ ] Document any issues encountered
2. [ ] Prepare demo video (optional)
3. [ ] Review code for understanding
4. [ ] Prepare to explain technical decisions
5. [ ] Ready for internship submission!

**Good luck! 🚀🎬**
