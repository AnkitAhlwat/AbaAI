from enum import Enum


class Piece(Enum):
    BLACK = 1
    WHITE = 2


class Move:
    def __init__(
            self,
            previous_player_positions: list,
            next_player_positions: list,
            player: Piece,
            previous_opponent_positions: list = None,
            next_opponent_positions: list = None,
    ):
        self._previous_player_positions = previous_player_positions
        self._next_player_positions = next_player_positions
        self._player = player

        self._previous_opponent_positions = previous_opponent_positions if previous_opponent_positions is not None else []
        self._next_opponent_positions = next_opponent_positions if next_opponent_positions is not None else []

    def __str__(self):
        return f'Player:{self.previous_player_positions} -> {self.next_player_positions}\n' \
               f'Opponent:{self.previous_opponent_positions} -> {self.next_opponent_positions}'

    def __lt__(self, other):
        if len(self.next_opponent_positions) != len(other.next_opponent_positions):
            return len(self.next_opponent_positions) > len(other.next_opponent_positions)
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
            'previous_player_positions': [{'x': position[0], 'y': position[1]} for position in
                                          self._previous_player_positions],
            'next_player_positions': [{'x': position[0], 'y': position[1]} for position in self._next_player_positions],
            'previous_opponent_positions': [{'x': position[0], 'y': position[1]} for position in
                                            self._previous_opponent_positions],
            'next_opponent_positions': [{'x': position[0], 'y': position[1]} for position in
                                        self._next_opponent_positions],
            'player': self._player.value
        }

    @staticmethod
    def from_json(json_data):
        previous_player_positions = [(position['x'], position['y']) for position in
                                     json_data['previous_player_positions']]
        next_player_positions = [(position['x'], position['y']) for position in
                                 json_data['next_player_positions']]
        previous_opponent_positions = [(position['x'], position['y']) for position in
                                       json_data['previous_opponent_positions']]
        next_opponent_positions = [(position['x'], position['y']) for position in
                                   json_data['next_opponent_positions']]
        player = Piece(json_data['player'])
        return Move(
            previous_player_positions,
            next_player_positions,
            player,
            previous_opponent_positions,
            next_opponent_positions
        )