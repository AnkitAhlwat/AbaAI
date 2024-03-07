import Box from "@mui/material/Box";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import { BoardLayouts } from "../constants/boardLayouts";
import PropTypes from "prop-types";
import { PlayerColors } from "../constants/playerColors";

const ConfigMenu = (props) => {
  // Destructuring props to extract config and setConfig
  const { config, setConfig } = props;

  // Function to handle changes in the board layout
  const handleLayoutChange = (event) => {
    // Update the config state with the new boardLayout value
    setConfig({ ...config, boardLayout: event.target.value });
  };

  const handleColorChange = (event) => {
    setConfig({ ...config, playerColor: event.target.value })
  }

  const handleGameModeChange = (event) => {
    setConfig({ ...config, gameMode: event.target.value })
  }

  return (
    <Box>
      <FormControl>
        <InputLabel>Board Layout</InputLabel>
        <Select value={config.boardLayout} onChange={handleLayoutChange}>
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
        <Select value={config.playerColor} onChange={handleColorChange}>
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
        <Select value={config.gameMode} onChange={handleGameModeChange}>
          {Object.values(["Human","Computer"]).map((mode) => (
            <MenuItem key={mode} value={mode}>
              {mode}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>
  );
};

ConfigMenu.propTypes = {
  config: PropTypes.object.isRequired,
  setConfig: PropTypes.func.isRequired,
};

export default ConfigMenu;
