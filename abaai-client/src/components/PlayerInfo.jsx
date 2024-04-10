import { Grid, Typography, Box } from "@mui/material";
import { SmartToy, Person } from "@mui/icons-material";
import GameClock from "./Clock";
import Proptypes from "prop-types";
import GameScore from "./GameScore";

const PlayerInfo = (props) => {
  const {
    isBot,
    color,
    numCapturedMarbles,
    movesRemaining,
    moveTimeRemaining,
    //clock controls
    activePlayer,
    isGameActive,
    toggleActivePlayer,
    gameStarted,
    gameConfigured,
    startGame,
    stopGame,
    resetClockSignal,
    pauseGame,
    resumeGame,
    resetGame,
    undoMove,
    // blackClock,
    // whiteClock,
    thisClock,
    updateGame,
    // onSubmitConfig
  } = props;

  const playerProfile = (
    <Grid container spacing={2}>
      <Grid item xs={2}>
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
      <Grid item xs={10}>
        <Typography
          variant="h5"
          sx={{
            color: "white",
          }}
        >
          {isBot ? "AI" : "Player"}
        </Typography>
      </Grid>
    </Grid>
  );

  const movesRemainingDisplay =
    movesRemaining !== null ? (
      <Typography
        variant="h5"
        sx={{
          color: "white",
        }}
      >
        Moves Remaining: {movesRemaining}
      </Typography>
    ) : (
      <Typography
        variant="h5"
        sx={{
          color: "white",
        }}
      >
        Moves Remaining: &infin;
      </Typography>
    );

  const moveTimer = (
    <Box
      sx={{
        backgroundColor: color == "black" ? "#2b2926" : "#989795",
        width: "fit-content",
        borderRadius: "5px",
        padding: "12px",
      }}
    >
      <Typography
        variant="h4"
        sx={{
          color: color == "black" ? "#7c7a78" : "#636260",
        }}
      >
        {moveTimeRemaining ? `${moveTimeRemaining.toFixed(2)}` : "0.00"}s
      </Typography>
    </Box>
  );

  return (
    <Grid container alignItems="center" justifyContent="space-between">
      <Grid item xs={2}>
        {playerProfile}
      </Grid>
      <Grid item xs={4}>
        <GameScore numCapturedMarbles={numCapturedMarbles} color={color} />
      </Grid>
      <Grid item xs={3}>
        {movesRemainingDisplay}
      </Grid>
      <Grid container item xs={3} justifyContent="right">
        {/* {moveTimer} */}
        <GameClock
        initialTime={thisClock}
        isTurn={activePlayer === color}
        playerId={color}                   
        activePlayer={activePlayer}
        gameStarted={gameStarted}
        isActive={isGameActive}
        resetClockSignal={resetClockSignal}
        undoClock={null}
        isAggregate={false}
      />
      </Grid>
    </Grid>
  );
};

PlayerInfo.propTypes = {
  isBot: Proptypes.bool,
  numCapturedMarbles: Proptypes.oneOf([0, 1, 2, 3, 4, 5, 6]).isRequired,
  color: Proptypes.oneOf(["black", "white"]).isRequired,
  movesRemaining: Proptypes.number,
  moveTimeRemaining: Proptypes.number,
};

export default PlayerInfo;
