#!/bin/bash

echo "🔥 Setting up Idea Forge..."

# Check for required tools
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed."; exit 1; }

# Check for uv
if ! command -v uv >/dev/null 2>&1; then
    echo "📦 UV not found. Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "✅ UV installed: $(uv --version)"

# Setup frontend
echo "📦 Installing frontend dependencies..."
npm install

# Setup backend with UV
echo "🐍 Setting up Python backend with UV..."
cd backend
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
cd ..

# Create .env files if they don't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Created .env file - please add your API keys"
fi

if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "📝 Created backend/.env file - please add your API keys"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure your model in backend/.env"
echo "   Choose ONE provider (OpenAI, Gemini, or Groq)"
echo "   See MODEL_SETUP.md for detailed instructions"
echo ""
echo "2. Add your API keys to backend/.env"
echo "   - SERPER_API_KEY (required - get at https://serper.dev)"
echo "   - Your chosen model's API key (see MODEL_SETUP.md)"
echo ""
echo "3. Test your configuration:"
echo "   cd backend && source .venv/bin/activate && python test_config.py"
echo ""
echo "4. Start the backend:"
echo "   cd backend && source .venv/bin/activate && python main.py"
echo ""
echo "5. Start the frontend (in another terminal):"
echo "   npm run dev"
echo ""
echo "6. Open http://localhost:3000"
echo ""
echo "💡 Using UV for Python package management (faster than pip!)"
