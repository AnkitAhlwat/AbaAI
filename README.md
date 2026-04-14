# AbaAI — Abalone Game Platform

An open platform for playing and testing AI agents against each other in Abalone.

## Architecture

```
AbaAI/
  client/     → React SPA (play as a human in the browser)
  server/     → FastAPI game server (manages sessions, validates moves)
  agents/     → Bot framework (connect your own AI to the server)
```

The server is model-agnostic. Any HTTP client — a browser, a Python script, a Rust CLI — can play.

## Quick Start

### 1. Start the server

```bash
cd server
pip install -r requirements.txt
uvicorn app:app --reload
```

The API docs are available at `http://localhost:8000/docs`.

### 2. Start the client (optional — for human players)

```bash
cd client
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

### 3. Run a bot

```bash
pip install -r agents/requirements.txt

# Create a game and play as a random bot
python -m agents.runner --server http://localhost:8000 --create --agent random

# Join an existing game with the alpha-beta agent
python -m agents.runner --server http://localhost:8000 --join GAME_ID --agent alphabeta
```

## API Reference

Five endpoints:

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/games` | Create a new game (returns game ID + player token) |
| `POST` | `/api/games/{id}/join` | Join as second player (returns player token) |
| `GET` | `/api/games/{id}/state` | Get current state (board, turn, legal moves) |
| `POST` | `/api/games/{id}/move` | Submit a move |
| `GET` | `/api/games/{id}/history` | Move history |

### Game state response

```json
{
  "game_id": "abc123",
  "status": "in_progress",
  "board": [[0,0,0,0,1,1,1,1,1], ...],
  "turn": "black",
  "your_turn": true,
  "captures": {"black": 0, "white": 2},
  "legal_moves": [
    {"from": ["E5"], "to": ["E6"]},
    {"from": ["D4","E5"], "to": ["D5","E6"], "pushed": ["F6"]}
  ],
  "move_number": 12
}
```

### Submitting a move

Pick from the legal moves list:
```json
{"move_index": 5}
```

Or specify explicitly in algebraic notation:
```json
{"from": ["D4", "E5"], "to": ["D5", "E6"]}
```

Pass your player token in the `X-Player-Token` header.

## Build Your Own Bot

1. Create a class that extends `AbaloneAgent`:

```python
from agents.base import AbaloneAgent

class MyBot(AbaloneAgent):
    def select_move(self, game_state: dict) -> dict:
        # game_state has: board, turn, legal_moves, captures, etc.
        # Return {"move_index": int} or {"from": [...], "to": [...]}
        return {"move_index": 0}  # always pick first legal move
```

2. Run it:

```bash
python -m agents.runner --server http://localhost:8000 --join GAME_ID --agent my_module.MyBot
```

## Board Coordinates

The board is a 9x9 grid. Algebraic notation uses letters I-A (top to bottom) and numbers 1-9 (left to right).

Cell values: `0` = empty, `1` = black, `2` = white, `-1` = out of bounds.

## License

GPL v3 — see [LICENSE](LICENSE).
