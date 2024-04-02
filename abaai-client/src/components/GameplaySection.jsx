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
