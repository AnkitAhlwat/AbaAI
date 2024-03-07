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

const Game = () => {
  // States
  const [aiMove, setAiMove] = useState("");
  const [selectedMarbles, setSelectedMarbles] = useState([]);
  const [movesStack, setMovesStack] = useState([]);
  const [config, setConfig] = useState({
    boardLayout: BoardLayouts.DEFAULT,
    playerColor: PlayerColors.BLACK,
    gameMode: "Computer"
  });
  const [gameStarted, setGameStarted] = useState(false);

  // Custom hooks
  const { board, setBoardArray } = useBoard(config.boardLayout); // import board state and setBoard function from useBoard hook

  // Callbacks
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

  const onUndoLastMove = useCallback(async () => {
    const responseData = await GameService.postUndoLastMove();
    console.log(responseData);
    setBoardArray(responseData.board);
    setMovesStack(responseData.moves_stack);
  }, [setBoardArray]);

  const onResetGame = useCallback(async () => {
    console.log("resetting game");
    const responseData = await GameService.resetGame();
    console.log(responseData);
    setBoardArray(responseData.board);
    setMovesStack(responseData.moves_stack);
  }, []);

  // JSX
  return (
    <Grid container spacing={2}>
      {/* Configuration Menu on the left */}
      <Grid item xs={3}>
        <GameClock
          initialTime={600}
          turnTimeLimit={15}
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
