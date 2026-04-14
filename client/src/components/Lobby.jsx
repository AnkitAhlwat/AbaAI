import { useState } from "react";
import {
  Box,
  Button,
  TextField,
  Typography,
  Paper,
  Stack,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Divider,
} from "@mui/material";
import GameService from "../services/game.service";

const Lobby = ({ onGameJoined }) => {
  const [joinGameId, setJoinGameId] = useState("");
  const [layout, setLayout] = useState("Default");
  const [error, setError] = useState(null);
  const [createdGameId, setCreatedGameId] = useState(null);

  const handleCreate = async () => {
    try {
      setError(null);
      const data = await GameService.createGame(layout);
      setCreatedGameId(data.game_id);
      onGameJoined(data.game_id, data.token, data.color);
    } catch (err) {
      setError("Failed to create game");
    }
  };

  const handleJoin = async () => {
    if (!joinGameId.trim()) return;
    try {
      setError(null);
      const data = await GameService.joinGame(joinGameId.trim());
      onGameJoined(data.game_id, data.token, data.color);
    } catch (err) {
      setError("Failed to join game — check the game ID");
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        backgroundColor: "#302e2b",
      }}
    >
      <Paper
        elevation={6}
        sx={{
          padding: 5,
          maxWidth: 440,
          width: "100%",
          backgroundColor: "#3d3a37",
          color: "white",
        }}
      >
        <Typography variant="h4" align="center" gutterBottom sx={{ fontWeight: 700 }}>
          AbaAI
        </Typography>
        <Typography variant="subtitle1" align="center" sx={{ mb: 3, opacity: 0.7 }}>
          Abalone Game Platform
        </Typography>

        <Stack spacing={2}>
          <FormControl fullWidth size="small">
            <InputLabel sx={{ color: "rgba(255,255,255,0.6)" }}>Board Layout</InputLabel>
            <Select
              value={layout}
              label="Board Layout"
              onChange={(e) => setLayout(e.target.value)}
              sx={{ color: "white", ".MuiOutlinedInput-notchedOutline": { borderColor: "rgba(255,255,255,0.3)" } }}
            >
              <MenuItem value="Default">Default</MenuItem>
              <MenuItem value="Belgian Daisy">Belgian Daisy</MenuItem>
              <MenuItem value="German Daisy">German Daisy</MenuItem>
            </Select>
          </FormControl>

          <Button
            variant="contained"
            fullWidth
            onClick={handleCreate}
            sx={{ py: 1.5, fontWeight: 600, fontSize: "1rem" }}
          >
            Create Game
          </Button>

          {createdGameId && (
            <Typography variant="body2" align="center" sx={{ opacity: 0.7 }}>
              Game ID: <strong>{createdGameId}</strong> — share with your opponent
            </Typography>
          )}
        </Stack>

        <Divider sx={{ my: 3, borderColor: "rgba(255,255,255,0.2)" }} />

        <Stack spacing={2}>
          <TextField
            label="Game ID"
            variant="outlined"
            size="small"
            fullWidth
            value={joinGameId}
            onChange={(e) => setJoinGameId(e.target.value)}
            sx={{
              input: { color: "white" },
              label: { color: "rgba(255,255,255,0.6)" },
              ".MuiOutlinedInput-notchedOutline": { borderColor: "rgba(255,255,255,0.3)" },
            }}
          />
          <Button
            variant="outlined"
            fullWidth
            onClick={handleJoin}
            sx={{ py: 1.5, fontWeight: 600, fontSize: "1rem", color: "white", borderColor: "rgba(255,255,255,0.4)" }}
          >
            Join Game
          </Button>
        </Stack>

        {error && (
          <Typography color="error" align="center" sx={{ mt: 2 }}>
            {error}
          </Typography>
        )}
      </Paper>
    </Box>
  );
};

export default Lobby;
