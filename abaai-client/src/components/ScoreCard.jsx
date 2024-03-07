import React from 'react';
import { Card, CardContent, Typography, Grid } from '@mui/material';

const ScoreCard = ({ blackSide, whiteSide, }) => {
    // If the game is just starting, initialize the score card to default values
    if (!blackSide || !whiteSide) {
        blackSide = { marblesKnockedOff: 0, totalMoves: 20 };
        whiteSide = { marblesKnockedOff: 0, totalMoves: 20 };
    }
    return (
        <Grid container spacing={2} justifyContent="center">
            <Grid item xs={12} md={6}>
                <Card
                    sx={{
                        backgroundColor: 'blue',
                        color: 'white',
                        borderRadius: '16px',
                        textAlign: 'center',
                        padding: '20px',
                    }}
                    variant="outlined"
                >
                    <CardContent>
                        <Typography variant="h5" gutterBottom sx={{ fontFamily: 'Roboto, sans-serif', fontWeight: 'bold' }}>
                            Black Side
                        </Typography>
                        <Typography sx={{ fontFamily: 'Roboto, sans-serif' }}>Marbles Knocked Off: {blackSide.marblesKnockedOff}</Typography>
                        <Typography sx={{ fontFamily: 'Roboto, sans-serif' }}>Total Moves Left: {blackSide.totalMoves}</Typography>
                    </CardContent>
                </Card>
            </Grid>
            <Grid item xs={12} md={6}>
                <Card
                    sx={{
                        backgroundColor: 'black',
                        color: 'white',
                        borderRadius: '16px',
                        textAlign: 'center',
                        padding: '20px',
                    }}
                    variant="outlined"
                >
                    <CardContent>
                        <Typography variant="h5" gutterBottom sx={{ fontFamily: 'Roboto, sans-serif', fontWeight: 'bold' }}>
                            White Side
                        </Typography>
                        <Typography sx={{ fontFamily: 'Roboto, sans-serif' }}>Marbles Knocked Off: {whiteSide.marblesKnockedOff}</Typography>
                        <Typography sx={{ fontFamily: 'Roboto, sans-serif' }}>Total Moves Left: {whiteSide.totalMoves}</Typography>
                    </CardContent>
                </Card>
            </Grid>
        </Grid>
    );
};

export default ScoreCard;
