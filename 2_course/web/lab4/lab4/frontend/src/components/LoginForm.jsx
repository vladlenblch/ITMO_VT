import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { login, register } from '../features/auth/authSlice';
import './LoginForm.css';

const LoginForm = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { status, error, token } = useSelector((state) => state.auth);
    const [formValues, setFormValues] = useState({ username: '', password: '' });
    const [formError, setFormError] = useState(null);
    const [mode, setMode] = useState('login');
    const isRegisterMode = mode === 'register';

    useEffect(() => {
        setFormError(error || null);
    }, [error]);

    useEffect(() => {
        if (token) {
            navigate('/app', { replace: true });
        }
    }, [token, navigate]);

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormValues((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        if (!formValues.username.trim() || !formValues.password.trim()) {
            setFormError('Введите логин и пароль');
            return;
        }
        setFormError(null);
        if (isRegisterMode) {
            dispatch(register(formValues));
        } else {
            dispatch(login(formValues));
        }
    };

    return (
        <form className="login-form" onSubmit={handleSubmit} noValidate>
            <h2>{isRegisterMode ? 'Регистрация' : 'Вход в систему'}</h2>
            <label>
                Логин
                <input
                    type="text"
                    name="username"
                    value={formValues.username}
                    onChange={handleChange}
                    autoComplete="username"
                    placeholder="Логин"
                />
            </label>
            <label>
                Пароль
                <input
                    type="password"
                    name="password"
                    value={formValues.password}
                    onChange={handleChange}
                    autoComplete="current-password"
                    placeholder="Пароль"
                />
            </label>
            {(formError) && <p className="login-form__error">{formError}</p>}
            <button type="submit" disabled={status === 'loading'}>
                {status === 'loading'
                    ? (isRegisterMode ? 'Создаём...' : 'Входим...')
                    : (isRegisterMode ? 'Создать аккаунт' : 'Войти')}
            </button>
            <button
                type="button"
                className="login-form__toggle"
                onClick={() => setMode(isRegisterMode ? 'login' : 'register')}
            >
                {isRegisterMode ? 'У меня уже есть аккаунт' : 'Создать новый аккаунт'}
            </button>
        </form>
    );
};

export default LoginForm;
