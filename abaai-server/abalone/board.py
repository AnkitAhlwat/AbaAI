from enum import Enum


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
    NONE = -1


class Board:
    def __init__(self, layout: BoardLayout = BoardLayout.DEFAULT):
        self._layout = layout
        self._board = [row[:] for row in layout.value]

    @property
    def board(self):
        return self._board

    def to_json(self):
        return self._board

    def get_space_state(self, x: int, y: int) -> SpaceState:
        return SpaceState(self._board[y][x])

    def set_space_state(self, x: int, y: int, state: SpaceState):
        self._board[y][x] = state.value

    def make_move(self, move):
        for position in move.previous_positions:
            self.set_space_state(position.x, position.y, SpaceState.EMPTY)

        for position in move.next_positions:
            self.set_space_state(position.x, position.y, SpaceState(move.player.value))

    def undo_move(self, move):
        for position in move.next_positions:
            self.set_space_state(position.x, position.y, SpaceState.EMPTY)

        for position in move.previous_positions:
            self.set_space_state(position.x, position.y, SpaceState(move.player.value))
