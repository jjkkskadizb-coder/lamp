#!/bin/bash
# Startup script for Railway

echo "🚀 Starting Indian Oil Lamp Server..."
echo "📍 Running on port: ${PORT:-8000}"
echo "🪔 The lamp is lighting up..."

# Run the Python script with python3
python3 oil_lamp.py
