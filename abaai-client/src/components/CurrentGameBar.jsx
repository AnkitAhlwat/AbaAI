import MoveHistory from "./MoveHistory";
import AIMoveDisplay from "./AiMove";
import GameClock from "./Clock";
import Proptypes from "prop-types";
import GameControls from "./GameControls";
import { Divider, Typography, Button } from "@mui/material";
import { Undo } from "@mui/icons-material";

const CurrentGameBar = (props) => {
  const { movesStack, aiMove, activePlayer, toggleActivePlayer, gameStarted, gameActive, startGame,
    stopGame, resetClockSignal, pauseGame, resumeGame, resetGame, undoMove, blackClock, whiteClock, 
  } = props;


  const dummyMovesStack = [
    {
      player: 1,
      previous_positions: [
        { x: 2, y: 6 },
        { x: 3, y: 6 },
      ],
      next_positions: [
        { x: 2, y: 5 },
        { x: 3, y: 5 },
      ],
    },
    {
      player: 2,
      previous_positions: [
        { x: 4, y: 2 },
        { x: 5, y: 2 },
      ],
      next_positions: [
        { x: 4, y: 3 },
        { x: 5, y: 3 },
      ],
    },
    {
      player: 1,
      previous_positions: [
        { x: 4, y: 6 },
        { x: 4, y: 7 },
        { x: 4, y: 8 },
      ],
      next_positions: [
        { x: 4, y: 5 },
        { x: 4, y: 6 },
        { x: 4, y: 7 },
      ],
    },
  ];

  const centerDivider = (text) => {
    if (text === "" || text === undefined) {
      return <Divider variant="middle" sx={{ bgcolor: "white" }} />;
    }
    return (
      <Divider
        variant="middle"
        sx={{
          color: "#f5f5f5",
          "&::before, &::after": {
            borderColor: "#f5f5f5",
          },
        }}
      >
        <Typography>{text}</Typography>
      </Divider>
    );
  };

  //for the take turn button
  // const handleClockResume = () => {
  //   if (!gameStarted) {
  //     startGame();
  //   } else {
  //     toggleActivePlayer();
  //     console.log("Resuming game"); // Placeholder action
  //   }
  // };

  const handlePlayerChange = () => {
    toggleActivePlayer();
    // Assuming activePlayer state changes, pause and resume clocks as necessary
    pauseClock(activePlayer);
    const nextPlayer = activePlayer === 'black' ? 'white' : 'black';
    resumeClock(nextPlayer);
  };

  return (
    <>
      <GameClock 
        initialTime={blackClock.time} 
        isTurn={activePlayer === 'black'}
        playerId="black" 
        activePlayer={activePlayer}
        gameStarted = {gameStarted}
        isActive = {gameActive}
        resetClockSignal={resetClockSignal}
        />
      <GameClock 
        initialTime={whiteClock.time}
        isTurn={activePlayer === 'white'}
        playerId="white" 
        activePlayer={activePlayer}
        gameStarted = {gameStarted}
        isActive = {gameActive}
        resetClockSignal={resetClockSignal}
        />

        <GameControls
        onTakeTurn={handlePlayerChange}
        toggleActivePlayer={toggleActivePlayer}
        onStart={startGame}
        onPause={() => pauseGame(activePlayer)}
        onResume={() => resumeGame(activePlayer)}
        onStop={() => stopGame(activePlayer)}
        isGameActive={gameActive}
        isCurrentPlayerActive={activePlayer}
        onReset={resetGame}
        onUndo={() => undoMove(activePlayer)}
        gameStarted={gameStarted}
        movesStack={movesStack}
      />
      {/* <Button onClick={handleClockResume} color="primary" variant="contained">
        Take turn
      </Button> */}
      {/* <GameClock currentPlayer={currentPlayer} isPaused={isPaused} togglePause={togglePause} /> */}
      {centerDivider("AI Suggested Move")}
      <AIMoveDisplay aiMove={aiMove} />
      {centerDivider("Move History")}
      <MoveHistory movesStack={dummyMovesStack} />
    </>
  );
};

CurrentGameBar.propTypes = {
  movesStack: Proptypes.array.isRequired,
  aiMove: Proptypes.string.isRequired,
  // activePlayer: PropTypes.string.isRequired,
  // toggleActivePlayer: PropTypes.func.isRequired,
  // gameStarted: PropTypes.bool.isRequired,
  // startGame: PropTypes.func.isRequired,
  // blackClock: PropTypes.object.isRequired,
  // whiteClock: PropTypes.object.isRequired,
  // pauseClock: PropTypes.func.isRequired,
  // resumeClock: PropTypes.func.isRequired,
  // resetClocks: PropTypes.func.isRequired,
};

export default CurrentGameBar;
