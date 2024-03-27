import Space from "./Space";

// Represents a specific abalone move
class Move {
    constructor(previousPositions, newPositions, player, previousOpponentPositions, nextOpponentPositions) {
        this.previous_player_positions = previousPositions;
        this.next_player_positions = newPositions;
        this.player = player
        this.previous_opponent_positions = previousOpponentPositions;
        this.next_opponent_positions = nextOpponentPositions;
    }

    static toNotation(move) {
        const { previous_player_positions, previous_opponent_positions, next_player_positions, next_opponent_positions } = move;

        const positionsToNotation = positions => positions.map(position => Space.getCodeByPosition(position)).join(',');

        const previousPlayer = `(${positionsToNotation(previous_player_positions)})`;
        const previousOpponent = previous_opponent_positions.length > 0 ? `,(${positionsToNotation(previous_opponent_positions)})` : '';
        const nextPlayer = `(${positionsToNotation(next_player_positions)})`;
        const nextOpponent = next_opponent_positions.length > 0 ? `,(${positionsToNotation(next_opponent_positions)})` : '';

        const previousPositions = `${previousPlayer}${previousOpponent}`;
        const nextPositions = `${nextPlayer}${nextOpponent}`;

        return `${previousPositions} -> ${nextPositions}`;
    }
}

export default Move;