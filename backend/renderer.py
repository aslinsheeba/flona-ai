"""
Optional: Video rendering using ffmpeg
Applies EDL to create final video with B-roll overlays
"""

import ffmpeg
import os
from typing import Dict, List
import subprocess
import json


def render_video_with_edl(
    aroll_path: str,
    broll_directory: str,
    edl: Dict,
    output_path: str
) -> str:
    """
    Render final video by overlaying B-roll clips according to EDL
    
    NOTE: This is an optional advanced feature
    Requires ffmpeg installed on system
    
    Args:
        aroll_path: Path to A-roll (talking head) video
        broll_directory: Directory containing B-roll clips
        edl: Edit Decision List
        output_path: Path for output video
        
    Returns:
        Path to rendered video
        
    Process:
    1. Extract A-roll audio
    2. For each edit in EDL, create overlay at specified timestamp
    3. Mute B-roll audio
    4. Composite final video
    """
    try:
        # Validate EDL
        if not edl.get("edits"):
            raise ValueError("EDL contains no edits")
        
        # Build ffmpeg filter complex for overlays
        filter_parts = []
        inputs = [ffmpeg.input(aroll_path)]
        
        # Add B-roll inputs
        broll_map = {}
        for idx, edit in enumerate(edl["edits"]):
            broll_path = os.path.join(broll_directory, edit["b_roll_clip"])
            if not os.path.exists(broll_path):
                print(f"Warning: B-roll not found: {broll_path}, skipping")
                continue
            
            broll_map[idx] = len(inputs)
            inputs.append(ffmpeg.input(broll_path))
        
        # Build complex filter for overlays
        # Note: This is a simplified version - production would need more sophisticated handling
        base_video = inputs[0].video
        
        for idx, edit in enumerate(edl["edits"]):
            if idx not in broll_map:
                continue
            
            broll_idx = broll_map[idx]
            start_time = edit["start_time"]
            duration = edit["duration"]
            
            # Overlay B-roll at specified time
            # Scale B-roll to match A-roll dimensions
            broll_video = inputs[broll_idx].video
            broll_video = broll_video.filter('scale', 1920, 1080)
            broll_video = broll_video.filter('setpts', f'PTS-STARTPTS+{start_time}/TB')
            
            # Overlay on base video
            base_video = ffmpeg.overlay(
                base_video,
                broll_video,
                enable=f'between(t,{start_time},{start_time + duration})'
            )
        
        # Add original audio from A-roll
        output = ffmpeg.output(
            base_video,
            inputs[0].audio,
            output_path,
            vcodec='libx264',
            acodec='aac'
        )
        
        # Run ffmpeg
        ffmpeg.run(output, overwrite_output=True)
        
        return output_path
    
    except Exception as e:
        raise Exception(f"Video rendering failed: {str(e)}")


def render_simple_overlay(
    aroll_path: str,
    broll_path: str,
    start_time: float,
    duration: float,
    output_path: str
) -> str:
    """
    Simple helper to overlay a single B-roll clip on A-roll
    Useful for testing
    
    Args:
        aroll_path: A-roll video path
        broll_path: B-roll video path  
        start_time: When to start overlay (seconds)
        duration: How long to show overlay (seconds)
        output_path: Output file path
        
    Returns:
        Path to output video
    """
    try:
        # Use subprocess for simpler ffmpeg command
        cmd = [
            'ffmpeg',
            '-i', aroll_path,
            '-i', broll_path,
            '-filter_complex',
            f'[1:v]scale=1920:1080,setpts=PTS-STARTPTS+{start_time}/TB[ovr];'
            f'[0:v][ovr]overlay=enable=\'between(t,{start_time},{start_time + duration})\'[v]',
            '-map', '[v]',
            '-map', '0:a',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-y',
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    
    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg rendering failed: {e.stderr.decode()}")


def export_edl_to_file(edl: Dict, output_path: str) -> str:
    """
    Export EDL to JSON file
    
    Args:
        edl: Edit Decision List
        output_path: Path to save JSON file
        
    Returns:
        Path to saved file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(edl, f, indent=2, ensure_ascii=False)
    
    return output_path
