import { Stack, Paper, Typography, Box } from "@mui/material";
import PropTypes from "prop-types";

const MoveHistory = ({ movesStack }) => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Move Stack
      </Typography>
      <Stack
        spacing={2}
        sx={{
          border: "1px solid #ccc",
        }}
      >
        {movesStack.map((move, index) => (
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
              Previous Position: {move.previousPosition}
            </Typography>
            <Typography variant="subtitle1" gutterBottom>
              New Position: {move.newPosition}
            </Typography>
            <Typography variant="subtitle1" gutterBottom>
              Player: {move.player}
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
