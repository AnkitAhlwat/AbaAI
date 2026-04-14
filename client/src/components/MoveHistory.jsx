import { Stack, Paper, Typography, Box, Grid } from "@mui/material";
import { useEffect, useRef } from "react";

const formatMove = (move) => {
  const from = (move.from || []).join(",");
  const to = (move.to || []).join(",");
  const pushed = move.pushed ? ` (push ${move.pushed.join(",")})` : "";
  return `${from} → ${to}${pushed}`;
};

const MoveHistory = ({ movesStack }) => {
  const stackRef = useRef(null);

  useEffect(() => {
    if (stackRef.current) {
      stackRef.current.scrollTop = stackRef.current.scrollHeight;
    }
  }, [movesStack]);

  if (!movesStack || movesStack.length === 0) {
    return (
      <Box sx={{ mt: 2, textAlign: "center" }}>
        <Typography sx={{ color: "rgba(255,255,255,0.4)", fontSize: "0.85rem" }}>
          No moves yet
        </Typography>
      </Box>
    );
  }

  const blackMoves = movesStack.filter((_, i) => i % 2 === 0);
  const whiteMoves = movesStack.filter((_, i) => i % 2 === 1);

  return (
    <Box sx={{ mt: 1 }}>
      <Typography sx={{ color: "rgba(255,255,255,0.6)", fontSize: "0.85rem", mb: 1, fontWeight: 600 }}>
        Move History
      </Typography>
      <Stack
        ref={stackRef}
        spacing={0.5}
        sx={{
          overflowY: "auto",
          maxHeight: "50vh",
          "&::-webkit-scrollbar": { width: "5px" },
          "&::-webkit-scrollbar-thumb": { backgroundColor: "#666", borderRadius: "6px" },
        }}
      >
        <Grid container>
          <Grid item xs={6}>
            {blackMoves.map((move, index) => (
              <Paper
                key={index}
                elevation={2}
                sx={{
                  padding: "3px",
                  margin: "2px",
                  borderRadius: "5px",
                  textAlign: "center",
                  backgroundColor: "#302e2b",
                  color: "#989795",
                }}
              >
                <Typography variant="subtitle2">{formatMove(move)}</Typography>
              </Paper>
            ))}
          </Grid>
          <Grid item xs={6}>
            {whiteMoves.map((move, index) => (
              <Paper
                key={index}
                elevation={2}
                sx={{
                  padding: "3px",
                  margin: "2px",
                  borderRadius: "5px",
                  textAlign: "center",
                  backgroundColor: "#989795",
                  color: "#484744",
                }}
              >
                <Typography variant="subtitle2">{formatMove(move)}</Typography>
              </Paper>
            ))}
          </Grid>
        </Grid>
      </Stack>
    </Box>
  );
};

export default MoveHistory;
