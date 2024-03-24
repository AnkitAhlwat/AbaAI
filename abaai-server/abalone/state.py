from abalone.board import Board
from abalone.movement import Move, Piece
from copy import deepcopy


class GameState:
    def __init__(
            self,
            board: Board,
            turn: Piece,
            remaining_player_marbles: int = 14,
            remaining_opponent_marbles: int = 14
    ):
        self._board = board
        self._turn = turn
        self._remaining_player_marbles = remaining_player_marbles
        self._remaining_opponent_marbles = remaining_opponent_marbles

    def is_game_over(self):
        return True if self._remaining_player_marbles <= 8 or self._remaining_opponent_marbles <= 8 else False

    @property
    def board(self):
        return self._board

    @property
    def turn(self):
        return self._turn

    @property
    def remaining_player_marbles(self) -> int:
        return self._remaining_player_marbles

    @property
    def remaining_opponent_marbles(self) -> int:
        return self._remaining_opponent_marbles


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
        if len(self._move.previous_opponent_positions) > len(self._move.next_opponent_positions):
            new_remaining_opponent_marbles = self._previous_state.remaining_opponent_marbles - 1
        else:
            new_remaining_opponent_marbles = self._previous_state.remaining_opponent_marbles

        return GameState(
            resulting_board,
            resulting_turn,
            self._previous_state.remaining_player_marbles,
            new_remaining_opponent_marbles
        )

    @classmethod
    def convert_moves_to_game_state_updates(cls, game_state: GameState, moves: list[Move]) -> list['GameStateUpdate']:
        return [cls(game_state, move) for move in moves]
