# Soccer 6v6 Simulator - Setup Guide

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Aklettka/soccer-6v6.git
cd soccer-6v6
```

2. **Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
cd ..
```

3. **Install frontend dependencies**
```bash
cd frontend
npm install
cd ..
```

### Running the Application

**Option 1: Separate Terminals**

Terminal 1 (Backend):
```bash
cd backend
python app.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm start
```

**Option 2: Using start script (Unix/Linux/Mac)**
```bash
chmod +x start.sh
./start.sh
```

### Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api
- Health Check: http://localhost:5000/api/health

## Directory Structure

```
backend/
├── models/
│   ├── player.py      # Player data model
│   ├── team.py        # Team data model
│   └── match.py       # Match data model
├── engine/
│   ├── simulator.py   # Main match simulator
│   ├── calculations.py # Game calculations
│   └── commentary.py  # Live commentary generator
├── routes/
│   ├── players.py     # Player API endpoints
│   ├── teams.py       # Team API endpoints
│   └── match.py       # Match API endpoints
├── database/
│   └── db.py          # Database layer
├── app.py             # Flask application
├── config.py          # Configuration
└── requirements.txt    # Python packages

frontend/
├── src/
│   ├── pages/
│   │   ├── PlayerManager.tsx     # Manage players
│   │   ├── PlayerManager.css
│   │   ├── TeamBuilder.tsx       # Build teams
│   │   ├── TeamBuilder.css
│   │   ├── MatchSimulator.tsx    # Simulate matches
│   │   └── MatchSimulator.css
│   ├── App.tsx        # Main app component
│   ├── App.css        # App styling
│   ├── index.tsx      # React entry point
│   └── index.css      # Global styles
├── public/
│   └── index.html     # HTML template
└── package.json       # NPM packages
```

## Features Explained

### Player Management
- Create players with custom attributes
- 6 key attributes determine player behavior
- View and delete existing players

### Team Building
- Create teams and assign players
- Choose team formation and tactics
- Exactly 6 players per team (1 GK, 2 DEF, 2 MID, 1 FWD)

### Match Simulation
- Real-time match simulation
- Minute-by-minute action
- Live commentary and statistics
- Auto-play or manual control

## API Documentation

### Health Check
```
GET /api/health
Response: {"status": "ok"}
```

### Players API

**Get all players**
```
GET /api/players
```

**Create player**
```
POST /api/players
Body: {
  "name": "John",
  "surname": "Doe",
  "number": 10,
  "position": "FWD",
  "attributes": {
    "dribbling": 85,
    "passing": 75,
    "shooting": 90,
    "defense": 40,
    "athleticism": 85,
    "mentality": 80
  }
}
```

### Teams API

**Create team**
```
POST /api/teams
Body: {
  "name": "FC Barcelona",
  "formation": "1-2-2-1",
  "tactics": "offensive",
  "player_ids": ["player_id_1", "player_id_2", ...]
}
```

### Match API

**Start match**
```
POST /api/match/start
Body: {
  "team_a_id": "team_id_1",
  "team_b_id": "team_id_2"
}
```

**Simulate minute**
```
POST /api/match/{match_id}/simulate
```

**Get match stats**
```
GET /api/match/{match_id}/stats
```

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.8+)
- Ensure Flask is installed: `pip install -r backend/requirements.txt`
- Check port 5000 is available

### Frontend won't start
- Check Node version: `node --version` (should be 14+)
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf frontend/node_modules && cd frontend && npm install`

### API connection errors
- Ensure backend is running on port 5000
- Check CORS is enabled in Flask
- Verify proxy in frontend package.json points to `http://localhost:5000`

## Development Tips

- Players are stored in `backend/database/players.json`
- Teams are stored in `backend/database/teams.json`
- Modify `engine/calculations.py` to adjust game mechanics
- Modify `engine/commentary.py` to add new commentary
- Add CSS variables to `frontend/src/index.css` for theming

## License

MIT License - Feel free to use this project for learning and development.
