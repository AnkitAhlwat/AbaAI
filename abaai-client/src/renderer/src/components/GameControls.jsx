import { Button, Stack } from "@mui/material";
import PropTypes from "prop-types";

const GameControls = ({ onReset, onUndo, movesStack }) => {
  return (
    <Stack
      direction="row"
      spacing={2}
      justifyContent="center"
      alignItems="center"
      sx={{ marginTop: "40px" }}
    >
      <Button variant="contained" onClick={onReset} color="warning">
        Reset
      </Button>
      <Button
        variant="contained"
        onClick={onUndo}
        color="info"
        disabled={movesStack.length === 0}
      >
        Undo
      </Button>
    </Stack>
  );
};

GameControls.propTypes = {
  onReset: PropTypes.func.isRequired,
  onUndo: PropTypes.func.isRequired,
  movesStack: PropTypes.array.isRequired,
};

export default GameControls;
