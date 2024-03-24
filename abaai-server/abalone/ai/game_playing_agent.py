from abalone.ai.state_space_generator import StateSpaceGenerator
from abalone.state import GameStateUpdate


class MiniMaxAgent:
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def minimax(self, game_state, depth, max_turn, alpha, beta):
        if depth == 0 or game_state.is_game_over():
            return self.evaluate(game_state)

        if max_turn:
            max_eval = float('-inf')
            for move in StateSpaceGenerator.generate_all_possible_moves(game_state):
                next_state = GameStateUpdate(game_state, move).resulting_state
                max_eval = max(max_eval, self.minimax(next_state, depth - 1, False, alpha, beta))
                if max_eval > beta:
                    return max_eval
                alpha = max(alpha, max_eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in StateSpaceGenerator.generate_all_possible_moves(game_state):
                next_state = GameStateUpdate(game_state, move).resulting_state
                min_eval = min(min_eval, self.minimax(next_state, depth - 1, True, alpha, beta))
                if min_eval < alpha:
                    return min_eval
                beta = min(beta, min_eval)
            return min_eval

    def get_best_move(self, game_state):
        best_move = None
        max_eval = float('-inf')
        for move in StateSpaceGenerator.generate_all_possible_moves(game_state):
            successor_state = GameStateUpdate(game_state, move).resulting_state
            eval = self.minimax(successor_state, self.max_depth, False, float('-inf'), float('inf'))
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move

    def evaluate(self, game_state):
        # Write our own evaluation function
        pass
