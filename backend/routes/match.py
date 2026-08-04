import uuid
from flask import Blueprint, request, jsonify
from models.match import Match, MatchStatus
from models.team import Team
from database.db import Database
from engine.simulator import Simulator

match_bp = Blueprint('match', __name__, url_prefix='/api/match')

# In-memory match storage (in production, use database)
active_matches = {}

@match_bp.route('/start', methods=['POST'])
def start_match():
    """Start a new match"""
    data = request.get_json()
    
    try:
        # Get teams
        teams = Database.load_teams()
        team_a = next((t for t in teams if t.id == data.get('team_a_id')), None)
        team_b = next((t for t in teams if t.id == data.get('team_b_id')), None)
        
        if not team_a or not team_b:
            return jsonify({"error": "Teams not found"}), 404
        
        # Create match
        match = Match(
            id=str(uuid.uuid4()),
            team_a=team_a,
            team_b=team_b
        )
        
        # Initialize simulator
        simulator = Simulator(match)
        simulator.start_match()
        
        # Store match and simulator
        active_matches[match.id] = {
            "match": match,
            "simulator": simulator
        }
        
        return jsonify(match.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@match_bp.route('/<match_id>', methods=['GET'])
def get_match(match_id):
    """Get match details"""
    if match_id not in active_matches:
        return jsonify({"error": "Match not found"}), 404
    
    match = active_matches[match_id]["match"]
    return jsonify(match.to_dict())

@match_bp.route('/<match_id>/simulate', methods=['POST'])
def simulate_minute(match_id):
    """Simulate next minute"""
    if match_id not in active_matches:
        return jsonify({"error": "Match not found"}), 404
    
    match = active_matches[match_id]["match"]
    simulator = active_matches[match_id]["simulator"]
    
    # Check if match is finished
    if match.status == MatchStatus.FINISHED:
        return jsonify({"error": "Match already finished"}), 400
    
    # Simulate minute
    events = simulator.simulate_minute()
    
    # Handle halftime
    if match.current_minute == 30 and match.half == 1:
        simulator.simulate_halftime()
        match.half = 2
        match.status = MatchStatus.SECOND_HALF
        match.current_minute = 30
    
    # Handle match end
    if match.current_minute == 60:
        simulator.simulate_match_end()
        match.status = MatchStatus.FINISHED
    
    return jsonify({
        "match": match.to_dict(),
        "events": [e.to_dict() for e in events]
    })

@match_bp.route('/<match_id>/events', methods=['GET'])
def get_match_events(match_id):
    """Get match events"""
    if match_id not in active_matches:
        return jsonify({"error": "Match not found"}), 404
    
    match = active_matches[match_id]["match"]
    return jsonify([e.to_dict() for e in match.events])

@match_bp.route('/<match_id>/stats', methods=['GET'])
def get_match_stats(match_id):
    """Get match statistics"""
    if match_id not in active_matches:
        return jsonify({"error": "Match not found"}), 404
    
    match = active_matches[match_id]["match"]
    
    stats = {
        "score": match.get_score(),
        "team_a": {
            "name": match.team_a.name,
            "stats": match.team_a.stats,
            "players": [{
                "name": f"{p.name} {p.surname}",
                "number": p.number,
                "position": p.position,
                "stats": p.stats,
                "conditioning": p.conditioning
            } for p in match.team_a.get_starting_xi()]
        },
        "team_b": {
            "name": match.team_b.name,
            "stats": match.team_b.stats,
            "players": [{
                "name": f"{p.name} {p.surname}",
                "number": p.number,
                "position": p.position,
                "stats": p.stats,
                "conditioning": p.conditioning
            } for p in match.team_b.get_starting_xi()]
        }
    }
    
    return jsonify(stats)
