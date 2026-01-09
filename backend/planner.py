"""
Edit planner - applies editor rules and generates EDL
Implements intelligent B-roll placement with reasoning
"""

import os
from typing import List, Dict
from matcher import find_best_match


def generate_edit_plan(
    transcript_segments: List[Dict],
    broll_clips: List[Dict],
    similarity_threshold: float = None,
    min_gap: float = None
) -> Dict:
    """
    Generate Edit Decision List (EDL) with intelligent B-roll placement
    
    Applies professional editor rules:
    1. Don't insert B-roll too frequently (minimum gap between edits)
    2. B-roll duration should not exceed segment duration
    3. Only insert if semantic similarity is above threshold
    4. Each decision must include reasoning
    
    Args:
        transcript_segments: List of transcript segments with start, end, text
        broll_clips: List of analyzed B-roll clips
        similarity_threshold: Minimum similarity score (default from env)
        min_gap: Minimum seconds between B-roll insertions (default from env)
        
    Returns:
        EDL dictionary with edits list
    """
    # Get thresholds from environment or use defaults
    if similarity_threshold is None:
        similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
    
    if min_gap is None:
        min_gap = float(os.getenv("MIN_GAP_BETWEEN_EDITS", "8.0"))
    
    edits = []
    last_edit_time = -min_gap  # Allow first edit at start
    
    for segment in transcript_segments:
        segment_start = segment['start']
        segment_duration = segment['end'] - segment['start']
        
        # Rule 1: Check minimum gap since last edit
        time_since_last_edit = segment_start - last_edit_time
        if time_since_last_edit < min_gap:
            continue  # Skip this segment - too soon after last edit
        
        # Find best matching B-roll
        print(f"DEBUG: Matching segment '{segment['text'][:50]}...'")
        best_clip, similarity, reason = find_best_match(
            segment['text'],
            broll_clips,
            threshold=similarity_threshold
        )
        
        print(f"DEBUG: Best match: {best_clip['clip_name'] if best_clip else 'NONE'} (Score: {similarity:.3f})")

        # If no match above threshold, skip
        if best_clip is None:
            print(f"DEBUG: Skipping - No match above threshold {similarity_threshold}")
            continue
        
        # Rule 2: B-roll duration should not exceed segment duration
        # Use 80% of segment duration to leave breathing room
        broll_duration = min(segment_duration * 0.8, segment_duration)
        
        # Ensure minimum duration of 2 seconds
        if broll_duration < 2.0:
            continue
        
        # Create edit decision
        edit = {
            "start_time": segment_start,
            "duration": round(broll_duration, 2),
            "b_roll_clip": best_clip['clip_name'],
            "reason": reason,
            "transcript_text": segment['text'][:100],  # Include excerpt for context
            "similarity_score": round(similarity, 3)
        }
        
        edits.append(edit)
        last_edit_time = segment_start + broll_duration
    
    # Generate EDL with metadata
    edl = {
        "metadata": {
            "total_segments": len(transcript_segments),
            "total_broll_clips": len(broll_clips),
            "edits_applied": len(edits),
            "similarity_threshold": similarity_threshold,
            "min_gap_seconds": min_gap
        },
        "edits": edits
    }
    
    return edl


def validate_edl(edl: Dict) -> bool:
    """
    Validate EDL structure and content
    
    Args:
        edl: Edit Decision List
        
    Returns:
        True if valid, raises exception otherwise
    """
    if "edits" not in edl:
        raise ValueError("EDL must contain 'edits' key")
    
    required_fields = ["start_time", "duration", "b_roll_clip", "reason"]
    
    for idx, edit in enumerate(edl["edits"]):
        for field in required_fields:
            if field not in edit:
                raise ValueError(f"Edit {idx} missing required field: {field}")
        
        if edit["duration"] <= 0:
            raise ValueError(f"Edit {idx} has invalid duration: {edit['duration']}")
        
        if edit["start_time"] < 0:
            raise ValueError(f"Edit {idx} has invalid start_time: {edit['start_time']}")
    
    return True
