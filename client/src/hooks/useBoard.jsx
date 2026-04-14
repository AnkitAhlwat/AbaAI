import { useState } from "react";

const EMPTY_BOARD = [
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

const useBoard = () => {
  const [boardArray, setBoardArray] = useState(EMPTY_BOARD);
  return { boardArray, setBoardArray };
};

export { useBoard };
