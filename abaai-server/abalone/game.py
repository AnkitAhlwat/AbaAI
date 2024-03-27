from random import shuffle

from abalone.ai.game_playing_agent_lucas import MiniMaxAgent
from abalone.ai.state_space_generator import StateSpaceGenerator
from abalone.board import BoardLayout, Board
from abalone.movement import Move, Piece
from abalone.stack import Stack
from abalone.state import GameState, GameStateUpdate


class GameUpdate:
    def __init__(self, ai_move: Move = None, moves_stack: Stack = None, game_state: GameState = None):
        self._game_state = game_state
        self._ai_move = ai_move
        self._moves_stack = moves_stack

    def to_json(self):
        return {
            "ai_move": self._ai_move.to_json() if self._ai_move is not None else None,
            "moves_stack": self._moves_stack.to_json() if self._moves_stack is not None else None,
            "game_state": self._game_state.to_json() if self._game_state is not None else None
        }


class GameOptions:
    def __init__(self, board_layout: BoardLayout = None):
        if board_layout is None:
            board_layout = BoardLayout.DEFAULT
        self._board_layout = board_layout

    @property
    def board_layout(self) -> BoardLayout:
        return self._board_layout

    @board_layout.setter
    def board_layout(self, value):
        self._board_layout = value


class Game:
    def __init__(self, game_options: GameOptions = None):
        if game_options is None:
            game_options = GameOptions()
        self._game_options = game_options
        self._moves_stack = Stack()
        self._current_game_state = GameState(Board(game_options.board_layout.value), Piece.BLACK)

        max_ai_depth = 1
        self._ai_agent = MiniMaxAgent(max_ai_depth)

    def set_up(self, config):
        if config['boardLayout'] == "Default":
            self._game_options.board_layout = BoardLayout.DEFAULT
        elif config['boardLayout'] == "Belgian Daisy":
            self._game_options.board_layout = BoardLayout.BELGIAN_DAISY
        else:
            self._game_options.board_layout = BoardLayout.GERMAN_DAISY

    def make_move(self, move) -> GameUpdate:
        # convert the move to a Move object
        try:
            move_obj = Move.from_json(move)
        except Exception as e:
            print(e)
            return GameUpdate(None, self._moves_stack)

        # make the move and push it to the stack
        self.__apply_move(move_obj)

        # let the AI decide on it's next move
        try:
            ai_move_obj = self.make_ai_move()
        except Exception as e:
            print(e)
            ai_move_obj = None

        return GameUpdate(ai_move_obj, self._moves_stack, self._current_game_state)

    def undo_move(self) -> GameUpdate:
        move = self._moves_stack.pop()
        self._current_game_state.undo_move(move)

        return GameUpdate(None, self._moves_stack, self._current_game_state)

    def make_ai_move(self) -> Move:
        # if it is the first move, choose a random move to make from the generated moves
        if self._moves_stack.is_empty():
            moves = StateSpaceGenerator.generate_all_possible_moves(self._current_game_state)
            shuffle(moves)
            return moves[0]

        # if it is not the first move, choose the best move to make from the generated moves
        ai_move = self._ai_agent.get_best_move(self._current_game_state)

        return ai_move

    def reset_game(self):
        """
        Resets the game and timer to the default state.
        Clears everything.
        """
        # clear the stack
        self._moves_stack.clear_stack()

        # reset the board to be the selected board
        board = Board(self._game_options.board_layout.value)
        self._current_game_state = GameState(board)

        return GameUpdate(None, self._moves_stack, self._current_game_state)

    def get_possible_moves(self):
        list_of_moves = StateSpaceGenerator.generate_all_possible_moves(self._current_game_state)
        return Game.format_possible_moves(list_of_moves)

    @staticmethod
    def format_possible_moves(moves: list[Move]) -> dict[str, list[dict]]:
        moves_dict = {}
        for move in moves:
            position_notation_list = sorted([pos.to_notation() for pos in move.previous_player_positions])
            key = str(position_notation_list)

            if key not in moves_dict.keys():
                moves_dict[key] = [move.to_json()]
            else:
                moves_dict[key].append(move.to_json())

        return moves_dict

    def __apply_move(self, move: Move):
        self._current_game_state = GameStateUpdate(self._current_game_state, move).resulting_state
        self._moves_stack.push(move)
