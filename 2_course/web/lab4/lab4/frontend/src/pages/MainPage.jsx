import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import Header from '../components/Header';
import PointControls from '../components/PointControls';
import AreaChart from '../components/AreaChart';
import ResultsTable from '../components/ResultsTable';
import LogoutButton from '../components/LogoutButton';
import { fetchResults } from '../features/points/pointsSlice';
import './MainPage.css';

const MainPage = () => {
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(fetchResults());
    }, [dispatch]);

    return (
        <div className="main-page">
            <div className="main-page__top-bar">
                <Header />
                <LogoutButton />
            </div>
            <div className="main-page__grid">
                <PointControls />
                <AreaChart />
                <ResultsTable />
            </div>
        </div>
    );
};

export default MainPage;
