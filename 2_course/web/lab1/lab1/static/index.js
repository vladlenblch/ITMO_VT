"use strict";

const state = {
    x: [],
    y: 0,
    r: 1.0,
};

const table = document.getElementById("result-table");
const error = document.getElementById("error");
const possibleXs = new Set([-4, -3, -2, -1, 0, 1, 2, 3, 4]);
const possibleRs = new Set([1.0, 1.5, 2.0, 2.5, 3.0]);

const validateState = (state) => {
    if (!Array.isArray(state.x) || state.x.length === 0) {
        error.hidden = false;
        error.innerText = "Выберите ровно одно значение X";
        throw new Error("Invalid state");
    }
    
    if (state.x.length > 1) {
        error.hidden = false;
        error.innerText = "Можно выбрать только одно значение X";
        throw new Error("Invalid state");
    }
    
    if (!possibleXs.has(parseInt(state.x[0]))) {
        error.hidden = false;
        error.innerText = `X должен быть в диапазоне [${[...possibleXs].join(", ")}]`;
        throw new Error("Invalid state");
    }

    const yNum = parseFloat(state.y);
    const yStr = state.y.trim();
    
    if (isNaN(yNum)) {
        error.hidden = false;
        error.innerText = "Y должен быть числом";
        throw new Error("Invalid state");
    }
    
    if (yNum < -3 || yNum > 3) {
        error.hidden = false;
        error.innerText = "Y должен быть в диапазоне [-3, 3]";
        throw new Error("Invalid state");
    }
    
    if (yNum > 3 || yNum < -3) {
        error.hidden = false;
        error.innerText = "Y должен быть в диапазоне [-3, 3]";
        throw new Error("Invalid state");
    }

    const rNum = parseFloat(state.r);
    if (isNaN(rNum) || !possibleRs.has(rNum)) {
        error.hidden = false;
        error.innerText = `R должен быть в диапазоне [${[...possibleRs].join(", ")}]`;
        throw new Error("Invalid state");
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
    state.r = ev.target.value;
});

document.getElementById("data-form").addEventListener("submit", async function (ev) {
    ev.preventDefault();

    validateState(state);

    const newRow = table.insertRow(-1);

    const rowX = newRow.insertCell(0);
    const rowY = newRow.insertCell(1);
    const rowR = newRow.insertCell(2);
    const rowTime = newRow.insertCell(3);
    const rowExecTime = newRow.insertCell(4);
    const rowResult = newRow.insertCell(5);

    const params = new URLSearchParams({
        x: state.x[0],
        y: state.y,
        r: state.r
    });

    const response = await fetch("/fcgi-bin/lab1.jar?" + params.toString());

    const results = {
        x: state.x[0],
        y: state.y,
        r: state.r,
        execTime: "",
        time: "",
        result: false,
    };

    if (response.ok) {
        error.hidden = true;
        const result = await response.json();
        results.time = new Date(result.now).toLocaleString();
        results.execTime = `${result.time} нс`;
        results.result = result.result ? "Попадание" : "Промах";
        
        drawPoint(parseFloat(state.x[0]), parseFloat(state.y), parseFloat(state.r));
    } else if (response.status === 400) {
        const result = await response.json();
        results.time = new Date(result.now).toLocaleString();
        results.execTime = "N/A";
        results.result = `Ошибка: ${result.reason}`;
    } else {
        results.time = "N/A";
        results.execTime = "N/A";
        results.result = "Ошибка"
    }

    const prevResults = JSON.parse(localStorage.getItem("results") || "[]");
    localStorage.setItem("results", JSON.stringify([...prevResults, results]));

    rowX.innerText = results.x.toString();
    rowY.innerText = results.y.toString();
    rowR.innerText = results.r.toString();
    rowTime.innerText = results.time;
    rowExecTime.innerText = results.execTime;
    rowResult.innerText = results.result;
});

const prevResults = JSON.parse(localStorage.getItem("results") || "[]");

prevResults.forEach(result => {
    const table = document.getElementById("result-table");

    const newRow = table.insertRow(-1);

    const rowX = newRow.insertCell(0);
    const rowY = newRow.insertCell(1);
    const rowR = newRow.insertCell(2);
    const rowTime = newRow.insertCell(3);
    const rowExecTime = newRow.insertCell(4);
    const rowResult = newRow.insertCell(5);

    rowX.innerText = result.x.toString();
    rowY.innerText = result.y.toString();
    rowR.innerText = result.r.toString();
    rowTime.innerText = result.time;
    rowExecTime.innerText = result.execTime;
    rowResult.innerText = result.result;
});

const canvas = document.getElementById('graph');
const ctx = canvas.getContext('2d');

const width = canvas.width;
const height = canvas.height;
const R = 150;
const centerX = width / 2;
const centerY = height / 2;

let currentPoint = null;

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
    ctx.lineTo(centerX, centerY - R/2);
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, R, 0, Math.PI / 2, false);
    ctx.lineTo(centerX, centerY);
    ctx.fill();

    ctx.beginPath();
    ctx.rect(centerX - R, centerY, R, R/2);
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

    if (showPoint) {
        const coords = convertToCanvasCoords(x, y, r);
        ctx.fillStyle = '#FF0000';
        ctx.beginPath();
        ctx.arc(coords.x, coords.y, 4, 0, 2 * Math.PI);
        ctx.fill();
    }
}

drawPoint(0, 0, 1, false);