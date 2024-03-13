// Represents a specific abalone move
class Move {
    constructor(previousPositions, newPositions, player) {
        this.previous_positions = previousPositions;
        this.next_positions = newPositions;
        this.player = player
    }
}

export default Move;