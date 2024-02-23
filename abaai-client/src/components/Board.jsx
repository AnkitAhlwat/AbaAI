import { Grid, Fab } from "@mui/material";
import { useBoardPositions } from "../hooks/useBoardPositions";
import { useBoard } from "../hooks/useBoard";
import { Marbles } from "../constants/marbles";
import { useCallback, useEffect, useState } from "react";

const Board = () => {
  // States
  const [startPositionSet, setStartPositionSet] = useState(false);

  // Hooks
  const { setDefaultBoardPosition } = useBoardPositions();
  const { board, setBoard } = useBoard();

  // Effects
  useEffect(() => {
    if (!startPositionSet) {
      setDefaultBoardPosition(board);
      setStartPositionSet(true);
    }
  }, [board, startPositionSet, setDefaultBoardPosition]);

  // Callbacks
  const onMarbleClick = useCallback((spot, rowIndex, columnIndex) => {
    console.log("Marble clicked");
    console.log(spot);
  });

  const onEmptySpotClick = useCallback((spot, rowIndex, columnIndex) => {
    setBoard((prevBoard) => {
      const newBoard = prevBoard.slice();
      newBoard[rowIndex][columnIndex].marble = "#00ee00";
      return newBoard;
    });
    console.log("Empty spot clicked");
    console.log(spot);
  });

  // Functions
  const renderRow = (row, rowIndex) => {
    return (
      <Grid container item justifyContent="center" key={rowIndex}>
        {row.map((spot, columnIndex) => (
          <Grid item key={`${rowIndex}-${columnIndex}`}>
            <Fab
              variant="contained"
              sx={{
                margin: "10px",
                backgroundColor: spot.marble,
              }}
              onClick={() => {
                if (spot.marble === Marbles.EMPTY) {
                  onEmptySpotClick(spot, rowIndex, columnIndex);
                } else {
                  onMarbleClick(spot, rowIndex, columnIndex);
                }
              }}
            >
              {`${spot.rowLetter}${spot.columnNumber}`}
            </Fab>
          </Grid>
        ))}
      </Grid>
    );
  };

  // JSX
  return (
    <Grid container direction="column" alignItems="center">
      {board.map((row, index) => renderRow(row, index))}
    </Grid>
  );
};

export { Board };
