import { Button, Stack } from "@mui/material";
import PropTypes from "prop-types";

// Displays the buttons that handle start,  pause,  stop, undo and reset
// temporarily has the taketurn button for testing turn changing and delay for server behaviour 
const GameControls = ({ onTakeTurn, toggleActivePlayer, onStart, onPause, onResume, onStop, isGameActive, 
  isCurrentPlayerActive, onReset, onUndo, gameStarted, movesStack }) => {
    if (!gameStarted) {
      return (
        <Stack
        direction="row"
        spacing={2}
        justifyContent="center"
        alignItems="center"
        sx={{ marginTop: "40px" }}
      >
        <Button
          variant="contained"
          onClick={onStart}
          color="info"
        >
          Start
        </Button>
      </Stack>
      );
    }

    return (
      <Stack
        direction="column" // Stack the button groups vertically
        spacing={2} // Adjust spacing between the button groups
        justifyContent="center"
        alignItems="center"
        sx={{ marginTop: "40px" }}
      >
      <Stack
        direction="row"
        spacing={2}
        justifyContent="center"
        alignItems="center"
        sx={{ marginTop: "40px" }}
      >
        <Button
          variant="contained"
          onClick={isGameActive ? onPause : onResume}
          color="info"
        >
          {isGameActive ? "Pause" : "Resume"}
        </Button>
        <Button
          variant="contained"
          onClick={onStop}
          color="info"
        >
          Stop
        </Button>
        <Button variant="contained" 
        onClick={onReset} 
        color="info">
          Reset
        </Button>
        <Button
          variant="contained"
          onClick={onUndo}
          color="info"
        >
          Undo
        </Button>
      </Stack>
      <Button
          variant="contained"
          onClick={toggleActivePlayer}
          color="info"
        >
          Take Turn
      </Button>
      </Stack>
    );
  };

GameControls.propTypes = {
  onReset: PropTypes.func.isRequired,
  // onUndo: PropTypes.func.isRequired,
  movesStack: PropTypes.array.isRequired,
};

export default GameControls;
