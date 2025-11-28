import { configureStore } from '@reduxjs/toolkit';
import authReducer from '../features/auth/authSlice';
import pointsReducer from '../features/points/pointsSlice';

const store = configureStore({
    reducer: {
        auth: authReducer,
        points: pointsReducer,
    },
});

export default store;
