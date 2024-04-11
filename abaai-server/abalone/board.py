import itertools
from enum import Enum


class Piece(Enum):
    BLACK = 1
    WHITE = 2


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
        [1, 1, 1, 1, 1, -1, -1, -1, -1]
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
        [1, 1, 0, 2, 2, -1, -1, -1, -1]
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


class SpaceState(Enum):
    EMPTY = 0
    MAX = 1
    MIN = 2
    OUT_OF_BOUNDS = -1


class OptimizedBoard:
    __slots__ = ['array', 'width', 'height']

    def __init__(self, layout=None):
        self.width = 9
        self.height = 9
        if layout is None:
            self.array = self._flatten_layout(BoardLayout.DEFAULT.value)
        elif isinstance(layout[0], int):
            self.array = layout
        elif isinstance(layout[0], list):
            self.array = self._flatten_layout(layout)

    @staticmethod
    def _flatten_layout(layout_2d):
        """Convert a 2D layout to a flat array if needed."""
        return list(itertools.chain.from_iterable(layout_2d))

    def _get_index(self, x: int, y: int) -> int:
        """Calculate the flat array index for the board position (x, y)."""
        return y * self.width + x

    def get_space_state(self, x: int, y: int) -> SpaceState:
        """Get the state of the space at position (x, y)."""
        index = self._get_index(x, y)
        return SpaceState(self.array[index])

    def set_space_state(self, x: int, y: int, state: SpaceState):
        """Set the state of the space at position (x, y)."""
        index = self._get_index(x, y)
        self.array[index] = state.value

    def make_move(self, move_obj):
        for position in move_obj.previous_player_positions:
            self.set_space_state(position[0], position[1], SpaceState.EMPTY)

        for position in move_obj.previous_opponent_positions:
            self.set_space_state(position[0], position[1], SpaceState.EMPTY)

        for position in move_obj.next_player_positions:
            self.set_space_state(position[0], position[1], SpaceState(move_obj.player.value))

        for position in move_obj.next_opponent_positions:
            self.set_space_state(position[0], position[1], SpaceState(3 - move_obj.player.value))

    def undo_move(self, move_obj):
        for position in move_obj.next_player_positions:
            self.set_space_state(position.x, position.y, SpaceState.EMPTY)

        for position in move_obj.next_opponent_positions:
            self.set_space_state(position.x, position.y, SpaceState.EMPTY)

        for position in move_obj.previous_player_positions:
            self.set_space_state(position.x, position.y, SpaceState(move_obj.player.value))

        for position in move_obj.previous_opponent_positions:
            self.set_space_state(position.x, position.y, SpaceState(3 - move_obj.player.value))

        return self.to_matrix()

    def __repr__(self):
        """Generate a 2D board-like representation for printing."""
        rows = [self.array[i:i + self.width] for i in range(0, self.height * self.width, self.width)]
        return '\n'.join([' '.join(str(cell) for cell in row) for row in rows])

    def to_json(self):
        return [self.array[i:i + self.width] for i in range(0, len(self.array), self.width)]

    def to_matrix(self):
        return [self.array[i:i + self.width] for i in range(0, len(self.array), self.width)]
