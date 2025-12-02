import './App.css';
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import MainPage from './pages/MainPage';
import ProtectedRoute from './routes/ProtectedRoute';
import { fetchCurrentUser } from './features/auth/authSlice';

const App = () => {
    const dispatch = useDispatch();
    const token = useSelector((state) => state.auth.token);

    useEffect(() => {
        if (token) {
            dispatch(fetchCurrentUser());
        }
    }, [token, dispatch]);

    return (
        <div className="App">
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route
                    path="/app"
                    element={(
                        <ProtectedRoute>
                            <MainPage />
                        </ProtectedRoute>
                    )}
                />
            </Routes>
        </div>
    );
};

export default App;
