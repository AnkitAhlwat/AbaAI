import React from 'react';
import { Grid, Paper, Avatar, Typography } from '@mui/material';
import AIAvatar from '../assets/robot.png';

// Displays each move the AI mades on the GUI interface
const AIMoveDisplay = ({ aiMove }) => {
    return (
        <Paper elevation={3} style={{ padding: '20px', margin: '20px' }}>
            <Grid container alignItems="center" spacing={2}>
                <Grid item>
                    <Avatar src={AIAvatar} alt="AI Avatar"/>
                </Grid>
                <Grid item>
                    <Typography variant="h6">AI Move:</Typography>
                    <Typography variant="subtitle1" gutterBottom>
                        {aiMove}
                    </Typography>
                </Grid>
            </Grid>
        </Paper>
    );
};

export default AIMoveDisplay;