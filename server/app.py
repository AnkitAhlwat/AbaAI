"""AbaAI Game Platform Server — FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .sessions import SessionManager

app = FastAPI(title="AbaAI Game Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = SessionManager()


# --- Request / Response models ---

class CreateGameRequest(BaseModel):
    layout: str = "Default"


class CreateGameResponse(BaseModel):
    game_id: str
    token: str
    color: str


class JoinGameResponse(BaseModel):
    game_id: str
    token: str
    color: str


class MoveRequest(BaseModel):
    move_index: int | None = None
    from_positions: list[str] | None = Field(None, alias="from")
    to_positions: list[str] | None = Field(None, alias="to")

    model_config = {"populate_by_name": True}


# --- Routes ---

@app.post("/api/games", response_model=CreateGameResponse)
def create_game(body: CreateGameRequest = CreateGameRequest()):
    session, token = manager.create_game(body.layout)
    return CreateGameResponse(game_id=session.game_id, token=token, color="black")


@app.post("/api/games/{game_id}/join", response_model=JoinGameResponse)
def join_game(game_id: str):
    result = manager.join_game(game_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Game not found or already full")
    session, token = result
    return JoinGameResponse(game_id=session.game_id, token=token, color="white")


@app.get("/api/games/{game_id}/state")
def get_state(game_id: str, x_player_token: str = Header()):
    session = manager.get_session(game_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game not found")
    if session.token_to_color(x_player_token) is None:
        raise HTTPException(status_code=403, detail="Invalid player token")
    return session.get_state_for_player(x_player_token)


@app.post("/api/games/{game_id}/move")
def make_move(game_id: str, body: MoveRequest, x_player_token: str = Header()):
    session = manager.get_session(game_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game not found")

    color = session.token_to_color(x_player_token)
    if color is None:
        raise HTTPException(status_code=403, detail="Invalid player token")

    if session.status != "in_progress":
        raise HTTPException(status_code=400, detail="Game is not in progress")

    if not session.is_players_turn(x_player_token):
        raise HTTPException(status_code=400, detail="Not your turn")

    move = None
    if body.move_index is not None:
        move = session.find_move_by_index(body.move_index)
        if move is None:
            raise HTTPException(status_code=400, detail="Invalid move index")
    elif body.from_positions is not None and body.to_positions is not None:
        move = session.find_move_by_notation(body.from_positions, body.to_positions)
        if move is None:
            raise HTTPException(status_code=400, detail="Illegal move")
    else:
        raise HTTPException(
            status_code=400,
            detail="Provide either 'move_index' or 'from'/'to' notation",
        )

    session.apply_move(move)
    return session.get_state_for_player(x_player_token)


@app.get("/api/games/{game_id}/history")
def get_history(game_id: str):
    session = manager.get_session(game_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"game_id": game_id, "moves": session.move_history}
