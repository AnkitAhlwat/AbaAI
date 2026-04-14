"""Session management for Abalone game platform."""

from __future__ import annotations

import secrets
import uuid

from .engine import (
    Board,
    BoardLayout,
    GameState,
    Move,
    Piece,
    apply_move,
    generate_all_legal_moves,
    notation_to_coord,
)


BOARD_LAYOUT_MAP = {
    "Default": BoardLayout.DEFAULT,
    "Belgian Daisy": BoardLayout.BELGIAN_DAISY,
    "German Daisy": BoardLayout.GERMAN_DAISY,
}


class GameSession:
    """A single game between two players."""

    def __init__(self, game_id: str, layout: BoardLayout = BoardLayout.DEFAULT):
        self.game_id = game_id
        self.layout = layout
        self.board = Board(layout.value)
        self.state = GameState(
            self.board, Piece.BLACK,
            self.board.count(Piece.BLACK.value),
            self.board.count(Piece.WHITE.value),
        )
        self.status = "waiting"  # waiting | in_progress | game_over

        self.player_black_token: str | None = None
        self.player_white_token: str | None = None
        self.winner: str | None = None

        self.move_history: list[dict] = []
        self._legal_moves: list[Move] | None = None

    @property
    def legal_moves(self) -> list[Move]:
        if self._legal_moves is None:
            self._legal_moves = generate_all_legal_moves(self.state)
        return self._legal_moves

    def assign_player(self, color: Piece) -> str:
        token = secrets.token_urlsafe(16)
        if color == Piece.BLACK:
            self.player_black_token = token
        else:
            self.player_white_token = token
        return token

    def token_to_color(self, token: str) -> Piece | None:
        if token == self.player_black_token:
            return Piece.BLACK
        if token == self.player_white_token:
            return Piece.WHITE
        return None

    def is_players_turn(self, token: str) -> bool:
        color = self.token_to_color(token)
        return color == self.state.turn

    def both_players_joined(self) -> bool:
        return self.player_black_token is not None and self.player_white_token is not None

    def apply_move(self, move: Move) -> None:
        self.state = apply_move(self.state, move)
        self.move_history.append(move.to_notation())
        self._legal_moves = None  # invalidate cache

        if self.state.is_game_over():
            self.status = "game_over"
            w = self.state.winner()
            self.winner = "black" if w == Piece.BLACK else "white" if w else None

    def find_move_by_index(self, index: int) -> Move | None:
        moves = self.legal_moves
        if 0 <= index < len(moves):
            return moves[index]
        return None

    def find_move_by_notation(self, from_notations: list[str], to_notations: list[str]) -> Move | None:
        from_coords = sorted(notation_to_coord(n) for n in from_notations)
        to_coords = sorted(notation_to_coord(n) for n in to_notations)

        for move in self.legal_moves:
            if sorted(move.from_positions) == from_coords and sorted(move.to_positions) == to_coords:
                return move
        return None

    def get_state_for_player(self, token: str) -> dict:
        color = self.token_to_color(token)
        state_dict = self.state.to_dict()

        moves_notation = [m.to_notation() for m in self.legal_moves] if self.status == "in_progress" else []

        return {
            "game_id": self.game_id,
            "status": self.status,
            "board": state_dict["board"],
            "turn": state_dict["turn"],
            "your_turn": self.is_players_turn(token) if color else False,
            "captures": state_dict["captures"],
            "legal_moves": moves_notation,
            "move_number": len(self.move_history),
            "winner": self.winner,
        }


class SessionManager:
    """Manages all active game sessions."""

    def __init__(self):
        self._sessions: dict[str, GameSession] = {}

    def create_game(self, layout_name: str = "Default") -> tuple[GameSession, str]:
        game_id = uuid.uuid4().hex[:8]
        layout = BOARD_LAYOUT_MAP.get(layout_name, BoardLayout.DEFAULT)
        session = GameSession(game_id, layout)
        token = session.assign_player(Piece.BLACK)
        self._sessions[game_id] = session
        return session, token

    def get_session(self, game_id: str) -> GameSession | None:
        return self._sessions.get(game_id)

    def join_game(self, game_id: str) -> tuple[GameSession, str] | None:
        session = self.get_session(game_id)
        if session is None:
            return None
        if session.player_white_token is not None:
            return None  # already full
        token = session.assign_player(Piece.WHITE)
        if session.both_players_joined():
            session.status = "in_progress"
        return session, token
