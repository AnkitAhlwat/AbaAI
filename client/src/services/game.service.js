import axios from 'axios';

const API = import.meta.env.VITE_API_BASE_URL;

class GameService {

    static async createGame(layout = "Default") {
        const url = `${API}/games`;
        const response = await axios.post(url, { layout });
        return response.data;
    }

    static async joinGame(gameId) {
        const url = `${API}/games/${gameId}/join`;
        const response = await axios.post(url);
        return response.data;
    }

    static async getState(gameId, token) {
        const url = `${API}/games/${gameId}/state`;
        const response = await axios.get(url, {
            headers: { "X-Player-Token": token }
        });
        return response.data;
    }

    static async submitMove(gameId, token, moveData) {
        const url = `${API}/games/${gameId}/move`;
        const response = await axios.post(url, moveData, {
            headers: { "X-Player-Token": token }
        });
        return response.data;
    }

    static async getHistory(gameId) {
        const url = `${API}/games/${gameId}/history`;
        const response = await axios.get(url);
        return response.data;
    }
}

export default GameService;
