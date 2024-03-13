import { Button, Grid } from "@mui/material";
import PropTypes from "prop-types";

// Displays buttons that handle marble movement
const MoveButtons = ({ onMoveSelection, selectedMarbles }) => {

  // Table to translate movement into board
  const move_map = [
    { label: "Up-Left", move: { x: 0, y: -1 } },
    { label: "Up-Right", move: { x: 1, y: -1 } },
    { label: "Down-Left", move: { x: -1, y: 1 } },
    { label: "Down-Right", move: { x: 0, y: 1 } },
    { label: "Left", move: { x: -1, y: 0 } },
    { label: "Right", move: { x: 1, y: 0 } },
  ];

  return (
    <Grid
      container
      spacing={2}
      sx={{
        alignItems: "center",
        justifyContent: "center",
        marginTop: 2,
      }}
    >
      {move_map.map((obj) => (
        <Grid item key={obj.label}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => onMoveSelection(obj.move)}
            disabled={selectedMarbles.length === 0}
          >
            {obj.label}
          </Button>
        </Grid>
      ))}
    </Grid>
  );
};

MoveButtons.propTypes = {
  onMoveSelection: PropTypes.func.isRequired,
  selectedMarbles: PropTypes.array.isRequired,
};

export default MoveButtons;
