import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

_configured = False

def configure_gemini():
    """Configure Gemini API with key from environment"""
    global _configured
    if _configured:
        return

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Fallback to checking if user put it in .env under a different name if needed
        # But standardizing on GEMINI_API_KEY is best.
        print("Warning: GEMINI_API_KEY not found in environment variables.")
        return
        
    genai.configure(api_key=api_key)
    _configured = True

def get_model(model_name: str = "gemini-flash-latest"):
    """Get a generative model instance"""
    configure_gemini()
    print(f"DEBUG: get_model called with {model_name}")
    return genai.GenerativeModel(model_name)
    
def get_embedding(text: str, model: str = "models/text-embedding-004"):
    """Get text embedding"""
    configure_gemini()
    result = genai.embed_content(
        model=model,
        content=text,
        task_type="semantic_similarity"
    )
    return result['embedding']
