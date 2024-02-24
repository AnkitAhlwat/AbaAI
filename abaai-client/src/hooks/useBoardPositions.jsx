import { Marbles } from "../constants/marbles";

// A custom hook that returns functions to set the board position to the default position, Belgian Daisy position, and German Daisy position
const useBoardPositions = () => {
  const setDefaultBoardPosition = (board) => {
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

  const setBelgianDaisyBoardPosition = (board) => {
    console.log("Belgian Daisy board position not implemented yet");
  };

  const setGermanDaisyBoardPosition = (board) => {
    console.log("German Daisy board position not implemented yet");
  };

  return {
    setDefaultBoardPosition,
    setBelgianDaisyBoardPosition,
    setGermanDaisyBoardPosition,
  };
};

export { useBoardPositions };
