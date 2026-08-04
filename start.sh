#!/bin/bash

echo "🚀 Starting Soccer 6v6 Simulator..."

# Check if running on Windows or Unix
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
  echo "Windows detected - please run backend and frontend manually:"
  echo "1. Terminal 1: cd backend && python app.py"
  echo "2. Terminal 2: cd frontend && npm start"
else
  echo "Starting backend..."
  cd backend
  python app.py &
  BACKEND_PID=$!
  
  sleep 2
  
  echo "Starting frontend..."
  cd ../frontend
  npm start &
  FRONTEND_PID=$!
  
  echo "✅ Both servers running!"
  echo "Backend: http://localhost:5000"
  echo "Frontend: http://localhost:3000"
  echo "Press Ctrl+C to stop both servers"
  
  # Wait for both processes
  wait $BACKEND_PID $FRONTEND_PID
fi
