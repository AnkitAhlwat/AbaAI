import { Stack, Paper, Typography, Box } from "@mui/material";
import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import Space from "../models/Space";

// Displays movement history of the GUI
const MoveHistory = ({ movesStack }) => {
  const [moveStackFormatted, setMoveStackFormatted] = useState([]); // The history of past moves

  // Updates movement history when a move is made
  useEffect(() => {
    const moveStackFormatted = movesStack.map((move) => {
      const prev_moves = move.previous_positions.map((position) => {
        return Space.getCodeByPosition(position);
      });
      const next_moves = move.next_positions.map((position) => {
        return Space.getCodeByPosition(position);
      });

      return {
        player: move.player,
        transition: `${prev_moves} -> ${next_moves}`,
      };
    });

    setMoveStackFormatted(moveStackFormatted);
  }, [movesStack]);

  // Returns UI component containing move history
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Move History
      </Typography>
      <Stack spacing={2}>
        {moveStackFormatted.map((move, index) => (
          <Paper
            key={index}
            elevation={3}
            sx={{
              padding: "10px",
              border: "1px solid #ccc",
              borderRadius: "5px",
            }}
          >
            <Typography variant="subtitle1" gutterBottom>
              Player: {move.player}
            </Typography>
            <Typography variant="subtitle1" gutterBottom>
              {move.transition}
            </Typography>
          </Paper>
        ))}
      </Stack>
    </Box>
  );
};

MoveHistory.propTypes = {
  movesStack: PropTypes.array.isRequired,
};

export default MoveHistory;
