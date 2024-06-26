import React, { useState, useEffect, useRef , useCallback} from 'react';
import { Box, Typography, Button } from '@mui/material';
import GameService from '../services/game.service';

// Displays the clock of the GUI
const GameClock = ({ initialGameTime = 0, turnTimeLimit = 15, gameStarted, setBoardArray}) => {
  const [gameTime, setGameTime] = useState(initialGameTime); // Total game time
  const [turnTime, setTurnTime] = useState(turnTimeLimit); // Time left per turn
  const [gameActive, setGameActive] = useState(false); // Whether game is being played
  const [turnActive, setTurnActive] = useState(false); // Whether turn is being played
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

  // Detects whether a move is made
  useEffect(() => {
    if (gameStarted){
      handleStart();
    }
  }, [gameStarted]);

  // Starts the timer if a move is made
  const handleStart = () => {
    startTimeRef.current = Date.now();
    setTimeout(() => {
        setGameActive(true);
        setTurnActive(true);
        setGameTime((prevTime) => prevTime + 1);
        setTurnTime((prevTime) => prevTime - 1);
    }, waitTimeRef.current);
  };

  // Stops the timer if button is pressed
  const handleStop = () => {
  };

  // Pauses the timer if button is pressed
  const handlePause = () => {
    waitTimeRef.current = 1000 - (Date.now() - startTimeRef.current)%1000;
    setGameActive(false);
    setTurnActive(false);
  };

  // Resets the timer if button is pressed
  const handleReset = useCallback(async () => {
    const responseData = await GameService.postResetGame();
    console.log(responseData);
    setGameTime(initialGameTime);
    setTurnTime(turnTimeLimit);
    setGameActive(false);
    setTurnActive(false);
    setBoardArray(responseData.board);
    // gameStarted(false);
  });

  // Returns UI component with clock information
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
