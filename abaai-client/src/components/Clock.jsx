import React, { useEffect } from 'react';
import { useCountdown } from '../hooks/useCountdown';
import { Box, Typography, Button } from '@mui/material';

const GameClock = (props) => {
  const { initialTime, isTurn, playerId, activePlayer, 
    gameStarted, isActive, resetClockSignal, undoClock, isAggregate} = props;
  const { start: startClock, stop: stopClock, pause: pauseClock,  
    resume: resumeClock, currentTime, isRunning, 
    recordMoveTime, undoLastMoveTime} = useCountdown(initialTime, true);
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
      if (!isTurn) {   // Pause the clock if it's not the player's turn
        pauseClock();
        // if (!isAggregate) return;
        // console.log("Recording move time for player: ", playerId)
        // console.log("Activeplayer: ", activePlayer)
        // console.log("IsTurn: ", isTurn)
        // recordMoveTime();
      }
        //add time taken to a stack, either in here or in useCountdown
    }, [isTurn, isActive]);

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

    //have the useCountdown hook pop the stack and add back the time to the clock (old)
    //reset the clock if it is a turn clock
    useEffect(() => {
        if (!isAggregate){
          stopClock();
          setInitialStart(true);
          if (gameStarted && isActive && isTurn) {
            startClock(); // Immediately start the clock for the new turn.
            setInitialStart(false);
          }
        }
      // console.log("In CLOCK (undoLastMoveTime) turn: ", isTurn)
      // console.log("Activeplayer: ", activePlayer)
      // if (gameStarted && !activePlayer){
      //   console.log("Undoing last move for player: ", playerId)
      //   undoLastMoveTime();
      // }
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
