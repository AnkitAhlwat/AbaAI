import React, { useEffect } from 'react';
import { useCountdown } from '../hooks/useCountdown';
import { Box, Typography, Button } from '@mui/material';

const GameClock = (props) => {
  const { initialTime, isTurn, playerId, activePlayer, 
    gameStarted, isActive, resetClockSignal, undoClock, isAggregate} = props;
  const { start: startClock, stop: stopClock, pause: pauseClock,  
    resume: resumeClock, currentTime, isRunning, 
    recordMoveTime, getMoveTimes} = useCountdown(initialTime, true);
  const [initialStart , setInitialStart] = React.useState(true);

  //start the game clock
  useEffect(() => {
    // Handle initial start separately
    if (gameStarted && isTurn && !isRunning && initialStart) {
      console.log(`Starting clock for player ${playerId}`);
      startClock();
      setInitialStart(false); // Prevent further starts
    }
  }, [gameStarted, isActive, isRunning, initialStart, activePlayer]);

    //pause or resume the game clock
    useEffect(() => {
      // console.log("Use Effect for the game clock: ", isActive, isTurn, activePlayer)
      if (!isActive && isTurn)
        pauseClock();
      else if (isActive && isTurn)
        resumeClock();
      if (!isTurn)
        pauseClock();
        if (!isAggregate) return;
        recordMoveTime();
        //add time taken to a stack, either in here or in useCountdown
    }, [isActive, isTurn, activePlayer]);

    //stop the game clock, currently same as reset
    useEffect(() => {
        // console.log("STOP CLOCK CALLED FOR: ", isActive, isTurn, activePlayer)
        stopClock();
        setInitialStart(true);
        if (gameStarted && isActive && isTurn) {
          startClock(); // Immediately start the clock for the new turn.
          setInitialStart(false);
        }
    }, [resetClockSignal]);

    //have the useCountdown hook pop the stack and add back the time to the clock
    useEffect(() => {
        getMoveTimes();
    }, [undoClock]);

  return (
    <Box>
      <Typography variant="h5" style={{ color: 'white' }}>
      {playerId === "black" ? "Black Player" : "White Player"}Time: {currentTime}
      </Typography>
    </Box>
  );
};

export default GameClock;
