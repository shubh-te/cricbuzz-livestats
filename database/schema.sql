CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    team TEXT DEFAULT 'Unknown',
    role TEXT,
    runs INTEGER,
    wickets INTEGER
);

CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team1 TEXT,
    team2 TEXT,
    winner TEXT,
    date TEXT
);