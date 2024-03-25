// Represents a specific abalone move
class Move {
    constructor(previousPositions, newPositions, player) {
        this.previous_player_positions = previousPositions;
        this.next_player_positions = newPositions;
        this.player = player
    }
}

export default Move;