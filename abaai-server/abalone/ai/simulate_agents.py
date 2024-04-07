from abalone.state import GameState, GameStateUpdate
from abalone.ai.game_playing_agent_revamped_iterative_deepening import AlphaBetaPruningAgentIterative
from abalone.ai.game_playing_agent_revamped_iterative_deeping_no_clumping import AlphaBetaPruningAgentIterativeNoClumping
def simulate_agents(game_state: GameState, max_moves: int):
    game_state = game_state
    agent1 = AlphaBetaPruningAgentIterative(max_depth=4)
    agent2 = AlphaBetaPruningAgentIterativeNoClumping(max_depth=4)

    for i in range(max_moves):
        if game_state.turn.value == 1:
            original_marbles = game_state.remaining_opponent_marbles
            original_opponent_marbles = game_state.remaining_player_marbles
            best_move = agent1.iterative_deepening_search(game_state)
            game_state = GameStateUpdate(game_state, best_move).resulting_state
            print(f'black move {best_move}')
            if game_state.remaining_player_marbles < original_marbles:
                print(f'marbles knocked off')
            if game_state.remaining_opponent_marbles < original_opponent_marbles:
                print(f'marbles knocked off')
        else:
            original_marbles = game_state.remaining_opponent_marbles
            original_opponent_marbles = game_state.remaining_player_marbles
            move = agent2.iterative_deepening_search(game_state)
            game_state = GameStateUpdate(game_state, move).resulting_state
            print(f'white move {move}')
            if game_state.remaining_player_marbles < original_marbles:
                print(f'marbles knocked off')
            if game_state.remaining_opponent_marbles < original_opponent_marbles:
                print(f'marbles knocked off')

    print(game_state.turn)
    print(game_state.remaining_player_marbles)
    print(game_state.remaining_opponent_marbles)
    agent1.write_t_table()
    agent2.write_t_table()

if __name__ == '__main__':
    simulate_agents(GameState(), 82)