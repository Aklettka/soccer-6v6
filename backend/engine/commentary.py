import random
from typing import List, Optional
from models.player import Player
from models.team import Team

class Commentary:
    """Generate natural language commentary for match events"""

    # Commentary templates
    PASS_TEMPLATES = [
        "{player_name} podał do {receiver_name}",
        "{player_name} wysyła piłkę do {receiver_name}",
        "{player_name} strata do {receiver_name}",
        "Piłka trafia do {receiver_name} od {player_name}",
        "{player_name} znajduje {receiver_name} piłką",
    ]

    PASS_FAILED = [
        "{player_name} chybił w podaniu",
        "Podanie {player_name} jest niedokładne",
        "{player_name} straciła piłkę w podaniu",
        "Piłka {player_name} trafia w boczną linię",
    ]

    DRIBBLE_TEMPLATES = [
        "{player_name} dryblinguje w kierunku bramki",
        "{player_name} biegnie z piłką",
        "{player_name} zmienia kierunek",
        "{player_name} omija rywala",
    ]

    TACKLE_SUCCESS = [
        "{defender_name} przejmuje piłkę od {attacker_name}",
        "{defender_name} wspaniale przejmuje piłkę!",
        "{defender_name} czysta przejęcie piłki",
        "{defender_name} ucina akcję {attacker_name}",
    ]

    TACKLE_FAILED = [
        "{defender_name} nie uciął przejęcia, {attacker_name} biegnie dalej",
        "{defender_name} straciła grę z piłką",
        "{attacker_name} przechodzi obok {defender_name}",
    ]

    SHOT_TEMPLATES = [
        "{player_name} strzela! ",
        "{player_name} podejmuje decyzję i strzela! ",
        "Okazja! {player_name} strzela! ",
    ]

    SHOT_SAVED = [
        "Bramkarz wybija piłkę!",
        "Świetna obrona bramkarza!",
        "Bramkarz parodniuje strzał!",
    ]

    SHOT_GOAL = [
        "GOOOOOOL!!!",
        "TO JUŻ GOOOOL!!!",
        "PIĘKNY GOOOOL!!!",
        "GOOOOL DLA DRUŻYNY!",
    ]

    SHOT_MISS = [
        "Piłka trafia obok słupka!",
        "Chybienie! Piłka leci wysoko nad bramką!",
        "Nietrafiła, piłka przechodzi obok bramki!",
    ]

    SHOT_POST = [
        "Piłka odbija się od słupka!",
        "Strzał w słupek! Tyle mi brakło!",
    ]

    FOUL_TEMPLATES = [
        "{player_name} fauli {opponent_name}",
        "{player_name} z zbyt dużą siłą podejmuje {opponent_name}",
        "{player_name} popełnia błąd na {opponent_name}",
    ]

    YELLOW_CARD = [
        "ŻÓŁTA KARTKA dla {player_name}!",
        "{player_name} dostaje żółtą kartkę!",
    ]

    RED_CARD = [
        "CZERWONA KARTKA! {player_name} wysłana z boiska!",
        "{player_name} wysłana z boiska za czerwoną kartkę!",
    ]

    SUBSTITUTION = [
        "{old_player_name} schodzi z boiska, wchodzi {new_player_name}",
        "Zmiana! {new_player_name} wchodzi za {old_player_name}",
    ]

    @staticmethod
    def random_template(templates: List[str]) -> str:
        return random.choice(templates)

    @staticmethod
    def generate_pass_commentary(passer: Player, receiver: Player, success: bool) -> str:
        if success:
            template = Commentary.random_template(Commentary.PASS_TEMPLATES)
            return template.format(player_name=passer.name, receiver_name=receiver.name)
        else:
            template = Commentary.random_template(Commentary.PASS_FAILED)
            return template.format(player_name=passer.name)

    @staticmethod
    def generate_tackle_commentary(defender: Player, attacker: Player, success: bool) -> str:
        if success:
            template = Commentary.random_template(Commentary.TACKLE_SUCCESS)
            return template.format(defender_name=defender.name, attacker_name=attacker.name)
        else:
            template = Commentary.random_template(Commentary.TACKLE_FAILED)
            return template.format(defender_name=defender.name, attacker_name=attacker.name)

    @staticmethod
    def generate_shot_commentary(shooter: Player, outcome: dict) -> str:
        template = Commentary.random_template(Commentary.SHOT_TEMPLATES)
        result_comment = ""

        if outcome["outcome"] == "goal":
            result_comment = Commentary.random_template(Commentary.SHOT_GOAL)
        elif outcome["outcome"] == "saved":
            result_comment = Commentary.random_template(Commentary.SHOT_SAVED)
        elif outcome["outcome"] == "miss":
            result_comment = Commentary.random_template(Commentary.SHOT_MISS)
        elif outcome["outcome"] == "post":
            result_comment = Commentary.random_template(Commentary.SHOT_POST)

        return template.format(player_name=shooter.name) + result_comment

    @staticmethod
    def generate_foul_commentary(player: Player, opponent: Player, card_type: Optional[str] = None) -> str:
        template = Commentary.random_template(Commentary.FOUL_TEMPLATES)
        comment = template.format(player_name=player.name, opponent_name=opponent.name)

        if card_type == "yellow":
            card_comment = Commentary.random_template(Commentary.YELLOW_CARD)
            comment += " " + card_comment.format(player_name=player.name)
        elif card_type == "red":
            card_comment = Commentary.random_template(Commentary.RED_CARD)
            comment += " " + card_comment.format(player_name=player.name)

        return comment

    @staticmethod
    def generate_substitution_commentary(old_player: Player, new_player: Player) -> str:
        template = Commentary.random_template(Commentary.SUBSTITUTION)
        return template.format(old_player_name=old_player.name, new_player_name=new_player.name)

    @staticmethod
    def generate_minute_start_commentary(minute: int) -> str:
        if minute == 1:
            return "🎺 POCZĄTEK MECZU! Rusza się piłka!"
        elif minute == 15:
            return "⏱️ 15 minut - mecz toczy się wyrównaną grę"
        elif minute == 30:
            return "⏱️ KONIEC PIERWSZEJ POŁOWY! Zespoły schodzą do szatni na przerwę."
        elif minute == 31:
            return "⏱️ POCZĄTEK DRUGIEJ POŁOWY! Wznowienie meczu!"
        elif minute == 45:
            return "🎯 KONIEC MECZU! Ostatni gwizdek arbitra!"
        return f"⏱️ Minuta {minute}"
