import { useSelector } from 'react-redux';
import './ResultsTable.css';

const ResultsTable = () => {
    const { items, status } = useSelector((state) => state.points);

    if (status === 'loading') {
        return <div className="results-table results-table__placeholder">Загружаем историю...</div>;
    }

    if (!items.length) {
        return (
            <div className="results-table results-table__placeholder">
                История проверок будет отображаться здесь
            </div>
        );
    }

    return (
        <div className="results-table">
            <table>
                <thead>
                    <tr>
                        <th>X</th>
                        <th>Y</th>
                        <th>R</th>
                        <th>Попадание</th>
                        <th>Время</th>
                    </tr>
                </thead>
                <tbody>
                    {items.map((item) => (
                        <tr key={item.id ?? `${item.x}-${item.y}-${item.timestamp}`}>
                            <td>{item.x}</td>
                            <td>{item.y}</td>
                            <td>{item.r}</td>
                            <td>
                                <span className={item.hit ? 'hit' : 'miss'}>
                                    {item.hit ? 'Да' : 'Нет'}
                                </span>
                            </td>
                            <td>{new Date(item.timestamp).toLocaleString()}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ResultsTable;
