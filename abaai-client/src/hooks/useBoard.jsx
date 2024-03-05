import { Marbles } from "../constants/marbles";
import { useState } from "react";

// A custom hook that generates the board and returns the board state and a function to set the board state
const useBoard = () => {
  const generateRow = (startColumnIndex, endColumnIndex, rowIndex) => {
    let row = [];
    for (let i = startColumnIndex; i < endColumnIndex + 1; i++) {
      const spot = {
        rowIndex: rowIndex,
        columnIndex: i,
        rowLetter: String.fromCharCode(65 + rowIndex),
        columnNumber: i + 1,
        marble: Marbles.EMPTY,
      };
      row.push(spot);
    }
    return row;
  };

  const generateBoard = () => {
    const rowLengthsBottomHalf = [5, 6, 7, 8, 9];
    const rowLengthsTopHalf = [8, 7, 6, 5];

    let board = [];
    let letterCount = 0;
    for (let i = 0; i < rowLengthsBottomHalf.length; i++) {
      const startColumnIndex = 0;
      const endColumnIndex = rowLengthsBottomHalf[i] - 1;

      board.unshift(generateRow(startColumnIndex, endColumnIndex, letterCount));
      letterCount++;
    }
    for (let i = 0; i < rowLengthsTopHalf.length; i++) {
      const startColumnIndex = 9 - rowLengthsTopHalf[i];
      const endColumnIndex = 9 - 1;

      board.unshift(generateRow(startColumnIndex, endColumnIndex, letterCount));
      letterCount++;
    }
    return board;
  };

  const [board, setBoard] = useState(() => generateBoard());

  return {
    board,
    setBoard,
  };
};

export { useBoard };
