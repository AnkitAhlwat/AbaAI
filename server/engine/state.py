from __future__ import annotations

from .board import Board, Piece, WIDTH
from .movement import Move


class GameState:
    __slots__ = ["_board", "_turn", "_black_remaining", "_white_remaining"]

    def __init__(
        self,
        board: Board | None = None,
        turn: Piece = Piece.BLACK,
        black_remaining: int = 14,
        white_remaining: int = 14,
    ):
        self._board = board if board is not None else Board()
        self._turn = turn
        self._black_remaining = black_remaining
        self._white_remaining = white_remaining

    @property
    def board(self) -> Board:
        return self._board

    @property
    def turn(self) -> Piece:
        return self._turn

    @property
    def black_remaining(self) -> int:
        return self._black_remaining

    @property
    def white_remaining(self) -> int:
        return self._white_remaining

    @property
    def remaining_player_marbles(self) -> int:
        return self._black_remaining if self._turn == Piece.BLACK else self._white_remaining

    @property
    def remaining_opponent_marbles(self) -> int:
        return self._white_remaining if self._turn == Piece.BLACK else self._black_remaining

    def is_game_over(self) -> bool:
        return self._black_remaining <= 8 or self._white_remaining <= 8

    def winner(self) -> Piece | None:
        if not self.is_game_over():
            return None
        if self._black_remaining <= 8:
            return Piece.WHITE
        return Piece.BLACK

    def __hash__(self):
        return hash((hash(self._board), self._turn.value))

    def __eq__(self, other):
        return (
            isinstance(other, GameState)
            and self._board == other._board
            and self._turn == other._turn
        )

    def to_dict(self) -> dict:
        captured_black = 14 - self._board.count(Piece.BLACK.value)
        captured_white = 14 - self._board.count(Piece.WHITE.value)
        return {
            "board": self._board.to_grid(),
            "turn": "black" if self._turn == Piece.BLACK else "white",
            "captures": {
                "black": captured_black,
                "white": captured_white,
            },
        }

    def piece_positions(self, piece: Piece) -> list[tuple[int, int]]:
        positions = []
        for idx, val in enumerate(self._board.array):
            if val == piece.value:
                positions.append((idx % WIDTH, idx // WIDTH))
        return positions


class GameStateUpdate:
    """Apply a move to a state to produce the resulting state."""

    __slots__ = ["_previous", "_move", "_resulting"]

    def __init__(self, previous: GameState, move: Move):
        self._previous = previous
        self._move = move
        self._resulting = self._generate()

    @property
    def resulting_state(self) -> GameState:
        return self._resulting

    def _generate(self) -> GameState:
        new_board = self._previous.board.copy()
        new_board.apply_move(self._move)

        next_turn = self._previous.turn.opponent
        black_count = new_board.count(Piece.BLACK.value)
        white_count = new_board.count(Piece.WHITE.value)

        return GameState(new_board, next_turn, black_count, white_count)
