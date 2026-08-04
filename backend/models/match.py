from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime
from models.team import Team

class MatchStatus(Enum):
    PENDING = "pending"
    FIRST_HALF = "first_half"
    HALFTIME = "halftime"
    SECOND_HALF = "second_half"
    FINISHED = "finished"

class EventType(Enum):
    PASS = "pass"
    TACKLE = "tackle"
    SHOT = "shot"
    GOAL = "goal"
    SAVE = "save"
    FOUL = "foul"
    SUBSTITUTION = "substitution"
    CORNER = "corner"
    THROW_IN = "throw_in"

@dataclass
class MatchEvent:
    """Represents a match event"""
    minute: int
    second: int
    event_type: EventType
    team_id: str
    player_id: str
    player_name: str
    description: str
    commentary: str
    result: str  # success, miss, blocked, etc.
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            "minute": self.minute,
            "second": self.second,
            "event_type": self.event_type.value,
            "team_id": self.team_id,
            "player_id": self.player_id,
            "player_name": self.player_name,
            "description": self.description,
            "commentary": self.commentary,
            "result": self.result,
            "timestamp": self.timestamp.isoformat()
        }

@dataclass
class Match:
    """Represents a match"""
    id: str
    team_a: Team
    team_b: Team
    status: MatchStatus = MatchStatus.PENDING
    current_minute: int = 0
    current_second: int = 0
    half: int = 1  # 1 or 2
    events: List[MatchEvent] = field(default_factory=list)
    possession_team_id: str = None
    ball_position: Dict = field(default_factory=lambda: {"x": 50, "y": 50})  # % of field
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.possession_team_id:
            self.possession_team_id = self.team_a.id

    def add_event(self, event: MatchEvent):
        """Add event to match"""
        self.events.append(event)

    def get_score(self) -> Dict:
        """Get current score"""
        team_a_goals = self.team_a.stats.get("goals", 0)
        team_b_goals = self.team_b.stats.get("goals", 0)
        return {
            "team_a": team_a_goals,
            "team_b": team_b_goals
        }

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "team_a": self.team_a.to_dict(),
            "team_b": self.team_b.to_dict(),
            "status": self.status.value,
            "current_minute": self.current_minute,
            "current_second": self.current_second,
            "half": self.half,
            "score": self.get_score(),
            "events": [e.to_dict() for e in self.events],
            "possession_team_id": self.possession_team_id,
            "ball_position": self.ball_position
        }
