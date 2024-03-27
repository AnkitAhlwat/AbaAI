from copy import deepcopy

from abalone.board import Board
from abalone.movement import Move, Piece, Position


class GameState:
    def __init__(
            self,
            board: Board = None,
            turn: Piece = Piece.BLACK,
    ):
        if board is None:
            board = Board()
        self._board = board
        self._turn = turn

    @property
    def board(self):
        return self._board

    @property
    def turn(self):
        return self._turn

    @property
    def player_marble_positions(self) -> list[Position]:
        return self._get_marble_positions(self._turn)

    @property
    def opponent_marble_positions(self) -> list[Position]:
        return self._get_marble_positions(Piece.WHITE if self._turn == Piece.BLACK else Piece.BLACK)

    @property
    def remaining_player_marbles(self) -> int:
        return len(self.player_marble_positions)

    @property
    def remaining_opponent_marbles(self) -> int:
        return len(self.opponent_marble_positions)

    def is_game_over(self):
        return True if self.remaining_player_marbles <= 8 or self.remaining_opponent_marbles <= 8 else False

    def undo_move(self, move: Move):
        self._board = Board(self._board.undo_move(move))
        self._turn = Piece.WHITE if self._turn == Piece.BLACK else Piece.BLACK

    def _get_marble_positions(self, piece: Piece):
        positions = []

        for y in range(9):
            for x in range(9):
                if self._board.array[y][x] == piece.value:
                    positions.append(Position(x, y))

        return positions

    def to_json(self):
        total_starting_marbles = 14
        remaining_black_marbles = sum([1 for row in self._board.array for cell in row if cell == Piece.BLACK.value])
        remaining_white_marbles = sum([1 for row in self._board.array for cell in row if cell == Piece.WHITE.value])

        return {
            'board': self._board.to_json(),
            'turn': self._turn.value,
            'captured_black_marbles': total_starting_marbles - remaining_black_marbles,
            'captured_white_marbles': total_starting_marbles - remaining_white_marbles,
            'player_marble_positions': [position.to_json() for position in self.player_marble_positions],
            'opponent_marble_positions': [position.to_json() for position in self.opponent_marble_positions]
        }


class GameStateUpdate:
    def __init__(self, previous_state: GameState, move: Move):
        self._previous_state = deepcopy(previous_state)
        self._move = move
        self._resulting_state = self.__generate_resulting_state()

    @property
    def previous_state(self) -> GameState:
        return self._previous_state

    @property
    def move(self) -> Move:
        return self._move

    @property
    def resulting_state(self) -> GameState:
        return self._resulting_state

    def __generate_resulting_state(self):
        resulting_board = Board(deepcopy(self._previous_state.board.make_move(self._move)))
        resulting_turn = Piece.WHITE if self._previous_state.turn == Piece.BLACK else Piece.BLACK

        # Check if a sumito move pushed a marble off the board
        return GameState(
            resulting_board,
            resulting_turn,
        )

    @classmethod
    def convert_moves_to_game_state_updates(cls, game_state: GameState, moves: list[Move]) -> list['GameStateUpdate']:
        return [cls(game_state, move) for move in moves]
