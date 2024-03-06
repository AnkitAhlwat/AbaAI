class Space {
    constructor(state, position) {
        this.state = state;
        this.position = position;
        this.str = Space.getCodeByPosition(position);
        this.selected = false;
    }

    getAdjacentSpaces() {
        const adjacentSpaces = [];
        const { x, y } = this.position;
        const possibleMoves = [
            { x: x - 1, y:  y },
            { x: x + 1, y },
            { x: x, y: y - 1 },
            { x: x, y: y + 1 },
            { x: x + 1, y: y - 1 },
            { x: x - 1, y: y + 1}
        ];
        for (const move of possibleMoves) {
            if (move.x >= 0 && move.x <= 8 && move.y >= 0 && move.y <= 8) {
                adjacentSpaces.push(move);
            }
        }
        return adjacentSpaces;
    }

    isAdjacentTo(space) {
        const adjacentSpaces = this.getAdjacentSpaces();
        for (const adjacentSpace of adjacentSpaces) {
            if (adjacentSpace.x === space.position.x && adjacentSpace.y === space.position.y) {
                return true;
            }
        }
        return false;
    }

    static areInStraightLine(space1, space2, space3) {
        const x1 = space1.position.x;
        const y1 = space1.position.y;
        const x2 = space2.position.x;
        const y2 = space2.position.y;
        const x3 = space3.position.x;
        const y3 = space3.position.y;

        if (x1 === x2 && x2 === x3) {
            return true;
        }
        if (y1 === y2 && y2 === y3) {
            return true;
        }
        if (x1 - x2 === y1 - y2 && x2 - x3 === y2 - y3) {
            return true;
        }
        if (x1 - x2 === y2 - y1 && x2 - x3 === y3 - y2) {
            return true;
        }
        return false;
    }

    static getCodeByPosition(position) {
        const letter = String.fromCharCode(65 + 8 - position.y);
        const number = position.x + 1;
        return `${letter}${number}`;
    }
}

export default Space;