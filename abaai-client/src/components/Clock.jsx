import React, { useEffect } from 'react';
import { useCountdown } from '../hooks/useCountdown';
import { Box, Typography, Button } from '@mui/material';

const GameClock = (props) => {
  const { initialTime, isActive, playerId, onMoveMade, gameStarted} = props;
  const { start: startClock, stop: stopClock, pause: pauseClock,  resume: resumeClock, currentTime, isRunning } = useCountdown(initialTime);
  // { start, stop, pause, resume, currentTime, isRunning };
  const [initialStart , setInitialStart] = React.useState(true);

    /* Current behaviour of the resume function, currently uses pausing function as well to simulate
     when a player makes a move, the clock will pause and the other player's clock will start    
     */
  useEffect(() => {
    // Handle initial start separately
    if (gameStarted && isActive && !isRunning && initialStart) {
      console.log(`Starting clock for player ${playerId}`);
      startClock();
      setInitialStart(false); // Prevent further starts
    }
  }, [gameStarted, isActive, isRunning, initialStart, startClock]);

  useEffect(() => {
    // Assuming gameStarted indicates the game has officially begun
    if (gameStarted) {
      if (isActive) {
        console.log(`Toggling clock for player ${playerId}`);
        if (!isRunning) {
          resumeClock();
        }
      } else if (isRunning) {
        pauseClock();
      }
    }
  }, [gameStarted, isActive, isRunning, pauseClock, resumeClock]);

  


  return (
    <Box>
      <Typography variant="h5" style={{ color: 'white' }}>
      {playerId === "black" ? "Black Player" : "White Player"}Time: {currentTime}
      </Typography>
    </Box>
  );
};

export default GameClock;
