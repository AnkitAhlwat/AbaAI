import { Grid, Typography, Button, Chip } from "@mui/material";
import { useCallback, useState, useEffect, useRef } from "react";
import { useBoard } from "../hooks/useBoard";
import GameService from "../services/game.service";
import GameplaySection from "./GameplaySection";
import MoveHistory from "./MoveHistory";

const Game = ({ gameId, playerToken, playerColor, onLeave }) => {
  const [gameState, setGameState] = useState(null);
  const [movesStack, setMovesStack] = useState([]);
  const [selectedMarbles, setSelectedMarbles] = useState([]);
  const { boardArray, setBoardArray } = useBoard();
  const pollRef = useRef(null);

  const fetchState = useCallback(async () => {
    try {
      const state = await GameService.getState(gameId, playerToken);
      setGameState(state);
      if (state.board) {
        setBoardArray(state.board);
      }
      return state;
    } catch (err) {
      console.error("Failed to fetch state:", err);
      return null;
    }
  }, [gameId, playerToken, setBoardArray]);

  const fetchHistory = useCallback(async () => {
    try {
      const data = await GameService.getHistory(gameId);
      setMovesStack(data.moves || []);
    } catch (err) {
      console.error("Failed to fetch history:", err);
    }
  }, [gameId]);

  // Poll for state updates
  useEffect(() => {
    fetchState();
    fetchHistory();

    pollRef.current = setInterval(() => {
      fetchState();
      fetchHistory();
    }, 1500);

    return () => clearInterval(pollRef.current);
  }, [fetchState, fetchHistory]);

  const onMoveSelection = useCallback(
    async (moveIndex) => {
      try {
        const result = await GameService.submitMove(gameId, playerToken, {
          move_index: moveIndex,
        });
        setGameState(result);
        if (result.board) {
          setBoardArray(result.board);
        }
        fetchHistory();
      } catch (err) {
        console.error("Move failed:", err);
      }
    },
    [gameId, playerToken, setBoardArray, fetchHistory]
  );

  const status = gameState?.status || "waiting";
  const turn = gameState?.turn || "black";
  const yourTurn = gameState?.your_turn || false;
  const captures = gameState?.captures || { black: 0, white: 0 };
  const legalMoves = gameState?.legal_moves || [];
  const moveNumber = gameState?.move_number || 0;
  const winner = gameState?.winner;
  const isGameActive = status === "in_progress";
  const currentTurn = turn === "black" ? 1 : 2;

  return (
    <Grid
      container
      sx={{ justifyContent: "center", alignItems: "flex-start", minHeight: "100vh", backgroundColor: "#302e2b" }}
    >
      {/* Header bar */}
      <Grid item xs={12} sx={{ p: 1, display: "flex", alignItems: "center", gap: 2 }}>
        <Button variant="outlined" size="small" onClick={onLeave} sx={{ color: "white", borderColor: "rgba(255,255,255,0.3)" }}>
          Leave
        </Button>
        <Chip label={`Game: ${gameId}`} size="small" sx={{ color: "white", backgroundColor: "rgba(255,255,255,0.1)" }} />
        <Chip label={`You: ${playerColor}`} size="small" sx={{ color: "white", backgroundColor: playerColor === "black" ? "#333" : "#ccc", fontWeight: 600 }} />

        {status === "waiting" && (
          <Typography sx={{ color: "orange", fontSize: "0.9rem" }}>
            Waiting for opponent to join...
          </Typography>
        )}
        {status === "in_progress" && (
          <Typography sx={{ color: yourTurn ? "#4caf50" : "rgba(255,255,255,0.5)", fontSize: "0.9rem", fontWeight: yourTurn ? 700 : 400 }}>
            {yourTurn ? "Your turn" : `${turn}'s turn`} &middot; Move #{moveNumber + 1}
          </Typography>
        )}
        {status === "game_over" && (
          <Typography sx={{ color: "#f44336", fontSize: "0.9rem", fontWeight: 700 }}>
            Game Over! {winner ? `${winner} wins` : "Draw"}
          </Typography>
        )}

        <Typography sx={{ color: "rgba(255,255,255,0.6)", fontSize: "0.85rem", ml: "auto" }}>
          Captured &mdash; Black: {captures.black} &middot; White: {captures.white}
        </Typography>
      </Grid>

      {/* Board */}
      <Grid
        container
        item
        xs={8}
        sx={{ justifyContent: "center", alignItems: "center", height: "88vh", padding: "5px" }}
      >
        <GameplaySection
          boardArray={boardArray}
          onMoveSelection={onMoveSelection}
          selectedMarbles={selectedMarbles}
          setSelectedMarbles={setSelectedMarbles}
          isGameActive={isGameActive && yourTurn}
          currentTurn={currentTurn}
          legalMoves={legalMoves}
          numCapturedBlackMarbles={captures.black}
          numCapturedWhiteMarbles={captures.white}
        />
      </Grid>

      {/* Sidebar */}
      <Grid item xs={4} sx={{ height: "88vh", padding: "5px", overflowY: "auto" }}>
        <MoveHistory movesStack={movesStack} />

        {isGameActive && yourTurn && legalMoves.length > 0 && (
          <Typography sx={{ color: "rgba(255,255,255,0.5)", fontSize: "0.8rem", mt: 2, textAlign: "center" }}>
            {legalMoves.length} legal moves available
          </Typography>
        )}
      </Grid>
    </Grid>
  );
};

export default Game;
