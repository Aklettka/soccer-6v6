// Simple service worker that emulates the Flask API in-browser using the Cache API for persistence.
// It intercepts requests to /api/* and responds with generated/stored JSON data so the app can work as a
// fully-static site (frontend + in-browser backend) suitable for GitHub Pages.

const DB_CACHE = 'soccer-db-v1';
const PLAYERS_KEY = '/db/players';
const TEAMS_KEY = '/db/teams';
const MATCHES_KEY = '/db/matches';

self.addEventListener('install', (event) => {
  event.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

// Helpers using Cache API to store JSON blobs by key
async function readDB(key) {
  const cache = await caches.open(DB_CACHE);
  const resp = await cache.match(key);
  if (!resp) return null;
  try {
    return await resp.json();
  } catch (e) {
    return null;
  }
}

async function writeDB(key, obj) {
  const cache = await caches.open(DB_CACHE);
  const body = JSON.stringify(obj);
  const resp = new Response(body, { headers: { 'Content-Type': 'application/json' } });
  await cache.put(key, resp);
}

function jsonResponse(obj, code = 200) {
  return new Response(JSON.stringify(obj), {
    status: code,
    headers: { 'Content-Type': 'application/json' }
  });
}

function uuid() {
  if (self.crypto && crypto.randomUUID) return crypto.randomUUID();
  // fallback
  return 'id-' + Math.random().toString(36).slice(2, 10);
}

// Minimal simulator ported to JS (simplified behavior matching original endpoints)
function createEmptyMatch(teamA, teamB) {
  return {
    id: uuid(),
    status: 'created',
    current_minute: 0,
    half: 1,
    team_a: teamA,
    team_b: teamB,
    score: { team_a: 0, team_b: 0 },
    events: []
  };
}

function generateEvent(match, team, type, minute, second) {
  const ev = {
    minute,
    second,
    event_type: type,
    team_id: team.id,
    player_id: (team.players && team.players.length) ? team.players[Math.floor(Math.random() * team.players.length)].id : '',
    player_name: (team.players && team.players.length) ? team.players[Math.floor(Math.random() * team.players.length)].name : '',
    description: type === 'goal' ? 'Goal scored' : type,
    commentary: `${type.toUpperCase()} at ${minute}'`,
    result: type
  };
  return ev;
}

function simulateOneMinute(match) {
  // Ensure status
  if (match.status === 'created') {
    match.status = 'first_half';
    match.current_minute = 0;
    match.half = 1;
  }

  if (match.current_minute >= 60 || match.status === 'finished') {
    match.status = 'finished';
    return { match, events: [] };
  }

  const numActions = Math.floor(Math.random() * 3) + 2; // 2-4
  const events = [];
  for (let i = 0; i < numActions; i++) {
    const second = (i + 1) * 15;
    const minute = match.current_minute + 1;
    // pick team with possession randomly
    const possession = Math.random() > 0.5 ? 'team_a' : 'team_b';
    const team = possession === 'team_a' ? match.team_a : match.team_b;
    const types = ['pass', 'dribble', 'shot'];
    let type = types[Math.floor(Math.random() * types.length)];
    // small chance of goal on shot
    if (type === 'shot' && Math.random() > 0.7) {
      type = 'goal';
    }
    const ev = generateEvent(match, team, type, minute, second);
    if (ev.event_type === 'goal') {
      if (possession === 'team_a') match.score.team_a += 1;
      else match.score.team_b += 1;
    }
    match.events.push(ev);
    events.push(ev);
  }

  match.current_minute += 1;
  if (match.current_minute === 30 && match.half === 1) {
    match.half = 2;
    match.status = 'second_half';
    // halftime event
    const ev = {
      minute: match.current_minute,
      second: 0,
      event_type: 'halftime',
      team_id: '',
      player_id: '',
      player_name: '',
      description: 'Halftime',
      commentary: 'Halftime',
      result: 'halftime'
    };
    match.events.push(ev);
    events.push(ev);
  }

  if (match.current_minute >= 60) {
    match.status = 'finished';
  }

  return { match, events };
}

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  // Only intercept same-origin /api/ requests
  if (url.origin === self.origin || url.origin === self.location.origin) {
    if (url.pathname.startsWith('/api/')) {
      event.respondWith(handleApiRequest(event.request));
      return;
    }
  }

  // Otherwise default fetch (serve static files normally)
  event.respondWith(fetch(event.request));
});

async function ensureDefaults() {
  const players = await readDB(PLAYERS_KEY);
  const teams = await readDB(TEAMS_KEY);
  const matches = await readDB(MATCHES_KEY);
  if (!players) await writeDB(PLAYERS_KEY, []);
  if (!teams) await writeDB(TEAMS_KEY, []);
  if (!matches) await writeDB(MATCHES_KEY, {});
}

async function handleApiRequest(request) {
  await ensureDefaults();
  const url = new URL(request.url);
  const parts = url.pathname.split('/').filter(Boolean); // ['api','players', ...]
  // health
  if (url.pathname === '/api/health' && request.method === 'GET') {
    return jsonResponse({ status: 'ok' });
  }

  // Players endpoints
  if (parts[1] === 'players') {
    if (request.method === 'GET' && parts.length === 2) {
      const players = (await readDB(PLAYERS_KEY)) || [];
      return jsonResponse(players);
    }
    if (request.method === 'GET' && parts.length === 3) {
      const players = (await readDB(PLAYERS_KEY)) || [];
      const p = players.find(x => x.id === parts[2]);
      if (!p) return jsonResponse({ error: 'Player not found' }, 404);
      return jsonResponse(p);
    }
    if (request.method === 'POST' && parts.length === 2) {
      const body = await request.json();
      const players = (await readDB(PLAYERS_KEY)) || [];
      const newPlayer = {
        id: uuid(),
        name: body.name || '',
        surname: body.surname || '',
        number: body.number || 0,
        position: body.position || 'FWD',
        attributes: body.attributes || {},
        conditioning: body.conditioning || 100.0,
        is_injured: body.is_injured || false,
        stats: {}
      };
      players.push(newPlayer);
      await writeDB(PLAYERS_KEY, players);
      return jsonResponse(newPlayer, 201);
    }
    if (request.method === 'PUT' && parts.length === 3) {
      const id = parts[2];
      const body = await request.json();
      const players = (await readDB(PLAYERS_KEY)) || [];
      const idx = players.findIndex(x => x.id === id);
      if (idx === -1) return jsonResponse({ error: 'Player not found' }, 404);
      const player = players[idx];
      Object.assign(player, body);
      players[idx] = player;
      await writeDB(PLAYERS_KEY, players);
      return jsonResponse(player);
    }
    if (request.method === 'DELETE' && parts.length === 3) {
      const id = parts[2];
      let players = (await readDB(PLAYERS_KEY)) || [];
      players = players.filter(x => x.id !== id);
      await writeDB(PLAYERS_KEY, players);
      return jsonResponse({ message: 'Player deleted' });
    }
  }

  // Teams endpoints
  if (parts[1] === 'teams') {
    if (request.method === 'GET' && parts.length === 2) {
      const teams = (await readDB(TEAMS_KEY)) || [];
      return jsonResponse(teams);
    }
    if (request.method === 'GET' && parts.length === 3) {
      const teams = (await readDB(TEAMS_KEY)) || [];
      const t = teams.find(x => x.id === parts[2]);
      if (!t) return jsonResponse({ error: 'Team not found' }, 404);
      return jsonResponse(t);
    }
    if (request.method === 'POST' && parts.length === 2) {
      const body = await request.json();
      const teams = (await readDB(TEAMS_KEY)) || [];
      const players = (await readDB(PLAYERS_KEY)) || [];
      const teamPlayers = (body.player_ids || []).map(pid => players.find(p => p.id === pid)).filter(Boolean);
      const newTeam = {
        id: uuid(),
        name: body.name || '',
        formation: body.formation || '1-2-2-1',
        tactics: body.tactics || 'balanced',
        players: teamPlayers
      };
      teams.push(newTeam);
      await writeDB(TEAMS_KEY, teams);
      return jsonResponse(newTeam, 201);
    }
    if (request.method === 'PUT' && parts.length === 3) {
      const id = parts[2];
      const body = await request.json();
      const teams = (await readDB(TEAMS_KEY)) || [];
      const players = (await readDB(PLAYERS_KEY)) || [];
      const idx = teams.findIndex(x => x.id === id);
      if (idx === -1) return jsonResponse({ error: 'Team not found' }, 404);
      const team = teams[idx];
      if ('name' in body) team.name = body.name;
      if ('formation' in body) team.formation = body.formation;
      if ('tactics' in body) team.tactics = body.tactics;
      if ('player_ids' in body) {
        team.players = (body.player_ids || []).map(pid => players.find(p => p.id === pid)).filter(Boolean);
      }
      teams[idx] = team;
      await writeDB(TEAMS_KEY, teams);
      return jsonResponse(team);
    }
    if (request.method === 'DELETE' && parts.length === 3) {
      const id = parts[2];
      let teams = (await readDB(TEAMS_KEY)) || [];
      teams = teams.filter(x => x.id !== id);
      await writeDB(TEAMS_KEY, teams);
      return jsonResponse({ message: 'Team deleted' });
    }
  }

  // Match endpoints
  if (parts[1] === 'match') {
    // POST /api/match/start
    if (request.method === 'POST' && parts.length === 2 && parts[1] === 'match' && url.pathname.endsWith('/start')) {
      const body = await request.json();
      const teams = (await readDB(TEAMS_KEY)) || [];
      const teamA = teams.find(t => t.id === body.team_a_id);
      const teamB = teams.find(t => t.id === body.team_b_id);
      if (!teamA || !teamB) return jsonResponse({ error: 'Teams not found' }, 404);
      const matches = (await readDB(MATCHES_KEY)) || {};
      const match = createEmptyMatch(teamA, teamB);
      matches[match.id] = match;
      await writeDB(MATCHES_KEY, matches);
      return jsonResponse(match, 201);
    }

    // POST /api/match/{id}/simulate
    if (request.method === 'POST' && parts.length === 3 && parts[1] === 'match' && parts[2].length > 0 && url.pathname.endsWith('/simulate')) {
      // path like /api/match/{id}/simulate -> parts = ['api','match','<id>','simulate'] but our split removed empties
      // adjust: rebuild check
    }

    // We'll handle any path starting with /api/match
    const matchPathMatch = url.pathname.match(/^\/api\/match(?:\/([^\/]+))(?:\/(simulate|events|stats))?$/);
    if (matchPathMatch) {
      const matchId = matchPathMatch[1];
      const action = matchPathMatch[2];
      const matches = (await readDB(MATCHES_KEY)) || {};
      if (!matchId) {
        return jsonResponse({ error: 'Bad match path' }, 400);
      }
      const match = matches[matchId];
      if (!match) return jsonResponse({ error: 'Match not found' }, 404);

      if (request.method === 'GET' && !action) {
        return jsonResponse(match);
      }
      if (request.method === 'POST' && action === 'simulate') {
        const result = simulateOneMinute(match);
        matches[matchId] = result.match;
        await writeDB(MATCHES_KEY, matches);
        return jsonResponse({ match: result.match, events: result.events });
      }
      if (request.method === 'GET' && action === 'events') {
        return jsonResponse(match.events || []);
      }
      if (request.method === 'GET' && action === 'stats') {
        const stats = {
          score: match.score,
          current_minute: match.current_minute,
          half: match.half,
          status: match.status
        };
        return jsonResponse(stats);
      }
    }
  }

  return jsonResponse({ error: 'Not found' }, 404);
}
