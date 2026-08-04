import json
import uuid
from flask import Blueprint, request, jsonify
from models.player import Player, PlayerAttributes
from database.db import Database

players_bp = Blueprint('players', __name__, url_prefix='/api/players')

@players_bp.route('', methods=['GET'])
def get_all_players():
    """Get all players"""
    players = Database.load_players()
    return jsonify([p.to_dict() for p in players])

@players_bp.route('/<player_id>', methods=['GET'])
def get_player(player_id):
    """Get player by ID"""
    player = Database.get_player(player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404
    return jsonify(player.to_dict())

@players_bp.route('', methods=['POST'])
def create_player():
    """Create new player"""
    data = request.get_json()
    
    try:
        attrs = PlayerAttributes(
            dribbling=data.get('attributes', {}).get('dribbling', 50),
            passing=data.get('attributes', {}).get('passing', 50),
            shooting=data.get('attributes', {}).get('shooting', 50),
            defense=data.get('attributes', {}).get('defense', 50),
            athleticism=data.get('attributes', {}).get('athleticism', 50),
            mentality=data.get('attributes', {}).get('mentality', 50),
            goalkeeper=data.get('attributes', {}).get('goalkeeper', 0)
        )
        
        player = Player(
            id=str(uuid.uuid4()),
            name=data.get('name', ''),
            surname=data.get('surname', ''),
            number=data.get('number', 0),
            position=data.get('position', 'FWD'),
            attributes=attrs
        )
        
        Database.add_player(player)
        return jsonify(player.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@players_bp.route('/<player_id>', methods=['PUT'])
def update_player(player_id):
    """Update player"""
    player = Database.get_player(player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404
    
    data = request.get_json()
    
    # Update basic info
    if 'name' in data:
        player.name = data['name']
    if 'surname' in data:
        player.surname = data['surname']
    if 'number' in data:
        player.number = data['number']
    if 'position' in data:
        player.position = data['position']
    
    # Update attributes
    if 'attributes' in data:
        attrs = data['attributes']
        player.attributes.dribbling = attrs.get('dribbling', player.attributes.dribbling)
        player.attributes.passing = attrs.get('passing', player.attributes.passing)
        player.attributes.shooting = attrs.get('shooting', player.attributes.shooting)
        player.attributes.defense = attrs.get('defense', player.attributes.defense)
        player.attributes.athleticism = attrs.get('athleticism', player.attributes.athleticism)
        player.attributes.mentality = attrs.get('mentality', player.attributes.mentality)
        player.attributes.goalkeeper = attrs.get('goalkeeper', player.attributes.goalkeeper)
    
    Database.update_player(player)
    return jsonify(player.to_dict())

@players_bp.route('/<player_id>', methods=['DELETE'])
def delete_player(player_id):
    """Delete player"""
    player = Database.get_player(player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404
    
    Database.delete_player(player_id)
    return jsonify({"message": "Player deleted"})
