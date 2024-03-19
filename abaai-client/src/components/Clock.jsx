import React, { useEffect } from 'react';
import { useCountdown } from '../hooks/useCountdown';
import { Box, Typography, Button } from '@mui/material';

const GameClock = (props) => {
  const { initialTime, isActive, playerId, onMoveMade, gameStarted} = props;
  const { start: startCountdown, currentTime, isRunning } = useCountdown(initialTime);

    // Start the clock when the component mounts or when it becomes active
    useEffect(() => {
      if (gameStarted && isActive) {
        startCountdown();
      }
    }, [gameStarted, isActive, isRunning, startCountdown]);
  


  return (
    <Box>
      <Typography variant="h5" style={{ color: 'white' }}>
      {playerId === "black" ? "Black Player" : "White Player"}Time: {currentTime}
      </Typography>
      {!isRunning && (
        <Button onClick={startCountdown} color="primary" variant="contained">
          Start
        </Button>
      )}
    </Box>
  );
};

export default GameClock;
