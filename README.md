# 🔥 Idea Forge

**AI-Powered Hackathon Idea Generator & Validator**

Inspired by [AI-Scientist](https://github.com/SakanaAI/AI-Scientist)'s iterative idea refinement approach, Idea Forge is a two-stage agentic system that helps you discover and validate winning hackathon ideas through targeted web research and critique-based refinement.

## 🎯 The Problem

Every hackathon, you face the same dilemma:
- Some events have descriptive problem statements
- Others require you to get creative and come up with your own ideas
- You end up iterating alone, gambling on what might be a "banger" winning project

**Idea Forge solves this** by automating the research and validation loop that experienced hackathon winners do naturally.

## ✨ Features

### Two Modes of Operation

**1. Independent Mode** 🔍
- Searches Reddit, HackerNews, and tech communities for real problems people face
- Identifies pain points and frustrations in your target domain
- Generates viable hackathon ideas based on actual user needs
- Perfect when you have a track but no specific problem statement

**2. Depth Mode** 🔄
A two-stage iterative process inspired by AI-Scientist:

| Stage | Agent | Role |
|-------|-------|------|
| 1 | **Researcher** | Searches for winning hackathon ideas on Devpost, social media, blogs |
| 2 | **Critique** | Evaluates ideas with strict scoring (1-10) across 6 dimensions |

The loop continues until:
- ✅ An idea meets your quality threshold (configurable 10-90%)
- ⏹️ You manually stop the process
- 🔄 Max iterations reached (returns best idea found)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Next.js Frontend                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Independent │  │   Depth     │  │  Threshold Slider   │  │
│  │    Mode     │  │    Mode     │  │     (1-9 → 10-90%)  │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Python Backend (Agno)                     │
│  ┌─────────────────────┐    ┌─────────────────────────────┐ │
│  │   Researcher Agent  │───▶│      Critique Agent         │ │
│  │  (Serper Web Search)│    │  (Scoring & Validation)     │ │
│  └─────────────────────┘    └─────────────────────────────┘ │
│              │                           │                   │
│              └───────────────────────────┘                   │
│                    Iterative Loop                            │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- [Serper API Key](https://serper.dev) (free tier available)
- [OpenAI API Key](https://platform.openai.com)

### Option 1: Setup Script
```bash
./setup.sh
```

### Option 2: Manual Setup
```bash
# Frontend
npm install

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Environment
cp .env.example .env
cp backend/.env.example backend/.env
# Edit both .env files with your API keys
```

### Running

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python main.py
# Server runs on http://localhost:8000

# Terminal 2: Frontend
npm run dev
# App runs on http://localhost:3000
```

### CLI Usage (No UI)
```bash
# Independent Mode
python backend/cli.py independent --track "AI/ML" --requirements "use computer vision"

# Depth Mode
python backend/cli.py depth \
  --track "FinTech" \
  --problem "Help college students manage their finances" \
  --threshold 7 \
  --max-iter 10
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | Yes |
| `SERPER_API_KEY` | Serper.dev API key for web search | Yes |
| `NEXT_PUBLIC_API_URL` | Backend URL (default: http://localhost:8000) | No |

### Threshold Slider

The threshold slider (1-9) maps to quality requirements:
- **1** = 10% (very lenient, accepts almost anything)
- **5** = 50% (balanced)
- **7** = 70% (recommended for competitive hackathons)
- **9** = 90% (very strict, only exceptional ideas pass)

## 📊 Scoring Dimensions

The Critique Agent evaluates ideas on 6 dimensions:

| Dimension | What it measures |
|-----------|------------------|
| **Innovation** | How novel and creative is this idea? |
| **Feasibility** | Can this be built in 24-48 hours? |
| **Impact** | Does this solve a meaningful problem? |
| **Demo Potential** | Will this wow judges in a 3-minute demo? |
| **Technical Depth** | Is there enough technical challenge? |
| **Market Fit** | Is there actual demand for this solution? |

## 🔌 API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/independent` | POST | Generate idea from problem discovery |
| `/api/depth` | POST | Start depth mode (SSE stream) |
| `/api/depth/stop` | POST | Stop current iteration |
| `/api/status` | GET | Get current forge status |

### Example Request
```bash
curl -X POST http://localhost:8000/api/independent \
  -H "Content-Type: application/json" \
  -d '{"track": "Healthcare", "requirements": "use AI for diagnosis"}'
```

## 📁 Project Structure

```
idea-forge/
├── app/                    # Next.js app router
├── components/             # React components
│   ├── ui/                 # shadcn/ui components
│   ├── ForgeInterface.tsx  # Main UI
│   └── IdeaCard.tsx        # Idea display card
├── backend/
│   ├── agents/
│   │   ├── researcher.py   # Stage 1: Web research
│   │   ├── critique.py     # Stage 2: Evaluation
│   │   └── forge.py        # Orchestrator
│   ├── tools/
│   │   └── serper.py       # Web search API
│   ├── prompts/            # Agent prompts
│   ├── main.py             # FastAPI server
│   └── cli.py              # CLI interface
└── lib/                    # Utilities
```

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a PR

## 📄 License

MIT

## 🙏 Acknowledgments

- [AI-Scientist](https://github.com/SakanaAI/AI-Scientist) for the iterative refinement inspiration
- [Agno](https://github.com/agno-agi/agno) for the agent framework
- [Serper](https://serper.dev) for the search API
- [shadcn/ui](https://ui.shadcn.com) for the UI components
