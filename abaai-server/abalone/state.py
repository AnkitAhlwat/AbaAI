from abalone.board import Board
from abalone.movement import Move, Piece
from copy import deepcopy


class GameState:
    def __init__(self, board: Board, turn: Piece):
        self._board = board
        self._turn = turn

    @property
    def board(self):
        return self._board

    @property
    def turn(self):
        return self._turn


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

        return GameState(resulting_board, resulting_turn)

    @classmethod
    def convert_moves_to_game_state_updates(cls, game_state: GameState, moves: list[Move]) -> list['GameStateUpdate']:
        return [cls(game_state, move) for move in moves]
