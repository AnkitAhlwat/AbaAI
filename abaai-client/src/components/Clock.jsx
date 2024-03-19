import React from 'react';
import { useCountdown } from '../hooks/useCountdown';
import { Box, Typography, Button } from '@mui/material';

const GameClock = (props) => {
  const { movesStack, aiMove, initialTime, playerId} = props;
  const { start: startCountdown, currentTime, isRunning } = useCountdown(initialTime);

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
