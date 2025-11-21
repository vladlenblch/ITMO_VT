"use strict";

const state = {
    x: [],
    y: 0,
    r: 1.0,
};

const table = document.getElementById("result-table");
const error = document.getElementById("error");
const possibleXs = new Set([-3, -2, -1, 0, 1, 2, 3, 4, 5]);
const possibleRs = new Set([1, 2, 3, 4, 5]);

const validateState = (state) => {
    if (!Array.isArray(state.x) || state.x.length === 0) {
        error.hidden = false;
        error.innerText = "Выберите ровно одно значение X";
        throw new Error("Невалидное значение");
    }

    if (state.x.length > 1) {
        error.hidden = false;
        error.innerText = "Можно выбрать только одно значение X";
        const allowedX = [-3, -2, -1, 0, 1, 2, 3, 4, 5];
    }

    if (!possibleXs.has(parseInt(state.x[0]))) {
        error.hidden = false;
        error.innerText = `X должен быть в диапазоне [${[...possibleXs].join(", ")}]`;
        throw new Error("Невалидное значение");
    }

    const yStr = String(state.y).trim();
    const numRegex = /^[+-]?(\d+(\.\d+)?|\.\d+)$/;
    if (!numRegex.test(yStr)) {
    }
    const yNum = parseFloat(yStr);
    if (!(yNum > -5 && yNum < 3)) {
        error.hidden = false;
        error.innerText = "Y должен быть в строго диапазоне (-5, 3)";
        throw new Error("Невалидное значение");
    }

    const rNum = parseInt(state.r);
    if (isNaN(rNum) || !possibleRs.has(rNum)) {
        error.hidden = false;
        error.innerText = `R должен быть одним из ${[...possibleRs].join(", ")}`;
        throw new Error("Невалидное значение");
    }

}

const checkboxes = document.querySelectorAll('#xs input[type="checkbox"]');
checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function(ev) {
        updateXState();
    });
});

const updateXState = () => {
    const checkedBoxes = document.querySelectorAll('#xs input[type="checkbox"]:checked');
    if (checkedBoxes.length > 0) {
        state.x = Array.from(checkedBoxes).map(cb => cb.value);
    } else {
        state.x = [];
    }
};

document.getElementById("y").addEventListener("input", (ev) => {
    state.y = ev.target.value;
});

document.getElementById("y").addEventListener("change", (ev) => {
    state.y = ev.target.value;
});

document.getElementById("r").addEventListener("change", (ev) => {
    state.r = parseInt(ev.target.value);
});

document.getElementById("data-form").addEventListener("submit", function (ev) {
    const yEl = document.getElementById('y');
    state.y = yEl ? String(yEl.value).trim() : '';
    const checkedR = document.querySelector('#r input[type="radio"]:checked');
    if (checkedR) state.r = parseInt(checkedR.value);
    updateXState();

    const hasX = Array.isArray(state.x) && state.x.length === 1;
    const hasY = state.y !== null && String(state.y).trim().length > 0;
    if (!hasX || !hasY) {
        ev.preventDefault();
        error.hidden = false;
        if (!hasX && !hasY) {
            error.innerText = 'Заполните X и Y';
        } else if (!hasX) {
            error.innerText = 'Выберите значение X';
        } else {
            error.innerText = 'Введите значение Y';
        }
        return;
    }

    try {
        validateState(state);
        error.hidden = true;
        error.innerText = '';
    } catch (e) {
        ev.preventDefault();
        error.hidden = false;
    }
});

if (error) { error.hidden = true; }

const canvas = document.getElementById('graph');
const ctx = canvas.getContext('2d');

const width = canvas.width;
const height = canvas.height;
const R = 150;
const centerX = width / 2;
const centerY = height / 2;

canvas.addEventListener('click', function (ev) {
    const rNum = parseInt(state.r);
    if (isNaN(rNum)) {
        error.hidden = false;
        error.innerText = 'Выберите R для определения координат';
        return;
    }

    const rect = canvas.getBoundingClientRect();
    const localX = ev.clientX - rect.left;
    const localY = ev.clientY - rect.top;
    const px = localX - centerX;
    const py = centerY - localY;
    const scale = R / rNum;

    const modelX = px / scale;
    const modelY = py / scale;

    let snappedX = Math.round(modelX);
    if (!possibleXs.has(snappedX)) {
        const xs = [...possibleXs].sort((a, b) => a - b);
        if (modelX < xs[0]) snappedX = xs[0];
        if (modelX > xs[xs.length - 1]) snappedX = xs[xs.length - 1];
    }

    let clampedY = modelY;
    if (clampedY <= -5) clampedY = -4.999;
    if (clampedY >= 3) clampedY = 2.999;

    const form = document.getElementById('data-form');
    const base = form && form.action ? form.action : window.location.pathname;
    const params = `?x=${encodeURIComponent(snappedX)}&y=${encodeURIComponent(clampedY)}&r=${encodeURIComponent(rNum)}`;
    window.location.href = base + params;
});

function drawBackground(r) {
    ctx.fillStyle = '#2c3e50';
    ctx.fillRect(0, 0, width, height);

    ctx.fillStyle = 'rgba(100, 181, 246, 0.3)';
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX + R, centerY);
    ctx.lineTo(centerX, centerY - R);
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, R, 0, Math.PI / 2, false);
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    ctx.rect(centerX - R / 2, centerY, R / 2, R);
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(centerX, 0);
    ctx.lineTo(centerX, height);
    ctx.moveTo(0, centerY);
    ctx.lineTo(width, centerY);
    ctx.strokeStyle = "#64B5F6";
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.strokeStyle = "rgba(100, 181, 246, 0.3)";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
        const offset = (R / 2) * i;
        ctx.beginPath();
        ctx.moveTo(centerX + offset, 0);
        ctx.lineTo(centerX + offset, height);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(centerX - offset, 0);
        ctx.lineTo(centerX - offset, height);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, centerY + offset);
        ctx.lineTo(width, centerY + offset);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, centerY - offset);
        ctx.lineTo(width, centerY - offset);
        ctx.stroke();
    }

    ctx.font = "12px monospace";
    ctx.fillStyle = "#e8f4fd";
    ctx.fillText("0", centerX + 6, centerY - 6);
    ctx.fillText("R/2", centerX + R / 2 - 6, centerY - 6);
    ctx.fillText("R", centerX + R - 6, centerY - 6);
    ctx.fillText("-R/2", centerX - R / 2 - 18, centerY - 6);
    ctx.fillText("-R", centerX - R - 6, centerY - 6);
    ctx.fillText("R/2", centerX + 6, centerY - R / 2 + 6);
    ctx.fillText("R", centerX + 6, centerY - R + 6);
    ctx.fillText("-R/2", centerX + 6, centerY + R / 2 + 6);
    ctx.fillText("-R", centerX + 6, centerY + R + 6);
}

function drawPointDot(x, y, r, hit = true) {
    const coords = convertToCanvasCoords(x, y, r);
    const color = hit ? '#2ecc71' : '#FF0000';
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(coords.x, coords.y, 5, 0, 2 * Math.PI);
    ctx.fill();
}

function drawHistory() {
    const rows = document.querySelectorAll('#result-table tr');
    if (rows.length > 1) {
        const cells = rows[1].children;
        if (cells.length >= 5) {
            const x = parseFloat(cells[0].innerText);
            const y = parseFloat(cells[1].innerText);
            const rCell = parseInt(cells[2].innerText) || state.r;
            const resultText = cells[4].innerText || '';
            const hit = resultText.toLowerCase().includes('попад');
            drawBackground(state.r);
            drawPointDot(x, y, rCell, hit);
        }
    }
}

function convertToCanvasCoords(x, y, r) {
    const scale = R / r;
    const canvasX = centerX + (x * scale);
    const canvasY = centerY - (y * scale);
    return { x: canvasX, y: canvasY };
}

function drawPoint(x, y, r, showPoint = true) {
    ctx.fillStyle = '#2c3e50';
    ctx.fillRect(0, 0, width, height);

    ctx.fillStyle = 'rgba(100, 181, 246, 0.3)';
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX + R, centerY);
    ctx.lineTo(centerX, centerY - R);
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, R, 0, Math.PI / 2, false);
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    ctx.rect(centerX - R/2, centerY, R/2, R);
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(centerX, 0);
    ctx.lineTo(centerX, height);
    ctx.moveTo(0, centerY);
    ctx.lineTo(width, centerY);
    ctx.strokeStyle = "#64B5F6";
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.strokeStyle = "rgba(100, 181, 246, 0.3)";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
        const offset = (R / 2) * i;
        ctx.beginPath();
        ctx.moveTo(centerX + offset, 0);
        ctx.lineTo(centerX + offset, height);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(centerX - offset, 0);
        ctx.lineTo(centerX - offset, height);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, centerY + offset);
        ctx.lineTo(width, centerY + offset);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, centerY - offset);
        ctx.lineTo(width, centerY - offset);
        ctx.stroke();
    }

    ctx.font = "12px monospace";
    ctx.fillStyle = "#e8f4fd";
    ctx.fillText("0", centerX + 6, centerY - 6);
    ctx.fillText("R/2", centerX + R / 2 - 6, centerY - 6);
    ctx.fillText("R", centerX + R - 6, centerY - 6);
    ctx.fillText("-R/2", centerX - R / 2 - 18, centerY - 6);
    ctx.fillText("-R", centerX - R - 6, centerY - 6);
    ctx.fillText("R/2", centerX + 6, centerY - R / 2 + 6);
    ctx.fillText("R", centerX + 6, centerY - R + 6);
    ctx.fillText("-R/2", centerX + 6, centerY + R / 2 + 6);
    ctx.fillText("-R", centerX + 6, centerY + R + 6);

}

updateXState();
const checkedR = document.querySelector('#r input[type="radio"]:checked');
if (checkedR) state.r = parseInt(checkedR.value);
const yInput = document.getElementById('y');
if (yInput && yInput.value) state.y = yInput.value;

drawBackground(state.r);
drawHistory();