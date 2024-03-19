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
import MoveButtons from "./MoveButtons";
import AIMoveDisplay from "./AiMove";
import Space from "../models/Space";
import ScoreCard from "./ScoreCard";
import SideBar from "./SideBar";
import GameplaySection from "./GameplaySection";
import RightSideBar from "./RightSideBar";

// Displays complete assembly of the GUI
const Game = () => {
  const [aiMove, setAiMove] = useState(""); // Tracks AI move history
  const [selectedMarbles, setSelectedMarbles] = useState([]); // Tracks which marbles are selected
  const [movesStack, setMovesStack] = useState([]); // Tracks player move history
  const [gameStarted, setGameStarted] = useState(false); // Tracks whether game has started
  const [activePlayer, setActivePlayer] = useState('black'); // Tracks which player's turn it is for clock logic, potentially temporary
  // const [currentPlayer, setCurrentPlayer] = useState('player1'); CLOCKSTUFF
  // const [isPaused, setIsPaused] = useState(false);

  // Tracks configuration options
  const [config, setConfig] = useState({
    boardLayout: BoardLayouts.DEFAULT,
    blackPlayer: "Human",
    whitePlayer: "Computer",
    blackTimeLimit: 15,
    whiteTimeLimit: 15,
    moveLimit: 20
  });

  const toggleActivePlayer = () => {
    setActivePlayer(prev => prev === 'black' ? 'white' : 'black');
  };

  // const togglePause = () => { CLOCKSTUFF
  //   setIsPaused(!isPaused);
  // };
  //currently used to switch the turn and aggregate clocks, can merge it with config options
  // const switchPlayer = () => {
  //   setCurrentPlayer(currentPlayer === 'player1' ? 'player2' : 'player1');
  // };

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

      //toggle the active player turn
      toggleActivePlayer();

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
  }, [setBoardArray]);

  // Returns assembly of the GUI
  return (
    <Grid
      container
      sx={{
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Grid
        container
        item
        xs={9}
        sx={{
          justifyContent: "center",
          alignItems: "center",
          height: "98vh",
          padding: "5px",
        }}
      >
        <GameplaySection
          board={board}
          onMoveSelection={onMoveSelection}
          selectedMarbles={selectedMarbles}
          setSelectedMarbles={setSelectedMarbles}

          // for the clock controls
          // currentPlayer={currentPlayer}
          // isPaused={isPaused}
          // togglePause={togglePause}
          // switchPlayer={switchPlayer}
        />
      </Grid>

      <Grid
        item
        xs={3}
        sx={{
          height: "95vh",
          padding: "5px",
        }}
      >
        {/* <AIMoveDisplay aiMove={aiMove} />
        <MoveHistory movesStack={movesStack} /> */}
        <RightSideBar
          config={config}
          setConfig={setConfig}
          movesStack={movesStack}
          aiMove={aiMove}

          //for the clock controls
          activePlayer={activePlayer}
          toggleActivePlayer={toggleActivePlayer}
          gameStarted={gameStarted}
          // currentPlayer={currentPlayer}
          // isPaused={isPaused}
          // togglePause={togglePause}
        />
      </Grid>
    </Grid>
  );
};

export default Game;
