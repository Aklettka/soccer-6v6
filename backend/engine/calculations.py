import random
from typing import Tuple, Dict
from models.player import Player

class Calculations:
    """Mathematical calculations for match events"""

    @staticmethod
    def calculate_tackle_success(
        defender: Player,
        attacker: Player,
        defender_position_bonus: float = 0.0
    ) -> bool:
        """
        Calculate if a tackle/interception succeeds
        Returns: True if defender wins the ball
        """
        defender_skill = defender.get_effective_rating("defense")
        attacker_skill = attacker.get_effective_rating("dribbling")
        
        # Base calculation: defender vs attacker
        skill_diff = (defender_skill - attacker_skill) * 0.7
        position_bonus = defender_position_bonus * 30  # Up to 30 points
        random_factor = random.uniform(-20, 20)
        
        success_chance = skill_diff + position_bonus + random_factor
        return success_chance > 0

    @staticmethod
    def calculate_pass_accuracy(
        passer: Player,
        distance: float = 1.0,  # 1 = short, 2 = medium, 3 = long
        pressure: float = 0.0
    ) -> bool:
        """
        Calculate if a pass is successful
        distance: 1.0 (short), 1.5 (medium), 2.0 (long)
        pressure: 0-1 (pressure from defenders)
        Returns: True if pass is completed
        """
        passing_skill = passer.get_effective_rating("passing")
        
        # Base accuracy decreases with distance
        base_accuracy = 85 - (distance * 15)
        
        # Pressure reduces accuracy
        pressure_penalty = pressure * 30
        
        # Player skill improves accuracy
        skill_bonus = (passing_skill - 50) * 0.4
        
        final_accuracy = base_accuracy + skill_bonus - pressure_penalty
        final_accuracy = max(30, min(95, final_accuracy))  # Clamp 30-95%
        
        return random.uniform(0, 100) < final_accuracy

    @staticmethod
    def calculate_shot_outcome(
        shooter: Player,
        goalkeeper: Player,
        distance: float = 1.0,
        pressure: float = 0.0
    ) -> Dict:
        """
        Calculate shot outcome (goal, on target, saved, miss, post)
        Returns: {outcome: str, power: int, accuracy: int}
        """
        shooting_skill = shooter.get_effective_rating("shooting")
        gk_skill = goalkeeper.get_effective_rating("goalkeeper")
        mentality = shooter.get_effective_rating("mentality")
        
        # Shot power (0-100)
        shot_power = shooting_skill * 0.6 + shooter.get_effective_rating("athleticism") * 0.3 + random.uniform(-10, 10)
        shot_power = max(20, min(100, shot_power))
        
        # Shot accuracy (0-100)
        shot_accuracy = shooting_skill * 0.5 + mentality * 0.3 - pressure * 20 + random.uniform(-15, 15)
        shot_accuracy = max(10, min(100, shot_accuracy))
        
        # If not on target, it's a miss
        if shot_accuracy < 40:
            return {"outcome": "miss", "power": int(shot_power), "accuracy": int(shot_accuracy)}
        
        # GK saves based on power and skill
        gk_reaction = gk_skill * 0.7 + random.uniform(-10, 10)
        shot_difficulty = shot_power - (distance * 10)
        
        if gk_reaction > shot_difficulty:
            return {"outcome": "saved", "power": int(shot_power), "accuracy": int(shot_accuracy)}
        
        # High power shots might hit the post
        if shot_power > 80 and random.random() < 0.15:
            return {"outcome": "post", "power": int(shot_power), "accuracy": int(shot_accuracy)}
        
        # Otherwise it's a goal
        return {"outcome": "goal", "power": int(shot_power), "accuracy": int(shot_accuracy)}

    @staticmethod
    def calculate_foul_probability(
        defender: Player,
        attacker: Player,
        intensity: float = 0.5
    ) -> Tuple[bool, str]:
        """
        Calculate if a foul occurs and severity
        intensity: 0-1 (0 = gentle, 1 = aggressive)
        Returns: (is_foul, card_type) - card_type: None, 'yellow', 'red'
        """
        # Base foul chance
        foul_chance = 15 + (intensity * 35)
        
        if random.uniform(0, 100) > foul_chance:
            return False, None
        
        # Card severity based on intensity and defender mentality
        mentality_factor = (50 - defender.get_effective_rating("mentality")) / 50
        severity = intensity * 0.7 + mentality_factor * 0.3 + random.uniform(-0.2, 0.2)
        
        if severity > 0.7:
            return True, "red"
        elif severity > 0.4:
            return True, "yellow"
        else:
            return True, None

    @staticmethod
    def calculate_possession_change(team_a_tactics: str, team_b_tactics: str) -> Dict:
        """
        Calculate possession percentages based on tactics
        Returns: {team_a: float, team_b: float}
        """
        base_possession = 50.0
        
        # Tactical modifiers
        tactics_modifier = {
            "defensive": -15,
            "balanced": 0,
            "offensive": 15
        }
        
        team_a_mod = tactics_modifier.get(team_a_tactics, 0)
        team_b_mod = tactics_modifier.get(team_b_tactics, 0)
        
        # Add randomness
        random_factor = random.uniform(-10, 10)
        
        team_a_possession = base_possession + team_a_mod - team_b_mod + random_factor
        team_a_possession = max(30, min(70, team_a_possession))  # Clamp 30-70%
        
        return {
            "team_a": team_a_possession,
            "team_b": 100 - team_a_possession
        }

    @staticmethod
    def calculate_player_rating(player_stats: Dict) -> float:
        """
        Calculate overall player rating based on match stats
        Returns: 1.0-10.0
        """
        touches = player_stats.get("touches", 1)
        passes_completed = player_stats.get("passes_completed", 0)
        passes_attempted = player_stats.get("passes_attempted", 1)
        shots_on_target = player_stats.get("shots_on_target", 0)
        goals = player_stats.get("goals", 0)
        assists = player_stats.get("assists", 0)
        tackles = player_stats.get("tackles", 0)
        
        # Base rating
        rating = 6.0
        
        # Pass accuracy bonus/penalty
        if passes_attempted > 0:
            pass_accuracy = passes_completed / passes_attempted
            rating += (pass_accuracy - 0.7) * 2  # Up to +2 or -1.4
        
        # Goals and assists
        rating += goals * 1.5
        rating += assists * 1.0
        
        # Shots on target
        rating += shots_on_target * 0.5
        
        # Tackles (for defenders)
        rating += tackles * 0.3
        
        # Involvement (touches)
        if touches > 30:
            rating += 0.5
        elif touches < 5:
            rating -= 1.0
        
        # Clamp to 1.0-10.0
        return max(1.0, min(10.0, rating))
