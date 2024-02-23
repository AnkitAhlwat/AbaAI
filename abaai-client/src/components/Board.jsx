import { Grid, Paper } from "@mui/material";
import { useBoardPositions } from "../hooks/useBoardPositions";
import { useBoard } from "../hooks/useBoard";

const Board = () => {
  // States

  // Hooks
  const { useDefaultBoardPosition } = useBoardPositions();
  const { board, setBoard } = useBoard();
  useDefaultBoardPosition(board);

  const renderRow = (row, rowIndex) => {
    return (
      <Grid container item justifyContent="center" key={rowIndex}>
        {row.map((spot, columnIndex) => (
          <Grid item key={`${rowIndex}-${columnIndex}`}>
            <Paper
              sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                width: "40px",
                height: "40px",
                borderRadius: "50%",
                margin: "4px",
                backgroundColor: spot.marble, // You can change the background color here
              }}
              elevation={3}
            >
              {`${spot.row}${spot.column}`}
            </Paper>
          </Grid>
        ))}
      </Grid>
    );
  };

  return (
    <Grid container direction="column" alignItems="center">
      {board
        .slice()
        .reverse()
        .map((row, index) => renderRow(row, index))}
    </Grid>
  );
};

export { Board };
