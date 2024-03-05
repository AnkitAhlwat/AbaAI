import { BoardLayouts } from "../constants/boardLayouts";
import { useEffect, useState } from "react";

// A custom hook that generates the board and returns the board state and a function to set the board state
const useBoard = (boardLayout) => {
  const emptyLayout = [
    [-1, -1, -1, -1, 0, 0, 0, 0, 0],
    [-1, -1, -1, 0, 0, 0, 0, 0, 0],
    [-1, -1, 0, 0, 0, 0, 0, 0, 0],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, -1],
    [0, 0, 0, 0, 0, 0, 0, -1, -1],
    [0, 0, 0, 0, 0, 0, -1, -1, -1],
    [0, 0, 0, 0, 0, -1, -1, -1, -1],
  ];

  const defaultLayout = [
    [-1, -1, -1, -1, 2, 2, 2, 2, 2],
    [-1, -1, -1, 2, 2, 2, 2, 2, 2],
    [-1, -1, 0, 0, 2, 2, 2, 0, 0],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, -1],
    [0, 0, 1, 1, 1, 0, 0, -1, -1],
    [1, 1, 1, 1, 1, 1, -1, -1, -1],
    [1, 1, 1, 1, 1, -1, -1, -1, -1],
  ];

  const germanDaisyLayout = [
    [-1, -1, -1, -1, 0, 0, 0, 0, 0],
    [-1, -1, -1, 2, 2, 0, 0, 1, 1],
    [-1, -1, 2, 2, 2, 0, 1, 1, 1],
    [-1, 0, 2, 2, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 2, 2, 0, -1],
    [1, 1, 1, 0, 2, 2, 2, -1, -1],
    [1, 1, 0, 0, 2, 2, -1, -1, -1],
    [0, 0, 0, 0, 0, -1, -1, -1, -1],
  ];

  const belgianDaisyLayout = [
    [-1, -1, -1, -1, 2, 2, 0, 1, 1],
    [-1, -1, -1, 2, 2, 2, 1, 1, 1],
    [-1, -1, 0, 2, 2, 0, 1, 1, 0],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, -1],
    [0, 1, 1, 0, 2, 2, 0, -1, -1],
    [1, 1, 1, 2, 2, 2, -1, -1, -1],
    [1, 1, 0, 2, 2, -1, -1, -1, -1],
  ];

  const [board, setBoard] = useState(emptyLayout);

  useEffect(() => {
    switch (boardLayout) {
      case BoardLayouts.DEFAULT:
        setBoard(defaultLayout);
        break;
      case BoardLayouts.GERMAN_DAISY:
        setBoard(germanDaisyLayout);
        break;
      case BoardLayouts.BELGIAN_DAISY:
        setBoard(belgianDaisyLayout);
        break;
      default:
        setBoard(emptyLayout);
    }
  }, [boardLayout, setBoard]);

  return {
    board,
    setBoard,
  };
};

export { useBoard };
