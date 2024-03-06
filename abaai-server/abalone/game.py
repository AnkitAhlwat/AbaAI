from board import BoardLayout, Board
from stack import Stack


class Game:
    def __init__(self, board: Board):
        if board is None:
            self.board = Board(BoardLayout.DEFAULT)
        else:
            self.board = board

        self.moves_stack = Stack()
        self.turn = None
