import { Marbles } from "../constants/marbles";

// A custom hook that returns functions to set the board position to the default position, Belgian Daisy position, and German Daisy position
const useBoardPositions = () => {

  // Sets the standard board position
  const setDefaultPosition = (board) => {
    for (const row of board) {
      for (const spot of row) {
        if (
          spot.rowLetter === "A" ||
          spot.rowLetter === "B" ||
          (spot.rowLetter === "C" && [3, 4, 5].includes(spot.columnNumber))
        ) {
          spot.marble = Marbles.BLUE;
        } else if (
          spot.rowLetter === "I" ||
          spot.rowLetter === "H" ||
          (spot.rowLetter === "G" && [5, 6, 7].includes(spot.columnNumber))
        ) {
          spot.marble = Marbles.RED;
        }
      }
    }
  };

  // Sets the belgian daisy board position
  const setBelgianDaisyPosition = (board) => {
    // Coordinates of marble positions
    const marblesByRow = {
      A: { blue: [1,2], red: [4,5] },
      B: { blue: [1,2,3], red: [4,5,6] },
      C: { blue: [2,3], red: [5,6] },
      G: { blue: [7,8], red: [4,5] },
      H: { blue: [7,8,9], red: [4,5,6] },
      I: { blue: [8,9], red: [5,6] }
    };

    // Colours spots according to coordinates
    for (const row of board) {
      const blueColumns = marblesByRow[row[0].rowLetter]?.blue;
      const redColumns = marblesByRow[row[0].rowLetter]?.red;
      for (const spot of row) {
        if (blueColumns && blueColumns.includes(spot.columnNumber)) {
          spot.marble = Marbles.BLUE;
        } else if (redColumns && redColumns.includes(spot.columnNumber)) {
          spot.marble = Marbles.RED;
        }
      }
    }
  };

  // Sets the german daisy board position
  const setGermanDaisyPosition = (board) => {
    // Coordinates of marble positions
    const marblesByRow = {
      B: { blue: [1,2], red: [5,6] },
      C: { blue: [1,2,3], red: [5,6,7] },
      D: { blue: [2,3], red: [6,7] },
      F: { blue: [7,8], red: [3,4] },
      G: { blue: [7,8,9], red: [3,4,5] },
      H: { blue: [8,9], red: [4,5] }
    };

    // Colours spots according to coordinates
    for (const row of board) {
      const blueColumns = marblesByRow[row[0].rowLetter]?.blue;
      const redColumns = marblesByRow[row[0].rowLetter]?.red;
      for (const spot of row) {
        if (blueColumns && blueColumns.includes(spot.columnNumber)) {
          spot.marble = Marbles.BLUE;
        } else if (redColumns && redColumns.includes(spot.columnNumber)) {
          spot.marble = Marbles.RED;
        }
      }
    }
  };

  return {
    setDefaultPosition,
    setBelgianDaisyPosition,
    setGermanDaisyPosition,
  };
};

export { useBoardPositions };
