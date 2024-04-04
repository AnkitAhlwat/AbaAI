import { BoardLayouts } from "../constants/boardLayouts";
import { useEffect, useMemo, useState } from "react";
import Space from "../models/Space";

// A custom hook that generates the board and returns the board state and a function to set the board state
const useBoard = (boardLayout) => {
  const emptyLayout = useMemo(
    () => [
      [-1, -1, -1, -1, 0, 0, 0, 0, 0],
      [-1, -1, -1, 0, 0, 0, 0, 0, 0],
      [-1, -1, 0, 0, 0, 0, 0, 0, 0],
      [-1, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, -1],
      [0, 0, 0, 0, 0, 0, 0, -1, -1],
      [0, 0, 0, 0, 0, 0, -1, -1, -1],
      [0, 0, 0, 0, 0, -1, -1, -1, -1],
    ],
    []
  );

  const defaultLayout = useMemo(
    () => [
      [-1, -1, -1, -1, 2, 2, 2, 2, 2],
      [-1, -1, -1, 2, 2, 2, 2, 2, 2],
      [-1, -1, 0, 0, 2, 2, 2, 0, 0],
      [-1, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, -1],
      [0, 0, 1, 1, 1, 0, 0, -1, -1],
      [1, 1, 1, 1, 1, 1, -1, -1, -1],
      [1, 1, 1, 1, 1, -1, -1, -1, -1],
    ],
    []
  );

  const germanDaisyLayout = useMemo(
    () => [
      [-1, -1, -1, -1, 0, 0, 0, 0, 0],
      [-1, -1, -1, 2, 2, 0, 0, 1, 1],
      [-1, -1, 2, 2, 2, 0, 1, 1, 1],
      [-1, 0, 2, 2, 0, 0, 1, 1, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 1, 1, 0, 0, 2, 2, 0, -1],
      [1, 1, 1, 0, 2, 2, 2, -1, -1],
      [1, 1, 0, 0, 2, 2, -1, -1, -1],
      [0, 0, 0, 0, 0, -1, -1, -1, -1],
    ],
    []
  );

  const belgianDaisyLayout = useMemo(
    () => [
      [-1, -1, -1, -1, 2, 2, 0, 1, 1],
      [-1, -1, -1, 2, 2, 2, 1, 1, 1],
      [-1, -1, 0, 2, 2, 0, 1, 1, 0],
      [-1, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, -1],
      [0, 1, 1, 0, 2, 2, 0, -1, -1],
      [1, 1, 1, 2, 2, 2, -1, -1, -1],
      [1, 1, 0, 2, 2, -1, -1, -1, -1],
    ],
    []
  );

  const [boardArray, setBoardArray] = useState(emptyLayout); // Tracks state of board array
  const [board, setBoard] = useState([]); // Tracks state of total board

  // Changes board layout depending on enum
  useEffect(() => {
    switch (boardLayout) {
      case BoardLayouts.DEFAULT:
        setBoardArray(defaultLayout);
        break;
      case BoardLayouts.GERMAN_DAISY:
        setBoardArray(germanDaisyLayout);
        break;
      case BoardLayouts.BELGIAN_DAISY:
        setBoardArray(belgianDaisyLayout);
        break;
      default:
        setBoardArray(emptyLayout);
    }
  }, [
    belgianDaisyLayout,
    boardLayout,
    defaultLayout,
    emptyLayout,
    germanDaisyLayout,
    setBoardArray,
  ]);

  // Initializes board when change is detected
  useEffect(() => {
    const newBoard = boardArray.map((row, rowIndex) => {
      return row.map((state, columnIndex) => {
        return new Space(state, { x: columnIndex, y: rowIndex });
      });
    });

    setBoard(newBoard);
  }, [boardArray, setBoard]);

  return {
    boardArray,
    setBoardArray,
    board,
    setBoard,
  };
};

export { useBoard };
