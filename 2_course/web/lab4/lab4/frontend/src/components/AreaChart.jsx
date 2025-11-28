import { useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { submitPoint } from '../features/points/pointsSlice';
import './AreaChart.css';

const CHART_SIZE = 300;
const PADDING = 0;
const DRAW_SIZE = CHART_SIZE - PADDING * 2;
const MAX_COORD = 4.5;
const SCALE = DRAW_SIZE / (MAX_COORD * 2);
const HALF = CHART_SIZE / 2;
const AREA_COLOR = 'rgba(60,116,255,0.8)';
const AXIS_MARKS = [1, 2, 3, 4];

const formatValue = (value) => Math.round(value * 100) / 100;

const AreaChart = () => {
    const dispatch = useDispatch();
    const svgRef = useRef(null);
    const { items, currentRadius } = useSelector((state) => state.points);
    const displayRadius = Math.max(currentRadius, 1);
    const latestPoint = items[0];

    const toSvgX = (value) => HALF + value * SCALE;
    const toSvgY = (value) => HALF - value * SCALE;

    const handleChartClick = (event) => {
        if (currentRadius <= 0) {
            return;
        }
        const rect = svgRef.current.getBoundingClientRect();
        const relativeX = event.clientX - rect.left;
        const relativeY = event.clientY - rect.top;
        const coordX = (relativeX - HALF) / SCALE;
        const coordY = (HALF - relativeY) / SCALE;
        dispatch(
            submitPoint({
                x: formatValue(coordX),
                y: formatValue(coordY),
                r: currentRadius,
            }),
        );
    };

    const trianglePath = `M ${toSvgX(0)} ${toSvgY(0)} L ${toSvgX(-displayRadius)} ${toSvgY(0)} L ${toSvgX(0)} ${toSvgY(displayRadius / 2)} Z`;
    const quarterArc = `
        M ${toSvgX(0)} ${toSvgY(0)}
        L ${toSvgX(-displayRadius)} ${toSvgY(0)}
        A ${displayRadius * SCALE} ${displayRadius * SCALE} 0 0 0 ${toSvgX(0)} ${toSvgY(-displayRadius)}
        Z
    `;

    return (
        <div className="area-chart">
            <svg
                ref={svgRef}
                width={CHART_SIZE}
                height={CHART_SIZE}
                viewBox={`0 0 ${CHART_SIZE} ${CHART_SIZE}`}
                onClick={handleChartClick}
            >
                <rect
                    x={PADDING}
                    y={PADDING}
                    width={DRAW_SIZE}
                    height={DRAW_SIZE}
                    fill="#f9fafb"
                    rx="24"
                />
                <path d={trianglePath} fill={AREA_COLOR} />
                <path d={quarterArc} fill={AREA_COLOR} />
                <rect
                    x={toSvgX(0)}
                    y={toSvgY(0)}
                    width={displayRadius * SCALE}
                    height={displayRadius * SCALE}
                    fill={AREA_COLOR}
                />
                <line
                    x1={PADDING}
                    y1={HALF}
                    x2={CHART_SIZE - PADDING}
                    y2={HALF}
                    stroke="#1f2937"
                    strokeWidth="2"
                />
                <line
                    x1={HALF}
                    y1={PADDING}
                    x2={HALF}
                    y2={CHART_SIZE - PADDING}
                    stroke="#1f2937"
                    strokeWidth="2"
                />
                {AXIS_MARKS.map((mark) => (
                    <g key={`axis-${mark}`}>
                        <line
                            x1={toSvgX(mark)}
                            x2={toSvgX(mark)}
                            y1={HALF - 5}
                            y2={HALF + 5}
                            stroke="#1f2937"
                        />
                        <line
                            x1={toSvgX(-mark)}
                            x2={toSvgX(-mark)}
                            y1={HALF - 5}
                            y2={HALF + 5}
                            stroke="#1f2937"
                        />
                        <text x={toSvgX(mark)} y={HALF + 18} textAnchor="middle" fontSize="12" fill="#1f2937">
                            {mark}
                        </text>
                        <text
                            x={toSvgX(-mark)}
                            y={HALF + 18}
                            textAnchor="middle"
                            fontSize="12"
                            fill="#1f2937"
                        >
                            {-mark}
                        </text>
                        <line
                            x1={HALF - 5}
                            x2={HALF + 5}
                            y1={toSvgY(mark)}
                            y2={toSvgY(mark)}
                            stroke="#1f2937"
                        />
                        <line
                            x1={HALF - 5}
                            x2={HALF + 5}
                            y1={toSvgY(-mark)}
                            y2={toSvgY(-mark)}
                            stroke="#1f2937"
                        />
                        <text
                            x={HALF + 18}
                            y={toSvgY(mark) + 4}
                            textAnchor="start"
                            fontSize="12"
                            fill="#1f2937"
                        >
                            {mark}
                        </text>
                        <text
                            x={HALF + 18}
                            y={toSvgY(-mark) + 4}
                            textAnchor="start"
                            fontSize="12"
                            fill="#1f2937"
                        >
                            {-mark}
                        </text>
                    </g>
                ))}
                {latestPoint && (
                    <circle
                        cx={toSvgX(latestPoint.x)}
                        cy={toSvgY(latestPoint.y)}
                        r={4}
                        fill={latestPoint.hit ? '#059669' : '#dc2626'}
                        stroke="#111827"
                        strokeWidth="1"
                    />
                )}
            </svg>
        </div>
    );
};

export default AreaChart;
