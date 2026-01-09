"""
Semantic matching engine using embeddings and cosine similarity
Matches transcript segments to B-roll clips with reasoning
"""

import os
import numpy as np
from typing import List, Dict, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from gemini_client import get_model, get_embedding as get_gemini_embedding


def get_embedding(text: str) -> List[float]:
    """
    Get embedding vector for text using Gemini API
    
    Args:
        text: Input text to embed
        
    Returns:
        Embedding vector as list of floats
    """
    try:
        return get_gemini_embedding(text)
    except Exception as e:
        print(f"Embedding error: {e}")
        # Return empty or random vector to prevent crash, though quality will trigger fallback
        return [0.0] * 768


def compute_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Compute cosine similarity between two embeddings
    
    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector
        
    Returns:
        Similarity score between 0 and 1
    """
    # Convert to numpy arrays and reshape for sklearn
    if not embedding1 or not embedding2:
        return 0.0
        
    # Ensure lengths match (Gemini embeddings are usually 768 dims)
    if len(embedding1) != len(embedding2):
        # Handle dimension mismatch if upgrading models gracefully
        min_len = min(len(embedding1), len(embedding2))
        embedding1 = embedding1[:min_len]
        embedding2 = embedding2[:min_len]
        
    vec1 = np.array(embedding1).reshape(1, -1)
    vec2 = np.array(embedding2).reshape(1, -1)
    
    similarity = cosine_similarity(vec1, vec2)[0][0]
    return float(similarity)


def find_best_match(
    segment_text: str,
    broll_clips: List[Dict[str, str]],
    threshold: float = 0.4
) -> Tuple[Dict[str, str] | None, float, str]:
    """
    Find best matching B-roll clip for a transcript segment
    
    Args:
        segment_text: Text from transcript segment
        broll_clips: List of B-roll clip analyses
        threshold: Minimum similarity threshold (Gemini scores might differ, lowered default slightly)
        
    Returns:
        Tuple of (best_clip, similarity_score, reason)
        Returns (None, 0.0, reason) if no match above threshold
    """
    if not broll_clips:
        return None, 0.0, "No B-roll clips available"
    
    # Get embedding for segment text
    segment_embedding = get_embedding(segment_text)
    
    # Compute similarities with all B-roll descriptions
    best_clip = None
    best_score = -1.0
    
    for clip in broll_clips:
        clip_embedding = get_embedding(clip['description'])
        similarity = compute_similarity(segment_embedding, clip_embedding)
        print(f"  - Clip '{clip['clip_name']}': {similarity:.3f}")
        
        if similarity > best_score:
            best_score = similarity
            best_clip = clip
    
    # Check if best match meets threshold
    if best_score < threshold:
        reason = f"No B-roll clip matched above threshold {threshold:.2f}. Best score: {best_score:.3f}"
        return None, best_score, reason
    
    # Generate reasoning
    reason = generate_match_reason(segment_text, best_clip['description'], best_score)
    
    return best_clip, best_score, reason


def generate_match_reason(segment_text: str, clip_description: str, similarity: float) -> str:
    """
    Generate human-readable reasoning for why a clip was matched
    
    Args:
        segment_text: Transcript segment text
        clip_description: B-roll clip description
        similarity: Similarity score
        
    Returns:
        Explanation string
    """
    try:
        model = get_model("gemini-flash-latest")
        
        prompt = f"""
        You are a video editor assistant. Explain in 1-2 sentences 
        why a specific B-roll clip is a good visual match for a spoken segment. 
        Be specific about thematic connections.
        
        Spoken text: "{segment_text}"
        B-roll clip: {clip_description}
        Similarity score: {similarity:.3f}
        
        Why is this a good match?
        """
        
        print(f"DEBUG: Generating match reason for similarity {similarity:.3f}...")
        response = model.generate_content(prompt)
        reasoning = response.text.strip()
        return f"{reasoning} (Similarity: {similarity:.3f})"
    
    except Exception as e:
        print(f"Reasoning generation error: {e}")
        # Fallback reasoning
        return f"Semantic match with similarity score {similarity:.3f}. " \
               f"The B-roll '{clip_description}' aligns with the spoken content about '{segment_text[:50]}...'"
