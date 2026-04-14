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

    Positions are (x, y) tuples.
    from_positions / to_positions: the player's marbles before and after.
    from_opponent / to_opponent: opponent marbles displaced (sumito).
    """

    __slots__ = ["from_positions", "to_positions", "player", "from_opponent", "to_opponent"]

    def __init__(
        self,
        from_positions: list[tuple[int, int]],
        to_positions: list[tuple[int, int]],
        player: Piece,
        from_opponent: list[tuple[int, int]] | None = None,
        to_opponent: list[tuple[int, int]] | None = None,
    ):
        self.from_positions = from_positions
        self.to_positions = to_positions
        self.player = player
        self.from_opponent = from_opponent or []
        self.to_opponent = to_opponent or []

    @property
    def is_sumito(self) -> bool:
        return len(self.from_opponent) > 0

    @property
    def is_capture(self) -> bool:
        return len(self.from_opponent) > len(self.to_opponent)

    def to_notation(self) -> dict:
        result = {
            "from": [coord_to_notation(x, y) for x, y in self.from_positions],
            "to": [coord_to_notation(x, y) for x, y in self.to_positions],
        }
        if self.from_opponent:
            result["pushed"] = [coord_to_notation(x, y) for x, y in self.from_opponent]
        return result

    def __lt__(self, other):
        if len(self.to_opponent) != len(other.to_opponent):
            return len(self.to_opponent) > len(other.to_opponent)
        return len(self.from_positions) > len(other.from_positions)

    def __repr__(self):
        frm = ",".join(coord_to_notation(x, y) for x, y in self.from_positions)
        to = ",".join(coord_to_notation(x, y) for x, y in self.to_positions)
        return f"{frm} -> {to}"

    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return (
            sorted(self.from_positions) == sorted(other.from_positions)
            and sorted(self.to_positions) == sorted(other.to_positions)
            and self.player == other.player
            and sorted(self.from_opponent) == sorted(other.from_opponent)
            and sorted(self.to_opponent) == sorted(other.to_opponent)
        )

    def __hash__(self):
        return hash((
            tuple(sorted(self.from_positions)),
            tuple(sorted(self.to_positions)),
            self.player,
            tuple(sorted(self.from_opponent)),
            tuple(sorted(self.to_opponent)),
        ))
