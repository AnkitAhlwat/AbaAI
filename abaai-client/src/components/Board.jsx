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
    outline: "solid 2px white",
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
    "&:hover": {
      backgroundColor: "#767271", // Change hover color
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
  4: {
    backgroundColor: "red",
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
const Board = ({
  boardArray,
  selectedMarbles,
  setSelectedMarbles,
  onMoveSelection,
  isGameActive,
  currentTurn,
}) => {
  // ------------------- State -------------------
  const [allPossibleMoves, setAllPossibleMoves] = useState({});
  const [validMovesForSelectedMarbles, setValidMovesForSelectedMarbles] =
    useState([]);
  const [board, setBoard] = useState([]);

  // ------------------- Functions/Callbacks -------------------
  const generateBoard = useCallback(() => {
    const newBoard = boardArray.map((row, rowIndex) => {
      return row.map((state, columnIndex) => {
        return new Space(state, { y: rowIndex, x: columnIndex });
      });
    });
    setBoard(newBoard);
  }, [boardArray]);

  const fetchPossibleMoves = useCallback(async () => {
    try {
      const responseData = await GameService.getPossibleMoves();
      console.log(responseData);
      setAllPossibleMoves(responseData);
    } catch (error) {
      console.error("Failed to fetch possible moves:", error);
    }
  }, [boardArray]);

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

  const onMarbleClick = useCallback(
    (space) => {
      let newSelectedMarbles = [];
      // Early return if the space has a move.
      if (space.move !== null) {
        onMoveSelection(space.move);
        deselectMarbles(selectedMarbles);
        setSelectedMarbles([]);
        generateBoard();
        return;
      }

      // If the space is not one of the current players marbles or a possible move, return.
      if (![currentTurn, 3, 4].includes(space.state)) {
        return;
      }

      // Deselect if the same marble is clicked again.
      if (selectedMarbles.includes(space)) {
        deselectMarbles([space]);
        setSelectedMarbles(
          selectedMarbles.filter((marble) => marble !== space)
        );
        return;
      }

      // Handle marble selection logic.
      if (selectedMarbles.length < 3) {
        const lastSelectedMarble = selectedMarbles[selectedMarbles.length - 1];
        // If adjacent or in a straight line, select the current marble.
        if (
          !lastSelectedMarble ||
          lastSelectedMarble.isAdjacentTo(space) ||
          (selectedMarbles.length === 2 &&
            Space.areInStraightLine(
              selectedMarbles[0],
              selectedMarbles[1],
              space
            ))
        ) {
          space.selected = true;
          newSelectedMarbles = [...selectedMarbles, space];
          setSelectedMarbles(newSelectedMarbles);
        } else {
          // Otherwise, deselect all and select the current marble.
          deselectMarbles(selectedMarbles);
          space.selected = true;
          newSelectedMarbles = [space];
          setSelectedMarbles(newSelectedMarbles);
        }
      } else {
        // If more than two marbles are already selected, reset and select the current one.
        deselectMarbles(selectedMarbles);
        space.selected = true;
        newSelectedMarbles = [space];
        setSelectedMarbles(newSelectedMarbles);
      }
    },
    [
      currentTurn,
      selectedMarbles,
      onMoveSelection,
      deselectMarbles,
      setSelectedMarbles,
      generateBoard,
    ]
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
    generateBoard();
  }, [generateBoard]);

  useEffect(() => {
    updateValidMoves();
  }, [updateValidMoves]);

  useEffect(() => {
    if (isGameActive) {
      fetchPossibleMoves();
    }
  }, [fetchPossibleMoves, isGameActive]);

  useEffect(() => {
    const clearHighlight = () => {
      for (let row = 0; row < board.length; row++) {
        for (let column = 0; column < board[row].length; column++) {
          if (board[row][column].state === 3) {
            board[row][column].state = boardArray[row][column];
          }
          if (board[row][column].state === 4) {
            board[row][column].state = boardArray[row][column];
          }
        }
      }
    };
    clearHighlight();
  }, [validMovesForSelectedMarbles, onMarbleClick, board, boardArray]);

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
          disabled={!isGameActive}
        >
          {space.str}
        </Fab>
      );
    },
    [getSpaceStyle, onMarbleClick, isGameActive]
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

  useEffect(() => {
    setBoard((prevBoard) => {
      validMovesForSelectedMarbles.map((move) => {
        move.next_player_positions.map((space) => {
          const opponentNum = currentTurn === 1 ? 2 : 1;

          const spaceObj = prevBoard[space.y][space.x];

          if (spaceObj.state === opponentNum) {
            spaceObj.state = 4;
            spaceObj.move = move;
          } else if (spaceObj.state !== currentTurn && spaceObj.state !== 4) {
            spaceObj.state = 3;
            spaceObj.move = move;
          }
        });
      });

      return [...prevBoard];
    });
  }, [currentTurn, setBoard, validMovesForSelectedMarbles]);

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
  boardArray: PropTypes.array.isRequired,
  onMoveSelection: PropTypes.func.isRequired,
  selectedMarbles: PropTypes.array.isRequired,
  setSelectedMarbles: PropTypes.func.isRequired,
  isGameActive: PropTypes.bool,
  currentTurn: PropTypes.number,
};

export { Board };
