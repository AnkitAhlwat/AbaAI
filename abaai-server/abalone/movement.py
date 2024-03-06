from enum import Enum


class Turn(Enum):
    MAX = 1
    MIN = 2


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Move:
    def __init__(self, previous_positions: list[Position], next_positions: list[Position], player: Turn):
        self._previous_positions = previous_positions
        self._next_positions = next_positions
        self._player = player

    @property
    def previous_positions(self):
        return self._previous_positions

    @property
    def next_positions(self):
        return self._next_positions

    @property
    def player(self):
        return self._player

    def to_json(self):
        return {
            'previous_positions': [{'x': position.x, 'y': position.y} for position in self._previous_positions],
            'next_positions': [{'x': position.x, 'y': position.y} for position in self._next_positions],
            'player': self._player.value
        }

    @classmethod
    def from_json(cls, json):
        previous_positions = [Position(position['x'], position['y']) for position in json['previous_positions']]
        next_positions = [Position(position['x'], position['y']) for position in json['next_positions']]
        player = Turn(json['player'])
        return cls(previous_positions, next_positions, player)
