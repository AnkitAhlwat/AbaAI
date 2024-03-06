import { Grid, Fab } from "@mui/material";
import PropTypes from "prop-types";
import SpaceStates from "../constants/spaceStates";
import { useState, useCallback } from "react";
import Space from "../models/Space";

const Board = ({ board }) => {
  // States
  const [selectedMarbles, setSelectedMarbles] = useState([]);

  const deselectMarbles = useCallback((marbles) => {
    for (const marble of marbles) {
      marble.selected = false;
    }
  }, []);

  const onMarbleClick = useCallback(
    (space) => {
      // if the space is empty or the space is already selected, return
      if (space.state === SpaceStates.EMPTY) {
        return;
      }

      // if there are no selected marbles, select the current marble
      if (selectedMarbles.length === 0) {
        space.selected = true;
        setSelectedMarbles([space]);
      }
      // if there is one selected marble, select the current marble if it is adjacent to the selected marble
      // otherwise selected the current marble and deselect the previous marble
      else if (selectedMarbles.length === 1) {
        setSelectedMarbles((previousSelectedMarbles) => {
          if (previousSelectedMarbles[0].isAdjacentTo(space)) {
            space.selected = true;
            return [...previousSelectedMarbles, space];
          } else if (previousSelectedMarbles[0] === space) {
            space.selected = false;
            return [];
          } else {
            deselectMarbles(previousSelectedMarbles);
            space.selected = true;
            return [space];
          }
        });
      }
      // if there are two selected marbles, select the current marble if it is in a straight line with the selected marbles
      // otherwise deselect all the marbles and select the current marble
      else if (selectedMarbles.length === 2) {
        setSelectedMarbles((previousSelectedMarbles) => {
          if (
            Space.areInStraightLine(
              previousSelectedMarbles[0],
              previousSelectedMarbles[1],
              space
            )
          ) {
            space.selected = true;
            return [...previousSelectedMarbles, space];
          } else {
            deselectMarbles(previousSelectedMarbles);
            space.selected = true;
            return [space];
          }
        });
      }
      // if the marble is already selected or there are more than two selected marbles, deselect all the marbles and select the current marble
      else if (selectedMarbles.includes(space) || selectedMarbles.length >= 3) {
        deselectMarbles(selectedMarbles);
        setSelectedMarbles([space]);
        space.selected = true;
      }
    },
    [deselectMarbles, selectedMarbles]
  );

  const onEmptySpaceClick = useCallback(
    (emptySpace) => {
      // if there are no selected marbles, return
      if (selectedMarbles.length === 0) {
        return;
      }

      // check if the empty space is adjacent to any of the selected marbles
      const isAdjacentToSelectedMarble = selectedMarbles.some((marble) =>
        marble.isAdjacentTo(emptySpace)
      );
      if (!isAdjacentToSelectedMarble) {
        return;
      }

      // if there is one selected marble, move the marble to the empty space
      if (selectedMarbles.length === 1) {
        const marble = selectedMarbles[0];
        marble.state = SpaceStates.EMPTY;
        emptySpace.state = marble.state;
      }

      //
    },
    [selectedMarbles]
  );

  const onSpaceClick = useCallback(
    (space) => {
      if (space.state === SpaceStates.EMPTY) {
        onEmptySpaceClick(space);
      } else {
        onMarbleClick(space);
      }
    },
    [onEmptySpaceClick, onMarbleClick]
  );

  const getSpaceColor = useCallback((space) => {
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
  }, []);

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
                  onClick={() => onSpaceClick(space)}
                >
                  {space.str}
                </Fab>
              )}
            </Grid>
          ))}
        </Grid>
      );
    },
    [getSpaceColor, onSpaceClick]
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
