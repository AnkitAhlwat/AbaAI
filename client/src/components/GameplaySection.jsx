import { Grid, Typography, Box } from "@mui/material";
import { Board } from "./Board";

const GameplaySection = ({
  boardArray,
  onMoveSelection,
  selectedMarbles,
  setSelectedMarbles,
  isGameActive,
  currentTurn,
  legalMoves,
  numCapturedBlackMarbles,
  numCapturedWhiteMarbles,
}) => {
  return (
    <Grid container>
      <Grid item xs={12}>
        <Box sx={{ display: "flex", justifyContent: "space-between", px: 2, py: 1 }}>
          <Typography sx={{ color: "white", fontWeight: 600 }}>
            White &mdash; Captured: {numCapturedWhiteMarbles}
          </Typography>
        </Box>
      </Grid>
      <Grid item xs={12} sx={{ my: 1 }}>
        <Board
          boardArray={boardArray}
          onMoveSelection={onMoveSelection}
          selectedMarbles={selectedMarbles}
          setSelectedMarbles={setSelectedMarbles}
          isGameActive={isGameActive}
          currentTurn={currentTurn}
          legalMoves={legalMoves}
        />
      </Grid>
      <Grid item xs={12}>
        <Box sx={{ display: "flex", justifyContent: "space-between", px: 2, py: 1 }}>
          <Typography sx={{ color: "white", fontWeight: 600 }}>
            Black &mdash; Captured: {numCapturedBlackMarbles}
          </Typography>
        </Box>
      </Grid>
    </Grid>
  );
};

export default GameplaySection;
