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
    highlighted: {
      backgroundColor: "yellow",
      boxShadow: "none",
      flexShrink: 1,
    },
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
    flexShrink: 1,
    highlighted: {
      backgroundColor: "yellow",
      boxShadow: "none",
      flexShrink: 1,
    },
  },
};

// Displays the playing board of the GUI
const Board = ({ board, selectedMarbles, setSelectedMarbles, onMoveSelection }) => {
  // ------------------- State -------------------
  const [allPossibleMoves, setAllPossibleMoves] = useState({});
  const [validMovesForSelectedMarbles, setValidMovesForSelectedMarbles] = useState([]);


  const fetchPossibleMoves = useCallback(async () => {
    try {
      const responseData = await GameService.getPossibleMoves();
      console.log(responseData);
      setAllPossibleMoves(responseData);
    } catch (error) {
      console.error("Failed to fetch possible moves:", error);
    }
  }, [board]);

  // ------------------- Functions/Callbacks -------------------
  const convertSelectedMarblesToKey = useCallback((selectedMarbles) => {
    const marbleNotationArray = selectedMarbles
      .map((marble) => {
        return marble.str;
      })
      .sort();

    // Create the proper key
    let key = "[";
    for (let i = 0; i < marbleNotationArray.length; i++) {
      key += `'${marbleNotationArray[i]}'`;
      if (i < marbleNotationArray.length - 1) {
        key += ", ";
      }
    }
    key += "]";

    return key;
  }, []);

  const updateValidMoves = useCallback(() => {
    const key = convertSelectedMarblesToKey(selectedMarbles);
    const validMovesForSelectedMarbles = allPossibleMoves[key];
    if (validMovesForSelectedMarbles !== undefined) {
      setValidMovesForSelectedMarbles(validMovesForSelectedMarbles);
    }
    if (validMovesForSelectedMarbles === undefined) {
      setValidMovesForSelectedMarbles([]);
    }
  }, [allPossibleMoves, convertSelectedMarblesToKey, selectedMarbles]);

  const deselectMarbles = useCallback((marbles) => {
    for (const marble of marbles) {
      marble.selected = false;
    }
  }, []);

  const arraysAreEqual = (array1, array2) => {
    if (array1.length !== array2.length) {
      return false;
    }

    for (let i = 0; i < array1.length; i++) {
      if (JSON.stringify(array1[i]) !== JSON.stringify(array2[i])) {
        return false;
      }
    }

    return true;
  };

  const canSumitoOccur = useCallback((selectedMarbles) => {
    const convertedMarbles = selectedMarbles.map(marble => ({
      x: marble.position.x,
      y: marble.position.y
    })).sort((a, b) => (a.x - b.x) || (a.y - b.y))

    const matchingMove = validMovesForSelectedMarbles.find(move => {
      if (move.previous_opponent_positions.length === 0) return false;
      return arraysAreEqual(move.previous_player_positions, convertedMarbles);
    });

    if (matchingMove) {
      console.log("Sumito can occur");
      return true;
    }

    return false;

  }, []);

  // A function that will execute the move if it is valid
  const executeMoveIfValid = useCallback((clickedSpace) => {
    let moveDirection = null;
    let exactMove = null;

    if (clickedSpace.state === 1 || clickedSpace.state === 2) return false;
    if (selectedMarbles.length > 0) {
      const firstSelectedMarble = selectedMarbles[0];

      // Calculate the direction of the move
      const directionX = clickedSpace.position.x - firstSelectedMarble.position.x;
      const directionY = clickedSpace.position.y - firstSelectedMarble.position.y;

      // normalize direction to -1, 0, or 1
      moveDirection = {
        x: Math.sign(directionX),
        y: Math.sign(directionY)
      };

      // Find the exact move that matches both the direction and ends in the clicked space
      validMovesForSelectedMarbles.forEach(move => {
        move.next_player_positions.forEach(position => {
          if (position.x === clickedSpace.position.x && position.y === clickedSpace.position.y) {
            exactMove = move;
          }
        });
      });
    }

    if (exactMove && selectedMarbles.length > 0) {
      const move = {
        from: selectedMarbles.map(marble => ({ x: marble.position.x, y: marble.position.y })),
        to: exactMove.next_player_positions.map(position => ({ x: position.x, y: position.y }))
      };
      onMoveSelection(move);
      return true;
    }

    return false;
  }, [validMovesForSelectedMarbles, selectedMarbles, onMoveSelection]);


  const onMarbleClick = useCallback(
    (space) => {
      let newSelectedMarbles = [];
      // Early return if the space is empty or the move is valid.
      if (space.state === SpaceStates.EMPTY || executeMoveIfValid(space)) {
        executeMoveIfValid(space);
      }

      // Deselect if the same marble is clicked again.
      if (selectedMarbles.includes(space)) {
        deselectMarbles([space]);
        setSelectedMarbles(selectedMarbles.filter(marble => marble !== space));
        return;
      }

      // Handle marble selection logic.
      if (selectedMarbles.length < 3) {
        const lastSelectedMarble = selectedMarbles[selectedMarbles.length - 1];
        // If adjacent or in a straight line, select the current marble.
        if (!lastSelectedMarble || lastSelectedMarble.isAdjacentTo(space) ||
          (selectedMarbles.length === 2 && Space.areInStraightLine(selectedMarbles[0], selectedMarbles[1], space))) {
          space.selected = true;
          newSelectedMarbles = [...selectedMarbles, space];
          setSelectedMarbles(newSelectedMarbles);
        } else { // Otherwise, deselect all and select the current marble.
          deselectMarbles(selectedMarbles);
          space.selected = true;
          newSelectedMarbles = [space];
          setSelectedMarbles(newSelectedMarbles);
        }
      } else { // If more than two marbles are already selected, reset and select the current one.
        deselectMarbles(selectedMarbles);
        space.selected = true;
        newSelectedMarbles = [space];
        setSelectedMarbles(newSelectedMarbles);
      }
      canSumitoOccur(newSelectedMarbles);
    },
    [executeMoveIfValid, selectedMarbles, setSelectedMarbles, deselectMarbles]
  );


  // A function that will return the color of the marble based on the state
  const getSpaceStyle = useCallback((space) => {
    if (space.selected) {
      return marbleStyles.selected;
    }
    return marbleStyles[space.state];
  }, []);

  // ------------------- Effects -------------------
  useEffect(() => {
    updateValidMoves();
  }, [updateValidMoves]);

  useEffect(() => {
    fetchPossibleMoves();
  }, [fetchPossibleMoves]);

  useEffect(() => {
    const clearHighlight = () => {
      for (let row of board) {
        for (let space of row) {
          if (space.state === 3) {
            space.state = 0;
          }
        }
      }
    };
    clearHighlight();
  }, [validMovesForSelectedMarbles, onMarbleClick]);

  // ------------------- Render -------------------
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
    [getSpaceStyle, onMarbleClick]
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

        {validMovesForSelectedMarbles.map((move) => {
          move.next_player_positions.map((space) => {
            if (board[space.y][space.x].state !== 1 && board[space.y][space.x].state !== 2)
              board[space.y][space.x].state = 3;
          })
        }
        )}

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
