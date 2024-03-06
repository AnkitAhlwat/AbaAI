import { BoardLayouts } from "../constants/boardLayouts";
import { useEffect, useState } from "react";
import Space from "../models/Space";

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

  const [boardArray, setBoardArray] = useState(emptyLayout);
  const [board, setBoard] = useState([]);

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
  }, [boardLayout, setBoardArray]);

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
