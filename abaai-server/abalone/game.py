import time

from abalone.ai.game_playing_agent_revamped_iterative_deepening import AlphaBetaPruningAgentIterative
from abalone.ai.state_space_generator import StateSpaceGenerator
from abalone.board import OptimizedBoard, BoardLayout
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
            black_time_limit_seconds: int = 180,
            black_turn_time: int = 15,
            white_time_limit_seconds: int = 180,
            white_turn_time: int = 15,
            move_limit: int = 20
    ):
        if board_layout is None:
            board_layout = BoardLayout.DEFAULT
        self._board_layout = board_layout
        self._is_black_ai = black_ai
        self._is_white_ai = white_ai
        self._black_time_limit_seconds = black_time_limit_seconds
        self._black_turn_time = black_turn_time
        self._white_time_limit_seconds = white_time_limit_seconds
        self._white_turn_time = white_turn_time
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
    def black_turn_time(self) -> int:
        return self._black_turn_time

    @property
    def white_time_limit_seconds(self) -> int:
        return self._white_time_limit_seconds

    @property
    def white_turn_time(self) -> int:
        return self._white_turn_time

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
            json_obj['blackTurnTime'],
            json_obj['whiteTimeLimit'],
            json_obj['whiteTurnTime'],
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
            "blackTurnTime": self._black_turn_time,
            "whiteTimeLimit": self._white_time_limit_seconds,
            "whiteTurnTime": self._white_turn_time,
            "moveLimit": self._move_limit
        }


class Game:
    def __init__(self):
        self._game_options = GameOptions()
        self._moves_stack = Stack()
        self._current_game_state = GameState(OptimizedBoard(self._game_options.board_layout.value))
        self._moves_remaining = [0, 0]
        self._game_started = False
        self._game_configured = False
        self._is_first_move = True

        self._agent = None

    def set_up(self, config) -> dict:
        self._game_options = GameOptions.from_json(config)
        self._current_game_state = GameState(OptimizedBoard(self._game_options.board_layout.value), Piece.BLACK)
        move_limit = self._game_options.move_limit
        self._moves_remaining = [move_limit, move_limit]
        self._game_configured = True

        return self.__to_json()

    def start_game(self) -> dict:
        self._game_started = True
        return self.__to_json()

    def get_game_status(self) -> dict:
        return self.__to_json()

    def make_move(self, move) -> dict:
        if self._is_first_move:
            self._is_first_move = False

        # convert the move to a Move object
        try:
            move_obj = Move.from_json(move)
        except Exception as e:
            print(e)
            return {"error": str(e)}

        # make the move and push it to the stack
        self._moves_stack.push(move_obj)
        self._moves_remaining[0 if self._current_game_state.turn == Piece.BLACK else 1] -= 1
        self._current_game_state = GameStateUpdate(self._current_game_state, move_obj).resulting_state

        return self.__to_json()

    def undo_move(self) -> dict:
        move = self._moves_stack.pop()
        self._moves_remaining[1 if self._current_game_state.turn == Piece.BLACK else 0] += 1
        self._current_game_state.undo_move(move)

        return self.__to_json()

    def get_ai_move(self) -> dict:
        # if self._game_options.is_black_ai and self._is_first_move:
        #     self._is_first_move = False
        #     # random move for first move
        #     all_moves = StateSpaceGenerator.generate_all_possible_moves(self._current_game_state)
        #
        #     return {
        #         "move": choice(all_moves).to_json(),
        #         "time_taken": 0.00
        #     }
        # else:
        start_time = time.time()
        print("start time:", start_time)

        # manually set the depth limit
        depth_limit = 4

        # set the time limit for the AI based on config
        if self._current_game_state.turn == Piece.BLACK:
            time_limit = self._game_options.black_turn_time
        else:
            time_limit = self._game_options.white_turn_time

        # if self._current_game_state.turn == Piece.BLACK:
        if self._agent is None:
            self._agent = AlphaBetaPruningAgentIterative(
                max_depth=depth_limit,
                max_time_sec=time_limit
            )
        move = self._agent.iterative_deepening_search(self._current_game_state)
        # else:
        # agent = alphaBetaPruningAgent(
        #     max_depth=depth_limit,
        #     max_time_sec=time_limit,
        #     game_state=self._current_game_state
        # )
        # move = agent.AlphaBetaPruningSearch()

        end_time = time.time()
        print("end time:", end_time)

        time_taken = end_time - start_time
        print("time taken:", time_taken, "seconds")

        return {
            "move": move.to_json(),
            "time_taken": float(f"{time_taken:.2f}")  # round to 2 decimal places
        }

    def reset_game(self) -> dict:
        """
        Resets the game and timer to the default state.
        Clears everything.
        """
        # clear the stack
        self._moves_stack.clear_stack()

        # set started to false
        self._game_started = False

        # set first move to true
        self._is_first_move = True

        # set moves remaining to normal
        move_limit = self._game_options.move_limit
        self._moves_remaining = [move_limit, move_limit]

        # reset the board to be the selected board
        board = OptimizedBoard(self._game_options.board_layout.value)
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
            "moves_stack": self._moves_stack.to_json(),
            "moves_remaining": self._moves_remaining,
            "is_first_move": self._is_first_move
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
