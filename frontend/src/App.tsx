import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import PlayerManager from './pages/PlayerManager';
import TeamBuilder from './pages/TeamBuilder';
import MatchSimulator from './pages/MatchSimulator';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="nav-container">
            <Link to="/" className="nav-logo">⚽ Soccer 6v6 Simulator</Link>
            <div className="nav-menu">
              <Link to="/" className="nav-link">Home</Link>
              <Link to="/players" className="nav-link">Players</Link>
              <Link to="/teams" className="nav-link">Teams</Link>
              <Link to="/match" className="nav-link">Match</Link>
            </div>
          </div>
        </nav>

        <div className="container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/players" element={<PlayerManager />} />
            <Route path="/teams" element={<TeamBuilder />} />
            <Route path="/match" element={<MatchSimulator />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div className="home">
      <div className="hero">
        <h1>⚽ Soccer 6v6 Match Simulator</h1>
        <p>Experience realistic football action with AI-powered players</p>
        <div className="hero-buttons">
          <Link to="/players" className="btn-primary button-large">Manage Players</Link>
          <Link to="/teams" className="btn-secondary button-large">Create Teams</Link>
          <Link to="/match" className="btn-success button-large">Start Match</Link>
        </div>
      </div>

      <div className="features">
        <div className="feature-card">
          <h3>🎮 Real-Time Simulation</h3>
          <p>Watch minute-by-minute action with live commentary</p>
        </div>
        <div className="feature-card">
          <h3>👥 Player Management</h3>
          <p>Create and manage your players with detailed attributes</p>
        </div>
        <div className="feature-card">
          <h3>📊 Detailed Statistics</h3>
          <p>Track player performance and team statistics</p>
        </div>
        <div className="feature-card">
          <h3>⚙️ AI Players</h3>
          <p>AI-powered players with realistic decision making</p>
        </div>
      </div>
    </div>
  );
}

export default App;
