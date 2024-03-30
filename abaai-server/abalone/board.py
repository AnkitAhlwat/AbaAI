from enum import Enum

from abalone.movement import Piece


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


class Board:
    def __init__(self, board_array: list[list[int]] = None):
        if board_array is None:
            self._array = [row[:]for row in BoardLayout.DEFAULT.value]
        else:
            self._array = [row[:] for row in board_array]

    def __repr__(self):
        return str(self._array)

    @property
    def array(self):
        return self._array

    def to_json(self):
        return self._array

    def get_space_state(self, x: int, y: int) -> SpaceState:
        return SpaceState(self._array[y][x])

    def set_space_state(self, x: int, y: int, state: SpaceState):
        self._array[y][x] = state.value

    def make_move(self, move) -> list[list[int]]:
        player = move.player
        opponent = Piece.WHITE if player == Piece.BLACK else Piece.BLACK

        # Set the previous positions to empty for both player and opponent
        for player_position in move.previous_player_positions:
            self.set_space_state(player_position.x, player_position.y, SpaceState.EMPTY)
        for opponent_position in move.previous_opponent_positions:
            self.set_space_state(opponent_position.x, opponent_position.y, SpaceState.EMPTY)

        # Set the next positions to the player and opponent numbers if it is not out of bounds (-1)
        for player_position in move.next_player_positions:
            if self.get_space_state(player_position.x, player_position.y) != SpaceState.OUT_OF_BOUNDS:
                self.set_space_state(player_position.x, player_position.y, SpaceState(player.value))
        for opponent_position in move.next_opponent_positions:
            if self.get_space_state(opponent_position.x, opponent_position.y) != SpaceState.OUT_OF_BOUNDS:
                self.set_space_state(opponent_position.x, opponent_position.y, SpaceState(opponent.value))

        return self._array

    def undo_move(self, move) -> list[list[int]]:
        for position in move.next_positions:
            self.set_space_state(position.x, position.y, SpaceState.EMPTY)

        for position in move.previous_positions:
            self.set_space_state(position.x, position.y, SpaceState(move.player.value))

        return self._array
