"""Unified Move type using (x, y) tuples with algebraic notation support."""

from __future__ import annotations

from .board import Piece


# --- Coordinate conversion ---
# Board grid: x = column (0-8), y = row (0-8, top = I = y0)
# Algebraic:  letter = row (I..A), number = column+1 (1..9)

def coord_to_notation(x: int, y: int) -> str:
    return f"{chr(73 - y)}{x + 1}"


def notation_to_coord(notation: str) -> tuple[int, int]:
    letter = notation[0].upper()
    number = int(notation[1])
    return (number - 1, 73 - ord(letter))


# Six hex directions on the Abalone board
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (-1, 1)]


class Move:
    """
    Represents a single Abalone move.

    Positions are stored as (x, y) tuples internally.
    from_positions / to_positions: the player's marbles before and after.
    from_opponent / to_opponent: opponent marbles displaced (sumito).
    """

    __slots__ = [
        "_from_positions",
        "_to_positions",
        "_player",
        "_from_opponent",
        "_to_opponent",
    ]

    def __init__(
        self,
        from_positions: list[tuple[int, int]],
        to_positions: list[tuple[int, int]],
        player: Piece,
        from_opponent: list[tuple[int, int]] | None = None,
        to_opponent: list[tuple[int, int]] | None = None,
    ):
        self._from_positions = from_positions
        self._to_positions = to_positions
        self._player = player
        self._from_opponent = from_opponent or []
        self._to_opponent = to_opponent or []

    # --- Properties ---

    @property
    def from_positions(self) -> list[tuple[int, int]]:
        return self._from_positions

    @property
    def to_positions(self) -> list[tuple[int, int]]:
        return self._to_positions

    @property
    def from_opponent(self) -> list[tuple[int, int]]:
        return self._from_opponent

    @property
    def to_opponent(self) -> list[tuple[int, int]]:
        return self._to_opponent

    @property
    def player(self) -> Piece:
        return self._player

    @property
    def is_sumito(self) -> bool:
        return len(self._from_opponent) > 0

    @property
    def is_capture(self) -> bool:
        return len(self._from_opponent) > len(self._to_opponent)

    # --- Algebraic notation ---

    def to_notation(self) -> dict:
        result = {
            "from": [coord_to_notation(x, y) for x, y in self._from_positions],
            "to": [coord_to_notation(x, y) for x, y in self._to_positions],
        }
        if self._from_opponent:
            pushed = [
                coord_to_notation(x, y)
                for x, y in self._from_opponent
            ]
            result["pushed"] = pushed
        return result

    @classmethod
    def from_notation(cls, data: dict, player: Piece) -> Move:
        from_positions = [notation_to_coord(n) for n in data["from"]]
        to_positions = [notation_to_coord(n) for n in data["to"]]
        return cls(from_positions, to_positions, player)

    # --- Sorting (prioritise sumito, then larger groups) ---

    def __lt__(self, other):
        if len(self._to_opponent) != len(other._to_opponent):
            return len(self._to_opponent) > len(other._to_opponent)
        return len(self._from_positions) > len(other._from_positions)

    def __repr__(self):
        frm = ",".join(coord_to_notation(x, y) for x, y in self._from_positions)
        to = ",".join(coord_to_notation(x, y) for x, y in self._to_positions)
        return f"{frm} -> {to}"

    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return (
            sorted(self._from_positions) == sorted(other._from_positions)
            and sorted(self._to_positions) == sorted(other._to_positions)
            and self._player == other._player
            and sorted(self._from_opponent) == sorted(other._from_opponent)
            and sorted(self._to_opponent) == sorted(other._to_opponent)
        )

    def __hash__(self):
        return hash((
            tuple(sorted(self._from_positions)),
            tuple(sorted(self._to_positions)),
            self._player,
        ))
