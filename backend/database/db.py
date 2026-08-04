import json
import os
from typing import List, Dict, Optional
from models.player import Player, PlayerAttributes
from models.team import Team

class Database:
    """Simple JSON-based database for players and teams"""

    PLAYERS_FILE = "database/players.json"
    TEAMS_FILE = "database/teams.json"

    @staticmethod
    def ensure_files_exist():
        """Create database files if they don't exist"""
        os.makedirs("database", exist_ok=True)
        
        if not os.path.exists(Database.PLAYERS_FILE):
            with open(Database.PLAYERS_FILE, 'w') as f:
                json.dump([], f, indent=2)
        
        if not os.path.exists(Database.TEAMS_FILE):
            with open(Database.TEAMS_FILE, 'w') as f:
                json.dump([], f, indent=2)

    @staticmethod
    def save_players(players: List[Player]):
        """Save players to JSON"""
        data = [p.to_dict() for p in players]
        with open(Database.PLAYERS_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load_players() -> List[Player]:
        """Load players from JSON"""
        Database.ensure_files_exist()
        with open(Database.PLAYERS_FILE, 'r') as f:
            data = json.load(f)
        
        players = []
        for p in data:
            attrs = PlayerAttributes(**p.get('attributes', {}))
            player = Player(
                id=p['id'],
                name=p['name'],
                surname=p['surname'],
                number=p['number'],
                position=p['position'],
                attributes=attrs,
                conditioning=p.get('conditioning', 100.0),
                is_injured=p.get('is_injured', False),
                stats=p.get('stats', {})
            )
            players.append(player)
        return players

    @staticmethod
    def add_player(player: Player):
        """Add player to database"""
        players = Database.load_players()
        players.append(player)
        Database.save_players(players)

    @staticmethod
    def get_player(player_id: str) -> Optional[Player]:
        """Get player by ID"""
        players = Database.load_players()
        for p in players:
            if p.id == player_id:
                return p
        return None

    @staticmethod
    def update_player(player: Player):
        """Update player in database"""
        players = Database.load_players()
        for i, p in enumerate(players):
            if p.id == player.id:
                players[i] = player
                Database.save_players(players)
                return

    @staticmethod
    def delete_player(player_id: str):
        """Delete player from database"""
        players = Database.load_players()
        players = [p for p in players if p.id != player_id]
        Database.save_players(players)

    @staticmethod
    def save_teams(teams: List[Team]):
        """Save teams to JSON"""
        data = [t.to_dict() for t in teams]
        with open(Database.TEAMS_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load_teams() -> List[Team]:
        """Load teams from JSON"""
        Database.ensure_files_exist()
        with open(Database.TEAMS_FILE, 'r') as f:
            data = json.load(f)
        
        teams = []
        for t in data:
            team = Team(
                id=t['id'],
                name=t['name'],
                formation=t.get('formation', '1-2-2-1'),
                tactics=t.get('tactics', 'balanced'),
                players=[]
            )
            teams.append(team)
        return teams

    @staticmethod
    def add_team(team: Team):
        """Add team to database"""
        teams = Database.load_teams()
        teams.append(team)
        Database.save_teams(teams)

    @staticmethod
    def get_team(team_id: str) -> Optional[Team]:
        """Get team by ID"""
        teams = Database.load_teams()
        for t in teams:
            if t.id == team_id:
                return t
        return None

    @staticmethod
    def update_team(team: Team):
        """Update team in database"""
        teams = Database.load_teams()
        for i, t in enumerate(teams):
            if t.id == team.id:
                teams[i] = team
                Database.save_teams(teams)
                return

    @staticmethod
    def delete_team(team_id: str):
        """Delete team from database"""
        teams = Database.load_teams()
        teams = [t for t in teams if t.id != team_id]
        Database.save_teams(teams)
