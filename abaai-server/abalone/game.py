from random import choice

from random import shuffle

from abalone.ai.game_playing_agent_lucas import MiniMaxAgent
from abalone.ai.state_space_generator import StateSpaceGenerator
from abalone.board import BoardLayout, Board
from abalone.movement import Move, Piece
from abalone.stack import Stack
from abalone.state import GameState, GameStateUpdate


class GameOptions:
    board_layout_map = {
        "Default": BoardLayout.DEFAULT,
        "Belgian Daisy": BoardLayout.BELGIAN_DAISY,
        "German Daisy": BoardLayout.GERMAN_DAISY
    }

    def __init__(
            self,
            board_layout: BoardLayout = None,
            black_ai: bool = False,
            white_ai: bool = True,
            black_time_limit_seconds: int = 20,
            white_time_limit_seconds: int = 20,
            move_limit: int = 20
    ):
        if board_layout is None:
            board_layout = BoardLayout.DEFAULT
        self._board_layout = board_layout
        self._is_black_ai = black_ai
        self._is_white_ai = white_ai
        self._black_time_limit_seconds = black_time_limit_seconds
        self._white_time_limit_seconds = white_time_limit_seconds
        self._move_limit = move_limit

    @property
    def board_layout(self) -> BoardLayout:
        return self._board_layout

    @property
    def is_black_ai(self) -> bool:
        return self._is_black_ai

    @property
    def is_white_ai(self) -> bool:
        return self._is_white_ai

    @property
    def black_time_limit_seconds(self) -> int:
        return self._black_time_limit_seconds

    @property
    def white_time_limit_seconds(self) -> int:
        return self._white_time_limit_seconds

    @property
    def move_limit(self) -> int:
        return self._move_limit

    @classmethod
    def from_json(cls, json_obj: dict) -> 'GameOptions':
        return cls(
            GameOptions.board_layout_map[json_obj['boardLayout']],
            json_obj['blackPlayer'] == "Computer",
            json_obj['whitePlayer'] == "Computer",
            json_obj['blackTimeLimit'],
            json_obj['whiteTimeLimit'],
            json_obj['moveLimit']
        )

    def to_json(self) -> dict:
        board_layout_name = None
        for key, value in GameOptions.board_layout_map.items():
            if value == self._board_layout:
                board_layout_name = key
                break

        return {
            "boardLayout": board_layout_name,
            "blackPlayer": "Computer" if self._is_black_ai else "Human",
            "whitePlayer": "Computer" if self._is_white_ai else "Human",
            "blackTimeLimit": self._black_time_limit_seconds,
            "whiteTimeLimit": self._white_time_limit_seconds,
            "moveLimit": self._move_limit
        }


class Game:
    def __init__(self):
        self._game_options = GameOptions()
        self._moves_stack = Stack()
        self._current_game_state = GameState(Board(self._game_options.board_layout.value))
        self._game_started = False
        self._game_configured = False

    def set_up(self, config) -> dict:
        self._game_options = GameOptions.from_json(config)
        self._current_game_state = GameState(Board(self._game_options.board_layout.value), Piece.BLACK)

        self._game_configured = True

        return self.__to_json()

        max_ai_depth = 1
        self._ai_agent = MiniMaxAgent(max_ai_depth)

    def set_up(self, config):
        if config['boardLayout'] == "Default":
            self._game_options.board_layout = BoardLayout.DEFAULT
        elif config['boardLayout'] == "Belgian Daisy":
            self._game_options.board_layout = BoardLayout.BELGIAN_DAISY
        else:
            self._game_options.board_layout = BoardLayout.GERMAN_DAISY
    def start_game(self) -> dict:
        self._game_started = True
        return self.__to_json()

    def get_game_status(self) -> dict:
        return self.__to_json()

    def make_move(self, move) -> dict:
        # convert the move to a Move object
        try:
            move_obj = Move.from_json(move)
        except Exception as e:
            print(e)
            return {"error": str(e)}

        # make the move and push it to the stack
        self.__apply_move(move_obj)

        return self.__to_json()

    def undo_move(self) -> dict:
        move = self._moves_stack.pop()
        self._current_game_state.undo_move(move)

        return self.__to_json()

    def get_ai_move(self) -> dict:
        # return a random move for now
        list_of_moves = StateSpaceGenerator.generate_all_possible_moves(self._current_game_state)
        move = choice(list_of_moves)
        return move.to_json()
    def make_ai_move(self) -> Move:
        # if it is the first move, choose a random move to make from the generated moves
        if self._moves_stack.is_empty():
            moves = StateSpaceGenerator.generate_all_possible_moves(self._current_game_state)
            shuffle(moves)
            return moves[0]

        # if it is not the first move, choose the best move to make from the generated moves
        ai_move = self._ai_agent.get_best_move(self._current_game_state)

        return ai_move

    def reset_game(self) -> dict:
        """
        Resets the game and timer to the default state.
        Clears everything.
        """
        # clear the stack
        self._moves_stack.clear_stack()

        # set started to false
        self._game_started = False

        # reset the board to be the selected board
        board = Board(self._game_options.board_layout.value)
        self._current_game_state = GameState(board)

        return self.__to_json()

    def get_possible_moves(self) -> dict:
        list_of_moves = StateSpaceGenerator.generate_all_possible_moves(self._current_game_state)
        return Game.__format_possible_moves(list_of_moves)

    def __to_json(self) -> dict:
        return {
            "game_options": self._game_options.to_json() if self._game_options is not None else None,
            "game_started": self._game_started,
            "game_configured": self._game_configured,
            "game_state": self._current_game_state.to_json(),
            "moves_stack": self._moves_stack.to_json()
        }

    @staticmethod
    def __format_possible_moves(moves: list[Move]) -> dict[str, list[dict]]:
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
