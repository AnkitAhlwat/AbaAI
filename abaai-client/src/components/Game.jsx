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
import MoveButtons from "./MoveButtons";
import AIMoveDisplay from "./AiMove";
import Space from "../models/Space";
import { PlayerColors } from "../constants/playerColors";
import ScoreCard from "./ScoreCard";

// Displays complete assembly of the GUI
const Game = () => {
  const [aiMove, setAiMove] = useState(""); // Tracks AI move history
  const [selectedMarbles, setSelectedMarbles] = useState([]); // Tracks which marbles are selected
  const [movesStack, setMovesStack] = useState([]); // Tracks player move history
  const [gameStarted, setGameStarted] = useState(false); // Tracks whether game has started

  // Tracks configuration options
  const [config, setConfig] = useState({
    boardLayout: BoardLayouts.DEFAULT,
    playerColor: PlayerColors.BLACK,
    gameMode: "Computer",
    moveLimit: 100,
    timeLimit: 15
  });

  const { board, setBoardArray } = useBoard(config.boardLayout); // import board state and setBoard function from useBoard hook

  // Handles new AI move
  const updateAiMove = useCallback((aiMove) => {
    const aiMoveNext = aiMove.next_positions;
    const aiMovePrev = aiMove.previous_positions;
    const prev_moves = aiMovePrev.map((position) => {
      return Space.getCodeByPosition(position);
    });
    const next_moves = aiMoveNext.map((position) => {
      return Space.getCodeByPosition(position);
    });

    const moveCode = `${prev_moves} -> ${next_moves}`;
    setAiMove(moveCode);
  }, []);

  // Handles move selection
  const onMoveSelection = useCallback(
    async (move) => {
      // get the previous and new positions of the selected marbles
      const previousPositions = selectedMarbles.map(
        (marble) => marble.position
      );
      const newPositions = previousPositions.map((position) => ({
        x: position.x + move.x,
        y: position.y + move.y,
      }));
      const marbleState = selectedMarbles[0].state;

      //set gamestarted to true
      if (!gameStarted) {
        setGameStarted(true);
      }

      setSelectedMarbles([]);

      // send post request to the server
      const moveObj = new Move(previousPositions, newPositions, marbleState);
      const responseData = await GameService.postMove(moveObj);

      // set the ai move card to show what the ai did
      updateAiMove(responseData.ai_move);

      // update the board and moves stack
      setMovesStack(responseData.moves_stack);
      setBoardArray(responseData.board);
    },
    [selectedMarbles, setBoardArray, updateAiMove, gameStarted]
  );

  // Handles move undo
  const onUndoLastMove = useCallback(async () => {
    const responseData = await GameService.postUndoLastMove();
    console.log(responseData);
    setBoardArray(responseData.board);
    setMovesStack(responseData.moves_stack);
  }, [setBoardArray]);

  // Handles game reset
  const onResetGame = useCallback(async () => {
    console.log("resetting game");
    const responseData = await GameService.resetGame();
    console.log(responseData);
    setBoardArray(responseData.board);
    setMovesStack(responseData.moves_stack);
  }, []);

  // Returns assembly of the GUI
  return (
    <Grid container spacing={2}>
      {/* Configuration Menu on the left */}
      <Grid item xs={3}>
        <GameClock
          initialTime={600}
          turnTimeLimit={config.timeLimit}
          gameStarted={gameStarted}
          setBoardArray={setBoardArray}
        />
        <ConfigMenu config={config} setConfig={setConfig} />
      </Grid>

      {/* Board in the middle */}
      <Grid
        container
        item
        xs={6}
        sx={{
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <ScoreCard />

        <Board
          board={board}
          onMoveSelection={onMoveSelection}
          selectedMarbles={selectedMarbles}
          setSelectedMarbles={setSelectedMarbles}
        />
        <MoveButtons
          onMoveSelection={onMoveSelection}
          selectedMarbles={selectedMarbles}
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
