import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PlayerManager.css';

interface Player {
  id: string;
  name: string;
  surname: string;
  number: number;
  position: string;
  attributes: {
    dribbling: number;
    passing: number;
    shooting: number;
    defense: number;
    athleticism: number;
    mentality: number;
    goalkeeper: number;
  };
  conditioning: number;
  is_injured: boolean;
}

function PlayerManager() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [newPlayer, setNewPlayer] = useState({
    name: '',
    surname: '',
    number: 1,
    position: 'FWD',
    attributes: {
      dribbling: 50,
      passing: 50,
      shooting: 50,
      defense: 50,
      athleticism: 50,
      mentality: 50,
      goalkeeper: 0
    }
  });

  useEffect(() => {
    fetchPlayers();
  }, []);

  const fetchPlayers = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/players');
      setPlayers(response.data);
    } catch (error) {
      console.error('Error fetching players:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddPlayer = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('/api/players', newPlayer);
      fetchPlayers();
      setNewPlayer({
        name: '',
        surname: '',
        number: 1,
        position: 'FWD',
        attributes: {
          dribbling: 50,
          passing: 50,
          shooting: 50,
          defense: 50,
          athleticism: 50,
          mentality: 50,
          goalkeeper: 0
        }
      });
      setShowForm(false);
    } catch (error) {
      console.error('Error adding player:', error);
    }
  };

  const handleDeletePlayer = async (playerId: string) => {
    try {
      await axios.delete(`/api/players/${playerId}`);
      fetchPlayers();
    } catch (error) {
      console.error('Error deleting player:', error);
    }
  };

  const positionColor = (position: string) => {
    const colors: { [key: string]: string } = {
      'GK': '#9f7aea',
      'DEF': '#ed8936',
      'MID': '#38b2ac',
      'FWD': '#f56565'
    };
    return colors[position] || '#cbd5e0';
  };

  return (
    <div className="player-manager">
      <h1>👥 Player Management</h1>

      <button
        className="btn-success"
        onClick={() => setShowForm(!showForm)}
      >
        {showForm ? 'Cancel' : '➕ Add New Player'}
      </button>

      {showForm && (
        <div className="form-container">
          <h2>Create New Player</h2>
          <form onSubmit={handleAddPlayer}>
            <div className="form-row">
              <div className="form-group">
                <label>First Name *</label>
                <input
                  type="text"
                  required
                  value={newPlayer.name}
                  onChange={(e) => setNewPlayer({ ...newPlayer, name: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label>Last Name *</label>
                <input
                  type="text"
                  required
                  value={newPlayer.surname}
                  onChange={(e) => setNewPlayer({ ...newPlayer, surname: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label>Number *</label>
                <input
                  type="number"
                  required
                  min="1"
                  max="99"
                  value={newPlayer.number}
                  onChange={(e) => setNewPlayer({ ...newPlayer, number: parseInt(e.target.value) })}
                />
              </div>
              <div className="form-group">
                <label>Position *</label>
                <select
                  value={newPlayer.position}
                  onChange={(e) => setNewPlayer({ ...newPlayer, position: e.target.value })}
                >
                  <option value="GK">Goalkeeper (GK)</option>
                  <option value="DEF">Defender (DEF)</option>
                  <option value="MID">Midfielder (MID)</option>
                  <option value="FWD">Forward (FWD)</option>
                </select>
              </div>
            </div>

            <div className="attributes-grid">
              {['dribbling', 'passing', 'shooting', 'defense', 'athleticism', 'mentality'].map(
                (attr) => (
                  <div key={attr} className="attribute-input">
                    <label>{attr.charAt(0).toUpperCase() + attr.slice(1)}</label>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={(newPlayer.attributes as any)[attr]}
                      onChange={(e) =>
                        setNewPlayer({
                          ...newPlayer,
                          attributes: {
                            ...newPlayer.attributes,
                            [attr]: parseInt(e.target.value)
                          }
                        })
                      }
                    />
                    <span>{(newPlayer.attributes as any)[attr]}</span>
                  </div>
                )
              )}
              {newPlayer.position === 'GK' && (
                <div className="attribute-input">
                  <label>Goalkeeper</label>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={newPlayer.attributes.goalkeeper}
                    onChange={(e) =>
                      setNewPlayer({
                        ...newPlayer,
                        attributes: {
                          ...newPlayer.attributes,
                          goalkeeper: parseInt(e.target.value)
                        }
                      })
                    }
                  />
                  <span>{newPlayer.attributes.goalkeeper}</span>
                </div>
              )}
            </div>

            <button type="submit" className="btn-primary">✅ Create Player</button>
          </form>
        </div>
      )}

      {loading ? (
        <p>Loading players...</p>
      ) : (
        <div className="players-grid">
          {players.length === 0 ? (
            <p className="empty-state">No players yet. Create your first player!</p>
          ) : (
            players.map((player) => (
              <div key={player.id} className="player-card">
                <div className="player-header">
                  <div>
                    <h3>{player.name} {player.surname}</h3>
                    <p className="player-number">#{player.number}</p>
                  </div>
                  <span
                    className="position-badge"
                    style={{ backgroundColor: positionColor(player.position) }}
                  >
                    {player.position}
                  </span>
                </div>

                <div className="attributes-display">
                  <div className="attr">
                    <span>Dribbling</span>
                    <div className="progress-bar">
                      <div style={{ width: `${player.attributes.dribbling}%` }}></div>
                    </div>
                    <span>{player.attributes.dribbling}</span>
                  </div>
                  <div className="attr">
                    <span>Passing</span>
                    <div className="progress-bar">
                      <div style={{ width: `${player.attributes.passing}%` }}></div>
                    </div>
                    <span>{player.attributes.passing}</span>
                  </div>
                  <div className="attr">
                    <span>Shooting</span>
                    <div className="progress-bar">
                      <div style={{ width: `${player.attributes.shooting}%` }}></div>
                    </div>
                    <span>{player.attributes.shooting}</span>
                  </div>
                  <div className="attr">
                    <span>Defense</span>
                    <div className="progress-bar">
                      <div style={{ width: `${player.attributes.defense}%` }}></div>
                    </div>
                    <span>{player.attributes.defense}</span>
                  </div>
                  <div className="attr">
                    <span>Athleticism</span>
                    <div className="progress-bar">
                      <div style={{ width: `${player.attributes.athleticism}%` }}></div>
                    </div>
                    <span>{player.attributes.athleticism}</span>
                  </div>
                  <div className="attr">
                    <span>Mentality</span>
                    <div className="progress-bar">
                      <div style={{ width: `${player.attributes.mentality}%` }}></div>
                    </div>
                    <span>{player.attributes.mentality}</span>
                  </div>
                </div>

                <button
                  className="btn-danger"
                  onClick={() => handleDeletePlayer(player.id)}
                >
                  🗑️ Delete
                </button>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default PlayerManager;
