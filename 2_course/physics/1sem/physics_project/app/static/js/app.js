let socket;
let isRunning = false;
let isCalculating = false;
let calculatedTrajectory = null;
let calcStartTime = null;
let calcCompleted = false;
let currentWindVector = [0, 0, 0];
let calculationsData = null;
const MIN_ARROW_LENGTH = 100;
const HEAD_LENGTH_RATIO = 0.2;
const HEAD_WIDTH_RATIO = 0.08;
const arrowFrame = {
    base: [0, 0, 0],
    length: MIN_ARROW_LENGTH
};

const layout = {
    title: '',
    paper_bgcolor: '#0f1c2c',
    plot_bgcolor: '#0b1624',
    legend: {
        font: {color: '#e6edf3'},
        bgcolor: 'rgba(0,0,0,0)'
    },
    scene: {
        aspectmode: 'data',
        xaxis: {
            backgroundcolor: '#0b1624',
            gridcolor: '#1f3048',
            color: '#b8d7ff',
            showbackground: true
        },
        yaxis: {
            backgroundcolor: '#0b1624',
            gridcolor: '#1f3048',
            color: '#b8d7ff',
            showbackground: true
        },
        zaxis: {
            backgroundcolor: '#0b1624',
            gridcolor: '#1f3048',
            color: '#b8d7ff',
            showbackground: true
        }
    },
    margin: {l: 0, r: 0, b: 0, t: 30}
};

const targetXInput = document.getElementById('target-x');
const targetYInput = document.getElementById('target-y');
const targetZInput = document.getElementById('target-z');

function toInt(val, fallback) {
    const parsed = parseInt(val, 10);
    return Number.isFinite(parsed) ? parsed : fallback;
}

function showCoordError(msg) {
    const el = document.getElementById('coord-error');
    el.innerText = msg;
    el.style.display = 'block';
}

function hideCoordError() {
    const el = document.getElementById('coord-error');
    el.style.display = 'none';
    el.innerText = '';
}

function getTargetStart() {
    return {
        x: Math.max(500, toInt(targetXInput.value, 0)),
        y: Math.max(500, toInt(targetYInput.value, 0)),
        z: Math.max(500, toInt(targetZInput.value, 0))
    };
}

function validateTargetInputs() {
    const x = toInt(targetXInput.value, NaN);
    const y = toInt(targetYInput.value, NaN);
    const z = toInt(targetZInput.value, NaN);
    if (!Number.isFinite(x) || !Number.isFinite(y) || !Number.isFinite(z)) {
        showCoordError('Введите числовые значения для координат (минимум 500).');
        return false;
    }
    if (x < 500 || y < 500 || z < 500) {
        showCoordError('Минимальное значение координат по всем осям - 500.');
        return false;
    }
    hideCoordError();
    return true;
}

function updateArrowFrameFromTarget(targetPoint) {
    if (!targetPoint) return;
    const safeX = Number(targetPoint.x) || 0;
    const safeY = Number(targetPoint.y) || 0;
    arrowFrame.base = [safeX / 2, safeY / 2, 0];
    const diagonal = Math.hypot(Math.abs(safeX), Math.abs(safeY));
    arrowFrame.length = Math.max(diagonal / 6, MIN_ARROW_LENGTH);
}

function getArrowBase() {
    return arrowFrame.base;
}

function getArrowLength() {
    return arrowFrame.length;
}

function restyleTargetPoint() {
    if (isRunning) return;
    const t = getTargetStart();
    Plotly.restyle('graph', { x: [[0]], y: [[0]], z: [[0]] }, [0]);
    Plotly.restyle('graph', { x: [[t.x]], y: [[t.y]], z: [[t.z]] }, [1]);
    updateArrowFrameFromTarget(t);
    updateWindArrowFromVector(currentWindVector);
}

const startTarget = getTargetStart();
updateArrowFrameFromTarget(startTarget);
Plotly.newPlot('graph', [{
    type: 'scatter3d', mode: 'lines+markers', name: 'Ракета',
    x: [0], y: [0], z: [0],
    line: {color: '#ff6b6b', width: 4},
    marker: {color: '#ff6b6b', size: 4}
}, {
    type: 'scatter3d', mode: 'lines+markers', name: 'Цель',
    x: [startTarget.x], y: [startTarget.y], z: [startTarget.z],
    line: {color: '#56ccf2', width: 4},
    marker: {color: '#56ccf2', size: 4}
}, {
    type: 'scatter3d',
    mode: 'lines+markers',
    name: 'Ветер',
    x: [0, 0],
    y: [0, 0],
    z: [0, 0],
    line: {color: '#7cff8c', width: 4},
    marker: {color: '#7cff8c', size: 4},
    hoverinfo: 'skip'
}], layout);

const wsInput = document.getElementById('wind-speed');
const wdInput = document.getElementById('wind-dir');

function sliderWindToVector(speed = Number(wsInput.value), dir = Number(wdInput.value)) {
    const radians = dir * Math.PI / 180;
    return [
        speed * Math.cos(radians),
        speed * Math.sin(radians),
        0
    ];
}

function buildArrowFromVector(vec) {
    const magnitude = Math.hypot(vec[0], vec[1], vec[2]);
    if (magnitude < 1e-6) {
        const base = getArrowBase();
        return {
            x: [base[0], base[0]],
            y: [base[1], base[1]],
            z: [base[2], base[2]]
        };
    }
    const direction = vec.map(component => component / magnitude);
    const base = getArrowBase();
    const length = getArrowLength();
    const headLength = Math.max(length * HEAD_LENGTH_RATIO, MIN_ARROW_LENGTH * 0.2);

    const perp = computePerpendicular(direction);
    const headWidth = Math.max(length * HEAD_WIDTH_RATIO, MIN_ARROW_LENGTH * 0.1);

    const tip = [
        base[0] + direction[0] * length,
        base[1] + direction[1] * length,
        base[2] + direction[2] * length
    ];

    const leftHead = [
        tip[0] - direction[0] * headLength + perp[0] * headWidth,
        tip[1] - direction[1] * headLength + perp[1] * headWidth,
        tip[2] - direction[2] * headLength + perp[2] * headWidth
    ];

    const rightHead = [
        tip[0] - direction[0] * headLength - perp[0] * headWidth,
        tip[1] - direction[1] * headLength - perp[1] * headWidth,
        tip[2] - direction[2] * headLength - perp[2] * headWidth
    ];

    return {
        x: [base[0], tip[0], null, tip[0], leftHead[0], null, tip[0], rightHead[0]],
        y: [base[1], tip[1], null, tip[1], leftHead[1], null, tip[1], rightHead[1]],
        z: [base[2], tip[2], null, tip[2], leftHead[2], null, tip[2], rightHead[2]]
    };
}

function computePerpendicular(direction) {
    let perp = [
        direction[1],
        -direction[0],
        0
    ];
    let norm = Math.hypot(perp[0], perp[1], perp[2]);
    if (norm < 1e-6) {
        perp = [
            0,
            -direction[2],
            direction[1]
        ];
        norm = Math.hypot(perp[0], perp[1], perp[2]);
        if (norm < 1e-6) {
            return [0, 0, 0];
        }
    }
    return perp.map(component => component / norm);
}

function updateWindArrow(arrowData) {
    if (!arrowData || !Array.isArray(arrowData.x) || !Array.isArray(arrowData.y) || !Array.isArray(arrowData.z)) {
        return;
    }
    Plotly.restyle('graph', {
        x: [arrowData.x],
        y: [arrowData.y],
        z: [arrowData.z]
    }, [2]);
}

function updateWindArrowFromVector(vec) {
    currentWindVector = vec.slice();
    updateWindArrow(buildArrowFromVector(vec));
}

function arrowPayloadToVector(payload) {
    if (!payload || !Array.isArray(payload.x) || payload.x.length < 2) return null;
    const dx = payload.x[1] - payload.x[0];
    const yVals = Array.isArray(payload.y) ? payload.y : [0, 0];
    const zVals = Array.isArray(payload.z) ? payload.z : [0, 0];
    const dy = (yVals[1] ?? yVals[0] ?? 0) - (yVals[0] ?? 0);
    const dz = (zVals[1] ?? zVals[0] ?? 0) - (zVals[0] ?? 0);
    return [dx, dy, dz];
}

updateWindArrowFromVector(sliderWindToVector());

function updateInputs() {
    document.getElementById('ws-val').innerText = wsInput.value;
    document.getElementById('wd-val').innerText = wdInput.value;
    if (!isRunning) {
        updateWindArrowFromVector(sliderWindToVector());
    }
    if (isRunning && socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            wind_speed: Number(wsInput.value),
            wind_dir: Number(wdInput.value)
        }));
    }
}

wsInput.oninput = updateInputs;
wdInput.oninput = updateInputs;

function showLoading() {
    document.getElementById('loading-indicator').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading-indicator').style.display = 'none';
}

function showSimulateButton() {
    document.getElementById('simulate-btn').style.display = 'block';
}

function hideSimulateButton() {
    document.getElementById('simulate-btn').style.display = 'none';
}

function resetCalcDuration() {
    const el = document.getElementById('calc-duration');
    el.style.display = 'none';
    el.innerText = 'Время расчета: —';
}

function setCalcDuration(seconds) {
    const el = document.getElementById('calc-duration');
    el.innerText = `Вычисления заняли ${seconds.toFixed(2)} с`;
    el.style.display = 'block';
}

function calculateTrajectory() {
    if (isCalculating) return;
    if (!validateTargetInputs()) return;

    document.getElementById('calculate-btn').disabled = true;
    isCalculating = true;
    calcStartTime = performance.now();
    calcCompleted = false;

    calculatedTrajectory = null;
    hideSimulateButton();
    resetCalcDuration();

    showLoading();

    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    socket = new WebSocket(`${protocol}://${window.location.host}/ws/calculate`);

    socket.onopen = function() {
        socket.send(JSON.stringify({
            wind_speed: Number(wsInput.value),
            wind_dir: Number(wdInput.value),
            target_x: Number(targetXInput.value),
            target_y: Number(targetYInput.value),
            target_z: Number(targetZInput.value),
            action: 'calculate'
        }));
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.status === 'calculating') {
            console.log('расчет траектории начат...');
        }
        else if (data.status === 'calculated') {
            calculatedTrajectory = data.trajectory_data;
            if (calculatedTrajectory && calculatedTrajectory.wind_arrow) {
                const vec = arrowPayloadToVector(calculatedTrajectory.wind_arrow);
                if (vec) updateWindArrowFromVector(vec);
            }
            hideLoading();
            document.getElementById('calculate-btn').disabled = false;
            isCalculating = false;
            showSimulateButton();
            calcCompleted = true;
            if (calcStartTime) {
                const elapsed = (performance.now() - calcStartTime) / 1000;
                setCalcDuration(elapsed);
            }
            console.log('траектория рассчитана успешно');
        }
        else if (data.error) {
            hideLoading();
            document.getElementById('calculate-btn').disabled = false;
            isCalculating = false;
            resetCalcDuration();
            console.error('ошибка расчета:', data.error);
            alert('Ошибка при расчете траектории: ' + data.error);
        }
    };

    socket.onclose = function() {
        isCalculating = false;
        document.getElementById('calculate-btn').disabled = false;
        hideLoading();
        if (!calcCompleted) {
            resetCalcDuration();
        }
        console.log("соединение закрыто");
    };

    socket.onerror = function(error) {
        isCalculating = false;
        document.getElementById('calculate-btn').disabled = false;
        hideLoading();
        if (!calcCompleted) {
            resetCalcDuration();
        }
        console.log("ошибка WebSocket:", error);
    };
}

function startSimulation() {
    if (isRunning || !calculatedTrajectory) return;
    if (!validateTargetInputs()) return;

    document.getElementById('simulate-btn').disabled = true;
    document.getElementById('calculate-btn').disabled = true;
    isRunning = true;

    const startT = getTargetStart();
    Plotly.restyle('graph', {x: [[0]], y: [[0]], z: [[0]]}, [0]);
    Plotly.restyle('graph', {x: [[startT.x]], y: [[startT.y]], z: [[startT.z]]}, [1]);
    updateArrowFrameFromTarget(startT);
    updateWindArrowFromVector(currentWindVector);

    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    socket = new WebSocket(`${protocol}://${window.location.host}/ws/simulate`);

    let mX = [0], mY = [0], mZ = [0];
    let tX = [startT.x], tY = [startT.y], tZ = [startT.z];

    socket.onopen = function() {
        socket.send(JSON.stringify({
            wind_speed: Number(wsInput.value),
            wind_dir: Number(wdInput.value),
            action: 'simulate',
            target_x: Number(targetXInput.value),
            target_y: Number(targetYInput.value),
            target_z: Number(targetZInput.value),
            trajectory_data: calculatedTrajectory
        }));

        document.getElementById('min-dist-row').style.display = 'none';
        document.getElementById('closest-time-row').style.display = 'none';
        document.getElementById('show-calculations-btn').style.display = 'none';
        calculationsData = null;
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);

        const timeStr = (typeof data.time === 'string') ? data.time : Number(data.time).toFixed(2);
        document.getElementById('time-disp').innerText = timeStr;
        document.getElementById('alt-disp').innerText = Math.round(data.missile[2]);
        document.getElementById('dist-disp').innerText = (typeof data.distance === 'number') ? data.distance.toFixed(2) : data.distance;
        if (data.min_distance !== undefined && data.min_distance !== null) {
            document.getElementById('min-dist-disp').innerText = Number(data.min_distance).toFixed(2);
            document.getElementById('min-dist-row').style.display = '';
        }
        if (data.closest_time !== undefined && data.closest_time !== null) {
            document.getElementById('closest-time-disp').innerText = data.closest_time;
            document.getElementById('closest-time-row').style.display = '';
        }
        if (data.missile_speed !== undefined) {
            document.getElementById('speed-disp').innerText = Number(data.missile_speed).toFixed(2);
        }

        if (data.closest_missile_speed !== undefined && data.closest_missile_speed !== null) {
            document.getElementById('speed-disp').innerText = Number(data.closest_missile_speed).toFixed(2);
        }

        mX.push(data.missile[0]);
        mY.push(data.missile[1]);
        mZ.push(data.missile[2]);

        tX.push(data.target[0]);
        tY.push(data.target[1]);
        tZ.push(data.target[2]);
        if (data.wind_arrow) {
            const vec = arrowPayloadToVector(data.wind_arrow);
            if (vec) {
                updateWindArrowFromVector(vec);
            }
        } else if (Array.isArray(data.wind)) {
            updateWindArrowFromVector(data.wind);
        }

        Plotly.restyle('graph', {
            x: [mX, tX],
            y: [mY, tY],
            z: [mZ, tZ]
        }, [0, 1]);

        if (data.calculations) {
            calculationsData = data.calculations;
            document.getElementById('show-calculations-btn').style.display = 'block';
        }

        if (data.hit) {
            isRunning = false;
            document.getElementById('simulate-btn').disabled = false;
            document.getElementById('calculate-btn').disabled = false;
            try { socket.close(); } catch (e) {}
            document.getElementById('min-dist-row').style.display = 'none';
            document.getElementById('closest-time-row').style.display = 'none';
            if (data.missile_speed !== undefined) {
                document.getElementById('speed-disp').innerText = Number(data.missile_speed).toFixed(2);
            }
            console.log('попадание обнаружено, симуляция остановлена.');
        }

        if (data.note === 'simulation_finished_no_hit' || data.note === 'terminated_divergence') {
            isRunning = false;
            document.getElementById('simulate-btn').disabled = false;
            document.getElementById('calculate-btn').disabled = false;
            try { socket.close(); } catch (e) {}
            console.log('симуляция завершена без попадания; итоговая сводка получена.');
            if (data.min_distance !== undefined && data.min_distance !== null) {
                document.getElementById('min-dist-row').style.display = '';
            }
            if (data.closest_time !== undefined && data.closest_time !== null) {
                document.getElementById('closest-time-row').style.display = '';
            }
            if (data.closest_missile_speed !== undefined && data.closest_missile_speed !== null) {
                document.getElementById('speed-disp').innerText = Number(data.closest_missile_speed).toFixed(2);
            }
        }
    };

    socket.onclose = function() {
        isRunning = false;
        document.getElementById('simulate-btn').disabled = false;
        document.getElementById('calculate-btn').disabled = false;
        console.log("соединение закрыто");
    };

    socket.onerror = function(error) {
        isRunning = false;
        document.getElementById('simulate-btn').disabled = false;
        document.getElementById('calculate-btn').disabled = false;
        console.log("ошибка WebSocket:", error);
    };
}

function resetCalculation() {
    calculatedTrajectory = null;
    hideSimulateButton();
    resetCalcDuration();
    calcCompleted = false;
    document.getElementById('show-calculations-btn').style.display = 'none';
    calculationsData = null;
}

wsInput.oninput = function() {
    updateInputs();
    resetCalculation();
};

wdInput.oninput = function() {
    updateInputs();
    resetCalculation();
};

function onTargetInputChange() {
    restyleTargetPoint();
    resetCalculation();
    hideCoordError();
}

targetXInput.oninput = onTargetInputChange;
targetYInput.oninput = onTargetInputChange;
targetZInput.oninput = onTargetInputChange;

function showCalculationsModal() {
    if (!calculationsData) {
        alert('нет данных о расчетах, запустите симуляцию сначала.');
        return;
    }
    
    const modal = document.getElementById('calculations-modal');
    const content = document.getElementById('calculations-content');
    
    let html = '';
    
    html += '<div class="calc-section">';
    html += '<h3>Параметры ракеты</h3>';
    const mp = calculationsData.missile_params;
    html += `<div class="calc-param"><span class="calc-param-label">Масса пустой ракеты:</span><span class="calc-param-value">${mp.mass_empty} кг</span></div>`;
    html += `<div class="calc-param"><span class="calc-param-label">Масса топлива:</span><span class="calc-param-value">${mp.fuel_mass} кг</span></div>`;
    html += `<div class="calc-param"><span class="calc-param-label">Время горения:</span><span class="calc-param-value">${mp.burn_time} с</span></div>`;
    const burnRate = (mp.burn_time > 0) ? (mp.fuel_mass / mp.burn_time) : 0;
    html += `<div class="calc-param"><span class="calc-param-label">Расход топлива:</span><span class="calc-param-value">${burnRate.toFixed(3)} кг/с</span></div>`;
    html += `<div class="calc-param"><span class="calc-param-label">Тяга:</span><span class="calc-param-value">${mp.thrust} Н</span></div>`;
    html += `<div class="calc-param"><span class="calc-param-label">Коэффициент сопротивления:</span><span class="calc-param-value">${mp.drag_coeff}</span></div>`;
    html += `<div class="calc-param"><span class="calc-param-label">Площадь поперечного сечения:</span><span class="calc-param-value">${mp.area} м²</span></div>`;
    html += `<div class="calc-param"><span class="calc-param-label">Широта:</span><span class="calc-param-value">${mp.latitude}°</span></div>`;
    html += '</div>';
    
    html += '<div class="calc-section">';
    html += '<h3>Параметры цели</h3>';
    const tp = calculationsData.target_params;
    html += `<div class="calc-param"><span class="calc-param-label">Начальная позиция (X, Y, Z):</span><span class="calc-param-value">(${tp.initial_pos.x}, ${tp.initial_pos.y}, ${tp.initial_pos.z}) м</span></div>`;
    html += `<div class="calc-param"><span class="calc-param-label">Скорость (Vx, Vy, Vz):</span><span class="calc-param-value">(${tp.velocity[0]}, ${tp.velocity[1]}, ${tp.velocity[2]}) м/с</span></div>`;
    html += '</div>';
    
    html += '<div class="calc-section">';
    html += '<h3>Параметры ветра</h3>';
    const wp = calculationsData.wind_params;
    html += `<div class="calc-param"><span class="calc-param-label">Начальный вектор ветра:</span><span class="calc-param-value">[${wp.initial[0].toFixed(2)}, ${wp.initial[1].toFixed(2)}, ${wp.initial[2].toFixed(2)}] м/с</span></div>`;
    html += `<div class="calc-param"><span class="calc-param-label">Конечный вектор ветра:</span><span class="calc-param-value">[${wp.final[0].toFixed(2)}, ${wp.final[1].toFixed(2)}, ${wp.final[2].toFixed(2)}] м/с</span></div>`;
    html += `<div class="calc-param"><span class="calc-param-label">Скорость ветра:</span><span class="calc-param-value">${wp.speed.toFixed(2)} м/с</span></div>`;
    html += `<div class="calc-param"><span class="calc-param-label">Направление ветра:</span><span class="calc-param-value">${wp.direction_deg.toFixed(2)}°</span></div>`;
    html += '</div>';
    
    html += '<div class="calc-section">';
    html += '<h3>Параметры симуляции</h3>';
    const sp = calculationsData.simulation_params;
    html += `<div class="calc-param"><span class="calc-param-label">Шаг времени (dt):</span><span class="calc-param-value">${sp.dt} с</span></div>`;
    html += `<div class="calc-param"><span class="calc-param-label">Максимальное время:</span><span class="calc-param-value">${sp.max_time} с</span></div>`;
    html += `<div class="calc-param"><span class="calc-param-label">Порог столкновения:</span><span class="calc-param-value">${sp.collision_threshold} м</span></div>`;
    html += `<div class="calc-param"><span class="calc-param-label">Вектор запуска:</span><span class="calc-param-value">[${sp.launch_vector[0].toFixed(4)}, ${sp.launch_vector[1].toFixed(4)}, ${sp.launch_vector[2].toFixed(4)}]</span></div>`;
    html += '</div>';
    
    html += '<div class="calc-section">';
    html += '<h3>Физические константы</h3>';
    const c = calculationsData.constants;
    html += `<div class="calc-param"><span class="calc-param-label">Ускорение свободного падения (g):</span><span class="calc-param-value">${c.G} м/с²</span></div>`;
    html += `<div class="calc-param"><span class="calc-param-label">Плотность воздуха (ρ):</span><span class="calc-param-value">${c.RHO} кг/м³</span></div>`;
    html += `<div class="calc-param"><span class="calc-param-label">Угловая скорость Земли (ω):</span><span class="calc-param-value">${c.OMEGA_EARTH} рад/с</span></div>`;
    html += '</div>';
    
    html += '<div class="calc-section">';
    html += '<h3>Используемые формулы</h3>';
    
    html += '<div class="formula-box">';
    html += '<strong>Тяга:</strong>';
    html += '<code>F_thrust = launch_direction × thrust_force</code>';
    html += '<div class="formula-description">Тяга направлена по вектору запуска и действует только во время горения топлива</div>';
    html += '</div>';
    
    html += '<div class="formula-box">';
    html += '<strong>Гравитация:</strong>';
    html += '<code>F_gravity = -m × g × [0, 0, 1]</code>';
    html += '<div class="formula-description">где m - текущая масса ракеты, g = 9.81 м/с²</div>';
    html += '</div>';
    
    html += '<div class="formula-box">';
    html += '<strong>Сопротивление воздуха (Drag):</strong>';
    html += '<code>F_drag = -0.5 × ρ × Cd × A × |v_rel|² × (v_rel / |v_rel|)</code>';
    html += '<div class="formula-description">где v_rel = v_missile - v_wind - относительная скорость, ρ - плотность воздуха, Cd - коэффициент сопротивления, A - площадь поперечного сечения</div>';
    html += '</div>';
    
    html += '<div class="formula-box">';
    html += '<strong>Сила Кориолиса:</strong>';
    html += '<code>F_coriolis = -2 × m × (ω × v)</code>';
    html += '<div class="formula-description">где ω - вектор угловой скорости Земли для данной широты, v - скорость ракеты</div>';
    html += '</div>';
    
    html += '<div class="formula-box">';
    html += '<strong>Расход топлива:</strong>';
    html += '<code>dm/dt = -fuel_mass / burn_time</code>';
    html += '<div class="formula-description">Линейный расход топлива во время горения</div>';
    html += '</div>';
    
    html += '<div class="formula-box">';
    html += '<strong>Движение цели:</strong>';
    html += '<code>r_target(t) = r_target(0) + v_target × t</code>';
    html += '<div class="formula-description">Равномерное прямолинейное движение цели</div>';
    html += '</div>';
    
    html += '<div class="formula-box">';
    html += '<strong>Интегрирование (RK4):</strong>';
    html += '<code>k1 = f(t, y)\nk2 = f(t + dt/2, y + dt×k1/2)\nk3 = f(t + dt/2, y + dt×k2/2)\nk4 = f(t + dt, y + dt×k3)\ny(t+dt) = y(t) + dt×(k1 + 2×k2 + 2×k3 + k4)/6</code>';
    html += '<div class="formula-description">Метод Рунге-Кутта 4-го порядка для численного интегрирования уравнений движения</div>';
    html += '</div>';
    
    html += '<div class="formula-box">';
    html += '<strong>Расстояние до цели:</strong>';
    html += '<code>d = ||r_missile - r_target||</code>';
    html += '<div class="formula-description">Евклидово расстояние между ракетой и целью</div>';
    html += '</div>';
    
    html += '</div>';
    
    content.innerHTML = html;
    modal.style.display = 'block';
}

function closeCalculationsModal() {
    const modal = document.getElementById('calculations-modal');
    modal.style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('calculations-modal');
    if (event.target === modal) {
        closeCalculationsModal();
    }
}
