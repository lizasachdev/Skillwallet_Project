#!/bin/bash
echo "============================================================"
echo "  Multimodal Construction Intelligence Platform"
echo "  Skill Wallet Capstone Project 1"
echo "============================================================"
echo ""

# Start FastAPI backend
echo "[1/2] Starting FastAPI Backend on port 8000..."
uvicorn backend.main:app --reload --port 8000 &
BACKEND_PID=$!

sleep 2

# Start React frontend
echo "[2/2] Starting React Frontend on port 5173..."
cd frontend && npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers running:"
echo "   Backend API: http://localhost:8000"
echo "   Frontend UI: http://localhost:5173"
echo "   API Docs:    http://localhost:8000/api/docs"
echo ""

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
