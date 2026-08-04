import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './MatchSimulator.css';

interface Team {
  id: string;
  name: string;
  formation: string;
  tactics: string;
  players: any[];
}

interface MatchEvent {
  minute: number;
  second: number;
  event_type: string;
  team_id: string;
  player_id: string;
  player_name: string;
  description: string;
  commentary: string;
  result: string;
}

interface Match {
  id: string;
  status: string;
  current_minute: number;
  half: number;
  team_a: Team;
  team_b: Team;
  score: { team_a: number; team_b: number };
  events: MatchEvent[];
}

function MatchSimulator() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [selectedTeamA, setSelectedTeamA] = useState<string>('');
  const [selectedTeamB, setSelectedTeamB] = useState<string>('');
  const [match, setMatch] = useState<Match | null>(null);
  const [loading, setLoading] = useState(false);
  const [simulating, setSimulating] = useState(false);
  const [autoSimulate, setAutoSimulate] = useState(false);
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    fetchTeams();
  }, []);

  useEffect(() => {
    if (autoSimulate && match && match.status !== 'finished') {
      const timer = setTimeout(() => {
        simulateNextMinute();
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [autoSimulate, match]);

  const fetchTeams = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/teams');
      setTeams(response.data);
    } catch (error) {
      console.error('Error fetching teams:', error);
    } finally {
      setLoading(false);
    }
  };

  const startMatch = async () => {
    if (!selectedTeamA || !selectedTeamB || selectedTeamA === selectedTeamB) {
      alert('Select two different teams!');
      return;
    }

    try {
      setSimulating(true);
      const response = await axios.post('/api/match/start', {
        team_a_id: selectedTeamA,
        team_b_id: selectedTeamB
      });
      setMatch(response.data);
      setAutoSimulate(false);
    } catch (error) {
      console.error('Error starting match:', error);
    } finally {
      setSimulating(false);
    }
  };

  const simulateNextMinute = async () => {
    if (!match) return;

    try {
      setSimulating(true);
      const response = await axios.post(`/api/match/${match.id}/simulate`, {});
      setMatch(response.data.match);
      
      // Fetch stats
      const statsResponse = await axios.get(`/api/match/${match.id}/stats`);
      setStats(statsResponse.data);
    } catch (error) {
      console.error('Error simulating minute:', error);
      setAutoSimulate(false);
    } finally {
      setSimulating(false);
    }
  };

  const stopAutoSimulate = () => {
    setAutoSimulate(false);
  };

  const resetMatch = () => {
    setMatch(null);
    setStats(null);
    setSelectedTeamA('');
    setSelectedTeamB('');
    setAutoSimulate(false);
  };

  if (loading) return <div className="match-simulator"><p>Loading...</p></div>;

  return (
    <div className="match-simulator">
      <h1>⚽ Match Simulator</h1>

      {!match ? (
        <div className="match-setup">
          <h2>Setup Match</h2>
          <div className="setup-container">
            <div className="team-selector">
              <label>Team A</label>
              <select
                value={selectedTeamA}
                onChange={(e) => setSelectedTeamA(e.target.value)}
              >
                <option value="">Select Team</option>
                {teams.map((team) => (
                  <option key={team.id} value={team.id}>
                    {team.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="vs-divider">VS</div>

            <div className="team-selector">
              <label>Team B</label>
              <select
                value={selectedTeamB}
                onChange={(e) => setSelectedTeamB(e.target.value)}
              >
                <option value="">Select Team</option>
                {teams.map((team) => (
                  <option key={team.id} value={team.id}>
                    {team.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button
            className="btn-success button-large"
            onClick={startMatch}
            disabled={simulating || !selectedTeamA || !selectedTeamB}
          >
            🏁 Start Match
          </button>
        </div>
      ) : (
        <div className="match-running">
          <div className="match-header">
            <div className="match-score">
              <div className="team-score">
                <h3>{match.team_a.name}</h3>
                <div className="score">{match.score.team_a}</div>
              </div>
              <div className="match-time">
                <div className="minute">⏱️ {match.current_minute}'</div>
                <div className="half">{match.half === 1 ? 'H1' : 'H2'}</div>
                <div className="status">{match.status.toUpperCase()}</div>
              </div>
              <div className="team-score">
                <h3>{match.team_b.name}</h3>
                <div className="score">{match.score.team_b}</div>
              </div>
            </div>
          </div>

          <div className="match-controls">
            {match.status !== 'finished' && (
              <>
                <button
                  className="btn-primary"
                  onClick={simulateNextMinute}
                  disabled={simulating}
                >
                  {simulating ? '⏳ Simulating...' : '▶️ Next Minute'}
                </button>
                <button
                  className={autoSimulate ? 'btn-danger' : 'btn-success'}
                  onClick={() => setAutoSimulate(!autoSimulate)}
                  disabled={simulating}
                >
                  {autoSimulate ? '⏸️ Pause' : '▶️▶️ Auto Play'}
                </button>
              </>
            )}
            <button className="btn-secondary" onClick={resetMatch}>
              🔄 New Match
            </button>
          </div>

          <div className="match-content">
            <div className="events-panel">
              <h3>📺 Live Commentary</h3>
              <div className="events-list">
                {match.events.length === 0 ? (
                  <p className="no-events">Waiting for events...</p>
                ) : (
                  [...match.events].reverse().map((event, idx) => (
                    <div key={idx} className="event-item">
                      <div className="event-time">{event.minute}'{event.second}"</div>
                      <div className="event-content">
                        <p className="event-commentary">{event.commentary}</p>
                        <p className="event-details">{event.description}</p>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>

            {stats && (
              <div className="stats-panel">
                <h3>📊 Live Statistics</h3>
                <div className="stats-content">
                  <div className="team-stats">
                    <h4>{stats.team_a.name}</h4>
                    <div className="stat-row">
                      <span>Possession:</span>
                      <span>{stats.team_a.stats.possession_percent || 50}%</span>
                    </div>
                    <div className="stat-row">
                      <span>Shots:</span>
                      <span>{stats.team_a.stats.shots || 0}</span>
                    </div>
                    <div className="stat-row">
                      <span>Shots on Target:</span>
                      <span>{stats.team_a.stats.shots_on_target || 0}</span>
                    </div>
                    <div className="stat-row">
                      <span>Passes:</span>
                      <span>{stats.team_a.stats.passes_completed || 0}</span>
                    </div>
                    <div className="stat-row">
                      <span>Tackles:</span>
                      <span>{stats.team_a.stats.tackles || 0}</span>
                    </div>
                  </div>

                  <div className="team-stats">
                    <h4>{stats.team_b.name}</h4>
                    <div className="stat-row">
                      <span>Possession:</span>
                      <span>{stats.team_b.stats.possession_percent || 50}%</span>
                    </div>
                    <div className="stat-row">
                      <span>Shots:</span>
                      <span>{stats.team_b.stats.shots || 0}</span>
                    </div>
                    <div className="stat-row">
                      <span>Shots on Target:</span>
                      <span>{stats.team_b.stats.shots_on_target || 0}</span>
                    </div>
                    <div className="stat-row">
                      <span>Passes:</span>
                      <span>{stats.team_b.stats.passes_completed || 0}</span>
                    </div>
                    <div className="stat-row">
                      <span>Tackles:</span>
                      <span>{stats.team_b.stats.tackles || 0}</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {match.status === 'finished' && (
            <div className="match-result">
              <h2>🏆 MATCH FINISHED</h2>
              <div className="result-score">
                <div>
                  <h3>{match.team_a.name}</h3>
                  <div className="final-score">{match.score.team_a}</div>
                </div>
                <div className="result-divider">-</div>
                <div>
                  <h3>{match.team_b.name}</h3>
                  <div className="final-score">{match.score.team_b}</div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default MatchSimulator;
