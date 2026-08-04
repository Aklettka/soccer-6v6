import random
import uuid
from typing import List, Optional, Dict, Tuple
from models.player import Player
from models.team import Team
from models.match import Match, MatchEvent, EventType, MatchStatus
from engine.calculations import Calculations
from engine.commentary import Commentary

class Simulator:
    """Main match simulator engine"""

    def __init__(self, match: Match):
        self.match = match
        self.possession_team = match.team_a
        self.defending_team = match.team_b
        self.events_this_minute = []

    def start_match(self):
        """Initialize match"""
        self.match.status = MatchStatus.FIRST_HALF
        self.match.current_minute = 0
        self.match.half = 1
        # Randomly decide who starts with possession
        if random.random() > 0.5:
            self.possession_team = self.match.team_b
            self.defending_team = self.match.team_a

    def simulate_minute(self) -> List[MatchEvent]:
        """Simulate one minute of football"""
        self.events_this_minute = []

        # Minute start commentary
        if self.match.current_minute in [0, 30]:
            event = MatchEvent(
                minute=self.match.current_minute + 1,
                second=0,
                event_type=EventType.CORNER,  # Use as generic event
                team_id=self.possession_team.id,
                player_id="",
                player_name="",
                description="Początek meczu",
                commentary=Commentary.generate_minute_start_commentary(self.match.current_minute + 1),
                result="start"
            )
            self.events_this_minute.append(event)
            self.match.add_event(event)

        # Generate 2-4 actions per minute
        num_actions = random.randint(2, 4)
        for action_num in range(num_actions):
            second = (action_num + 1) * 15  # Spread actions throughout minute
            self._simulate_action(second)

        # Update conditioning
        for player in self.possession_team.players[:6]:  # Only starting XI
            player.reduce_conditioning(amount=2.0 if random.random() > 0.3 else 1.0)
        for player in self.defending_team.players[:6]:
            player.reduce_conditioning(amount=2.0 if random.random() > 0.3 else 1.0)

        # Increment time
        self.match.current_minute += 1

        return self.events_this_minute

    def _simulate_action(self, second: int):
        """Simulate a single action"""
        # Decide action type based on possession
        action_type = random.choice(["pass", "pass", "dribble", "shot"])  # 50% pass, 25% dribble, 25% shot

        passer = random.choice(self.possession_team.get_starting_xi())
        
        if action_type == "pass":
            self._simulate_pass(passer, second)
        elif action_type == "dribble":
            self._simulate_dribble(passer, second)
        elif action_type == "shot":
            self._simulate_shot(passer, second)

    def _simulate_pass(self, passer: Player, second: int):
        """Simulate a pass"""
        # Select receiver (same team)
        receivers = [p for p in self.possession_team.get_starting_xi() if p.id != passer.id]
        if not receivers:
            return

        receiver = random.choice(receivers)
        
        # Estimate distance (1-3 scale)
        distance = random.uniform(1.0, 2.5)
        
        # Calculate pressure from defenders
        pressure = random.uniform(0.0, 0.5)
        
        # Check if pass is successful
        success = Calculations.calculate_pass_accuracy(passer, distance, pressure)
        
        if success:
            # Successful pass
            commentary = Commentary.generate_pass_commentary(passer, receiver, True)
            result = "completed"
            
            # Update stats
            passer.stats["touches"] += 1
            passer.stats["passes_attempted"] += 1
            passer.stats["passes_completed"] += 1
            receiver.stats["touches"] += 1
        else:
            # Intercepted or failed
            commentary = Commentary.generate_pass_commentary(passer, receiver, False)
            result = "failed"
            
            # Update stats
            passer.stats["touches"] += 1
            passer.stats["passes_attempted"] += 1
            
            # Switch possession (50% chance)
            if random.random() > 0.3:
                self._change_possession()

        event = MatchEvent(
            minute=self.match.current_minute + 1,
            second=second,
            event_type=EventType.PASS,
            team_id=self.possession_team.id,
            player_id=passer.id,
            player_name=f"{passer.name} {passer.surname}",
            description=f"Pass from {passer.name} to {receiver.name}",
            commentary=commentary,
            result=result
        )
        self.events_this_minute.append(event)
        self.match.add_event(event)

    def _simulate_dribble(self, player: Player, second: int):
        """Simulate a dribbling action"""
        player.stats["touches"] += 1
        
        # Random defender tries to tackle
        defender = random.choice(self.defending_team.get_starting_xi())
        
        success = Calculations.calculate_tackle_success(
            defender=defender,
            attacker=player,
            defender_position_bonus=random.uniform(-0.5, 1.0)
        )
        
        if success:
            # Defender wins ball
            commentary = Commentary.generate_tackle_commentary(defender, player, True)
            defender.stats["tackles"] += 1
            defender.stats["touches"] += 1
            self._change_possession()
        else:
            # Attacker continues
            commentary = Commentary.generate_tackle_commentary(defender, player, False)
            commentary = Commentary.random_template(Commentary.DRIBBLE_TEMPLATES).format(player_name=player.name)

        event = MatchEvent(
            minute=self.match.current_minute + 1,
            second=second,
            event_type=EventType.TACKLE if success else EventType.PASS,
            team_id=self.possession_team.id,
            player_id=player.id,
            player_name=f"{player.name} {player.surname}",
            description=f"Dribble by {player.name}",
            commentary=commentary,
            result="success" if not success else "tackled"
        )
        self.events_this_minute.append(event)
        self.match.add_event(event)

    def _simulate_shot(self, shooter: Player, second: int):
        """Simulate a shot on goal"""
        shooter.stats["touches"] += 1
        shooter.stats["shots"] += 1
        
        goalkeeper = self.defending_team.get_goalkeeper()
        if not goalkeeper:
            return
        
        distance = random.uniform(0.8, 2.0)  # Shooting distance
        pressure = random.uniform(0.0, 0.7)
        
        outcome = Calculations.calculate_shot_outcome(shooter, goalkeeper, distance, pressure)
        
        commentary = Commentary.generate_shot_commentary(shooter, outcome)
        
        if outcome["outcome"] == "goal":
            # GOAL!
            self.possession_team.stats["goals"] += 1
            shooter.stats["goals"] += 1
            # Check for assist (last passer)
            result = "goal"
        elif outcome["outcome"] == "saved":
            goalkeeper.stats["touches"] += 1
            result = "saved"
            # Possible counter-attack
            if random.random() > 0.7:
                self._change_possession()
        elif outcome["outcome"] in ["miss", "post"]:
            result = outcome["outcome"]
            # Possible set piece for defending team
            if random.random() > 0.8:
                self._change_possession()
        
        shooter.stats["shots_on_target"] += 1 if outcome["outcome"] in ["goal", "saved"] else 0
        self.possession_team.stats["shots"] += 1
        self.possession_team.stats["shots_on_target"] += 1 if outcome["outcome"] in ["goal", "saved"] else 0
        
        event = MatchEvent(
            minute=self.match.current_minute + 1,
            second=second,
            event_type=EventType.GOAL if outcome["outcome"] == "goal" else EventType.SHOT,
            team_id=self.possession_team.id,
            player_id=shooter.id,
            player_name=f"{shooter.name} {shooter.surname}",
            description=f"Shot by {shooter.name} - {outcome['outcome']}",
            commentary=commentary,
            result=result
        )
        self.events_this_minute.append(event)
        self.match.add_event(event)

    def _change_possession(self):
        """Switch possession to the other team"""
        self.possession_team, self.defending_team = self.defending_team, self.possession_team

    def simulate_halftime(self):
        """Handle halftime: restore conditioning, half-time commentary"""
        self.match.status = MatchStatus.HALFTIME
        
        event = MatchEvent(
            minute=30,
            second=0,
            event_type=EventType.CORNER,
            team_id="",
            player_id="",
            player_name="",
            description="Halftime",
            commentary="⏸️ KONIEC PIERWSZEJ POŁOWY! Drużyny wchodzą do szatni. Wynik: " + str(self.match.get_score()["team_a"]) + "-" + str(self.match.get_score()["team_b"]),
            result="halftime"
        )
        self.match.add_event(event)
        
        # Restore conditioning
        for player in self.match.team_a.players:
            player.restore_conditioning(30)
        for player in self.match.team_b.players:
            player.restore_conditioning(30)

    def simulate_match_end(self):
        """Handle end of match: calculate final stats"""
        self.match.status = MatchStatus.FINISHED
        
        # Calculate player ratings
        for player in self.match.team_a.players:
            player.stats["rating"] = Calculations.calculate_player_rating(player.stats)
        for player in self.match.team_b.players:
            player.stats["rating"] = Calculations.calculate_player_rating(player.stats)
        
        event = MatchEvent(
            minute=60,
            second=0,
            event_type=EventType.CORNER,
            team_id="",
            player_id="",
            player_name="",
            description="Match End",
            commentary="🏁 KONIEC MECZU! " + str(self.match.get_score()["team_a"]) + " - " + str(self.match.get_score()["team_b"]),
            result="match_end"
        )
        self.match.add_event(event)
