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
  const [activePlayer, setActivePlayer] = useState("black"); // Tracks which player's turn it is for clock logic, potentially temporary
  // const [currentPlayer, setCurrentPlayer] = useState('player1'); CLOCKSTUFF
  const [isGameActive, setIsGameActive] = useState(false);
  const [resetClockSignal, setResetClockSignal] = useState(0);
  const [possibleMoves, setPossibleMoves] = useState([]);

  // Tracks configuration options
  const [config, setConfig] = useState({
    boardLayout: BoardLayouts.DEFAULT,
    blackPlayer: "Human",
    whitePlayer: "Computer",
    blackTimeLimit: 15,
    whiteTimeLimit: 15,
    moveLimit: 20,
  });

  const toggleTurn = () => {
    setActivePlayer((prev) => (prev === "black" ? "white" : "black"));
  };

  //Defines aggregate clock states for each player, temporary
  const [blackClock, setBlackClock] = useState({
    time: 180,
    isRunning: false,
  });
  const [whiteClock, setWhiteClock] = useState({
    time: 180,
    isRunning: false,
  });

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
  const resetGame = () => {
    //reset the board logic here
    setBlackClock({ time: blackClock.time, isRunning: false });
    setWhiteClock({ time: whiteClock.time, isRunning: false });
    setGameStarted(false);
    setResetClockSignal((prev) => prev + 1);
  };

  //stop the game and reset the clocks, this should also completely reset the game state
  const stopGame = () => {
    setBlackClock({ time: blackClock.time, isRunning: false });
    setWhiteClock({ time: whiteClock.time, isRunning: false });
    setGameStarted(false);
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
  const startGame = useCallback(() => {
    if (!gameStarted) {
      setGameStarted(true);
      setIsGameActive(true);
      resumeGame("black");
    }
  }, [gameStarted, resumeGame]);

  const { board, setBoardArray } = useBoard(config.boardLayout); // import board state and setBoard function from useBoard hook

  // Handles new AI move
  const updateAiMove = useCallback((aiMove) => {
    setAiMove(Move.toNotation(aiMove));
  }, []);

  // Handles move selection
  const onMoveSelection = useCallback(
    async (move) => {
      // get the previous and new positions of the selected marbles
      console.log("Move:", move);
      const marbleState = selectedMarbles[0].state;
      //toggle the active player turn
      toggleTurn();

      //set gamestarted to true
      if (!gameStarted) {
        setGameStarted(true);
      }

      setSelectedMarbles([]);

      // send post request to the server
      const moveObj = new Move(
        move.previous_player_positions,
        move.next_player_positions,
        marbleState,
        move.previous_opponent_positions,
        move.next_opponent_positions
      );
      const responseData = await GameService.postMove(moveObj);
      setMovesStack(responseData.moves_stack);
      setBoardArray(responseData.game_state.board);

      // set the ai move card to display the move that the ai generated
      const aiMove = await GameService.getAiMoveForCurrentState();
      updateAiMove(aiMove);
    },
    [selectedMarbles, gameStarted, setBoardArray, updateAiMove]
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
          toggleActivePlayer={toggleTurn}
          gameStarted={gameStarted}
          gameActive={isGameActive}
          startGame={startGame}
          stopGame={stopGame}
          resetClockSignal={resetClockSignal}
          pauseGame={pauseGame}
          resumeGame={resumeGame}
          resetGame={resetGame}
          undoMove={onUndoLastMove}
          blackClock={blackClock}
          whiteClock={whiteClock}
          // currentPlayer={currentPlayer}
          // isPaused={isPaused}
          // togglePause={togglePause}
        />
      </Grid>
    </Grid>
  );
};

export default Game;
