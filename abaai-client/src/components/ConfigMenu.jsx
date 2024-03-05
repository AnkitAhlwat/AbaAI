import Box from "@mui/material/Box";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import { BoardLayouts } from "../constants/boardLayouts";
import PropTypes from "prop-types";

const ConfigMenu = (props) => {
  const { config, setConfig } = props;

  const handleLayoutChange = (event) => {
    setConfig({ ...config, boardLayout: event.target.value });
  };

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
    </Box>
  );
};

ConfigMenu.propTypes = {
  config: PropTypes.object.isRequired,
  setConfig: PropTypes.func.isRequired,
};

export default ConfigMenu;
