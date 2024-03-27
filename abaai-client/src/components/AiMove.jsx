import { Grid, Paper, Avatar, Typography } from "@mui/material";
import AIAvatar from "../assets/robot.png";
import Proptypes from "prop-types";
import Move from "../models/Move";

// Displays each move the AI mades on the GUI interface
const AIMoveDisplay = ({ aiMove }) => {
  return (
    <Paper
      elevation={3}
      sx={{
        padding: "20px",
        backgroundColor: "#3c3b39",
        marginTop: "5px",
        marginBottom: "10px",
      }}
    >
      <Grid container alignItems="center" spacing={2}>
        <Grid item>
          <Avatar src={AIAvatar} alt="AI Avatar" />
        </Grid>
        <Grid item>
          <Typography
            variant="subtitle1"
            gutterBottom
            sx={{
              color: "#f5f5f5",
            }}
          >
            {aiMove ? Move.toNotation(aiMove) : "..."}
          </Typography>
        </Grid>
      </Grid>
    </Paper>
  );
};

AIMoveDisplay.propTypes = {
  aiMove: Proptypes.string.isRequired,
};

export default AIMoveDisplay;
