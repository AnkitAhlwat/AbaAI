import axios from 'axios';

// Handles requests to the server end
class GameService {

    // Posts config options to python server
    static async postConfig(config) {
        try {
            const url = `${import.meta.env.VITE_API_BASE_URL}/game/configure`
            const response = await axios.post(url, config)
            console.log(response.data)
        } catch (error) {
            console.error('Error setting config')
        }
    }

    static async startGame() {
        try {
            const url = `${import.meta.env.VITE_API_BASE_URL}/game/start`
            const response = await axios.post(url)
            console.log(response.data)
        } catch (error) {
            console.error('Error starting game')
        }
    }

    // Posts move request to python server
    static async postMove(move) {
        try {
            const url = `${import.meta.env.VITE_API_BASE_URL}/game/move`;
            const response = await axios.post(url, move);
            return response.data;
        } catch (error) {
            console.error('Error making move:', error);
        }
    }

    // Posts undo move request to python server
    static async postUndoLastMove() {
        try {
            const url = `${import.meta.env.VITE_API_BASE_URL}/game/undo`;
            const response = await axios.post(url);
            return response.data;
        } catch (error) {
            console.error('Error undoing last move:', error);
        }
    }

    // Posts reset request to python server
    static async postResetGame() {
        try {
            const url = `${import.meta.env.VITE_API_BASE_URL}/game/reset`;
            const response = await axios.post(url);
            return response.data;
        } catch (error) {
            console.error('Error resetting game:', error);
        }
    }

    static async getPossibleMoves() {
        try {
            const url = `${import.meta.env.VITE_API_BASE_URL}/game/possibleMoves`;
            const response = await axios.get(url);
            return response.data;
        } catch (error) {
            console.error('Error getting possible moves:', error);
        }
    }

    static async getAiMoveForCurrentState() {
        try {
            const url = `${import.meta.env.VITE_API_BASE_URL}/game/aiMove`;
            const response = await axios.get(url);
            return response.data;
        } catch (error) {
            console.error('Error getting ai move:', error);
        }
    }
    
    static async getGameStatus() {
        try {
            const url = `${import.meta.env.VITE_API_BASE_URL}/game`;
            const response = await axios.get(url);
            return response.data;
        } catch (error) {
            console.error('Error getting game status:', error);
        }
    }
}


export default GameService;