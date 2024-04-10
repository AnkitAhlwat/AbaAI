import React, { useState, useRef, useCallback, useEffect } from 'react';

export const useCountdown = (totalSeconds, isAggregate = false) => {
  const [isRunning, setIsRunning] = useState(false);
  const [currentTime, setCurrentTime] = useState('');
  const startTimeRef = useRef(0);
  const elapsedPauseTimeRef = useRef(0);
  const pauseStartTimeRef = useRef(0);
  const requestRef = useRef();
  const totalMilliseconds = totalSeconds * 1000;
  const moveTimesStack = isAggregate ? useRef([]) : null;  //tracks if this is an aggregate timer for undo functionality
  const moveDuration = useRef(0);
  const allMoveDuration = useRef(0); //tracks all move duration for the game

  const formatTime = useCallback((milliseconds) => {
    let totalSeconds = milliseconds / 1000;
    let seconds = Math.floor(totalSeconds % 60);
    let minutes = Math.floor(totalSeconds / 60);
    const hundredths = Math.floor((totalSeconds - seconds) * 100) % 100;
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}.${hundredths < 10 ? '0' : ''}${hundredths}`;
  }, []);

  const getRemainingMilliseconds = useCallback(() => {
    const elapsed = isRunning
      ? Date.now() - startTimeRef.current - elapsedPauseTimeRef.current
      : pauseStartTimeRef.current ? pauseStartTimeRef.current - startTimeRef.current - elapsedPauseTimeRef.current : 0;
    return Math.max(0, totalMilliseconds - elapsed);
  }, [isRunning, totalMilliseconds]);

  useEffect(() => {
    if (!isRunning) {
      return;
    }
    const update = () => {
      const newTime = formatTime(getRemainingMilliseconds());
      setCurrentTime(newTime);
      requestRef.current = requestAnimationFrame(update);
    };
    requestRef.current = requestAnimationFrame(update);
    return () => cancelAnimationFrame(requestRef.current);
  }, [isRunning, formatTime, getRemainingMilliseconds]);

  const start = useCallback(() => {
    console.log("Start called")
    if (!isRunning) {
      console.log("Starting clock")
      startTimeRef.current = Date.now();
      elapsedPauseTimeRef.current = 0;
      setIsRunning(true);
    }
  }, [isRunning]);

  const stop = useCallback(() => {
    setIsRunning(false);
    cancelAnimationFrame(requestRef.current);
    startTimeRef.current = 0;
    elapsedPauseTimeRef.current = 0;
    pauseStartTimeRef.current = 0;
    moveDuration.current = 0;
    moveTimesStack.current = [];
    setCurrentTime(formatTime(totalMilliseconds)); // Optionally reset the displayed time
  }, [formatTime, totalMilliseconds]);

  const pause = useCallback(() => {
    if (isRunning) {
      console.log("Pausing clock")
      setIsRunning(false);
      pauseStartTimeRef.current = Date.now();
      cancelAnimationFrame(requestRef.current);
      // moveDuration.current += Date.now() - startTimeRef.current - elapsedPauseTimeRef.current - allMoveDuration.current;
      allMoveDuration.current += moveDuration.current;
    }
  }, [isRunning]);

  const resume = useCallback(() => {
    if (!isRunning && pauseStartTimeRef.current !== 0) {
      console.log("Resuming clock")
      elapsedPauseTimeRef.current += Date.now() - pauseStartTimeRef.current;
      pauseStartTimeRef.current = 0;
      setIsRunning(true);
    }
  }, [isRunning]);

  //record the move time to be added to a stack
  const recordMoveTime = useCallback(() => { 
    console.log("Recording move time: ", moveDuration.current)
    moveTimesStack.current.push(moveDuration.current);
    moveDuration.current = 0; 
  }, [isAggregate]);

  //undo the last move time from the stack
  const undoLastMoveTime = useCallback(() => {
    const lastMoveTime = moveTimesStack.current.pop();
    console.log("Last Move Time: ", lastMoveTime)
    const currentMilliseconds = getRemainingMilliseconds() + lastMoveTime;
    setCurrentTime(formatTime(currentMilliseconds));
}, [getRemainingMilliseconds, formatTime, isAggregate]);

  // Initialize currentTime with the formatted total time
  useEffect(() => {
    setCurrentTime(formatTime(totalMilliseconds));
  }, [totalMilliseconds, formatTime]);

  return { start, stop, pause, resume, currentTime, isRunning, recordMoveTime, undoLastMoveTime};
};
