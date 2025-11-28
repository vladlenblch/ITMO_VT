import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setRadius, submitPoint } from '../features/points/pointsSlice';
import './PointControls.css';

const X_VALUES = [-4, -3, -2, -1, 0, 1, 2, 3, 4];
const R_VALUES = [1, 2, 3, 4];

const PointControls = () => {
    const dispatch = useDispatch();
    const { submissionStatus, currentRadius } = useSelector((state) => state.points);
    const [formValues, setFormValues] = useState({
        x: 0,
        y: '',
        r: currentRadius,
    });
    const [error, setError] = useState(null);

    const handleXChange = (value) => {
        setFormValues((prev) => ({ ...prev, x: value }));
    };

    const handleYChange = (event) => {
        setFormValues((prev) => ({ ...prev, y: event.target.value }));
    };

    useEffect(() => {
        setFormValues((prev) => ({ ...prev, r: currentRadius }));
    }, [currentRadius]);

    const handleRadiusChange = (value) => {
        setFormValues((prev) => ({ ...prev, r: value }));
        dispatch(setRadius(value));
    };

    const isYValid = (value) => {
        if (value.trim() === '') {
            return false;
        }
        const numeric = Number(value.replace(',', '.'));
        return !Number.isNaN(numeric) && numeric > -3 && numeric < 5;
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        if (!isYValid(formValues.y)) {
            setError('Y должен быть числом в диапазоне (-3; 5)');
            return;
        }
        if (formValues.r <= 0) {
            setError('R должен быть положительным');
            return;
        }
        setError(null);
        dispatch(
            submitPoint({
                x: formValues.x,
                y: Number(formValues.y.replace(',', '.')),
                r: formValues.r,
            }),
        );
    };

    return (
        <form className="point-controls" onSubmit={handleSubmit}>
            <div className="point-controls__group">
                <p>X координата</p>
                <div className="point-controls__radio-grid">
                    {X_VALUES.map((value) => (
                        <label key={value}>
                            <input
                                type="radio"
                                name="x"
                                value={value}
                                checked={formValues.x === value}
                                onChange={() => handleXChange(value)}
                            />
                            <span>{value}</span>
                        </label>
                    ))}
                </div>
            </div>
            <div className="point-controls__group">
                <label htmlFor="y-input">
                    Y координата (-3; 5)
                    <input
                        id="y-input"
                        type="text"
                        value={formValues.y}
                        onChange={handleYChange}
                        placeholder="Число в промежутке"
                    />
                </label>
            </div>
            <div className="point-controls__group">
                <p>Радиус R</p>
                <div className="point-controls__radio-grid">
                    {R_VALUES.map((value) => (
                        <label key={`r-${value}`}>
                            <input
                                type="radio"
                                name="r"
                                value={value}
                                checked={formValues.r === value}
                                onChange={() => handleRadiusChange(value)}
                            />
                            <span>{value}</span>
                        </label>
                    ))}
                </div>
            </div>
            {(error) && <p className="point-controls__error">{error}</p>}
            <button type="submit" disabled={submissionStatus === 'loading'}>
                {submissionStatus === 'loading' ? 'Отправляем...' : 'Проверить точку'}
            </button>
        </form>
    );
};

export default PointControls;
