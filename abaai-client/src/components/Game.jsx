import { BoardLayouts } from "../constants/boardLayouts";
import { Board } from "./Board";
import ConfigMenu from "./ConfigMenu";
import { useState } from "react";
import { useBoard } from "../hooks/useBoard";

const Game = () => {
  const [config, setConfig] = useState({
    boardLayout: BoardLayouts.DEFAULT,
  });
  const { board } = useBoard(config.boardLayout); // import board state and setBoard function from useBoard hook

  return (
    <>
      <Board board={board} />
      <ConfigMenu config={config} setConfig={setConfig} />
    </>
  );
};

export default Game;
