import apiClient from './apiClient';

const authApi = {
    register: (credentials) => apiClient.post('/auth/register', credentials),
    login: (credentials) => apiClient.post('/auth/login', credentials),
    logout: () => apiClient.post('/auth/logout'),
    me: () => apiClient.get('/auth/me'),
    listCredentials: () => apiClient.get('/auth/credentials'),
    setPassword: (payload) => apiClient.post('/auth/credentials/password', payload),
    deleteCredential: (id) => apiClient.delete(`/auth/credentials/${id}`),
};

export default authApi;
