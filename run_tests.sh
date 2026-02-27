#!/bin/bash
# Test runner script for Baby Monitor integration
# This script runs all tests and displays results

set -e  # Exit on error

echo "🧪 Running Baby Monitor Integration Tests..."
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "${YELLOW}Virtual environment not found. Creating one...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    echo "${YELLOW}Installing test dependencies...${NC}"
    pip install -q -r requirements-dev.txt
else
    source venv/bin/activate
fi

# Ensure dependencies are installed
if ! python -c "import pytest" 2>/dev/null; then
    echo "${YELLOW}Installing test dependencies...${NC}"
    pip install -q -r requirements-dev.txt
fi

echo "📋 Running pytest..."
echo ""

# Run pytest with coverage
if pytest tests/ --cov=custom_components/babymonitor --cov-report=term-missing --cov-report=html -v; then
    echo ""
    echo "${GREEN}✅ All tests passed!${NC}"
    echo ""
    echo "📊 Coverage report generated in htmlcov/index.html"
    exit 0
else
    echo ""
    echo "${RED}❌ Tests failed!${NC}"
    echo ""
    echo "Please fix the failing tests before pushing."
    exit 1
fi
