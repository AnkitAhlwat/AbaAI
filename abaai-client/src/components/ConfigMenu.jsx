import Box from "@mui/material/Box";
import FormControl from "@mui/material/FormControl";
import Button from "@mui/material/Button";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import { BoardLayouts } from "../constants/boardLayouts";
import PropTypes from "prop-types";
import { useState } from "react";
import { TextField } from "@mui/material";
import GameService from "../services/game.service";

const SelectInput = ({ label, value, onChange, options }) => (
  <FormControl
    sx={{ width: 1 }}
    variant="filled"
    style={{ backgroundColor: "gray" }}
  >
    <InputLabel style={{ fontWeight: "bold", color: "white" }}>
      {label}
    </InputLabel>
    <Select value={value} onChange={onChange} style={{ color: "white" }}>
      {options.map((option) => (
        <MenuItem key={option} value={option}>
          {option}
        </MenuItem>
      ))}
    </Select>
  </FormControl>
);

const NumberInput = ({ id, label, value, onChange }) => (
  <FormControl
    sx={{ width: 1 }}
    variant="filled"
    style={{ backgroundColor: "gray" }}
  >
    <TextField
      id={id}
      label={label}
      type="number"
      value={value}
      onInput={onChange}
      InputProps={{ style: { color: "white" } }}
      InputLabelProps={{ style: { color: "white" } }}
    />
  </FormControl>
);

const ConfigMenu = ({ config, setConfig, onSubmitConfig, switchToGameTab }) => {
  const handleLayoutChange = (event) =>
    setConfig({ ...config, boardLayout: event.target.value });
  const handlePlayerChange = (event, player) =>
    setConfig({ ...config, [player]: event.target.value });
  const handleSubmit = async () => {
    onSubmitConfig();
    switchToGameTab();
  };

  if (!config) return null;

  return (
    <Box style={{ margin: "auto", textAlign: "center" }}>
      <SelectInput
        label="Board Layout"
        value={config.boardLayout}
        onChange={handleLayoutChange}
        options={Object.values(BoardLayouts)}
      />
      <br />
      <br />
      <SelectInput
        label="Black Player"
        value={config.blackPlayer}
        onChange={(e) => handlePlayerChange(e, "blackPlayer")}
        options={["Human", "Computer"]}
      />
      <br />
      <br />
      <SelectInput
        label="White Player"
        value={config.whitePlayer}
        onChange={(e) => handlePlayerChange(e, "whitePlayer")}
        options={["Human", "Computer"]}
      />
      <br />
      <br />
      <NumberInput
        id="black-time-limit"
        label="Black Time Limit (Seconds)"
        value={config.blackTimeLimit}
        onChange={(e) => {
          if (e.target.value && e.target.value >= 0) {
            setConfig({ ...config, blackTimeLimit: parseInt(e.target.value) });
          } else {
            setConfig({ ...config, blackTimeLimit: "" });
          }
        }}
      />
      <br />
      <br />
      <NumberInput
        id="white-time-limit"
        label="White Time Limit (Seconds)"
        value={config.whiteTimeLimit}
        onChange={(e) => {
          if (e.target.value && e.target.value >= 0) {
            setConfig({ ...config, whiteTimeLimit: parseInt(e.target.value) });
          } else {
            setConfig({ ...config, whiteTimeLimit: "" });
          }
        }}
      />
      <br />
      <br />
      <NumberInput
        id="move-limit"
        label="Move Limit"
        value={config.moveLimit}
        onChange={(e) => {
          if (e.target.value && e.target.value >= 0) {
            setConfig({ ...config, moveLimit: parseInt(e.target.value) });
          } else {
            setConfig({ ...config, moveLimit: "" });
          }
        }}
      />
      <br />
      <br />
      <FormControl variant="filled">
        <Button variant="contained" onClick={handleSubmit}>
          Submit
        </Button>
      </FormControl>
    </Box>
  );
};

ConfigMenu.propTypes = {
  config: PropTypes.object,
  setConfig: PropTypes.func.isRequired,
  onSubmitConfig: PropTypes.func.isRequired,
  switchToGameTab: PropTypes.func.isRequired,
};

export default ConfigMenu;
