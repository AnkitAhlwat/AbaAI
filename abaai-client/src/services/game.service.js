import axios from 'axios';

class GameService {
    static async postMove(move) {
        try {
            const url = `${import.meta.env.VITE_API_BASE_URL}/game/move`;
            const response = await axios.post(url, move);
            return response.data;
        } catch (error) {
            console.error('Error making move:', error);
        }
    }

    static async postUndoLastMove() {
        try {
            const url = `${import.meta.env.VITE_API_BASE_URL}/game/undo`;
            const response = await axios.post(url);
            return response.data;
        } catch (error) {
            console.error('Error undoing last move:', error);
        }
    }

    static async postResetGame() {
        try {
            const url = `${import.meta.env.VITE_API_BASE_URL}/game/reset`;
            const response = await axios.post(url);
            return response.data;
        } catch (error) {
            console.error('Error resetting game:', error);
        }
    }
}


export default GameService;