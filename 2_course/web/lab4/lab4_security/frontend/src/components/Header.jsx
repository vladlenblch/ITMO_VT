import { useSelector } from 'react-redux';
import './Header.css';

const Header = () => {
    const userLogin = useSelector((state) => state.auth.user?.username);

    return (
        <header className="app-header">
            <div className="app-header__identity">
                <p className="app-header__label">{userLogin ? 'Пользователь' : 'ФИО'}</p>
                <p className="app-header__value">{userLogin ?? 'Ларионов Владислав Васильевич'}</p>
            </div>
            {!userLogin && (
                <>
                    <div className="app-header__identity">
                        <p className="app-header__label">Группа</p>
                        <p className="app-header__value">P3209</p>
                    </div>
                    <div className="app-header__identity">
                        <p className="app-header__label">Вариант</p>
                        <p className="app-header__value">254</p>
                    </div>
                </>
            )}
        </header>
    );
};

export default Header;
