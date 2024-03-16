import MoveHistory from "./MoveHistory";
import AIMoveDisplay from "./AiMove";
import GameClock from "./Clock";
import Proptypes from "prop-types";
import { Divider, Typography } from "@mui/material";

const CurrentGameBar = (props) => {
  const { movesStack, aiMove } = props;

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
      <MoveHistory movesStack={movesStack} />
    </>
  );
};

CurrentGameBar.propTypes = {
  movesStack: Proptypes.array.isRequired,
  aiMove: Proptypes.string.isRequired,
};

export default CurrentGameBar;
