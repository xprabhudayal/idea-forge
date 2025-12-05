#!/usr/bin/env python3
"""Test script to verify model configuration."""
import os
from dotenv import load_dotenv

load_dotenv()

def test_config():
    """Test the model configuration."""
    print("🔍 Testing Idea Forge Configuration\n")
    print("=" * 50)
    
    # Check Serper API
    serper_key = os.getenv("SERPER_API_KEY")
    if serper_key:
        print("✅ SERPER_API_KEY: Set")
    else:
        print("❌ SERPER_API_KEY: Not set (REQUIRED)")
    
    print("\n" + "=" * 50)
    print("Model Configuration:")
    print("=" * 50)
    
    # Check which model is enabled
    use_openai = os.getenv("USE_OPENAI", "false").lower() == "true"
    use_gemini = os.getenv("USE_GEMINI", "false").lower() == "true"
    use_groq = os.getenv("USE_GROQ", "false").lower() == "true"
    
    enabled_count = sum([use_openai, use_gemini, use_groq])
    
    if enabled_count == 0:
        print("❌ No model enabled!")
        print("   Set one of USE_OPENAI, USE_GEMINI, or USE_GROQ to true")
        return False
    
    if enabled_count > 1:
        print("❌ Multiple models enabled!")
        print("   Only one should be true:")
        if use_openai: print("   - USE_OPENAI=true")
        if use_gemini: print("   - USE_GEMINI=true")
        if use_groq: print("   - USE_GROQ=true")
        return False
    
    # Check OpenAI
    if use_openai:
        print("\n🤖 Provider: OpenAI")
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-4o")
        print(f"   Model: {model}")
        if api_key:
            print(f"   API Key: {api_key[:10]}...{api_key[-4:]}")
            print("   ✅ Configuration valid")
        else:
            print("   ❌ OPENAI_API_KEY not set")
            return False
    
    # Check Gemini
    elif use_gemini:
        print("\n🤖 Provider: Google Gemini")
        api_key = os.getenv("GEMINI_API_KEY")
        model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
        print(f"   Model: {model}")
        if api_key:
            print(f"   API Key: {api_key[:10]}...{api_key[-4:]}")
            print("   ✅ Configuration valid")
        else:
            print("   ❌ GEMINI_API_KEY not set")
            return False
    
    # Check Groq
    elif use_groq:
        print("\n🤖 Provider: Groq")
        api_key = os.getenv("GROQ_API_KEY")
        model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        print(f"   Model: {model}")
        if api_key:
            print(f"   API Key: {api_key[:10]}...{api_key[-4:]}")
            print("   ✅ Configuration valid")
        else:
            print("   ❌ GROQ_API_KEY not set")
            return False
    
    print("\n" + "=" * 50)
    print("✅ Configuration test passed!")
    print("=" * 50)
    
    # Try to import and initialize
    print("\n🔧 Testing model initialization...")
    try:
        from config import get_model_config, get_model_name
        model, model_id = get_model_config()
        print(f"✅ Successfully initialized: {model_id}")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize model: {e}")
        return False


if __name__ == "__main__":
    success = test_config()
    exit(0 if success else 1)
