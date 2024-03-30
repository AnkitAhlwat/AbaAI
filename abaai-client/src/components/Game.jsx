import { Grid } from "@mui/material";
import { useCallback, useState, useEffect } from "react";
import { BoardLayouts } from "../constants/boardLayouts";
import { useBoard } from "../hooks/useBoard";
import Move from "../models/Move";
import GameService from "../services/game.service";
import GameplaySection from "./GameplaySection";
import RightSideBar from "./RightSideBar";

// Displays complete assembly of the GUI
const Game = () => {
  // ##################### States #####################
  const [blackAiMove, setBlackAiMove] = useState(null); // Tracks AI move history
  const [whiteAiMove, setWhiteAiMove] = useState(null); // Tracks AI move history
  const [selectedMarbles, setSelectedMarbles] = useState([]); // Tracks which marbles are selected
  const [movesStack, setMovesStack] = useState([]); // Tracks player move history
  const [gameStarted, setGameStarted] = useState(false); // Tracks whether game has started
  const [activePlayer, setActivePlayer] = useState("black"); // Tracks which player's turn it is for clock logic, potentially temporary
  const [isGameActive, setIsGameActive] = useState(false);
  const [isGameConfigured, setIsGameConfigured] = useState(false); // Tracks whether game has been configured
  const [resetClockSignal, setResetClockSignal] = useState(0);
  const [config, setConfig] = useState(null); // Tracks configuration options
  const [numCapturedBlackMarbles, setNumCapturedBlackMarbles] = useState(0); // Tracks number of black marbles captured
  const [numCapturedWhiteMarbles, setNumCapturedWhiteMarbles] = useState(0); // Tracks number of white marbles captured
  const [currentTurn, setCurrentTurn] = useState(0); // Tracks current turn
  //Defines aggregate clock states for each player, temporary
  const [blackClock, setBlackClock] = useState({
    time: 180,
    isRunning: false,
  });
  const [whiteClock, setWhiteClock] = useState({
    time: 180,
    isRunning: false,
  });

  // ##################### Custom Hooks #####################
  const { boardArray, setBoardArray } = useBoard(config?.boardLayout); // import board state and setBoard function from useBoard hook

  // ##################### Functions/Callbacks #####################
  // When the page loads, we want to fetch the state of the game from the server and update accordingly
  const updateGame = useCallback(
    async (gameStatus) => {
      if (!gameStatus) {
        gameStatus = await GameService.getGameStatus();
      }

      console.log("Game Status:", gameStatus);

      // Set the configuration options
      setConfig(gameStatus.game_options);

      // Set the state of the game
      setIsGameActive(gameStatus.game_started);
      setIsGameConfigured(gameStatus.game_configured);

      // Set the board state
      setBoardArray(gameStatus.game_state.board);

      // Set the player turn
      setCurrentTurn(gameStatus.game_state.turn);

      // Set the moves stack
      setMovesStack(gameStatus.moves_stack);

      // Set the captured marbles
      setNumCapturedBlackMarbles(gameStatus.game_state.captured_black_marbles);
      setNumCapturedWhiteMarbles(gameStatus.game_state.captured_white_marbles);
    },
    [setBoardArray]
  );

  const toggleTurn = () => {
    setActivePlayer((prev) => (prev === "black" ? "white" : "black"));
  };

  // Pause the game
  const pauseGame = (player) => {
    setIsGameActive(false);
    if (player === "black") {
      setBlackClock((clock) => ({ ...clock, isRunning: false }));
    } else {
      setWhiteClock((clock) => ({ ...clock, isRunning: false }));
    }
  };

  // Resume Game
  const resumeGame = (player) => {
    setIsGameActive(true);
    if (player === "black") {
      setBlackClock((clock) => ({ ...clock, isRunning: true }));
    } else {
      setWhiteClock((clock) => ({ ...clock, isRunning: true }));
    }
  };

  //reset the game and clocks
  const resetGame = async () => {
    const gameStatus = await GameService.postResetGame();
    updateGame(gameStatus);

    //reset the board logic here
    setBlackClock({ time: blackClock.time, isRunning: false });
    setWhiteClock({ time: whiteClock.time, isRunning: false });
    setGameStarted(false);
    setIsGameActive(false);
    setResetClockSignal((prev) => prev + 1);
    setBlackAiMove(null);
    setWhiteAiMove(null);
  };

  //stop the game and reset the clocks, this should also completely reset the game state
  const stopGame = () => {
    setBlackClock({ time: blackClock.time, isRunning: false });
    setWhiteClock({ time: whiteClock.time, isRunning: false });
    setGameStarted(false);
    setIsGameActive(false);
    setResetClockSignal((prev) => prev + 1);
  };

  //undo the last move
  const undoMove = (player) => {
    //undo the last move logic here
    //reset the turn clocks
    //reset the board to the last state
    //add back the time that the last turn took to the previous player's clock
    //need to be able to do this multiple times
    if (player === "black") {
      setBlackClock((clock) => ({ ...clock, isRunning: false }));
    } else {
      setWhiteClock((clock) => ({ ...clock, isRunning: false }));
    }
  };

  //logic to start the game and black game clock
  const startGame = useCallback(async () => {
    if (!gameStarted) {
      const gameStatus = await GameService.startGame();
      updateGame(gameStatus);
      setGameStarted(true);
      resumeGame("black");
    }
  }, [gameStarted, updateGame]);

  // Handles move selection
  const onMoveSelection = useCallback(
    async (move) => {
      console.log("Move:", move);

      //toggle the active player turn
      toggleTurn();

      //set gamestarted to true
      if (!gameStarted) {
        setGameStarted(true);
      }

      // // send post request to the server
      const moveObj = new Move(
        move.previous_player_positions,
        move.next_player_positions,
        currentTurn,
        move.previous_opponent_positions,
        move.next_opponent_positions
      );
      const gameStatus = await GameService.postMove(moveObj);
      updateGame(gameStatus);

      // set the ai move card to display the move that the ai generated
      const aiMove = await GameService.getAiMoveForCurrentState();
      if (gameStatus.game_state.turn === 1) {
        setBlackAiMove(aiMove);
      } else {
        setWhiteAiMove(aiMove);
      }
    },
    [gameStarted, currentTurn, updateGame]
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

  // ##################### Effects #####################
  useEffect(() => {
    updateGame();
  }, [updateGame]); // should only run once when the component mounts (page loaded or refreshed)

  // ##################### Render #####################
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
        xs={8}
        sx={{
          justifyContent: "center",
          alignItems: "center",
          height: "98vh",
          padding: "5px",
        }}
      >
        <GameplaySection
          boardArray={boardArray}
          onMoveSelection={onMoveSelection}
          selectedMarbles={selectedMarbles}
          setSelectedMarbles={setSelectedMarbles}
          numCapturedBlackMarbles={numCapturedBlackMarbles}
          numCapturedWhiteMarbles={numCapturedWhiteMarbles}
          isGameActive={isGameActive}
          currentTurn={currentTurn}

          //for the clock controls
          // blackClock={blackClock}
          // whiteClock={whiteClock}
          // pauseClock={pauseClock}
          // resumeClock={resumeClock}
          // resetClocks={resetClocks}
        />
      </Grid>

      <Grid
        item
        xs={4}
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
          blackAiMove={blackAiMove}
          whiteAiMove={whiteAiMove}
          currentTurn={currentTurn}
          //for the clock controls
          activePlayer={activePlayer}
          toggleActivePlayer={toggleTurn}
          gameStarted={gameStarted}
          gameActive={isGameActive}
          gameConfigured={isGameConfigured}
          startGame={startGame}
          stopGame={stopGame}
          resetClockSignal={resetClockSignal}
          pauseGame={pauseGame}
          resumeGame={resumeGame}
          resetGame={resetGame}
          undoMove={onUndoLastMove}
          blackClock={blackClock}
          whiteClock={whiteClock}
          updateGame={updateGame}
          onApplyMove={onMoveSelection}
          // currentPlayer={currentPlayer}
          // isPaused={isPaused}
          // togglePause={togglePause}
        />
      </Grid>
    </Grid>
  );
};

export default Game;
