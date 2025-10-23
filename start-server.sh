#!/bin/bash

echo "🚀 Starting Stripe M2 Reader Setup Server..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3"
    echo "   macOS: brew install python3"
    echo "   Ubuntu: sudo apt-get install python3"
    exit 1
fi

# Check if HTML file exists
if [ ! -f "index.html" ]; then
    echo "❌ index.html not found in current directory"
    echo "   Make sure this script is in the same folder as the HTML file"
    exit 1
fi

echo "✅ Python 3 found"
echo "✅ HTML file found"
echo
echo "Starting server on http://localhost:8000/"
echo

# Start the Python HTTP server
python3 serve.py
