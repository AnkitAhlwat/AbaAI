from enum import Enum


class Piece(Enum):
    BLACK = 1
    WHITE = 2


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def as_tuple(self):
        return self.x, self.y

    def is_adjacent_to(self, position2) -> bool:
        return position2 in self.get_adjacent_positions()

    def get_adjacent_positions(self) -> list['Position']:
        x, y = self.x, self.y
        possible_moves = [
            Position(x - 1, y),
            Position(x + 1, y),
            Position(x, y - 1),
            Position(x, y + 1),
            Position(x + 1, y - 1),
            Position(x - 1, y + 1)
        ]

        return possible_moves

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

    @staticmethod
    def are_in_line(position1: 'Position', position2: 'Position', position3: 'Position') -> bool:
        return (
                (position1.x == position2.x == position3.x)
                or
                (position1.y == position2.y == position3.y)
                or
                (position1.x - position1.y == position2.x - position2.y == position3.x - position3.y)
                or
                (position1.x + position1.y == position2.x + position2.y == position3.x + position3.y)
        )

    @staticmethod
    def are_positions_adjacent_and_in_line(position1: 'Position', position2: 'Position', position3: 'Position') -> bool:
        # check if the positions are all along the same line
        if not Position.are_in_line(position1, position2, position3):
            return False

        # check if the positions are adjacent to each other
        if not (
                (position1.is_adjacent_to(position2) and position2.is_adjacent_to(position3))
                or
                (position1.is_adjacent_to(position3) and position3.is_adjacent_to(position2))
                or
                (position2.is_adjacent_to(position1) and position1.is_adjacent_to(position3))
        ):
            return False

        return True


class Move:
    def __init__(self, previous_positions: list[Position], next_positions: list[Position], player: Piece):
        self._previous_positions = previous_positions
        self._next_positions = next_positions
        self._player = player

    def __repr__(self):
        return f'Previous: {self._previous_positions}, Next: {self._next_positions}, Player: {self._player}'

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
