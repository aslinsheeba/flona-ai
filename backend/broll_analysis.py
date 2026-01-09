"""
B-roll analysis module
Generates descriptions for B-roll clips using Gemini
"""

import os
from typing import List, Dict
from pathlib import Path
from gemini_client import get_model

def analyze_broll_clip(clip_path: str) -> Dict[str, str]:
    """
    Analyze a B-roll clip and generate description
    
    For MVP: Uses filename + optional LLM enhancement
    In production: Could use vision models to analyze actual video content
    
    Args:
        clip_path: Path to the B-roll video file
        
    Returns:
        Dictionary with clip_name and description
    """
    clip_name = Path(clip_path).name
    
    # Extract meaningful description from filename
    # Remove extension and replace separators
    base_description = Path(clip_path).stem.replace("_", " ").replace("-", " ")
    
    # Enhance description using LLM
    try:
        enhanced_description = enhance_description_with_llm(base_description)
    except:
        # Fallback to filename-based description
        enhanced_description = base_description
    
    return {
        "clip_name": clip_name,
        "description": enhanced_description
    }


def enhance_description_with_llm(base_description: str) -> str:
    """
    Use Gemini to enhance and expand clip description
    
    Args:
        base_description: Basic description from filename
        
    Returns:
        Enhanced, detailed description
    """
    try:
        # Use a more stable model identifier
        model = get_model("gemini-flash-latest")
        
        prompt = f"""
        You are a video editor assistant. Given a brief video clip name, 
        expand it into a detailed 1-2 sentence description of what the clip 
        likely contains. Focus on visual elements, mood, and context.
        
        Clip name: {base_description}
        """
        
        print(f"DEBUG: Enhancing description for: {base_description}...")
        response = model.generate_content(prompt)
        desc = response.text.strip()
        print(f"DEBUG: Enhanced to: {desc[:50]}...")
        return desc
    
    except Exception as e:
        print(f"Error enhancing description: {e}")
        # Fallback to original description
        return base_description


def analyze_multiple_broll(clip_paths: List[str]) -> List[Dict[str, str]]:
    """
    Analyze multiple B-roll clips
    
    Args:
        clip_paths: List of paths to B-roll video files
        
    Returns:
        List of clip analyses
    """
    analyses = []
    for clip_path in clip_paths:
        analysis = analyze_broll_clip(clip_path)
        analyses.append(analysis)
    
    return analyses
