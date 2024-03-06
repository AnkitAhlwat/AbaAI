from abalone.board import BoardLayout, Board
from abalone.movement import Move
from abalone.stack import Stack


class GameUpdate:
    def __init__(self, ai_move: Move = None, moves_stack: Stack = None):
        self._ai_move = ai_move
        self._moves_stack = moves_stack

    def to_json(self):
        return {
            "ai_move": self._ai_move,
            "moves_stack": self._moves_stack.to_json()
        }


class Game:
    def __init__(self, board: Board = None):
        if board is None:
            self.board = Board(BoardLayout.DEFAULT)
        else:
            self.board = board

        self.moves_stack = Stack()
        self.turn = None

    def make_move(self, move) -> GameUpdate:
        # convert the move to a Move object
        try:
            move_obj = Move.from_json(move)
        except Exception as e:
            print(e)
            return GameUpdate(None, self.moves_stack)

        self.moves_stack.push(move_obj)
        self.board.make_move(move_obj)

        return GameUpdate(None, self.moves_stack)
