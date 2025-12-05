# UV Guide for Idea Forge

This project uses [UV](https://github.com/astral-sh/uv) - an extremely fast Python package installer and resolver written in Rust.

## Why UV?

- ⚡ **10-100x faster** than pip
- 🔒 **Deterministic** dependency resolution
- 🎯 **Drop-in replacement** for pip/venv
- 🚀 **No compilation needed** - pre-built binaries
- 💾 **Disk space efficient** - shared package cache

## Installation

### macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### With Homebrew
```bash
brew install uv
```

### Verify Installation
```bash
uv --version
# Should show: uv 0.x.x
```

## Basic Usage

### Create Virtual Environment
```bash
cd backend
uv venv
# Creates .venv directory
```

### Install Dependencies
```bash
# From requirements.txt
uv pip install -r requirements.txt

# Or from pyproject.toml
uv sync

# Install single package
uv pip install agno
```

### Run Scripts (No Activation Needed!)
```bash
# Run directly with uv
uv run main.py
uv run cli.py independent --track "AI/ML"
uv run test_config.py

# This automatically:
# 1. Activates the virtual environment
# 2. Runs the script
# 3. Deactivates when done
```

### Traditional Activation (Optional)
```bash
# Activate manually if you prefer
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Then run normally
python main.py
```

## Common Commands

| Task | UV Command | Traditional |
|------|------------|-------------|
| Create venv | `uv venv` | `python -m venv venv` |
| Install deps | `uv pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Install package | `uv pip install agno` | `pip install agno` |
| Run script | `uv run main.py` | `source venv/bin/activate && python main.py` |
| List packages | `uv pip list` | `pip list` |
| Freeze deps | `uv pip freeze` | `pip freeze` |

## Project Structure

```
backend/
├── .venv/              # Virtual environment (created by uv venv)
├── .python-version     # Python version specification
├── pyproject.toml      # Project metadata & dependencies
├── requirements.txt    # Legacy format (still supported)
└── *.py               # Python files
```

## Workflow Examples

### First Time Setup
```bash
cd backend
uv venv                          # Create virtual environment
uv pip install -r requirements.txt  # Install dependencies
uv run test_config.py            # Test configuration
uv run main.py                   # Start server
```

### Daily Development
```bash
cd backend
uv run main.py                   # Just run - no activation needed!
```

### Adding New Dependencies
```bash
cd backend
uv pip install new-package       # Install
uv pip freeze > requirements.txt # Update requirements
```

### Using pyproject.toml (Recommended)
```bash
cd backend
# Edit pyproject.toml to add dependency
uv sync                          # Install all dependencies
```

## Advantages Over pip

### Speed Comparison
```
Installing 50 packages:
- pip:  ~45 seconds
- uv:   ~2 seconds  (22x faster!)
```

### Disk Space
UV uses a global cache, so packages are only downloaded once:
```
~/.cache/uv/
└── wheels/
    └── agno-1.0.0-py3-none-any.whl  # Shared across projects
```

### Deterministic Builds
UV resolves dependencies deterministically, ensuring:
- Same versions across all environments
- No "works on my machine" issues
- Reproducible builds

## Troubleshooting

### UV not found after installation
```bash
# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Or restart terminal
```

### Virtual environment not activating
```bash
# Don't need to activate! Just use:
uv run main.py

# But if you want to activate:
source .venv/bin/activate
```

### Package not found
```bash
# Clear cache and reinstall
uv cache clean
uv pip install -r requirements.txt
```

### Conflict with existing venv
```bash
# Remove old venv
rm -rf venv/

# Create new with UV
uv venv
uv pip install -r requirements.txt
```

## Migration from pip/venv

If you have an existing project with pip:

```bash
# 1. Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Remove old venv
rm -rf venv/

# 3. Create new with UV
uv venv

# 4. Install dependencies
uv pip install -r requirements.txt

# 5. Run your project
uv run main.py
```

## Best Practices

1. **Use `uv run`** for scripts - no activation needed
2. **Keep requirements.txt** for compatibility
3. **Use pyproject.toml** for modern Python projects
4. **Commit `.python-version`** to specify Python version
5. **Don't commit `.venv/`** - add to .gitignore

## Resources

- [UV Documentation](https://github.com/astral-sh/uv)
- [UV vs pip Comparison](https://github.com/astral-sh/uv#benchmarks)
- [Python Packaging Guide](https://packaging.python.org/)

## Quick Reference Card

```bash
# Setup
uv venv                    # Create virtual environment
uv pip install -r req.txt  # Install dependencies

# Run (no activation!)
uv run main.py            # Run script
uv run cli.py --help      # Run with args

# Manage packages
uv pip install package    # Add package
uv pip uninstall package  # Remove package
uv pip list              # List installed
uv pip freeze            # Show versions

# Sync from pyproject.toml
uv sync                  # Install all deps

# Cache management
uv cache clean           # Clear cache
uv cache dir             # Show cache location
```
