import { Grid, Fab, Box } from "@mui/material";
import { useCallback, useState, useEffect } from "react";
import SpaceStates from "../constants/spaceStates";
import Space from "../models/Space";

const marbleStyles = {
  1: {
    backgroundColor: "black",
    color: "white",
    outline: "solid 2px black",
    boxShadow: "none",
    "&:hover": { backgroundColor: "#767271" },
    flexShrink: 1,
  },
  2: {
    backgroundColor: "white",
    color: "black",
    outline: "solid 2px white",
    boxShadow: "none",
    "&:hover": { backgroundColor: "#767271" },
    flexShrink: 1,
  },
  0: {
    backgroundColor: "#ae694a",
    boxShadow: "none",
    flexShrink: 1,
    "&:hover": { backgroundColor: "#767271" },
  },
  selected: {
    backgroundColor: "rgba(115,149,82,255)",
    boxShadow: "none",
    outline: "solid 2px black",
    flexShrink: 1,
    "&:hover": { backgroundColor: "rgba(130,180,100,255)" },
  },
  3: {
    backgroundColor: "yellow",
    boxShadow: "none",
    flexShrink: 1,
  },
  4: {
    backgroundColor: "red",
    boxShadow: "none",
    flexShrink: 1,
  },
};

/**
 * Convert algebraic notation "E5" to {x, y} grid coords.
 * Letter = row: I(y=0) .. A(y=8). Number = col+1: 1(x=0) .. 9(x=8).
 */
function notationToXY(notation) {
  const letter = notation[0].toUpperCase();
  const number = parseInt(notation[1], 10);
  return { x: number - 1, y: 73 - letter.charCodeAt(0) };
}

const Board = ({
  boardArray,
  selectedMarbles,
  setSelectedMarbles,
  onMoveSelection,
  isGameActive,
  currentTurn,
  legalMoves = [],
}) => {
  const [board, setBoard] = useState([]);
  const [validMoveTargets, setValidMoveTargets] = useState([]);

  const generateBoard = useCallback(() => {
    if (!boardArray || boardArray.length === 0) return;
    const newBoard = boardArray.map((row, rowIndex) =>
      row.map((state, columnIndex) => new Space(state, { y: rowIndex, x: columnIndex }))
    );
    setBoard(newBoard);
  }, [boardArray]);

  useEffect(() => {
    generateBoard();
  }, [generateBoard]);

  // When selected marbles change, find legal moves that start from those marbles
  useEffect(() => {
    if (selectedMarbles.length === 0 || !legalMoves.length) {
      setValidMoveTargets([]);
      return;
    }

    const selectedNotations = selectedMarbles
      .map((m) => m.str)
      .sort();

    const matching = [];
    legalMoves.forEach((move, idx) => {
      const moveFrom = [...move.from].sort();
      if (
        moveFrom.length === selectedNotations.length &&
        moveFrom.every((val, i) => val === selectedNotations[i])
      ) {
        matching.push({ move, idx });
      }
    });

    setValidMoveTargets(matching);
  }, [selectedMarbles, legalMoves]);

  // Highlight destinations on the board
  useEffect(() => {
    if (!board.length) return;

    // Clear previous highlights
    for (const row of board) {
      for (const space of row) {
        if (space.state === 3 || space.state === 4) {
          space.state = boardArray[space.position.y][space.position.x];
          space.move = null;
          space.moveIndex = null;
        }
      }
    }

    // Apply new highlights
    for (const { move, idx } of validMoveTargets) {
      for (const notation of move.to) {
        const { x, y } = notationToXY(notation);
        if (y >= 0 && y < board.length && x >= 0 && x < board[y].length) {
          const space = board[y][x];
          const opponentVal = currentTurn === 1 ? 2 : 1;
          if (space.state === opponentVal) {
            space.state = 4;
          } else if (space.state !== currentTurn) {
            space.state = 3;
          }
          space.moveIndex = idx;
        }
      }
    }

    setBoard([...board]);
  }, [validMoveTargets]);

  const deselectMarbles = useCallback((marbles) => {
    for (const marble of marbles) {
      marble.selected = false;
    }
  }, []);

  const onMarbleClick = useCallback(
    (space) => {
      // If clicking a highlighted destination, submit that move
      if (space.moveIndex != null) {
        onMoveSelection(space.moveIndex);
        deselectMarbles(selectedMarbles);
        setSelectedMarbles([]);
        return;
      }

      if (![currentTurn].includes(space.state)) {
        return;
      }

      if (selectedMarbles.includes(space)) {
        deselectMarbles([space]);
        setSelectedMarbles(selectedMarbles.filter((m) => m !== space));
        return;
      }

      let newSelected = [];
      if (selectedMarbles.length < 3) {
        const last = selectedMarbles[selectedMarbles.length - 1];
        if (
          !last ||
          last.isAdjacentTo(space) ||
          (selectedMarbles.length === 2 &&
            Space.areInStraightLine(selectedMarbles[0], selectedMarbles[1], space))
        ) {
          space.selected = true;
          newSelected = [...selectedMarbles, space];
        } else {
          deselectMarbles(selectedMarbles);
          space.selected = true;
          newSelected = [space];
        }
      } else {
        deselectMarbles(selectedMarbles);
        space.selected = true;
        newSelected = [space];
      }
      setSelectedMarbles(newSelected);
    },
    [currentTurn, selectedMarbles, onMoveSelection, deselectMarbles, setSelectedMarbles]
  );

  const getSpaceStyle = useCallback((space) => {
    if (space.selected) return marbleStyles.selected;
    return marbleStyles[space.state] || marbleStyles[0];
  }, []);

  const renderMarble = useCallback(
    (space) => (
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
    ),
    [getSpaceStyle, onMarbleClick, isGameActive]
  );

  const renderRow = useCallback(
    (row, rowIndex) => (
      <Grid
        container
        item
        justifyContent="center"
        key={rowIndex}
        sx={{ flexShrink: 1, flexWrap: "nowrap" }}
      >
        {row.map((space, columnIndex) => (
          <Grid item key={`${rowIndex}-${columnIndex}`} sx={{ flexShrink: 1, flexWrap: "nowrap" }}>
            {space.state !== SpaceStates.NONE && renderMarble(space)}
          </Grid>
        ))}
      </Grid>
    ),
    [renderMarble]
  );

  return (
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
  );
};

export { Board };
