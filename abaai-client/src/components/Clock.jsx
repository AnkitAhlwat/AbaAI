import React, { useEffect } from 'react';
import { useCountdown } from '../hooks/useCountdown';
import { Box, Typography, Button } from '@mui/material';

const GameClock = (props) => {
  const { initialTime, isTurn, playerId, activePlayer, gameStarted, isActive, resetClockSignal} = props;
  const { start: startClock, stop: stopClock, pause: pauseClock,  resume: resumeClock, currentTime, isRunning 
  } = useCountdown(initialTime);
  const [initialStart , setInitialStart] = React.useState(true);
  // const [turnClockTime, setTurnClockTime] = useState(initialTime);
  // const [scoreClockTime, setScoreClockTime] = useState(initialTime);

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
      if (!isActive && isTurn) {
        pauseClock();
      } else if (isActive && isTurn) {
        resumeClock();
      } if (!isTurn) {
        pauseClock();
      }
    }, [isActive, isTurn, activePlayer]);

    //stop the game clock, currently same as reset
    useEffect(() => {
        stopClock();
        setInitialStart(true);
        if (gameStarted && isActive) {
          startClock(); // Immediately start the clock for the new turn.
          setInitialStart(false);
        }
    }, [resetClockSignal]);

    //reset the game clock
    // useEffect(() => {
    //     stopClock();
    //     setInitialStart(true);
    // }, [resetClockSignal]);

    //reset the turn clocks each turn
    // const resetTurnClock = () => {
    //   setTurnClockTime(initialTime);
    // };

    // useEffect(() => {
    //   stopClock();
    //   setInitialStart(true);
    // }, [resetSignal]);


  //triggered when the active status of the game is changed for taking turns 
  useEffect(() => {
    if (gameStarted) {
      if (isActive) {
        console.log(`Toggling clock for player ${playerId}`);
        if (isRunning) {
          pauseClock();
        }
      } else if (!isRunning) {
        resumeClock();
      }
    }
  // }, [isActive]);
}, []);


  return (
    <Box>
      <Typography variant="h5" style={{ color: 'white' }}>
      {playerId === "black" ? "Black Player" : "White Player"}Time: {currentTime}
      </Typography>
    </Box>
  );
};

export default GameClock;
