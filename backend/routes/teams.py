import uuid
from flask import Blueprint, request, jsonify
from models.team import Team
from models.player import Player
from database.db import Database

teams_bp = Blueprint('teams', __name__, url_prefix='/api/teams')

@teams_bp.route('', methods=['GET'])
def get_all_teams():
    """Get all teams"""
    teams = Database.load_teams()
    return jsonify([t.to_dict() for t in teams])

@teams_bp.route('/<team_id>', methods=['GET'])
def get_team(team_id):
    """Get team by ID"""
    team = Database.get_team(team_id)
    if not team:
        return jsonify({"error": "Team not found"}), 404
    return jsonify(team.to_dict())

@teams_bp.route('', methods=['POST'])
def create_team():
    """Create new team"""
    data = request.get_json()
    
    try:
        team = Team(
            id=str(uuid.uuid4()),
            name=data.get('name', ''),
            formation=data.get('formation', '1-2-2-1'),
            tactics=data.get('tactics', 'balanced')
        )
        
        # Add players to team
        player_ids = data.get('player_ids', [])
        players = Database.load_players()
        for player_id in player_ids:
            player = next((p for p in players if p.id == player_id), None)
            if player:
                team.add_player(player)
        
        Database.add_team(team)
        return jsonify(team.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@teams_bp.route('/<team_id>', methods=['PUT'])
def update_team(team_id):
    """Update team"""
    team = Database.get_team(team_id)
    if not team:
        return jsonify({"error": "Team not found"}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        team.name = data['name']
    if 'formation' in data:
        team.formation = data['formation']
    if 'tactics' in data:
        team.tactics = data['tactics']
    
    # Update team players
    if 'player_ids' in data:
        team.players = []
        players = Database.load_players()
        for player_id in data['player_ids']:
            player = next((p for p in players if p.id == player_id), None)
            if player:
                team.add_player(player)
    
    Database.update_team(team)
    return jsonify(team.to_dict())

@teams_bp.route('/<team_id>', methods=['DELETE'])
def delete_team(team_id):
    """Delete team"""
    team = Database.get_team(team_id)
    if not team:
        return jsonify({"error": "Team not found"}), 404
    
    Database.delete_team(team_id)
    return jsonify({"message": "Team deleted"})
