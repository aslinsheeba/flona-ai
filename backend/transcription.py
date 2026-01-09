"""
Transcription service using Google Gemini API
Extracts transcript with precise timestamps from A-roll video
"""

import os
import json
import time
from typing import List, Dict
import google.generativeai as genai
from gemini_client import get_model, configure_gemini

def transcribe_video(video_path: str) -> List[Dict[str, any]]:
    """
    Transcribe video using Google Gemini
    
    Args:
        video_path: Path to the video file
        
    Returns:
        List of transcript segments with start, end, and text
    """
    try:
        configure_gemini()
        
        # Upload file to Gemini
        print(f"DEBUG: Uploading {os.path.basename(video_path)} to Gemini...")
        uploaded_file = genai.upload_file(path=video_path)
        
        # Wait for processing
        print(f"DEBUG: Waiting for file {uploaded_file.name} to process...")
        max_retries = 30
        retry_count = 0
        while uploaded_file.state.name == "PROCESSING" and retry_count < max_retries:
            time.sleep(2)
            uploaded_file = genai.get_file(uploaded_file.name)
            retry_count += 1
            
        if uploaded_file.state.name == "FAILED":
            raise Exception("File upload to Gemini failed")
            
        # Try different model names as fallback
        models_to_try = [
            "gemini-flash-latest",
            "gemini-2.0-flash-lite",
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "gemini-pro"
        ]
        response = None
        last_error = None
        
        prompt = """
        ACT AS A PROFESSIONAL VIDEO EDITOR.
        Transcribe the spoken audio in this file.
        Output ONLY a valid JSON list of objects.
        Do not include any markdown formatting or explanation outside the JSON.
        
        Each object MUST have these fields:
        - "start": float (start time in seconds)
        - "end": float (end time in seconds)
        - "text": string (the transcribed text content)
        
        CRITICAL: Break the transcription into many small segments (roughly 5-8 seconds each).
        This allows for better B-roll placement.
        Ensuring timestamps are precise.
        """
        
        for model_name in models_to_try:
            try:
                print(f"DEBUG: Attempting transcription with model: {model_name}")
                model = get_model(model_name)
                response = model.generate_content(
                    [uploaded_file, prompt],
                    generation_config={"response_mime_type": "application/json"}
                )
                if response:
                    print(f"DEBUG: Successfully got response from {model_name}")
                    break
            except Exception as e:
                print(f"DEBUG: Model {model_name} failed: {e}")
                last_error = str(e)
                continue
                
        if not response:
            raise Exception(f"All models failed. Last error: {last_error}")
        
        # Parse JSON response
        try:
            segments = json.loads(response.text)
        except json.JSONDecodeError as e:
            text = response.text
            print(f"DEBUG: raw response text: {text[:200]}...")
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            segments = json.loads(text)
            
        # Validate segments structure
        validated_segments = []
        for seg in segments:
            if isinstance(seg, dict) and "start" in seg and "end" in seg and "text" in seg:
                validated_segments.append({
                    "start": float(seg["start"]),
                    "end": float(seg["end"]),
                    "text": str(seg["text"]).strip()
                })
                
        if not validated_segments:
            print("DEBUG: No valid segments found in JSON.")
            return [{
                "start": 0.0,
                "end": 10.0,
                "text": "Transcription produced no valid segments."
            }]

        print(f"DEBUG: Successfully extracted {len(validated_segments)} segments.")
        return validated_segments
    
    except Exception as e:
        print(f"DEBUG: Transcription error: {e}")
        return [{
            "start": 0.0,
            "end": 5.0,
            "text": f"Error during transcription: {str(e)}"
        }]


def format_transcript(segments: List[Dict[str, any]]) -> str:
    """
    Format transcript segments into readable text
    
    Args:
        segments: List of transcript segments
        
    Returns:
        Formatted transcript string
    """
    formatted = []
    for seg in segments:
        formatted.append(f"[{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text']}")
    return "\n".join(formatted)
