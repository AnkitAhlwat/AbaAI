import MoveHistory from "./MoveHistory";
import AIMoveDisplay from "./AiMove";
import GameClock from "./Clock";
import Proptypes from "prop-types";
import GameControls from "./GameControls";
import { Divider, Typography, Button, Grid } from "@mui/material";
import { Undo } from "@mui/icons-material";
import { useMemo } from "react";

const CurrentGameBar = (props) => {
  const {
    config,
    movesStack,
    blackAiMove,
    whiteAiMove,
    currentTurn,
    activePlayer,
    toggleActivePlayer,
    gameStarted,
    gameActive,
    startGame,
    stopGame,
    resetClockSignal,
    pauseGame,
    resumeGame,
    resetGame,
    undoMove,
    undoSignal,
    blackClock,
    whiteClock,
    onApplyMove,
  } = props;

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

  const hasAiPlayer = useMemo(() => {
    return (
      config.blackPlayer === "Computer" || config.whitePlayer === "Computer"
    );
  }, [config]);

  const handlePlayerChange = () => {
    toggleActivePlayer();
    // Assuming activePlayer state changes, pause and resume clocks as necessary
    pauseClock(activePlayer);
    const nextPlayer = activePlayer === "black" ? "white" : "black";
    resumeClock(nextPlayer);
  };

  return (
    <>
      <GameClock
        initialTime={config?.whiteTimeLimit}
        isTurn={activePlayer === "white"}
        playerId="white"
        activePlayer={activePlayer}
        gameStarted={gameStarted}
        isActive={gameActive}
        resetClockSignal={resetClockSignal}
        undoClock={undoSignal}
        isAggregate={true}
      />
      <GameClock
        initialTime={config?.blackTimeLimit}
        isTurn={activePlayer === "black"}
        playerId="black"
        activePlayer={activePlayer}
        gameStarted={gameStarted}
        isActive={gameActive}
        resetClockSignal={resetClockSignal}
        undoClock={undoSignal}
        isAggregate={true}
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
      {hasAiPlayer && (
        <>
          {centerDivider("AI Suggested Move")}
          <Grid container spacing={1}>
            <Grid item xs={6}>
              {config.blackPlayer === "Computer" && (
                <AIMoveDisplay
                  aiMove={blackAiMove}
                  onApplyMove={onApplyMove}
                  disabled={
                    !(currentTurn === 1) ||
                    !blackAiMove ||
                    !gameActive ||
                    !gameStarted
                  }
                />
              )}
            </Grid>
            <Grid item xs={6}>
              {config.whitePlayer === "Computer" && (
                <AIMoveDisplay
                  aiMove={whiteAiMove}
                  onApplyMove={onApplyMove}
                  disabled={
                    !(currentTurn === 2) ||
                    !whiteAiMove ||
                    !gameActive ||
                    !gameStarted
                  }
                  isWhite
                />
              )}
            </Grid>
          </Grid>
        </>
      )}
      {centerDivider("Move History")}
      <MoveHistory movesStack={movesStack} />
    </>
  );
};

CurrentGameBar.propTypes = {
  config: Proptypes.object.isRequired,
  movesStack: Proptypes.array.isRequired,
  blackAiMove: Proptypes.object,
  whiteAiMove: Proptypes.object,
  currentTurn: Proptypes.number.isRequired,
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
