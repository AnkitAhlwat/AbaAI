# def generate_hex_lookup_table():
#     lookup_table = []
#     for row in range(9):
#         for column in range(9):
#             # Calculate row offset for hexagonal layout
#             row_offset = max(0, 4 - abs(4 - row))
#             # Adjust for hexagonal grid coordinates
#             q = column - row_offset
#             r = row - 4
#             # Append the calculated hex coordinates to the lookup table
#             # Only include valid positions (not out of bounds)
#             if not (row < 4 and column < 4 - row) and not (row > 4 and column > 13 - row):
#                 lookup_table.append((q, r))
#             else:
#                 lookup_table.append(None)  # Mark out-of-bounds positions as None
#     return lookup_table

# def flat_index_to_hex(index):
#     row = index // 9
#     column = index % 9
#
#     row_offset = max(0, 4 - abs(4 - row))
#     q = column - row_offset
#     r = row - 4
#
#     return q, r


# def hex_distance(hex_a, hex_b):
#     x1, y1, z1 = qr_to_cube(hex_a)
#     x2, y2, z2 = qr_to_cube(hex_b)
#     return (abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)) // 2


# def qr_to_cube(hex):
#     q, r = hex
#     x = q
#     z = r
#     y = -x - z
#     return x, y, z

# def cube_distance(a, b):
#     return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
#

# def simulate_moves(game_state: GameState, max_moves: int):
#     agent = AlphaBetaPruningAgent(max_depth=3)
#     print("Initial Board")
#     print(game_state.board)
#     game_state = game_state
#     i = 0
#     start_time = time.time()
#     while i < max_moves:
#         best_move = agent.AlphaBetaPruningSearch(game_state)
#         print(f"{game_state.turn.name}->({best_move})")
#         original_marbles = game_state.remaining_opponent_marbles
#         original_opponent_marbles = game_state.remaining_player_marbles
#         game_state = GameStateUpdate(game_state, best_move).resulting_state
#         if game_state.remaining_player_marbles < original_marbles:
#             print(f'marbles knocked off')
#         if game_state.remaining_opponent_marbles < original_opponent_marbles:
#             print(f'marbles knocked off')
#
#         i += 1
#     finish_time = time.time()
#     print(finish_time - start_time)
#     print(game_state.board)
#     print(game_state.turn)
#     print(game_state.remaining_opponent_marbles)
#     print(game_state.remaining_player_marbles)

#
# gemeran_daisy = GameState(board=OptimizedBoard(BoardLayout.GERMAN_DAISY.value),turn=Piece.BLACK)
# # print(generate_hex_lookup_table())
# # simulate_moves(gemeran_daisy, 55)
# agent = AlphaBetaPruningAgent(max_depth=4)
# current_time = time.time()
# best_move = agent.AlphaBetaPruningSearch(gemeran_daisy)
# finish_time = time.time()
# print(finish_time - current_time)
# print(best_move)
