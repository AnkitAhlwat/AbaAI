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
  } = props;

  return (
    <Grid container>
      <Grid item xs={12}>
        <PlayerInfo
          isBot
          color="white"
          numCapturedMarbles={numCapturedBlackMarbles}
          // movesRemaining={19}
          moveTimeRemaining={20}
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
          movesRemaining={18}
          moveTimeRemaining={20}
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
};

export default GameplaySection;
