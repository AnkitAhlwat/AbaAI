import { Box } from "@mui/material";

const SideBar = (props) => {
  const { children } = props;

  return (
    <Box
      sx={{
        backgroundColor: "#262522",
        borderRadius: "5px",
        height: "100%",
        padding: "10px",
      }}
    >
      {children}
    </Box>
  );
};

export default SideBar;
