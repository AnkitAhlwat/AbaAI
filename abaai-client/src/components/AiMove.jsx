import { Grid, Paper, Avatar, Typography, Button } from "@mui/material";
import AIAvatar from "../assets/robot.png";
import Proptypes from "prop-types";
import Move from "../models/Move";

// Displays each move the AI mades on the GUI interface
const AIMoveDisplay = ({ aiMove, onApplyMove }) => {
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
        <Grid item xs={12}>
          <Typography
            variant="subtitle2"
            gutterBottom
            sx={{
              color: "#f5f5f5",
              backgroundColor: "#262522",
              paddingTop: "10px",
              paddingBottom: "10px",
              borderRadius: "5px",
            }}
            textAlign={"center"}
          >
            {aiMove ? Move.toNotation(aiMove) : "..."}
          </Typography>
        </Grid>
        <Grid item>
          <Button
            variant="contained"
            color="success"
            onClick={() => onApplyMove(aiMove)}
          >
            Apply
          </Button>
        </Grid>
      </Grid>
    </Paper>
  );
};

AIMoveDisplay.propTypes = {
  aiMove: Proptypes.object,
  onApplyMove: Proptypes.func,
};

export default AIMoveDisplay;
