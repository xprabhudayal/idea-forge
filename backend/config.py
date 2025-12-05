"""Configuration module for model selection."""
import os
from typing import Tuple, Any
from dotenv import load_dotenv

load_dotenv()


def get_model_config() -> Tuple[Any, str]:
    """
    Get the configured model based on environment variables.
    
    Returns:
        Tuple of (client, model_id)
    
    Raises:
        ValueError: If no model is configured or multiple models are enabled
    """
    use_openai = os.getenv("USE_OPENAI", "false").lower() == "true"
    use_gemini = os.getenv("USE_GEMINI", "false").lower() == "true"
    use_groq = os.getenv("USE_GROQ", "false").lower() == "true"
    
    # Count how many are enabled
    enabled_count = sum([use_openai, use_gemini, use_groq])
    
    if enabled_count == 0:
        raise ValueError(
            "No model configured. Set one of USE_OPENAI, USE_GEMINI, or USE_GROQ to true in .env"
        )
    
    if enabled_count > 1:
        raise ValueError(
            "Multiple models enabled. Only one of USE_OPENAI, USE_GEMINI, or USE_GROQ should be true"
        )
    
    if use_openai:
        from agno.models.openai import OpenAIChat
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        model_id = os.getenv("OPENAI_MODEL", "gpt-4o")
        return OpenAIChat(id=model_id, api_key=api_key), model_id
    
    elif use_gemini:
        from agno.models.google import Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")
        model_id = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
        return Gemini(id=model_id, api_key=api_key), model_id
    
    elif use_groq:
        from agno.models.groq import Groq
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment")
        model_id = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        return Groq(id=model_id, api_key=api_key), model_id
    
    raise ValueError("Invalid model configuration")


def get_model_name() -> str:
    """Get the name of the currently configured model."""
    use_openai = os.getenv("USE_OPENAI", "false").lower() == "true"
    use_gemini = os.getenv("USE_GEMINI", "false").lower() == "true"
    use_groq = os.getenv("USE_GROQ", "false").lower() == "true"
    
    if use_openai:
        return os.getenv("OPENAI_MODEL", "gpt-4o")
    elif use_gemini:
        return os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    elif use_groq:
        return os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    return "unknown"
