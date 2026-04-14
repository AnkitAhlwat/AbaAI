import itertools
from enum import Enum


class Piece(Enum):
    BLACK = 1
    WHITE = 2

    @property
    def opponent(self):
        return Piece.WHITE if self == Piece.BLACK else Piece.BLACK


class SpaceState(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    OUT_OF_BOUNDS = -1


class BoardLayout(Enum):
    EMPTY = [
        [-1, -1, -1, -1, 0, 0, 0, 0, 0],
        [-1, -1, -1, 0, 0, 0, 0, 0, 0],
        [-1, -1, 0, 0, 0, 0, 0, 0, 0],
        [-1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, -1],
        [0, 0, 0, 0, 0, 0, 0, -1, -1],
        [0, 0, 0, 0, 0, 0, -1, -1, -1],
        [0, 0, 0, 0, 0, -1, -1, -1, -1],
    ]

    DEFAULT = [
        [-1, -1, -1, -1, 2, 2, 2, 2, 2],
        [-1, -1, -1, 2, 2, 2, 2, 2, 2],
        [-1, -1, 0, 0, 2, 2, 2, 0, 0],
        [-1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, -1],
        [0, 0, 1, 1, 1, 0, 0, -1, -1],
        [1, 1, 1, 1, 1, 1, -1, -1, -1],
        [1, 1, 1, 1, 1, -1, -1, -1, -1],
    ]

    BELGIAN_DAISY = [
        [-1, -1, -1, -1, 2, 2, 0, 1, 1],
        [-1, -1, -1, 2, 2, 2, 1, 1, 1],
        [-1, -1, 0, 2, 2, 0, 1, 1, 0],
        [-1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, -1],
        [0, 1, 1, 0, 2, 2, 0, -1, -1],
        [1, 1, 1, 2, 2, 2, -1, -1, -1],
        [1, 1, 0, 2, 2, -1, -1, -1, -1],
    ]

    GERMAN_DAISY = [
        [-1, -1, -1, -1, 0, 0, 0, 0, 0],
        [-1, -1, -1, 2, 2, 0, 0, 1, 1],
        [-1, -1, 2, 2, 2, 0, 1, 1, 1],
        [-1, 0, 2, 2, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 2, 2, 0, -1],
        [1, 1, 1, 0, 2, 2, 2, -1, -1],
        [1, 1, 0, 0, 2, 2, -1, -1, -1],
        [0, 0, 0, 0, 0, -1, -1, -1, -1],
    ]


WIDTH = 9
HEIGHT = 9


class Board:
    __slots__ = ["array"]

    def __init__(self, layout=None):
        if layout is None:
            self.array = self._flatten_layout(BoardLayout.DEFAULT.value)
        elif isinstance(layout, list) and layout and isinstance(layout[0], int):
            self.array = list(layout)
        elif isinstance(layout, list) and layout and isinstance(layout[0], list):
            self.array = self._flatten_layout(layout)
        else:
            self.array = self._flatten_layout(BoardLayout.DEFAULT.value)

    def copy(self):
        b = Board.__new__(Board)
        b.array = self.array[:]
        return b

    @staticmethod
    def _flatten_layout(layout_2d):
        return list(itertools.chain.from_iterable(layout_2d))

    @staticmethod
    def _get_index(x: int, y: int) -> int:
        return y * WIDTH + x

    def get(self, x: int, y: int) -> int:
        return self.array[self._get_index(x, y)]

    def set(self, x: int, y: int, value: int):
        self.array[self._get_index(x, y)] = value

    def apply_move(self, move):
        for x, y in move.from_positions:
            self.set(x, y, SpaceState.EMPTY.value)
        for x, y in move.from_opponent:
            self.set(x, y, SpaceState.EMPTY.value)
        for x, y in move.to_positions:
            self.set(x, y, move.player.value)
        for x, y in move.to_opponent:
            self.set(x, y, move.player.opponent.value)

    def count(self, piece_value: int) -> int:
        return self.array.count(piece_value)

    def to_grid(self):
        return [self.array[i:i + WIDTH] for i in range(0, len(self.array), WIDTH)]

    def __repr__(self):
        rows = [self.array[i:i + WIDTH] for i in range(0, HEIGHT * WIDTH, WIDTH)]
        return "\n".join(" ".join(str(cell) for cell in row) for row in rows)

    def __hash__(self):
        return hash(tuple(self.array))

    def __eq__(self, other):
        return isinstance(other, Board) and self.array == other.array
