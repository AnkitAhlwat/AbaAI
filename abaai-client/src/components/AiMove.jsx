import { Grid, Paper, Avatar, Typography, Button } from "@mui/material";
import AIAvatar from "../assets/robot.png";
import Proptypes from "prop-types";
import Move from "../models/Move";

// Displays each move the AI mades on the GUI interface
const AIMoveDisplay = ({ aiMove, onApplyMove, isWhite, disabled }) => {
  const { move, time_taken } = aiMove || {};

  return (
    <Paper
      elevation={3}
      sx={{
        padding: "20px",
        backgroundColor: isWhite ? "#989795" : "#302e2b",
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
            {move ? Move.toNotation(move) : "..."}
          </Typography>
        </Grid>
        <Grid item xs={6}>
          <Button
            variant="contained"
            color="success"
            onClick={() => onApplyMove(move)}
            disabled={disabled}
          >
            Apply
          </Button>
        </Grid>
        {time_taken !== undefined && (
          <Grid item xs={6}>
            <Typography
              variant="subtitle2"
              color={isWhite ? "#262522" : "#f5f5f5"}
              textAlign={"center"}
            >
              {time_taken} s
            </Typography>
          </Grid>
        )}
      </Grid>
    </Paper>
  );
};

AIMoveDisplay.propTypes = {
  aiMove: Proptypes.object,
  onApplyMove: Proptypes.func,
};

export default AIMoveDisplay;
