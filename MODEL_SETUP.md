# Model Configuration Guide

Idea Forge supports three LLM providers: OpenAI, Google Gemini, and Groq. You can choose any one based on your needs.

## Quick Comparison

| Provider | Best For | Speed | Cost | Quality |
|----------|----------|-------|------|---------|
| **Groq** | Testing, rapid iteration | ⚡⚡⚡ Very Fast | 💰 Free tier | ⭐⭐⭐ Good |
| **Gemini** | Production, cost-effective | ⚡⚡ Fast | 💰💰 Cheap | ⭐⭐⭐⭐ Very Good |
| **OpenAI** | Best quality results | ⚡ Medium | 💰💰💰 Expensive | ⭐⭐⭐⭐⭐ Excellent |

## Setup Instructions

### Option 1: Groq (Recommended for Testing)

**Why Groq?** Free tier, extremely fast inference, good quality.

1. Get API Key:
   - Visit https://console.groq.com
   - Sign up for free account
   - Go to API Keys section
   - Create new API key

2. Configure `backend/.env`:
   ```bash
   SERPER_API_KEY=your_serper_key
   
   USE_OPENAI=false
   USE_GEMINI=false
   USE_GROQ=true
   
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

3. Available Groq Models:
   - `llama-3.3-70b-versatile` (recommended, balanced)
   - `llama-3.1-70b-versatile` (good alternative)
   - `mixtral-8x7b-32768` (large context window)
   - `gemma2-9b-it` (smaller, faster)

### Option 2: Google Gemini (Recommended for Production)

**Why Gemini?** Very affordable, fast, excellent quality, generous free tier.

1. Get API Key:
   - Visit https://ai.google.dev
   - Click "Get API key in Google AI Studio"
   - Create new API key

2. Configure `backend/.env`:
   ```bash
   SERPER_API_KEY=your_serper_key
   
   USE_OPENAI=false
   USE_GEMINI=true
   USE_GROQ=false
   
   GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxx
   GEMINI_MODEL=gemini-2.0-flash-exp
   ```

3. Available Gemini Models:
   - `gemini-2.0-flash-exp` (recommended, latest experimental)
   - `gemini-1.5-flash` (stable, fast)
   - `gemini-1.5-pro` (highest quality)
   - `gemini-1.5-flash-8b` (fastest, cheapest)

### Option 3: OpenAI (Best Quality)

**Why OpenAI?** Industry-leading quality, most reliable.

1. Get API Key:
   - Visit https://platform.openai.com
   - Sign up and add payment method
   - Go to API Keys section
   - Create new secret key

2. Configure `backend/.env`:
   ```bash
   SERPER_API_KEY=your_serper_key
   
   USE_OPENAI=true
   USE_GEMINI=false
   USE_GROQ=false
   
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
   OPENAI_MODEL=gpt-4o
   ```

3. Available OpenAI Models:
   - `gpt-4o` (recommended, best balance)
   - `gpt-4o-mini` (cheaper, faster)
   - `gpt-4-turbo` (previous generation)

## Switching Models

To switch between providers, just update your `backend/.env`:

```bash
# Switch from Groq to Gemini
USE_GROQ=false
USE_GEMINI=true
GEMINI_API_KEY=your_key_here
```

Then restart the backend:
```bash
# Stop the server (Ctrl+C)
# Start again with UV
cd backend
uv run main.py

# Or traditional way
source .venv/bin/activate
python main.py
```

You'll see: `✅ Idea Forge initialized with model: gemini-2.0-flash-exp`

## Cost Estimates (per 1000 ideas generated)

| Provider | Model | Estimated Cost |
|----------|-------|----------------|
| Groq | llama-3.3-70b | $0 (free tier) |
| Gemini | gemini-2.0-flash | ~$0.50 |
| Gemini | gemini-1.5-pro | ~$2.00 |
| OpenAI | gpt-4o-mini | ~$1.50 |
| OpenAI | gpt-4o | ~$15.00 |

*Estimates based on average token usage per idea generation cycle*

## Troubleshooting

### Error: "No model configured"
- Make sure ONE of `USE_OPENAI`, `USE_GEMINI`, or `USE_GROQ` is set to `true`

### Error: "Multiple models enabled"
- Only ONE provider should be `true`, set others to `false`

### Error: "API key not set"
- Check that you've set the correct API key variable for your chosen provider
- Make sure there are no extra spaces in the `.env` file

### Model not responding / slow
- **Groq**: Check rate limits on free tier
- **Gemini**: Try switching to `gemini-1.5-flash` for faster responses
- **OpenAI**: Check your account has credits

## Performance Tips

1. **For Development**: Use Groq (free + fast)
2. **For Testing Quality**: Use Gemini 2.0 Flash (cheap + good)
3. **For Production**: Use Gemini 1.5 Pro or GPT-4o (best quality)
4. **For Cost Optimization**: Use Gemini 1.5 Flash 8B (cheapest)

## API Rate Limits

| Provider | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Groq | 30 req/min | Higher limits |
| Gemini | 15 req/min | 1000+ req/min |
| OpenAI | N/A | Tier-based |
