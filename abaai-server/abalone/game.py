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
            "ai_move": self._ai_move.to_json() if self._ai_move is not None else None,
            "moves_stack": self._moves_stack.to_json(),
            "board": self._board.to_json() if self._board is not None else None,
            "turn": self._turn.value if self._turn is not None else None
        }


class Game:
    ai_increment = -1

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

        try:
            ai_move_obj = self.make_ai_move()
        except Exception as e:
            print(e)
            ai_move_obj = None

        return GameUpdate(ai_move_obj, self._moves_stack, board=self._board)

    def undo_move(self) -> GameUpdate:
        move = self._moves_stack.pop()
        self._board.undo_move(move)

        return GameUpdate(None, self._moves_stack, self._board)

    def make_ai_move(self) -> Move:
        hard_coded_move = Game.get_default_ai_move()
        ai_move_obj = Move.from_json(hard_coded_move)

        self._moves_stack.push(ai_move_obj)
        self._board.make_move(ai_move_obj)

        return ai_move_obj
    
    def reset_game(self):
        """
        Resets the game and timer to the default state.
        Clears everything.
        """
        #clear the stack
        self._moves_stack.clear_stack()

        #rest the board to be the default board
        #TODO: reset to the position the plauyer has selected
        self._board = Board(BoardLayout.DEFAULT)

        #set the turn to be black
        self._turn = 1

        return GameUpdate(None, self._moves_stack, board=self._board)


    @classmethod
    def get_default_ai_move(cls):
        cls.ai_increment += 1
        return {"previous_positions": [{"x": 5, "y": 2+cls.ai_increment},
                                       {"x": 5, "y": 1+cls.ai_increment},
                                       {"x": 5, "y": 0+cls.ai_increment}],
                "next_positions": [{"x": 5, "y": 3+cls.ai_increment},
                                   {"x": 5, "y": 2+cls.ai_increment},
                                   {"x": 5, "y": 1+cls.ai_increment}],
                "player": 2}
