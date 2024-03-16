from enum import Enum


class Piece(Enum):
    BLACK = 1
    WHITE = 2


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @staticmethod
    def get_y_from_letter(letter: str):
        return (65 + 8) - ord(letter)

    @staticmethod
    def get_letter_from_y(y: int):
        return chr(65 + 8 - y)

    @staticmethod
    def get_x_from_number(number: int):
        return number - 1

    @staticmethod
    def get_number_from_x(x: int):
        return x + 1


class Move:
    def __init__(self, previous_positions: list[Position], next_positions: list[Position], player: Piece):
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
        player = Piece(json['player'])
        return cls(previous_positions, next_positions, player)
