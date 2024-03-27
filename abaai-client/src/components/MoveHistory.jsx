import { Stack, Paper, Typography, Box, Grid } from "@mui/material";
import PropTypes from "prop-types";
import { useEffect, useRef, useState } from "react";
import Move from "../models/Move";

// Displays movement history of the GUI
const MoveHistory = ({ movesStack }) => {
  const [blackMovesStack, setBlackMovesStack] = useState([]); // The history of past moves for black player
  const [whiteMovesStack, setWhiteMovesStack] = useState([]); // The history of past moves for white player
  const stackRef = useRef(null);

  // Updates movement history when a move is made
  useEffect(() => {
    if (!movesStack) return;

    const moveStackFormatted = movesStack.map((move) => {
      return {
        player: move.player,
        transition: Move.toNotation(move),
      };
    });

    setBlackMovesStack(moveStackFormatted.filter((move) => move.player === 1));
    setWhiteMovesStack(moveStackFormatted.filter((move) => move.player === 2));
  }, [movesStack]);

  useEffect(() => {
    // Scroll to the bottom of the container when the component mounts or when its content changes
    if (stackRef.current) {
      stackRef.current.scrollTop = stackRef.current.scrollHeight;
    }
  }, [stackRef.current?.scrollHeight, movesStack]);

  // Returns UI component containing move history
  return (
    <Box sx={{ marginTop: "10px" }}>
      <Stack
        ref={stackRef}
        spacing={2}
        sx={{
          overflowY: "auto",
          maxHeight: "560px",
          "&::-webkit-scrollbar": {
            width: "5px",
          },
          "&::-webkit-scrollbar-thumb": {
            backgroundColor: "#666",
            borderRadius: "6px",
          },
          "&::-webkit-scrollbar-thumb:hover": {
            backgroundColor: "#4",
          },
        }}
      >
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
