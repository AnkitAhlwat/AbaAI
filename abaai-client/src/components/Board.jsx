import { Grid, Fab } from "@mui/material";
import PropTypes from "prop-types";
import SpaceStates from "../constants/spaceStates";
import { useEffect } from "react";
import { useState, useCallback } from "react";
import Space from "../models/Space";

const Board = ({ board }) => {
  // States
  const [selectedMarbles, setSelectedMarbles] = useState([]);

  // Callbacks
  const onMarbleClick = useCallback(
    (space) => {
      // a function that will handle the click event of a marble
      if (space.state === SpaceStates.EMPTY) {
        return;
      }

      // if the marble is already selected, deselect it
      if (selectedMarbles.includes(space)) {
        space.selected = false;
        const updatedSelectedMarbles = selectedMarbles.filter(
          (selectedMarble) => selectedMarble !== space
        );
        setSelectedMarbles(updatedSelectedMarbles);
        return;
      }

      if (selectedMarbles.length === 0) {
        space.selected = true;
        setSelectedMarbles([space]);
      } else if (selectedMarbles.length === 1) {
        // if the marble is not adjacent to the either of the selected marbles, return
        const isAdjacent = selectedMarbles.some((selectedMarble) =>
          selectedMarble.isAdjacentTo(space)
        );
        if (!isAdjacent) {
          return;
        }

        space.selected = true;
        setSelectedMarbles([...selectedMarbles, space]);
      } else if (selectedMarbles.length === 2) {
        // if the marble is not in line with the selected marbles, return
        const areInStraightLine = Space.areInStraightLine(
          selectedMarbles[0],
          selectedMarbles[1],
          space
        );
        if (!areInStraightLine) {
          return;
        }

        space.selected = true;
        setSelectedMarbles([...selectedMarbles, space]);
      } else if (selectedMarbles.length >= 3) {
        // if there are already 3 marbles selected, deselect all the marbles and select the current marble
        for (const marble of selectedMarbles) {
          marble.selected = false;
        }
        space.selected = true;
        setSelectedMarbles([space]);
      }

      console.log(space);
      console.log(selectedMarbles);
    },
    [selectedMarbles, setSelectedMarbles]
  );

  const getSpaceColor = useCallback(
    (space) => {
      if (space.selected) {
        return "green";
      }
      // a function that will return the color of the marble based on the state
      switch (space.state) {
        case SpaceStates.BLACK:
          return "grey";
        case SpaceStates.WHITE:
          return "white";
        case SpaceStates.EMPTY:
          return "beige";
        case SpaceStates.NONE:
          return "red";
        default:
          return "transparent";
      }
    },
    [selectedMarbles]
  );

  // Functions
  const renderRow = useCallback(
    (row, rowIndex) => {
      // a function that will render a row of the board
      return (
        <Grid container item justifyContent="center" key={rowIndex}>
          {row.map((space, columnIndex) => (
            <Grid item key={`${rowIndex}-${columnIndex}`}>
              {space.state !== SpaceStates.NONE && (
                <Fab
                  variant="contained"
                  sx={{
                    margin: "10px",
                    backgroundColor: getSpaceColor(space),
                  }}
                  onClick={() => onMarbleClick(space)}
                >
                  {space.str}
                </Fab>
              )}
            </Grid>
          ))}
        </Grid>
      );
    },
    [getSpaceColor, onMarbleClick]
  );

  // JSX
  return (
    // a grid container that will render the board by looping through all the rows in the board and rendering each row
    <Grid container direction="column" alignItems="center">
      {board.map((row, index) => renderRow(row, index))}
    </Grid>
  );
};

Board.propTypes = {
  board: PropTypes.array.isRequired,
};

export { Board };
