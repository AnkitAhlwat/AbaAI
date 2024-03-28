from enum import Enum
import itertools

from abalone.movement import Move, Position

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
    __slots__ = ['_array', '_width', '_height']

    def __init__(self, layout=None):
        self._width = 9
        self._height = 9
        if layout is None:
            self._array = self._flatten_layout(BoardLayout.DEFAULT.value)
        if isinstance(layout[0], list):
            self._array = self._flatten_layout(layout)
        else:
            self._array = layout

    @staticmethod
    def _flatten_layout(layout_2d):
        """Convert a 2D layout to a flat array if needed."""
        return list(itertools.chain.from_iterable(layout_2d))

    def _get_index(self, x: int, y: int) -> int:
        """Calculate the flat array index for the board position (x, y)."""
        return y * self._width + x

    def get_space_state(self, x: int, y: int) -> SpaceState:
        """Get the state of the space at position (x, y)."""
        index = self._get_index(x, y)
        return SpaceState(self._array[index])

    def set_space_state(self, x: int, y: int, state: SpaceState):
        """Set the state of the space at position (x, y)."""
        index = self._get_index(x, y)
        self._array[index] = state.value


    def make_move(self, move_obj):
        for position in move_obj.previous_player_positions:
            self.set_space_state(position.x, position.y, SpaceState.EMPTY)

        for position in move_obj.previous_opponent_positions:
            self.set_space_state(position.x, position.y, SpaceState.EMPTY)

        for position in move_obj.next_player_positions:
            self.set_space_state(position.x, position.y, SpaceState(move_obj.player.value))

        for position in move_obj.next_opponent_positions:
            self.set_space_state(position.x, position.y, SpaceState(3 - move_obj.player.value))

    def __repr__(self):
        """Generate a 2D board-like representation for printing."""
        rows = [self._array[i:i + self._width] for i in range(0, self._height * self._width, self._width)]
        return '\n'.join([' '.join(str(cell) for cell in row) for row in rows])


board =OptimizedBoard(
    [-1, -1, -1, -1, 0, 0, 0, 0, 0,
        -1, -1, -1, 0, 0, 1, 2, 2, 2,
        -1, -1, 0, 0, 2, 1, 2, 2, 2,
        -1, 0, 0, 2, 1, 1, 1, 1, 0,
        0, 0, 0, 1, 1, 1, 2, 0, 0,
        0, 0, 2, 2, 1, 2, 0, 0, -1,
        0, 0, 2, 2, 1, 0, 0, -1, -1,
        0, 0, 0, 0, 0, 0, -1, -1, -1,
        0, 0, 0, 0, 0, -1, -1, -1, -1])
print(board)

move = Move(
    previous_player_positions=[Position(4, 5), Position(5, 4), Position(6, 3)],
    next_player_positions=[Position(5, 4), Position(6, 3), Position(7, 2)],
    player=Piece.BLACK,
    previous_opponent_positions=[Position(7, 2), Position(8, 1)],
    next_opponent_positions=[Position(8, 1)]
)
board.make_move(move)
print()
print(board)