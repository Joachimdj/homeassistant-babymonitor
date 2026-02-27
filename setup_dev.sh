#!/bin/bash
# Setup script for development environment

echo "🔧 Setting up development environment..."
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements-dev.txt

echo ""
echo "✅ Development environment ready!"
echo ""
echo "📝 Next steps:"
echo "  1. Activate venv: source venv/bin/activate"
echo "  2. Run tests: ./run_tests.sh"
echo "  3. Check coverage: open htmlcov/index.html"
echo ""
echo "🎣 Pre-push hook is already installed and will run tests before every push."
echo ""
