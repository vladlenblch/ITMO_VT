import apiClient from './apiClient';

const authApi = {
    register: (credentials) => apiClient.post('/auth/register', credentials),
    login: (credentials) => apiClient.post('/auth/login', credentials),
    logout: () => apiClient.post('/auth/logout'),
    me: () => apiClient.get('/auth/me'),
};

export default authApi;
