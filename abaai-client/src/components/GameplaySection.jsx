import { Grid } from "@mui/material";
import PlayerInfo from "./PlayerInfo";
import { Board } from "./Board";
import Proptypes from "prop-types";

const GameplaySection = (props) => {
  const { board, onMoveSelection, selectedMarbles, setSelectedMarbles } = props;

  return (
    <Grid container>
      <Grid item xs={12}>
        <PlayerInfo
          isBot
          color="white"
          numCapturedMarbles={5}
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
          board={board}
          onMoveSelection={onMoveSelection}
          selectedMarbles={selectedMarbles}
          setSelectedMarbles={setSelectedMarbles}
        />
      </Grid>
      <Grid item xs={12}>
        <PlayerInfo
          color="black"
          numCapturedMarbles={2}
          movesRemaining={18}
          moveTimeRemaining={20}
        />
      </Grid>
    </Grid>
  );
};

GameplaySection.propTypes = {
  board: Proptypes.array.isRequired,
  onMoveSelection: Proptypes.func.isRequired,
  selectedMarbles: Proptypes.array.isRequired,
  setSelectedMarbles: Proptypes.func.isRequired,
};

export default GameplaySection;
