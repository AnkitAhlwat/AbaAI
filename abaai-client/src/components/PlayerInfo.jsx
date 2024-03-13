import { Grid, Typography } from "@mui/material";
import { SmartToy, Person } from "@mui/icons-material";
import Proptypes from "prop-types";
import GameScore from "./GameScore";

const PlayerInfo = (props) => {
  const { isBot, color, numCapturedMarbles } = props;

  const playerProfile = (
    <Grid container spacing={2}>
      <Grid item xs={1}>
        {isBot ? (
          <SmartToy
            sx={{
              color: "white",
            }}
          />
        ) : (
          <Person
            sx={{
              color: "white",
            }}
          />
        )}
      </Grid>
      <Grid item xs={11}>
        <Typography
          variant="h6"
          sx={{
            color: "white",
          }}
        >
          {isBot ? "AI" : "Player"}
        </Typography>
      </Grid>
    </Grid>
  );

  return (
    <Grid container>
      <Grid item xs={3}>
        {playerProfile}
      </Grid>
      <Grid item xs={3}>
        <GameScore numCapturedMarbles={numCapturedMarbles} color={color} />
      </Grid>
      <Grid item xs={3}></Grid>
    </Grid>
  );
};

PlayerInfo.propTypes = {
  isBot: Proptypes.bool,
  numCapturedMarbles: Proptypes.oneOf([0, 1, 2, 3, 4, 5, 6]).isRequired,
  color: Proptypes.oneOf(["black", "white"]).isRequired,
};

export default PlayerInfo;
