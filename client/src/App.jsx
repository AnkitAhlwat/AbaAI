import { useState } from "react";
import Game from "./components/Game";
import Lobby from "./components/Lobby";

function App() {
  const [session, setSession] = useState(null);

  const handleGameJoined = (gameId, token, color) => {
    setSession({ gameId, token, color });
  };

  const handleLeaveGame = () => {
    setSession(null);
  };

  if (!session) {
    return <Lobby onGameJoined={handleGameJoined} />;
  }

  return (
    <Game
      gameId={session.gameId}
      playerToken={session.token}
      playerColor={session.color}
      onLeave={handleLeaveGame}
    />
  );
}

export default App;
