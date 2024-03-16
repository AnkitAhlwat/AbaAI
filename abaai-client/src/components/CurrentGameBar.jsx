import MoveHistory from "./MoveHistory";
import AIMoveDisplay from "./AiMove";
import GameClock from "./Clock";
import Proptypes from "prop-types";
import { Divider, Typography } from "@mui/material";

const CurrentGameBar = (props) => {
  const { movesStack, aiMove } = props;

  const dummyMovesStack = [
    {
      player: 1,
      previous_positions: [
        { x: 2, y: 6 },
        { x: 3, y: 6 },
      ],
      next_positions: [
        { x: 2, y: 5 },
        { x: 3, y: 5 },
      ],
    },
    {
      player: 2,
      previous_positions: [
        { x: 4, y: 2 },
        { x: 5, y: 2 },
      ],
      next_positions: [
        { x: 4, y: 3 },
        { x: 5, y: 3 },
      ],
    },
    {
      player: 1,
      previous_positions: [
        { x: 4, y: 6 },
        { x: 4, y: 7 },
        { x: 4, y: 8 },
      ],
      next_positions: [
        { x: 4, y: 5 },
        { x: 4, y: 6 },
        { x: 4, y: 7 },
      ],
    },
  ];

  const centerDivider = (text) => {
    if (text === "" || text === undefined) {
      return <Divider variant="middle" sx={{ bgcolor: "white" }} />;
    }
    return (
      <Divider
        variant="middle"
        sx={{
          color: "#f5f5f5",
          "&::before, &::after": {
            borderColor: "#f5f5f5",
          },
        }}
      >
        <Typography>{text}</Typography>
      </Divider>
    );
  };

  return (
    <>
      <GameClock />
      {centerDivider("AI Suggested Move")}
      <AIMoveDisplay aiMove={aiMove} />
      {centerDivider("Move History")}
      <MoveHistory movesStack={dummyMovesStack} />
    </>
  );
};

CurrentGameBar.propTypes = {
  movesStack: Proptypes.array.isRequired,
  aiMove: Proptypes.string.isRequired,
};

export default CurrentGameBar;
