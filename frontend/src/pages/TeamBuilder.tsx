import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './TeamBuilder.css';

interface Player {
  id: string;
  name: string;
  surname: string;
  number: number;
  position: string;
  attributes: any;
}

interface Team {
  id: string;
  name: string;
  formation: string;
  tactics: string;
  players: Player[];
}

function TeamBuilder() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [allPlayers, setAllPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [newTeam, setNewTeam] = useState({
    name: '',
    formation: '1-2-2-1',
    tactics: 'balanced',
    player_ids: [] as string[]
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [teamsRes, playersRes] = await Promise.all([
        axios.get('/api/teams'),
        axios.get('/api/players')
      ]);
      setTeams(teamsRes.data);
      setAllPlayers(playersRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTeam = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newTeam.player_ids.length !== 6) {
      alert('Please select exactly 6 players (1 GK, 2 DEF, 2 MID, 1 FWD)');
      return;
    }
    try {
      await axios.post('/api/teams', newTeam);
      fetchData();
      setNewTeam({
        name: '',
        formation: '1-2-2-1',
        tactics: 'balanced',
        player_ids: []
      });
      setShowForm(false);
    } catch (error) {
      console.error('Error adding team:', error);
    }
  };

  const handleDeleteTeam = async (teamId: string) => {
    try {
      await axios.delete(`/api/teams/${teamId}`);
      fetchData();
    } catch (error) {
      console.error('Error deleting team:', error);
    }
  };

  const togglePlayerSelection = (playerId: string) => {
    setNewTeam((prev) => {
      const ids = prev.player_ids.includes(playerId)
        ? prev.player_ids.filter((id) => id !== playerId)
        : [...prev.player_ids, playerId];
      return { ...prev, player_ids: ids };
    });
  };

  const getSelectedPlayerCount = () => {
    const gk = newTeam.player_ids.filter((id) => {
      const p = allPlayers.find((pl) => pl.id === id);
      return p?.position === 'GK';
    }).length;
    const def = newTeam.player_ids.filter((id) => {
      const p = allPlayers.find((pl) => pl.id === id);
      return p?.position === 'DEF';
    }).length;
    const mid = newTeam.player_ids.filter((id) => {
      const p = allPlayers.find((pl) => pl.id === id);
      return p?.position === 'MID';
    }).length;
    const fwd = newTeam.player_ids.filter((id) => {
      const p = allPlayers.find((pl) => pl.id === id);
      return p?.position === 'FWD';
    }).length;
    return { gk, def, mid, fwd };
  };

  const count = getSelectedPlayerCount();

  return (
    <div className="team-builder">
      <h1>🏆 Team Builder</h1>

      <button className="btn-success" onClick={() => setShowForm(!showForm)}>
        {showForm ? 'Cancel' : '➕ Create Team'}
      </button>

      {showForm && (
        <div className="form-container">
          <h2>Create New Team</h2>
          <form onSubmit={handleAddTeam}>
            <div className="form-row">
              <div className="form-group">
                <label>Team Name *</label>
                <input
                  type="text"
                  required
                  value={newTeam.name}
                  onChange={(e) => setNewTeam({ ...newTeam, name: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label>Formation</label>
                <select
                  value={newTeam.formation}
                  onChange={(e) => setNewTeam({ ...newTeam, formation: e.target.value })}
                >
                  <option value="1-2-2-1">1-2-2-1</option>
                  <option value="1-1-3-1">1-1-3-1</option>
                  <option value="1-3-1-1">1-3-1-1</option>
                </select>
              </div>
              <div className="form-group">
                <label>Tactics</label>
                <select
                  value={newTeam.tactics}
                  onChange={(e) => setNewTeam({ ...newTeam, tactics: e.target.value })}
                >
                  <option value="defensive">Defensive</option>
                  <option value="balanced">Balanced</option>
                  <option value="offensive">Offensive</option>
                </select>
              </div>
            </div>

            <div className="selection-info">
              <p>Select 6 players: 1 GK, 2 DEF, 2 MID, 1 FWD</p>
              <div className="position-count">
                <span className={count.gk === 1 ? 'complete' : 'incomplete'}>GK: {count.gk}/1</span>
                <span className={count.def === 2 ? 'complete' : 'incomplete'}>DEF: {count.def}/2</span>
                <span className={count.mid === 2 ? 'complete' : 'incomplete'}>MID: {count.mid}/2</span>
                <span className={count.fwd === 1 ? 'complete' : 'incomplete'}>FWD: {count.fwd}/1</span>
              </div>
            </div>

            <div className="players-selection">
              {allPlayers.length === 0 ? (
                <p>No players available. Create players first!</p>
              ) : (
                allPlayers.map((player) => (
                  <label key={player.id} className="player-checkbox">
                    <input
                      type="checkbox"
                      checked={newTeam.player_ids.includes(player.id)}
                      onChange={() => togglePlayerSelection(player.id)}
                    />
                    <span>{player.name} {player.surname} - {player.position} (#{player.number})</span>
                  </label>
                ))
              )}
            </div>

            <button type="submit" className="btn-primary" disabled={newTeam.player_ids.length !== 6}>
              ✅ Create Team
            </button>
          </form>
        </div>
      )}

      {loading ? (
        <p>Loading teams...</p>
      ) : (
        <div className="teams-grid">
          {teams.length === 0 ? (
            <p className="empty-state">No teams yet. Create your first team!</p>
          ) : (
            teams.map((team) => (
              <div key={team.id} className="team-card">
                <div className="team-header">
                  <h3>{team.name}</h3>
                  <span className="formation-badge">{team.formation}</span>
                </div>
                <p className="tactics">Tactics: <strong>{team.tactics}</strong></p>
                <div className="team-players">
                  {team.players.map((player) => (
                    <div key={player.id} className="team-player">
                      <span className="player-position">{player.position}</span>
                      <span>{player.name} {player.surname} #{player.number}</span>
                    </div>
                  ))}
                </div>
                <button
                  className="btn-danger"
                  onClick={() => handleDeleteTeam(team.id)}
                >
                  🗑️ Delete Team
                </button>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default TeamBuilder;
