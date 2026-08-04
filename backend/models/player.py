from dataclasses import dataclass, asdict
from typing import Dict, Optional
import json

@dataclass
class PlayerAttributes:
    """Player skill attributes (0-100)"""
    dribbling: int = 50
    passing: int = 50
    shooting: int = 50
    defense: int = 50
    athleticism: int = 50
    mentality: int = 50
    goalkeeper: int = 0  # Only for GK

    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class Player:
    """Represents a player"""
    id: str
    name: str
    surname: str
    number: int
    position: str  # GK, DEF, MID, FWD
    attributes: PlayerAttributes
    conditioning: float = 100.0  # 0-100%
    is_injured: bool = False
    stats: Dict = None

    def __post_init__(self):
        if self.stats is None:
            self.stats = {
                "touches": 0,
                "passes_completed": 0,
                "passes_attempted": 0,
                "tackles": 0,
                "interceptions": 0,
                "shots": 0,
                "shots_on_target": 0,
                "goals": 0,
                "assists": 0,
                "yellow_cards": 0,
                "red_cards": 0,
                "rating": 0.0
            }

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "number": self.number,
            "position": self.position,
            "attributes": self.attributes.to_dict(),
            "conditioning": self.conditioning,
            "is_injured": self.is_injured,
            "stats": self.stats
        }

    def get_effective_rating(self, attribute_name: str) -> float:
        """Get attribute value adjusted by conditioning and injury"""
        base_value = getattr(self.attributes, attribute_name, 0)
        conditioning_multiplier = self.conditioning / 100.0
        injury_multiplier = 0.7 if self.is_injured else 1.0
        return base_value * conditioning_multiplier * injury_multiplier

    def reduce_conditioning(self, amount: float = 2.0):
        """Reduce conditioning during match"""
        self.conditioning = max(0, self.conditioning - amount)

    def restore_conditioning(self, amount: float = 30.0):
        """Restore conditioning at halftime"""
        self.conditioning = min(100, self.conditioning + amount)
