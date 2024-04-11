import time
from random import choice

from abalone.ai.cython.cython_clumping_agent import AlphaBetaPruningAgentAnkit
from abalone.ai.ankit_agent import AlphaBetaPruningAgentAnkit as AlphaBetaPruningAgentAnkit2
from abalone.ai.state_space_optimized import StateSpaceGenerator
from abalone.board import OptimizedBoard, BoardLayout
from abalone.state import GameState, GameStateUpdate
from abalone.ai.game_playing_agent_revamped_iterative_deepening import AlphaBetaPruningAgentIterative
from abalone.ai.game_playing_agent_revamped_iterative_deeping_no_clumping import AlphaBetaPruningAgentIterativeNoClumping
def simulate_agents(game_state: GameState, max_moves: int):
    game_state = game_state
    # agent1 = AlphaBetaPruningAgentIterative(max_depth=4)
    agent1 = AlphaBetaPruningAgentAnkit(max_depth=4)
    # agent2 = AlphaBetaPruningAgentIterativeNoClumping(max_depth=4)
    agent2 = AlphaBetaPruningAgentAnkit2(max_depth=4)
    for i in range(max_moves):
        if game_state.turn.value == 2:
            start = time.time()
            original_marbles = game_state.remaining_opponent_marbles
            original_opponent_marbles = game_state.remaining_player_marbles
            best_move = agent1.iterative_deepening_search(game_state)
            game_state = GameStateUpdate(game_state, best_move).resulting_state
            print(f'black move {best_move}')
            print(f'time taken: {time.time() - start}')
            if game_state.remaining_player_marbles < original_marbles:
                print(f'marbles knocked off')
            if game_state.remaining_opponent_marbles < original_opponent_marbles:
                print(f'marbles knocked off')
        else:
            start = time.time()
            original_marbles = game_state.remaining_opponent_marbles
            original_opponent_marbles = game_state.remaining_player_marbles
            move = agent2.iterative_deepening_search(game_state)
            game_state = GameStateUpdate(game_state, move).resulting_state
            print(f'white move {move}')
            print(f'time taken: {time.time() - start}')
            if game_state.remaining_player_marbles < original_marbles:
                print(f'marbles knocked off')
            if game_state.remaining_opponent_marbles < original_opponent_marbles:
                print(f'marbles knocked off')

    print(game_state.turn)
    print(game_state.remaining_player_marbles)
    print(game_state.remaining_opponent_marbles)
    agent1.write_t_table()
    # agent2.write_t_table()

def train_agent():
    game_state = GameState(OptimizedBoard(BoardLayout.GERMAN_DAISY.value))
    agent1 = AlphaBetaPruningAgentAnkit(max_depth=4)
    all_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
    for i in range(len(sorted(all_moves))):
        game_state = GameState(OptimizedBoard(BoardLayout.GERMAN_DAISY.value))
        agent1 = AlphaBetaPruningAgentAnkit(max_depth=4)
        move = all_moves[i]
        game_state = GameStateUpdate(game_state, move).resulting_state
        for i in range(6):
            best_move = agent1.iterative_deepening_search(game_state)
            print(f'{game_state.turn.value} {best_move}')
            game_state = GameStateUpdate(game_state, best_move).resulting_state
        print(game_state.turn)
        print(game_state.remaining_player_marbles)
        print(game_state.remaining_opponent_marbles)
        agent1.write_t_table()



if __name__ == '__main__':
    start = time.time()
    # simulate_agents(GameState(OptimizedBoard([[-1, -1, -1, -1, 0, 0, 0, 2, 2], [-1, -1, -1, 2, 0, 0, 0, 2, 2], [-1, -1, 0, 0, 2, 0, 2, 2, 0], [-1, 0, 0, 2, 1, 2, 2, 0, 0], [0, 0, 0, 1, 1, 2, 2, 0, 0], [0, 0, 1, 1, 1, 2, 0, 0, -1], [0, 1, 1, 1, 1, 1, 0, -1, -1], [0, 1, 0, 0, 0, 1, -1, -1, -1], [0, 1, 0, 0, 0, -1, -1, -1, -1]])), 2)
    # simulate_agents(GameState(OptimizedBoard(BoardLayout.BELGIAN_DAISY.value)),50)
    # print(f'total time taken: {time.time() - start}')
    train_agent()