import { Grid, Fab } from "@mui/material";
import { useBoardPositions } from "../hooks/useBoardPositions";
import { useBoard } from "../hooks/useBoard";
import { Marbles } from "../constants/marbles";
import { useCallback, useEffect, useState } from "react";

const Board = () => {
  // States
  const [startPositionSet, setStartPositionSet] = useState(false);
  const [selectedMarble, setSelectedMarble] = useState(null);

  // Hooks
  const { setDefaultPosition, setBelgianDaisyPosition, setGermanDaisyPosition } = useBoardPositions(); // import board position functions from useBoardPositions hook
  const { board, setBoard } = useBoard(); // import board state and setBoard function from useBoard hook

  // Effects
  useEffect(() => {
    // if the board is not set, set the board position to the default position
    if (!startPositionSet) {
      setBelgianDaisyPosition(board);
      setStartPositionSet(true);
    }
  }, [board, startPositionSet, setDefaultPosition]); // when the dependencies in this array change the effect will run again

  // Callbacks
  const onMarbleClick = useCallback((spot, rowIndex, columnIndex) => {
    // a callback function that will be called when a marble is clicked
    console.log("Marble clicked");
    console.log(spot);
    
    //check is the marble has already been selected, else select the new one
    if (selectedMarble && selectedMarble.rowIndex == rowIndex && selectedMarble.columnIndex == columnIndex){
      setSelectedMarble(null);
    } else {
      setSelectedMarble({rowIndex, columnIndex, color: spot.marble})
    }
  }, [selectedMarble]);

  const onEmptySpotClick = useCallback((spot, rowIndex, columnIndex) => {
    // a callback function that will be called when an empty spot is clicked
    console.log("Empty spot clicked");
    console.log(spot);

    if (selectedMarble){
      setBoard((prevBoard) => {
        const newBoard = prevBoard.map(row => row.map(spot => ({ ...spot })));
        newBoard[selectedMarble.rowIndex][selectedMarble.columnIndex].marble = Marbles.EMPTY;
        newBoard[rowIndex][columnIndex].marble = selectedMarble.color;
        return newBoard;
      });
      setSelectedMarble(null);
    } 
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