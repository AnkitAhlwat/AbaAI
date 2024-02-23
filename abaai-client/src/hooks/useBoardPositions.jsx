import { Marbles } from "../constants/marbles";

const useBoardPositions = () => {
  const useDefaultBoardPosition = (board) => {
    for (const row of board) {
      for (const spot of row) {
        if (
          spot.row === "A" ||
          spot.row === "B" ||
          (spot.row === "C" && [3, 4, 5].includes(spot.column))
        ) {
          spot.marble = Marbles.BLUE;
        } else if (
          spot.row === "I" ||
          spot.row === "H" ||
          (spot.row === "G" && [5, 6, 7].includes(spot.column))
        ) {
          spot.marble = Marbles.RED;
        }
      }
    }
  };

  const useBelgianDaisyBoardPosition = (board) => {
    console.log("Belgian Daisy board position not implemented yet");
  };

  const useGermanDaisyBoardPosition = (board) => {
    console.log("German Daisy board position not implemented yet");
  };

  return {
    useDefaultBoardPosition,
    useBelgianDaisyBoardPosition,
    useGermanDaisyBoardPosition,
  };
};

export { useBoardPositions };
