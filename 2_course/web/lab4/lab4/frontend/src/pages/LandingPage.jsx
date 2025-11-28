import Header from '../components/Header';
import LoginForm from '../components/LoginForm';
import './LandingPage.css';

const LandingPage = () => {
    return (
        <div className="landing-page">
            <Header />
            <section className="landing-page__hero">
                <div>
                    <p className="eyebrow">Лабораторная работа №4</p>
                    <h1>SpringBoot + React + PostgreSQL</h1>
                </div>
                <LoginForm />
            </section>
        </div>
    );
};

export default LandingPage;
