import { Grid } from "@mui/material";
import PlayerInfo from "./PlayerInfo";
import { Board } from "./Board";
import Proptypes from "prop-types";

const GameplaySection = (props) => {
  const {
    boardArray,
    onMoveSelection,
    selectedMarbles,
    setSelectedMarbles,
    numCapturedBlackMarbles,
    numCapturedWhiteMarbles,
    isGameActive,
    currentTurn,
    blackMovetimeRemaining,
    whiteMovetimeRemaining,
    blackMovesRemaining,
    whiteMovesRemaining,
    //clock controls
    activePlayer,
    toggleActivePlayer,
    gameStarted,
    startGame,
    stopGame,
    resetClockSignal,
    pauseGame,
    resumeGame,
    resetGame,
    undoMove,
    blackClock,
    whiteClock,
    updateGame,
    onApplyMove,
    config
    // onSubmitConfig
  } = props;


  return (
    <Grid container>
      <Grid item xs={12}>
        <PlayerInfo
          isBot
          color="white"
          numCapturedMarbles={numCapturedBlackMarbles}
          movesRemaining={whiteMovesRemaining}
          moveTimeRemaining={whiteMovetimeRemaining}
          //clock controls
          activePlayer={activePlayer}
          toggleActivePlayer={toggleActivePlayer}
          gameStarted={gameStarted}
          isGameActive={isGameActive}
          startGame={startGame}
          stopGame={stopGame}
          resetClockSignal={resetClockSignal}
          pauseGame={pauseGame}
          resumeGame={resumeGame}
          resetGame={resetGame}
          undoMove={undoMove}
          // blackClock={blackClock}
          thisClock={config?.whiteTurnTime}
          onApplyMove={onApplyMove}
          //onSubmitConfig={onSubmitConfig}
        />
      </Grid>
      <Grid
        item
        xs={12}
        sx={{
          marginTop: "10px",
          marginBottom: "10px",
        }}
      >
        <Board
          boardArray={boardArray}
          onMoveSelection={onMoveSelection}
          selectedMarbles={selectedMarbles}
          setSelectedMarbles={setSelectedMarbles}
          isGameActive={isGameActive}
          currentTurn={currentTurn}
        />
      </Grid>
      <Grid item xs={12}>
        <PlayerInfo
          color="black"
          numCapturedMarbles={numCapturedWhiteMarbles}
          movesRemaining={blackMovesRemaining}
          moveTimeRemaining={blackMovetimeRemaining}
          //clock controls
          activePlayer={activePlayer}
          toggleActivePlayer={toggleActivePlayer}
          gameStarted={gameStarted}
          isGameActive={isGameActive}
          startGame={startGame}
          stopGame={stopGame}
          resetClockSignal={resetClockSignal}
          pauseGame={pauseGame}
          resumeGame={resumeGame}
          resetGame={resetGame}
          undoMove={undoMove}
          thisClock={config?.blackTurnTime}
          onApplyMove={onApplyMove}
          //onSubmitConfig={onSubmitConfig}
        />
      </Grid>
    </Grid>
  );
};

GameplaySection.propTypes = {
  boardArray: Proptypes.array.isRequired,
  onMoveSelection: Proptypes.func.isRequired,
  selectedMarbles: Proptypes.array.isRequired,
  setSelectedMarbles: Proptypes.func.isRequired,
  numCapturedBlackMarbles: Proptypes.number.isRequired,
  numCapturedWhiteMarbles: Proptypes.number.isRequired,
  isGameActive: Proptypes.bool.isRequired,
  currentTurn: Proptypes.number.isRequired,
  blackMovetimeRemaining: Proptypes.number.isRequired,
  whiteMovetimeRemaining: Proptypes.number.isRequired,
  blackMovesRemaining: Proptypes.number.isRequired,
  whiteMovesRemaining: Proptypes.number.isRequired,
};

export default GameplaySection;
