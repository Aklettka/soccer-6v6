from dataclasses import dataclass, field
from typing import List, Dict
from models.player import Player

@dataclass
class Team:
    """Represents a team"""
    id: str
    name: str
    players: List[Player] = field(default_factory=list)
    formation: str = "1-2-2-1"  # GK-DEF-MID-FWD
    tactics: str = "balanced"  # defensive, balanced, offensive
    possession: float = 50.0
    stats: Dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.stats:
            self.stats = {
                "goals": 0,
                "shots": 0,
                "shots_on_target": 0,
                "passes": 0,
                "passes_completed": 0,
                "tackles": 0,
                "fouls": 0,
                "corner_kicks": 0,
                "possession_percent": 50.0
            }

    def add_player(self, player: Player):
        """Add player to team"""
        self.players.append(player)

    def get_player(self, player_id: str) -> Player:
        """Get player by ID"""
        for player in self.players:
            if player.id == player_id:
                return player
        return None

    def get_players_by_position(self, position: str) -> List[Player]:
        """Get all players in specific position"""
        return [p for p in self.players if p.position == position]

    def get_goalkeeper(self) -> Player:
        """Get goalkeeper"""
        gk = self.get_players_by_position("GK")
        return gk[0] if gk else None

    def get_defenders(self) -> List[Player]:
        """Get defenders"""
        return self.get_players_by_position("DEF")

    def get_midfielders(self) -> List[Player]:
        """Get midfielders"""
        return self.get_players_by_position("MID")

    def get_forwards(self) -> List[Player]:
        """Get forwards"""
        return self.get_players_by_position("FWD")

    def get_starting_xi(self) -> List[Player]:
        """Get 6 starting players (1 GK, 2 DEF, 2 MID, 1 FWD)"""
        return self.players[:6]

    def get_substitutes(self) -> List[Player]:
        """Get substitute players"""
        return self.players[6:]

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "formation": self.formation,
            "tactics": self.tactics,
            "players": [p.to_dict() for p in self.players],
            "stats": self.stats
        }
