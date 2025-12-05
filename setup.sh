#!/bin/bash

echo "🔥 Setting up Idea Forge..."

# Check for required tools
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed."; exit 1; }

# Setup frontend
echo "📦 Installing frontend dependencies..."
npm install

# Setup backend
echo "🐍 Setting up Python backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
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
echo "1. Add your API keys to .env and backend/.env"
echo "   - OPENAI_API_KEY"
echo "   - SERPER_API_KEY (get one at https://serper.dev)"
echo ""
echo "2. Start the backend:"
echo "   cd backend && source venv/bin/activate && python main.py"
echo ""
echo "3. Start the frontend (in another terminal):"
echo "   npm run dev"
echo ""
echo "4. Open http://localhost:3000"
