import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setRadius, submitPoint } from '../features/points/pointsSlice';
import { pointSchema, validationConstants } from '../validation/schemas';
import './PointControls.css';

const PointControls = () => {
    const dispatch = useDispatch();
    const { submissionStatus, currentRadius, error: serverError } = useSelector((state) => state.points);
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

    useEffect(() => {
        if (serverError) {
            setError(serverError);
        }
    }, [serverError]);

    const handleSubmit = (event) => {
        event.preventDefault();
        const result = pointSchema.safeParse({
            x: formValues.x,
            y: formValues.y,
            r: formValues.r,
        });

        if (!result.success) {
            setError(result.error.issues[0]?.message || 'Проверьте корректность данных');
            return;
        }

        setError(null);
        dispatch(submitPoint(result.data));
    };

    return (
        <form className="point-controls" onSubmit={handleSubmit}>
            <div className="point-controls__group">
                <p>X координата</p>
                <div className="point-controls__radio-grid">
                    {validationConstants.ALLOWED_X_VALUES.map((value) => (
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
                    {validationConstants.ALLOWED_R_VALUES.map((value) => (
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
