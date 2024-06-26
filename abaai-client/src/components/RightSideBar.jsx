import { useEffect, useState } from "react";
import SideBar from "./SideBar";
import ConfigMenu from "./ConfigMenu";
import { TabContext, TabList, TabPanel } from "@mui/lab";
import { Box, Tab } from "@mui/material";
import CurrentGameBar from "./CurrentGameBar";

const Tabs = {
  GAME: "1",
  CONFIG: "2",
};

const RightSideBar = (props) => {
  const {
    config,
    setConfig,
    movesStack,
    blackAiMove,
    whiteAiMove,
    currentTurn,
    activePlayer,
    toggleActivePlayer,
    gameStarted,
    gameActive,
    gameConfigured,
    startGame,
    stopGame,
    pauseGame,
    resumeGame,
    resetGame,
    undoMove,
    undoSignal,
    blackClock,
    whiteClock,
    resetClockSignal,
    onSubmitConfig,
    onApplyMove,
    //onSubmitConfig,
  } = props;

  const [value, setValue] = useState(Tabs.CONFIG);
  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const switchToGameTab = () => {
    setValue(Tabs.GAME);
  };

  const switchToConfigTab = () => {
    setValue(Tabs.CONFIG);
  };

  useEffect(() => {
    if (gameConfigured) {
      switchToGameTab();
    } else {
      switchToConfigTab();
    }
  }, [gameConfigured]);

  return (
    <SideBar>
      <TabContext value={value}>
        <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
          <TabList onChange={handleChange}>
            <Tab
              label="Current Game"
              value={Tabs.GAME}
              sx={{ color: "white" }}
              disabled={!gameConfigured}
            />
            <Tab
              label="Game Configuration"
              value={Tabs.CONFIG}
              sx={{ color: "white" }}
              disabled={gameActive}
            />
          </TabList>
        </Box>
        <TabPanel value={Tabs.GAME}>
          <CurrentGameBar
            config={config}
            movesStack={movesStack}
            blackAiMove={blackAiMove}
            whiteAiMove={whiteAiMove}
            currentTurn={currentTurn}
            //clock controls
            activePlayer={activePlayer}
            toggleActivePlayer={toggleActivePlayer}
            gameStarted={gameStarted}
            gameActive={gameActive}
            startGame={startGame}
            stopGame={stopGame}
            resetClockSignal={resetClockSignal}
            pauseGame={pauseGame}
            resumeGame={resumeGame}
            resetGame={resetGame}
            undoMove={undoMove}
            undoSignal={undoSignal}
            blackClock={blackClock}
            whiteClock={whiteClock}
            onApplyMove={onApplyMove}
            //onSubmitConfig={onSubmitConfig}
            // currentPlayer={currentPlayer}
            // isPaused={isPaused}
            // togglePause={togglePause}
          />
        </TabPanel>
        <TabPanel value={Tabs.CONFIG}>
          <ConfigMenu
            config={config}
            setConfig={setConfig}
            onSubmitConfig={onSubmitConfig}
            switchToGameTab={switchToGameTab}
          />
        </TabPanel>
      </TabContext>
    </SideBar>
  );
};

export default RightSideBar;
