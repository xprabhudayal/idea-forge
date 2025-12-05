# Quick Start Guide

Get Idea Forge running in 5 minutes!

## 1️⃣ Choose Your Model

Pick ONE provider based on your needs:

| If you want... | Choose | Why |
|----------------|--------|-----|
| 🆓 Free + Fast | **Groq** | Free tier, 30 req/min, good quality |
| 💰 Cheap + Good | **Gemini** | $0.50 per 1000 ideas, very fast |
| 🏆 Best Quality | **OpenAI** | Industry-leading, most reliable |

## 2️⃣ Get API Keys

### Groq (Recommended for Testing)
1. Go to https://console.groq.com
2. Sign up (free)
3. Create API key
4. Copy key starting with `gsk_...`

### Gemini (Recommended for Production)
1. Go to https://ai.google.dev
2. Click "Get API key"
3. Create API key
4. Copy key starting with `AIza...`

### OpenAI
1. Go to https://platform.openai.com
2. Add payment method
3. Create API key
4. Copy key starting with `sk-proj-...`

### Serper (Required for All)
1. Go to https://serper.dev
2. Sign up (free tier: 2500 searches)
3. Copy API key

## 3️⃣ Setup

**Install UV** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Setup project:**
```bash
# Clone or navigate to idea-forge
cd idea-forge

# Run setup script (installs UV if needed)
./setup.sh

# Configure backend/.env
nano backend/.env  # or use your editor
```

## 4️⃣ Configure backend/.env

### For Groq (Free):
```bash
SERPER_API_KEY=your_serper_key_here

USE_OPENAI=false
USE_GEMINI=false
USE_GROQ=true

GROQ_API_KEY=gsk_your_groq_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### For Gemini (Cheap):
```bash
SERPER_API_KEY=your_serper_key_here

USE_OPENAI=false
USE_GEMINI=true
USE_GROQ=false

GEMINI_API_KEY=AIza_your_gemini_key_here
GEMINI_MODEL=gemini-2.0-flash-exp
```

### For OpenAI (Best):
```bash
SERPER_API_KEY=your_serper_key_here

USE_OPENAI=true
USE_GEMINI=false
USE_GROQ=false

OPENAI_API_KEY=sk-proj-your_openai_key_here
OPENAI_MODEL=gpt-4o
```

## 5️⃣ Test Configuration

**With UV (Recommended):**
```bash
cd backend
uv run test_config.py
```

**Traditional way:**
```bash
cd backend
source .venv/bin/activate
python test_config.py
```

Should see: `✅ Configuration test passed!`

## 6️⃣ Run

**With UV (Recommended):**
```bash
# Terminal 1: Backend
cd backend
uv run main.py

# Terminal 2: Frontend
npm run dev
```

**Traditional way:**
```bash
# Terminal 1: Backend
cd backend
source .venv/bin/activate
python main.py

# Terminal 2: Frontend
npm run dev
```

## 7️⃣ Use

Open http://localhost:3000

### Independent Mode
1. Enter track: "AI/ML"
2. Click "Generate Idea"
3. Get idea based on real problems from Reddit

### Depth Mode
1. Enter track: "FinTech"
2. Enter problem: "Help students budget better"
3. Set threshold: 7 (70%)
4. Click "Start Forge"
5. Watch it iterate until it finds a winner!

## 🚀 CLI Usage

**With UV (Recommended):**
```bash
cd backend

# Independent mode
uv run cli.py independent --track "Healthcare" --requirements "use AI"

# Depth mode
uv run cli.py depth --track "EdTech" --problem "Make learning fun" --threshold 8
```

**Traditional way:**
```bash
cd backend
source .venv/bin/activate
python cli.py independent --track "Healthcare"
```

## 🐛 Troubleshooting

### "No module named 'agno'"
```bash
cd backend
uv pip install -r requirements.txt
# or
uv sync
```

### "No model configured"
Check `backend/.env` - ONE of USE_OPENAI/USE_GEMINI/USE_GROQ must be `true`

### "API key not set"
Make sure you copied the full API key with no spaces

### Backend won't start
```bash
cd backend
python test_config.py  # This will show what's wrong
```

## 📚 More Help

- **Model Setup**: See [MODEL_SETUP.md](./MODEL_SETUP.md)
- **Full Docs**: See [README.md](./README.md)
- **Issues**: Check [GitHub Issues](https://github.com/xprabhudayal/idea-forge/issues)
