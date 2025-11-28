import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { logout, clearAuthState } from '../features/auth/authSlice';
import { clearPoints } from '../features/points/pointsSlice';
import './LogoutButton.css';

const LogoutButton = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleLogout = () => {
        dispatch(logout());
        dispatch(clearAuthState());
        dispatch(clearPoints());
        navigate('/', { replace: true });
    };

    return (
        <button type="button" className="logout-button" onClick={handleLogout}>
            Выйти
        </button>
    );
};

export default LogoutButton;
