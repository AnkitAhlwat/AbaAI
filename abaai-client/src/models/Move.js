// Represents a specific abalone move
class Move {
    constructor(previousPositions, newPositions, player, previousOpponentPositions, nextOpponentPositions) {
        this.previous_player_positions = previousPositions;
        this.next_player_positions = newPositions;
        this.player = player
        this.previous_opponent_positions = previousOpponentPositions;
        this.next_opponent_positions = nextOpponentPositions;
    }
}

export default Move;