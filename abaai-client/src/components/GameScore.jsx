import { Box } from "@mui/material";
import Proptypes from "prop-types";

const GameScore = ({ numCapturedMarbles, color }) => {
  const opposingColor = color === "black" ? "white" : "black";

  return (
    <Box sx={{ display: "flex", alignItems: "center" }}>
      {[...Array(6)].map((_, index) => (
        <Box
          key={index}
          sx={{
            width: 20,
            height: 20,
            borderRadius: "50%",
            marginX: 1,
            backgroundColor:
              index < numCapturedMarbles ? opposingColor : "transparent",
            border: "2px solid grey",
          }}
        />
      ))}
    </Box>
  );
};

GameScore.propTypes = {
  numCapturedMarbles: Proptypes.oneOf([0, 1, 2, 3, 4, 5, 6]).isRequired,
  color: Proptypes.oneOf(["black", "white"]).isRequired,
};

export default GameScore;
