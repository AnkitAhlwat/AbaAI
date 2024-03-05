import { Grid, Fab } from "@mui/material";
import PropTypes from "prop-types";

const Board = ({ boardArray }) => {
  // States
  // const [selectedMarble, setSelectedMarble] = useState(null);

  // Callbacks
  // const onMarbleClick = useCallback(
  //   (spot, rowIndex, columnIndex) => {
  //     // a callback function that will be called when a marble is clicked
  //     console.log("Marble clicked");
  //     console.log(spot);

  //     //check is the marble has already been selected, else select the new one
  //     if (
  //       selectedMarble &&
  //       selectedMarble.rowIndex == rowIndex &&
  //       selectedMarble.columnIndex == columnIndex
  //     ) {
  //       setSelectedMarble(null);
  //     } else {
  //       setSelectedMarble({ rowIndex, columnIndex, color: spot.marble });
  //     }
  //   },
  //   [selectedMarble]
  // );
  const getMarbleColor = (state) => {
    // a function that will return the color of the marble based on the state
    switch (state) {
      case 1:
        return "grey";
      case 2:
        return "white";
      case 0:
        return "beige";
      default:
        return "transparent";
    }
  };

  // Functions
  const renderRow = (row, rowIndex) => {
    // a function that will render a row of the board
    return (
      <Grid container item justifyContent="center" key={rowIndex}>
        {row.map((state, columnIndex) => (
          <Grid item key={`${rowIndex}-${columnIndex}`}>
            {
              <Fab
                variant="contained"
                sx={{
                  margin: "10px",
                  backgroundColor: state === -1 ? "red" : getMarbleColor(state),
                }}
              >
                {state}
              </Fab>
            }
          </Grid>
        ))}
      </Grid>
    );
  };

  // JSX
  return (
    // a grid container that will render the board by looping through all the rows in the board and rendering each row
    <Grid container direction="column" alignItems="center">
      {boardArray.map((row, index) => renderRow(row, index))}
    </Grid>
  );
};

Board.propTypes = {
  boardArray: PropTypes.array.isRequired,
};

export { Board };
