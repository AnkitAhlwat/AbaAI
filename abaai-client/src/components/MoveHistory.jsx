import { Stack, Paper, Typography, Box, Grid } from "@mui/material";
import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import Space from "../models/Space";

// Displays movement history of the GUI
const MoveHistory = ({ movesStack }) => {
  const [blackMovesStack, setBlackMovesStack] = useState([]); // The history of past moves for black player
  const [whiteMovesStack, setWhiteMovesStack] = useState([]); // The history of past moves for white player

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

    setBlackMovesStack(moveStackFormatted.filter((move) => move.player === 1));
    setWhiteMovesStack(moveStackFormatted.filter((move) => move.player === 2));
  }, [movesStack]);

  // Returns UI component containing move history
  return (
    <Box sx={{ marginTop: "10px" }}>
      <Stack spacing={2}>
        <Grid container>
          <Grid item xs={6}>
            {blackMovesStack.map((move, index) => (
              <Paper
                key={index}
                elevation={3}
                sx={{
                  padding: "3px",
                  margin: "2px",
                  borderRadius: "5px",
                  textAlign: "center",
                  backgroundColor: "#302e2b",
                  color: "#989795",
                }}
              >
                <Typography variant="subtitle2">{move.transition}</Typography>
              </Paper>
            ))}
          </Grid>
          <Grid item xs={6}>
            {whiteMovesStack.map((move, index) => (
              <Paper
                key={index}
                elevation={3}
                sx={{
                  padding: "3px",
                  margin: "2px",
                  borderRadius: "5px",
                  textAlign: "center",
                  backgroundColor: "#989795",
                  color: "#484744",
                }}
              >
                <Typography variant="subtitle2">{move.transition}</Typography>
              </Paper>
            ))}
          </Grid>
        </Grid>
      </Stack>
    </Box>
  );
};

MoveHistory.propTypes = {
  movesStack: PropTypes.array.isRequired,
};

export default MoveHistory;
