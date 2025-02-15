import axios from 'axios';

export const api = axios.create({
    baseURL: 'http://localhost:5000/api',
    headers: {
        'Content-Type': 'application/json',
    }
});

// Add response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        // Handle common error cases
        if (error.response?.status === 401) {
            // Handle unauthorized
            console.error('Unauthorized access');
        }
        if (error.response?.status === 404) {
            // Handle not found
            console.error('Resource not found');
        }
        return Promise.reject(error);
    }
); 