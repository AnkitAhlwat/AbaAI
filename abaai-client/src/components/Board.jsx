import { Grid, Fab, Box } from "@mui/material";
import PropTypes from "prop-types";
import SpaceStates from "../constants/spaceStates";
import { useCallback, useState, useEffect } from "react";
import Space from "../models/Space";
import GameService from "../services/game.service";

const marbleStyles = {
  // Black marble
  1: {
    backgroundColor: "black",
    color: "white",
    outline: "solid 2px black",
    boxShadow: "none",
    "&:hover": {
      backgroundColor: "#767271", // Change hover color
    },
    flexShrink: 1,
  },
  // White marble
  2: {
    backgroundColor: "white",
    color: "black",
    outline: "solid 2px black",
    boxShadow: "none",
    "&:hover": {
      backgroundColor: "#767271", // Change hover color
    },
    flexShrink: 1,
  },
  // Empty space
  0: {
    backgroundColor: "#ae694a",
    boxShadow: "none",
    flexShrink: 1,
  },
  selected: {
    backgroundColor: "rgba(115,149,82,255)",
    boxShadow: "none",
    outline: "solid 2px black",
    flexShrink: 1,
    "&:hover": {
      backgroundColor: "rgba(130,180,100,255)", // Change hover color
    },
  },
  // Possible moves
  3: {
    backgroundColor: "yellow",
    boxShadow: "none",
    outline: "solid 2px black",
    flexShrink: 1,
  },

};

// Displays the playing board of the GUI
const Board = ({ board, selectedMarbles, setSelectedMarbles }) => {
  const [possibleMoves, setPossibleMoves] = useState({});
  const [validMoves, setValidMoves] = useState([]);

  const fetchPossibleMoves = useCallback(async () => {
    try {
      const responseData = await GameService.getPossibleMoves();
      console.log(responseData);
      setPossibleMoves(responseData);
    } catch (error) {
      console.error("Failed to fetch possible moves:", error);
    }
  }, []);

  useEffect(() => {
    fetchPossibleMoves();
  }, [fetchPossibleMoves])

  useEffect(() => {
    const updateHighlightedMoves = () => {
      let marbleKey = [];
      let turn = "black"
      selectedMarbles.forEach(marble => {
        marbleKey.push([marble.position.x, marble.position.y]);
      });
      const sortedMarbleKey = marbleKey.sort();
      let myString = "[";
      sortedMarbleKey.forEach(marble => {
        myString += `'${marble[0]},${marble[1]}', `;
      });
      myString = myString.slice(0, -2);
      myString += "]";
      if (selectedMarbles[0].state == 2) {
        turn = "white";
      }
      if (possibleMoves[turn][myString] !== undefined) {
        setValidMoves(possibleMoves[turn][myString]);
        console.log(validMoves);
        console.log(possibleMoves[turn][myString]);
        possibleMoves[turn][myString].forEach(move => {
          if (move[0]) {
            move = move[0];
          }
          let state = board[move.y][move.x];
          state.state = 3;
        });

      }
    };

    // Call the update function if there are selected marbles
    if (selectedMarbles.length > 0) {
      updateHighlightedMoves();
    }
  }, [possibleMoves, selectedMarbles]);
  // Callback when a marble is deselected
  const deselectMarbles = useCallback((marbles) => {
    for (const marble of marbles) {
      marble.selected = false;
    }
  }, []);

  const onMarbleClick = useCallback(
    (space) => {
      // If the space is empty or the space is already selected, return
      if (space.state === SpaceStates.EMPTY) return;

      // If there are no selected marbles, select the current marble
      if (selectedMarbles.length === 0) {
        space.selected = true;
        setSelectedMarbles([space]);
      }

      // If there is one selected marble, select the current marble if it is adjacent to the selected marble
      // Otherwise selected the current marble and deselect the previous marble
      else if (selectedMarbles.length === 1) {
        setSelectedMarbles((previousSelectedMarbles) => {
          if (
            previousSelectedMarbles[0].isAdjacentTo(space) &&
            !space.selected &&
            space.state === previousSelectedMarbles[0].state
          ) {
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

      // If there are two selected marbles, select the current marble if it is in a straight line with the selected marbles
      // Otherwise deselect all the marbles and select the current marble
      else if (selectedMarbles.length === 2) {
        setSelectedMarbles((previousSelectedMarbles) => {
          if (
            Space.areInStraightLine(
              previousSelectedMarbles[0],
              previousSelectedMarbles[1],
              space
            ) &&
            !space.selected &&
            space.state === previousSelectedMarbles[0].state
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

      // If the marble is already selected or there are more than two selected marbles, deselect all the marbles and select the current marble
      else if (selectedMarbles.includes(space) || selectedMarbles.length >= 3) {
        deselectMarbles(selectedMarbles);
        setSelectedMarbles([space]);
        space.selected = true;
      }
    },
    [deselectMarbles, selectedMarbles, setSelectedMarbles]
  );

  // A function that will return the color of the marble based on the state
  const getSpaceStyle = useCallback((space) => {
    if (space.selected) {
      return marbleStyles.selected;
    } else if (space.highlighted) {
      return marbleStyles.possibleMoves;
    }

    return marbleStyles[space.state];
  }, []);

  const renderMarble = useCallback(
    (space) => {
      return (
        <Fab
          variant="contained"
          sx={{
            ...getSpaceStyle(space),
            margin: "5px",
            width: "80px",
            height: "80px",
          }}
          onClick={() => onMarbleClick(space)}
        >
          {space.str}
        </Fab>
      );
    },
    [getSpaceStyle, onMarbleClick, validMoves]
  );

  // A function that will render a row of the board
  const renderRow = useCallback(
    (row, rowIndex) => {
      return (
        <Grid
          container
          item
          justifyContent="center"
          key={rowIndex}
          sx={{
            flexShrink: 1,
            flexWrap: "nowrap",
          }}
        >
          {row.map((space, columnIndex) => (
            <Grid
              item
              key={`${rowIndex}-${columnIndex}`}
              sx={{
                flexShrink: 1,
                flexWrap: "nowrap",
              }}
            >
              {space.state !== SpaceStates.NONE && renderMarble(space)}
            </Grid>
          ))}
        </Grid>
      );
    },
    [renderMarble]
  );

  // Return a grid that will render the board by looping through all the rows in the board and rendering each row
  return (
    <>
      <Box
        sx={{
          backgroundColor: "#6f2404",
          borderRadius: "5px",
          padding: "20px",
          flexShrink: 1,
        }}
      >
        {board.map((row, index) => renderRow(row, index))}
      </Box>
    </>
  );
};

Board.propTypes = {
  board: PropTypes.array.isRequired,
  onMoveSelection: PropTypes.func.isRequired,
  selectedMarbles: PropTypes.array.isRequired,
  setSelectedMarbles: PropTypes.func.isRequired,
};

export { Board };
