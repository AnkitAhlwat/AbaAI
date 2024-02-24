import { Grid, Fab } from "@mui/material";
import { useBoardPositions } from "../hooks/useBoardPositions";
import { useBoard } from "../hooks/useBoard";
import { Marbles } from "../constants/marbles";
import { useCallback, useEffect, useState } from "react";

const Board = () => {
  // States
  const [startPositionSet, setStartPositionSet] = useState(false);

  // Hooks
  const { setDefaultBoardPosition } = useBoardPositions(); // import setDefaultBoardPosition function from useBoardPositions hook
  const { board, setBoard } = useBoard(); // import board state and setBoard function from useBoard hook

  // Effects
  useEffect(() => {
    // if the board is not set, set the board position to the default position
    if (!startPositionSet) {
      setDefaultBoardPosition(board);
      setStartPositionSet(true);
    }
  }, [board, startPositionSet, setDefaultBoardPosition]); // when the dependencies in this array change the effect will run again

  // Callbacks
  const onMarbleClick = useCallback((spot, rowIndex, columnIndex) => {
    // a callback function that will be called when a marble is clicked
    console.log("Marble clicked");
    console.log(spot);
  });

  const onEmptySpotClick = useCallback((spot, rowIndex, columnIndex) => {
    // a callback function that will be called when an empty spot is clicked
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
    // a function that will render a row of the board
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
    // a grid container that will render the board by looping through all the rows in the board and rendering each row
    <Grid container direction="column" alignItems="center">
      {board.map((row, index) => renderRow(row, index))}
    </Grid>
  );
};

export { Board };
