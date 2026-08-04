# Soccer 6v6 Match Simulator

Realtime 6v6 football match simulator with Python backend and React frontend.

## Features

- ⚽ **Realistic Match Simulation** - Minute-by-minute football action
- 👥 **Player Management** - Create and manage players with detailed attributes
- 🎯 **AI-Powered Players** - Realistic decision making and team tactics
- 📊 **Live Statistics** - Track player and team performance in real-time
- 🎙️ **Live Commentary** - Natural language commentary for all match events
- 🏆 **Team Building** - Create custom teams with different formations and tactics

## Project Structure

```
soccer-6v6/
├── backend/
│   ├── models/           # Data models (Player, Team, Match)
│   ├── engine/           # Simulation engine (Simulator, Calculations, Commentary)
│   ├── routes/           # API endpoints (players, teams, match)
│   ├── database/         # Database layer
│   ├── app.py            # Flask app
│   ├── config.py         # Configuration
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/        # React pages
│   │   │   ├── PlayerManager.tsx
│   │   │   ├── TeamBuilder.tsx
│   │   │   └── MatchSimulator.tsx
│   │   ├── App.tsx        # Main app component
│   │   └── index.tsx      # Entry point
│   ├── public/
│   └── package.json
└── README.md
```

## Getting Started

### Backend Setup

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Run Flask server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

1. Install Node dependencies:
```bash
cd frontend
npm install
```

2. Start development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## Usage

1. **Create Players** - Go to Players page and add players with attributes
2. **Build Teams** - Create teams and select 6 players (1 GK, 2 DEF, 2 MID, 1 FWD)
3. **Start Match** - Go to Match page, select two teams, and start the simulation
4. **Watch** - Watch the match unfold with live commentary and statistics

## API Endpoints

### Players
- `GET /api/players` - Get all players
- `GET /api/players/<id>` - Get player by ID
- `POST /api/players` - Create new player
- `PUT /api/players/<id>` - Update player
- `DELETE /api/players/<id>` - Delete player

### Teams
- `GET /api/teams` - Get all teams
- `GET /api/teams/<id>` - Get team by ID
- `POST /api/teams` - Create new team
- `PUT /api/teams/<id>` - Update team
- `DELETE /api/teams/<id>` - Delete team

### Match
- `POST /api/match/start` - Start new match
- `GET /api/match/<id>` - Get match details
- `POST /api/match/<id>/simulate` - Simulate next minute
- `GET /api/match/<id>/events` - Get match events
- `GET /api/match/<id>/stats` - Get match statistics

## Match Mechanics

### Attributes
Each player has 6 key attributes (0-100):
- **Dribbling** - Ability to control and move with the ball
- **Passing** - Accuracy and vision for passing
- **Shooting** - Accuracy and power of shots
- **Defense** - Defensive positioning and tackling ability
- **Athleticism** - Speed, stamina, and physical ability
- **Mentality** - Confidence and composure under pressure

### Match Events
The simulator generates realistic events:
- **Pass** - Players attempt accurate passes
- **Dribble** - Players try to move past defenders
- **Tackle** - Defenders try to win the ball
- **Shot** - Forwards attempt shots on goal
- **Goal** - Successful shots
- **Foul** - Aggressive challenges
- **Substitution** - Team changes

### Tactics
Teams can play with different tactics:
- **Defensive** - Focus on defending, lower possession
- **Balanced** - Balanced attack and defense
- **Offensive** - Focus on attacking, higher possession

## Technologies

- **Backend**: Python, Flask, Flask-CORS
- **Frontend**: React, TypeScript, Axios, React Router
- **Database**: JSON-based storage (easy to swap with real database)

## Future Enhancements

- [ ] Real database integration (PostgreSQL/MongoDB)
- [ ] Player injuries and suspensions
- [ ] Historical match records
- [ ] Tournament mode
- [ ] Multiplayer matches
- [ ] Advanced player attributes
- [ ] Custom field conditions
- [ ] Weather effects on gameplay

## License

MIT
