import apiClient from './apiClient';

const pointsApi = {
    fetchResults: () => apiClient.get('/points'),
    submitPoint: (payload) => apiClient.post('/points', payload),
};

export default pointsApi;
