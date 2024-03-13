import Box from "@mui/material/Box";
import FormControl from "@mui/material/FormControl";
import Button from "@mui/material/Button"
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import { BoardLayouts } from "../constants/boardLayouts";
import PropTypes from "prop-types";
import { useState } from "react";
import { PlayerColors } from "../constants/playerColors";
import { TextField } from "@mui/material";

const ConfigMenu = (props) => {

  // Destructuring props to extract config and setConfig
  const { config, setConfig } = props;

  // State variables for moveLimit and timeLimit
  const [moveLimit, setMoveLimit] = useState('');
  const [timeLimit, setTimeLimit] = useState('');

  // Function to handle changes in the board layout
  const handleLayoutChange = (event) => {
    setConfig({ ...config, boardLayout: event.target.value });
  };

  // Function to handle change in player color
  const handleColorChange = (event) => {
    setConfig({ ...config, playerColor: event.target.value })
  }

  // Function to handle change to game mode
  const handleGameModeChange = (event) => {
    setConfig({ ...config, gameMode: event.target.value })
  }

  // Function to handle change to move limit
  const handleMoveLimitChange = (event) => {
    setMoveLimit(event.target.value)
  }

  // Function to handle change to time limit
  const handleTimeLimitChange = (event) => {
    setTimeLimit(event.target.value)
  }

  // Update time limit and move limit when button pressed
  const handleSubmit = () => {
    setConfig({
      ...config,
      moveLimit: parseInt(moveLimit), // Convert to integer
      timeLimit: parseInt(timeLimit), // Convert to integer
    })
  }

  // Returns config menu UI component
  return (
    <Box>
      <FormControl>
        <InputLabel>Board Layout</InputLabel>
        <Select value={config.boardLayout} onChange={handleLayoutChange} label="Board Layout">
          {Object.values(BoardLayouts).map((layout) => (
            <MenuItem key={layout} value={layout}>
              {layout}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <br></br>
      <br></br>
      <FormControl>
        <InputLabel>Color</InputLabel>
        <Select value={config.playerColor} onChange={handleColorChange} label="Color">
          {Object.values(PlayerColors).map((color) => (
            <MenuItem key={color} value={color}>
              {color}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <br></br>
      <br></br>
      <FormControl>
        <InputLabel>Game Mode</InputLabel>
        <Select value={config.gameMode} onChange={handleGameModeChange} label="Game Mode">
          {Object.values(["Human","Computer"]).map((mode) => (
            <MenuItem key={mode} value={mode}>
              {mode}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <br></br>
      <br></br>
      <FormControl>
        <TextField
          id="move-limit"
          label="Move Limit"
          type="number"
          value={moveLimit}
          onInput={handleMoveLimitChange}
        />
      </FormControl>
      <br></br>
      <br></br>
      <FormControl>
        <TextField
          id="time-limit"
          label="Time Limit (Seconds)"
          type="number"
          value={timeLimit}
          onInput={handleTimeLimitChange}
        />
      </FormControl>
      <br></br>
      <br></br>
      <FormControl>
        <Button variant="contained" onClick={handleSubmit}>
         Submit
        </Button>
      </FormControl>
    </Box>
  );
};

ConfigMenu.propTypes = {
  config: PropTypes.object.isRequired,
  setConfig: PropTypes.func.isRequired,
};

export default ConfigMenu;
