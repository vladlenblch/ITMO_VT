import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { login, register } from '../features/auth/authSlice';
import { credentialsSchema, loginSchema } from '../validation/schemas';
import './LoginForm.css';

const LoginForm = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { status, error, token, recoveryCodes, ownershipFilePath, ownershipFileContent } = useSelector((state) => state.auth);
    const [formValues, setFormValues] = useState({
        username: '',
        password: '',
        credentialType: 'password',
        value: '',
    });
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
        if (formError) {
            setFormError(null);
        }
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        if (isRegisterMode) {
            const result = credentialsSchema.safeParse(formValues);
            if (!result.success) {
                setFormError(result.error.issues[0]?.message || 'Проверьте данные для входа');
                return;
            }
            setFormError(null);
            dispatch(register(result.data));
        } else {
            const result = loginSchema.safeParse({
                username: formValues.username,
                credentialType: formValues.credentialType,
                value: formValues.credentialType === 'ownership'
                    ? 'file-present'
                    : (formValues.value || formValues.password),
            });
            if (!result.success) {
                setFormError(result.error.issues[0]?.message || 'Проверьте данные для входа');
                return;
            }
            const payload = {
                username: result.data.username,
                credentialType: result.data.credentialType.toUpperCase(),
                value: result.data.value,
            };
            setFormError(null);
            dispatch(login(payload));
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
            {isRegisterMode ? (
                <label>
                    Пароль
                    <input
                        type="password"
                        name="password"
                        value={formValues.password}
                        onChange={handleChange}
                        autoComplete="new-password"
                        placeholder="Пароль"
                    />
                </label>
            ) : (
                <>
                    <div className="login-form__segmented">
                        <button
                            type="button"
                            className={formValues.credentialType === 'password' ? 'active' : ''}
                            onClick={() => setFormValues((prev) => ({ ...prev, credentialType: 'password', value: '' }))}
                        >
                            Пароль
                        </button>
                        <button
                            type="button"
                            className={formValues.credentialType === 'recovery' ? 'active' : ''}
                            onClick={() => setFormValues((prev) => ({ ...prev, credentialType: 'recovery', value: '' }))}
                        >
                            Резервный код
                        </button>
                        <button
                            type="button"
                            className={formValues.credentialType === 'ownership' ? 'active' : ''}
                            onClick={() => setFormValues((prev) => ({ ...prev, credentialType: 'ownership', value: '' }))}
                        >
                            Право владения
                        </button>
                    </div>
                    {formValues.credentialType === 'password' && (
                        <label>
                            Пароль
                            <input
                                type="password"
                                name="value"
                                value={formValues.value}
                                onChange={handleChange}
                                autoComplete="current-password"
                                placeholder="Пароль"
                            />
                        </label>
                    )}
                    {formValues.credentialType === 'recovery' && (
                        <label>
                            Резервный код
                            <input
                                type="text"
                                name="value"
                                value={formValues.value}
                                onChange={handleChange}
                                autoComplete="one-time-code"
                                placeholder="Вставьте одноразовый код"
                            />
                        </label>
                    )}
                </>
            )}
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
            {isRegisterMode && (!!recoveryCodes.length || ownershipFilePath) && (
                <div className="login-form__recovery">
                    {!!ownershipFilePath && (
                        <>
                            <p>Создан файл права владения:</p>
                            <code>{ownershipFilePath}</code>
                            {ownershipFileContent && <p>Токен в файле: {ownershipFileContent}</p>}
                        </>
                    )}
                    {!!recoveryCodes.length && (
                        <>
                            <p>Сохраните эти 5 recovery-кодов — каждый работает один раз:</p>
                            <ul>
                                {recoveryCodes.map((code) => <li key={code}>{code}</li>)}
                            </ul>
                        </>
                    )}
                </div>
            )}
        </form>
    );
};

export default LoginForm;
