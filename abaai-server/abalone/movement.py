from enum import Enum


class Turn(Enum):
    MAX = 1
    MIN = 2


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Move:
    def __init__(self, previous_position: Position, next_position: Position, player: Turn):
        self.previous_position = previous_position
        self.next_position = next_position
        self.player = player
