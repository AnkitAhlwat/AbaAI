import { Marbles } from "../constants/marbles";
import { useState } from "react";

const useBoard = () => {
  const generateRow = (startColumnNum, endColumnNum, letter) => {
    let row = [];
    for (let i = startColumnNum; i < endColumnNum + 1; i++) {
      const spot = {
        row: letter,
        column: i,
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
      const startColumnNum = 1;
      const endColumnNum = rowLengthsBottomHalf[i];

      board.push(
        generateRow(
          startColumnNum,
          endColumnNum,
          String.fromCharCode(65 + letterCount)
        )
      );
      letterCount++;
    }
    for (let i = 0; i < rowLengthsTopHalf.length; i++) {
      const startColumnNum = 9 - rowLengthsTopHalf[i] + 1;
      const endColumnNum = 9;

      board.push(
        generateRow(
          startColumnNum,
          endColumnNum,
          String.fromCharCode(65 + letterCount)
        )
      );
      letterCount++;
    }

    return board;
  };

  const [board, setBoard] = useState(generateBoard());

  return {
    board,
    setBoard,
  };
};

export { useBoard };
