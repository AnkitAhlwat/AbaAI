import { useState } from "react";
import SideBar from "./SideBar";
import ConfigMenu from "./ConfigMenu";
import { TabContext, TabList, TabPanel } from "@mui/lab";
import { Box, Tab } from "@mui/material";
import CurrentGameBar from "./CurrentGameBar";

const RightSideBar = (props) => {
  const { config, setConfig, movesStack, aiMove } = props;

  const [value, setValue] = useState("2");
  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <SideBar>
      <TabContext value={value}>
        <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
          <TabList onChange={handleChange}>
            <Tab label="Current Game" value="1" sx={{ color: "white" }} />
            <Tab label="Game Configuration" value="2" sx={{ color: "white" }} />
          </TabList>
        </Box>
        <TabPanel value="1">
          <CurrentGameBar movesStack={movesStack} aiMove={aiMove} />
        </TabPanel>
        <TabPanel value="2">
          <ConfigMenu config={config} setConfig={setConfig} />
        </TabPanel>
      </TabContext>
    </SideBar>
  );
};

export default RightSideBar;
