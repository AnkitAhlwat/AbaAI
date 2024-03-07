import { BoardLayouts } from "../constants/boardLayouts";
import { Board } from "./Board";
import ConfigMenu from "./ConfigMenu";
import { useCallback, useState } from "react";
import { useBoard } from "../hooks/useBoard";
import MoveHistory from "./MoveHistory";
import { Grid } from "@mui/material";
import GameService from "../services/game.service";
import Move from "../models/Move";
import GameControls from "./GameControls";
import GameClock from "./Clock";
import AIMoveDisplay from "./AiMove";
import Space from "../models/Space";


const Game = () => {
  // States
  const [aiMove, setAiMove] = useState("");
  const [selectedMarbles, setSelectedMarbles] = useState([]);
  const [movesStack, setMovesStack] = useState([]);
  const [config, setConfig] = useState({
    boardLayout: BoardLayouts.DEFAULT,
  });

  // Custom hooks
  const { board, boardArray, setBoardArray } = useBoard(config.boardLayout); // import board state and setBoard function from useBoard hook

  // Callbacks
  const onMoveSelection = useCallback(
    async (move) => {
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

      // send post request to the server
      const moveObj = new Move(previousPositions, newPositions, marbleState);
      const responseData = await GameService.postMove(moveObj);
      const aiMoveNext = responseData.ai_move.next_positions
      const aiMovePrev = responseData.ai_move.previous_positions
      const prev_moves = aiMovePrev.map((position) => {
        return Space.getCodeByPosition(position);
      });
      const next_moves = aiMoveNext.map((position) => {
        return Space.getCodeByPosition(position);
      });


      const aiMove = `${prev_moves} -> ${next_moves}`;
      setAiMove(aiMove);
      setMovesStack(responseData.moves_stack);
      setBoardArray(responseData.board)
    },
    [boardArray, selectedMarbles, setBoardArray]
  );

  const onUndoLastMove = useCallback(async () => {
    const responseData = await GameService.postUndoLastMove();
    console.log(responseData);
    setBoardArray(responseData.board);
    setMovesStack(responseData.moves_stack);
  }, [setBoardArray]);

  const onResetGame = useCallback(async () => {
    console.log("resetting game");
    // const responseData = await GameService.resetGame();
    // console.log(responseData);
    // setBoardArray(responseData.board);
    // setMovesStack(responseData.moves_stack);
  }, []);

  // JSX
  return (
    <Grid container spacing={2}>
      {/* Configuration Menu on the left */}
      <Grid item xs={3}>
        <GameClock initialTime={600} turnTimeLimit={15} />
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
        <GameControls
          onUndo={onUndoLastMove}
          onReset={onResetGame}
          movesStack={movesStack}
        />
      </Grid>

      {/* Move History on the right */}
      <Grid item xs={3}>
        <AIMoveDisplay aiMove={aiMove} />
        <MoveHistory movesStack={movesStack} />
      </Grid>
    </Grid>
  );
};

export default Game;
