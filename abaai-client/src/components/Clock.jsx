import React, { useState, useEffect, useRef } from 'react';
import { Box, Typography, Button } from '@mui/material';

const GameClock = ({ initialGameTime = 0, turnTimeLimit = 15 }) => {
  const [gameTime, setGameTime] = useState(initialGameTime);
  const [turnTime, setTurnTime] = useState(turnTimeLimit);
  const [gameActive, setGameActive] = useState(false);
  const [turnActive, setTurnActive] = useState(false);
  const waitTimeRef = useRef(1000);
  const startTimeRef = useRef(0);

  // Game time counter
  useEffect(() => {
    let gameTimer;
    if (gameActive) {
      gameTimer = setInterval(() => {
        setGameTime((prevTime) => prevTime + 1);
      }, 1000);
    }
    return () => clearInterval(gameTimer);
  }, [gameActive]);

  // Turn time countdown
  useEffect(() => {
    let turnTimer;
    if (turnActive && turnTime > 0) {
      turnTimer = setInterval(() => {
        setTurnTime((prevTime) => prevTime - 1);
      }, 1000);
    } else if (turnTime === 0) {
      setTurnActive(false);
    }else if (turnTime < 0){
        setTurnTime(0);
    }
    return () => clearInterval(turnTimer);
  }, [turnActive, turnTime]);

  const handleStart = () => {
    startTimeRef.current = Date.now();
    setTimeout(() => {
        setGameActive(true);
        setTurnActive(true);
        setGameTime((prevTime) => prevTime + 1);
        setTurnTime((prevTime) => prevTime - 1);
    }, waitTimeRef.current);
  };

  const handleStop = () => {
  };

  const handlePause = () => {
    waitTimeRef.current = 1000 - (Date.now() - startTimeRef.current)%1000;
    setGameActive(false);
    setTurnActive(false);
  };

  const handleReset = () => {
    setGameTime(initialGameTime);
    setTurnTime(turnTimeLimit);
    setGameActive(false);
    setTurnActive(false);
  };

  return (
    <Box>
      <Typography variant="h5">Game Time: {Math.floor(gameTime / 60)}:{String(gameTime % 60).padStart(2, '0')}</Typography>
      <Typography variant="h6">Turn Time Left: {turnTime}</Typography>
      <Button onClick={handleStart} disabled={gameActive}>Start</Button>
      <Button onClick={handleStop}>Stop</Button>
      <Button onClick={handlePause} disabled={!gameActive}>Pause</Button>
      <Button onClick={handleReset}>Reset Time</Button>
    </Box>
  );
};

export default GameClock;
