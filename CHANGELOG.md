# Changelog

## [1.1.0] - Multi-Model Support & UV Integration

### Added
- **Multi-Model Support**: Choose between OpenAI, Google Gemini, or Groq
- **UV Package Manager**: 10-100x faster than pip, with `uv run` for instant script execution
- **Environment-based Configuration**: Simple `.env` file configuration
- **Model Configuration Module**: `backend/config.py` for centralized model management
- **Configuration Test Script**: `backend/test_config.py` to verify setup
- **Comprehensive Guides**: 
  - `MODEL_SETUP.md` - Setup instructions for all providers
  - `UV_GUIDE.md` - Complete UV usage guide
  - `QUICK_START.md` - 5-minute setup guide

### Changed
- **Migrated to UV**: All Python package management now uses UV
- Updated `ResearcherAgent` to use dynamic model configuration
- Updated `CritiqueAgent` to use dynamic model configuration
- Updated `IdeaForge` orchestrator to initialize without hardcoded model
- Enhanced startup logging to show which model is being used
- Updated `requirements.txt` to include Gemini and Groq dependencies
- Added `pyproject.toml` for modern Python packaging
- Updated all documentation to use UV commands

### Configuration
Set ONE of these to `true` in `backend/.env`:
- `USE_OPENAI=true` - Use OpenAI GPT models
- `USE_GEMINI=true` - Use Google Gemini models
- `USE_GROQ=true` - Use Groq models (Llama, Mixtral)

### Migration from v1.0.0
If you were using the original version with hardcoded OpenAI:

1. Update `backend/.env`:
   ```bash
   USE_OPENAI=true
   OPENAI_API_KEY=your_existing_key
   OPENAI_MODEL=gpt-4o
   ```

2. No code changes needed - everything is backward compatible!

## [1.0.0] - Initial Release

### Features
- Two-stage agentic system (Researcher + Critique)
- Independent Mode: Problem discovery from Reddit/blogs
- Depth Mode: Iterative refinement with scoring
- Next.js frontend with real-time updates
- FastAPI backend with SSE streaming
- Serper API integration for web search
- CLI interface for headless usage
- Docker support
