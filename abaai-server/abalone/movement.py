from enum import Enum


class Piece(Enum):
    BLACK = 1
    WHITE = 2


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def to_notation(self):
        return f'{Position.get_letter_from_y(self.y)}{Position.get_number_from_x(self.x)}'

    @staticmethod
    def to_notation_generic(x: int, y: int):
        return f'{Position.get_letter_from_y(y)}{Position.get_number_from_x(x)}'

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

    def to_json(self):
        return {'x': self.x, 'y': self.y}

    def to_string(self):
        return f'({self.x},{self.y})'

    def __iter__(self):
        """Allow the Position object to be iterable, so it can be unpacked like a tuple."""
        return iter((self.x, self.y))

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of range for Position")


class Move:
    def __init__(
            self,
            previous_player_positions: list[Position],
            next_player_positions: list[Position],
            player: Piece,
            previous_opponent_positions: list[Position] = None,
            next_opponent_positions: list[Position] = None,
    ):
        self._previous_player_positions = previous_player_positions
        self._next_player_positions = next_player_positions
        self._player = player

        # If sumito move, then the opponent positions will be provided
        if previous_opponent_positions is None:
            self._previous_opponent_positions = []
        else:
            self._previous_opponent_positions = previous_opponent_positions

        if next_opponent_positions is None:
            self._next_opponent_positions = []
        else:
            self._next_opponent_positions = next_opponent_positions

    def __str__(self):
        return self.__to_move_notation()

    def __lt__(self, other):
        return len(self.previous_player_positions) > len(other.previous_player_positions)

    @property
    def previous_player_positions(self):
        return self._previous_player_positions

    @property
    def next_player_positions(self):
        return self._next_player_positions

    @property
    def previous_opponent_positions(self):
        return self._previous_opponent_positions

    @property
    def next_opponent_positions(self):
        return self._next_opponent_positions

    @property
    def player(self):
        return self._player

    def to_json(self):
        return {
            'previous_player_positions': [{'x': position.x, 'y': position.y} for position in
                                          self._previous_player_positions],
            'next_player_positions': [{'x': position.x, 'y': position.y} for position in self._next_player_positions],
            'previous_opponent_positions': [{'x': position.x, 'y': position.y} for position in
                                            self._previous_opponent_positions],
            'next_opponent_positions': [{'x': position.x, 'y': position.y} for position in
                                        self._next_opponent_positions],
            'player': self._player.value
        }

    @classmethod
    def from_json(cls, json):
        previous_positions = [Position(position['x'], position['y']) for position in json['previous_player_positions']]
        next_positions = [Position(position['x'], position['y']) for position in json['next_player_positions']]
        if json['previous_opponent_positions']:
            previous_opponent_positions = [Position(position['x'], position['y']) for position in
                                           json['previous_opponent_positions']]
        else:
            previous_opponent_positions = None

        if json['next_opponent_positions']:
            next_opponent_positions = [Position(position['x'], position['y']) for position in
                                       json['next_opponent_positions']]
        else:
            next_opponent_positions = None

        player = Piece(json['player'])
        return cls(previous_positions, next_positions, player, previous_opponent_positions, next_opponent_positions)

    def __to_move_notation(self):
        previous_player_positions = self.__positions_to_notation(self._previous_player_positions)
        previous_opponent_positions = f",{self.__positions_to_notation(self._previous_opponent_positions)}" \
            if len(self._previous_opponent_positions) > 0 \
            else ""

        next_player_positions = self.__positions_to_notation(self._next_player_positions)
        next_opponent_positions = f",{self.__positions_to_notation(self._next_opponent_positions)}" \
            if len(self._next_opponent_positions) > 0 \
            else ""

        previous_positions = f"{previous_player_positions}{previous_opponent_positions}"
        next_positions = f"{next_player_positions}{next_opponent_positions}"

        return f"{previous_positions} -> {next_positions}"

    @staticmethod
    def __positions_to_notation(positions: list[Position]):
        return "(" + ",".join([position.to_notation() for position in positions]) + ")"
