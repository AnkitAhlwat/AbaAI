from abalone.board_ai import OptimizedBoard
from abalone.movement import Move, Piece


class GameState:
    def __init__(
            self,
            board: OptimizedBoard = None,
            turn: Piece = Piece.BLACK,
            remaining_player_marbles: int = 14,
            remaining_opponent_marbles: int = 14
    ):
        if board is None:
            board = OptimizedBoard()
        self._board = board
        self._turn = turn
        self._remaining_player_marbles = remaining_player_marbles
        self._remaining_opponent_marbles = remaining_opponent_marbles

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

    def is_game_over(self):
        return True if self._remaining_player_marbles <= 8 or self._remaining_opponent_marbles <= 8 else False

    def undo_move(self, move: Move):
        self._board = OptimizedBoard(self._board.undo_move(move))
        self._turn = Piece.WHITE if self._turn == Piece.BLACK else Piece.BLACK

        # Check if a sumito move pushed a marble off the board
        if len(move.previous_opponent_positions) > len(move.next_opponent_positions):
            self._remaining_opponent_marbles += 1

    def to_json(self):
        total_starting_marbles = 14
        remaining_black_marbles = self._board.array.count(Piece.BLACK.value)
        remaining_white_marbles = self._board.array.count(Piece.WHITE.value)

        return {
            'board': self._board.to_json(),
            'turn': self._turn.value,
            'captured_black_marbles': total_starting_marbles - remaining_black_marbles,
            'captured_white_marbles': total_starting_marbles - remaining_white_marbles,
        }


class GameStateUpdate:
    def __init__(self, previous_state: GameState, move: Move):
        self._previous_state = previous_state

        self._previous_state = previous_state
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
        resulting_turn = Piece.WHITE if self._previous_state.turn.value == 1 else Piece.BLACK
        new_board = self._previous_state.board.array[:]
        resulting_board = OptimizedBoard(new_board)
        resulting_board.make_move(self._move)
        player_marbles = resulting_board.array.count(self._move.player.value)
        opponent_marbles = resulting_board.array.count(3 - self._move.player.value)

        return GameState(
            resulting_board,
            resulting_turn,
            player_marbles,
            opponent_marbles
        )


    @classmethod
    def convert_moves_to_game_state_updates(cls, game_state: GameState, moves: list[Move]) -> list['GameStateUpdate']:
        return [cls(game_state, move) for move in moves]
