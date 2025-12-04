import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
    deleteCredential,
    listCredentials,
} from '../features/auth/authSlice';
import './CredentialsManager.css';

const CredentialsManager = () => {
    const dispatch = useDispatch();
    const { credentials } = useSelector((state) => state.auth);

    useEffect(() => {
        dispatch(listCredentials());
    }, [dispatch]);

    const handleDelete = (id) => {
        dispatch(deleteCredential(id));
    };

    const remainingRecovery = credentials.filter((c) => c.type === 'RECOVERY' && !c.used).length;

    return (
        <div className="credentials-manager">
            <div className="credentials-manager__header">
                <h3>Способы входа</h3>
                <div className="credentials-manager__actions">
                    <span className="credentials-manager__hint">
                        Осталось recovery-кодов: {remainingRecovery}
                    </span>
                </div>
            </div>
            <div className="credentials-manager__list">
                {credentials.length === 0 && <p>Способы входа ещё не настроены.</p>}
                {credentials.map((item) => (
                    <div className="credentials-manager__item" key={item.id}>
                        <div>
                            <p className="credentials-manager__type">
                                {item.type === 'RECOVERY' && (item.displayValue || 'Recovery код')}
                                {item.type === 'PASSWORD' && 'Пароль'}
                                {item.type === 'OWNERSHIP' && 'Право владения (файл)'}
                            </p>
                            <p className="credentials-manager__meta">
                                Создан: {new Date(item.createdAt).toLocaleString()}
                                {item.type === 'RECOVERY' && (
                                    <span className={item.used ? 'used' : 'active'}>
                                        {item.used ? 'использован' : 'не использован'}
                                    </span>
                                )}
                            </p>
                        </div>
                        <button type="button" onClick={() => handleDelete(item.id)}>
                            Удалить
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CredentialsManager;
