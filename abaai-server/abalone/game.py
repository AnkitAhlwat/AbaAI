from abalone.board import BoardLayout, Board
from abalone.movement import Move, Turn
from abalone.stack import Stack


class GameUpdate:
    def __init__(self, ai_move: Move = None, moves_stack: Stack = None, board: Board = None, turn: Turn = None):
        self._ai_move = ai_move
        self._moves_stack = moves_stack
        self._board = board
        self._turn = turn

    def to_json(self):
        return {
            "ai_move": self._ai_move,
            "moves_stack": self._moves_stack.to_json(),
            "board": self._board.to_json() if self._board is not None else None,
            "turn": self._turn.value if self._turn is not None else None
        }


class Game:
    def __init__(self, board: Board = None):
        if board is None:
            self._board = Board(BoardLayout.DEFAULT)
        else:
            self._board = board

        self._moves_stack = Stack()
        self._turn = None

    def set_up(self, config):
        pass

    def make_move(self, move) -> GameUpdate:
        # convert the move to a Move object
        try:
            move_obj = Move.from_json(move)
        except Exception as e:
            print(e)
            return GameUpdate(None, self._moves_stack)

        self._moves_stack.push(move_obj)
        self._board.make_move(move_obj)

        return GameUpdate(None, self._moves_stack)

    def undo_move(self) -> GameUpdate:
        move = self._moves_stack.pop()
        self._board.undo_move(move)

        return GameUpdate(None, self._moves_stack, self._board)
