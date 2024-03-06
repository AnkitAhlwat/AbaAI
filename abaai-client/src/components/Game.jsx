import { BoardLayouts } from "../constants/boardLayouts";
import { Board } from "./Board";
import ConfigMenu from "./ConfigMenu";
import { useCallback, useState } from "react";
import { useBoard } from "../hooks/useBoard";
import MoveHistory from "./MoveHistory";
import { Grid } from "@mui/material";

const Game = () => {
  // States
  const [selectedMarbles, setSelectedMarbles] = useState([]);
  const [movesStack, setMovesStack] = useState([]);
  const [config, setConfig] = useState({
    boardLayout: BoardLayouts.DEFAULT,
  });

  // Custom hooks
  const { board, boardArray, setBoardArray } = useBoard(config.boardLayout); // import board state and setBoard function from useBoard hook

  // Callbacks
  const onMoveSelection = useCallback(
    (move) => {
      const newBoardArray = [...boardArray];
      const previousPositions = selectedMarbles.map(
        (marble) => marble.position
      );
      const newPositions = previousPositions.map((position) => ({
        x: position.x + move.x,
        y: position.y + move.y,
      }));
      const marbleState = selectedMarbles[0].state;

      // set all the previous positions to empty
      for (const position of previousPositions) {
        newBoardArray[position.y][position.x] = 0;
      }

      // set all the new positions to the marble state
      for (const position of newPositions) {
        newBoardArray[position.y][position.x] = marbleState;
      }

      // update the board array (will trigger a re-render of the board component with the new board array) and reset the selected marbles
      setBoardArray(newBoardArray);
      setSelectedMarbles([]);
    },
    [boardArray, selectedMarbles, setBoardArray]
  );

  // JSX
  return (
    <Grid container spacing={2}>
      {/* Configuration Menu on the left */}
      <Grid item xs={3}>
        <ConfigMenu config={config} setConfig={setConfig} />
      </Grid>

      {/* Board in the middle */}
      <Grid item xs={6}>
        <Board
          board={board}
          onMoveSelection={onMoveSelection}
          selectedMarbles={selectedMarbles}
          setSelectedMarbles={setSelectedMarbles}
        />
      </Grid>

      {/* Move History on the right */}
      <Grid item xs={3}>
        <MoveHistory movesStack={movesStack} />
      </Grid>
    </Grid>
  );
};

export default Game;