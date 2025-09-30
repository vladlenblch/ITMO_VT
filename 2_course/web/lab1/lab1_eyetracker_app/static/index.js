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

    const rNum = parseFloat(state.r);
    if (isNaN(rNum) || !possibleRs.has(rNum)) {
        error.hidden = false;
        error.innerText = `R должен быть в диапазоне [${[...possibleRs].join(", ")}]`;
        throw new Error("Invalid state");
    }

    error.hidden = true;
}

const checkboxes = document.querySelectorAll('#xs input[type="checkbox"]');
checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function(ev) {
        if (ev.target.checked) {
            checkboxes.forEach(cb => {
                if (cb !== ev.target) {
                    cb.checked = false;
                }
            });
        }
        updateXState();
    });
});

const updateXState = () => {
    const checkedBoxes = document.querySelectorAll('#xs input[type="checkbox"]:checked');
    if (checkedBoxes.length > 0) {
        state.x = Array.from(checkedBoxes).map(cb => cb.value);
        error.hidden = true;
    } else {
        state.x = [];
    }
};

document.getElementById("y").addEventListener("input", (ev) => {
    const value = ev.target.value;
    
    const validPattern = /^[-]?[0-9]*\.?[0-9]*$/;
    
    if (value === "" || validPattern.test(value)) {
        state.y = value;
        ev.target.style.borderColor = "#4A90E2";
    } else {
        ev.target.value = value.slice(0, -1);
        ev.target.style.borderColor = "#FF6B6B";
    }
});

document.getElementById("y").addEventListener("keypress", (ev) => {
    const char = ev.key;
    const currentValue = ev.target.value;
    
    if (!/^[0-9.-]$/.test(char) && !["Backspace", "Delete", "ArrowLeft", "ArrowRight", "Tab"].includes(char)) {
        ev.preventDefault();
    }
    
    if (char === "-" && currentValue.length > 0) {
        ev.preventDefault();
    }
    
    if (char === "." && currentValue.includes(".")) {
        ev.preventDefault();
    }
});

document.getElementById("y").addEventListener("change", (ev) => {
    const value = ev.target.value;
    const numValue = parseFloat(value);
    
    if (isNaN(numValue)) {
        ev.target.style.borderColor = "#FF6B6B";
        error.hidden = false;
        error.innerText = "Y должен быть числом";
        ev.target.focus();
    } else if (numValue < -3 || numValue > 3) {
        ev.target.style.borderColor = "#FF6B6B";
        error.hidden = false;
        error.innerText = "Y должен быть в диапазоне [-3, 3]";
        ev.target.focus();
    } else {
        state.y = value;
        ev.target.style.borderColor = "#4A90E2";
        error.hidden = true;
    }
});

document.getElementById("r").addEventListener("change", (ev) => {
    const value = parseFloat(ev.target.value);
    if (!possibleRs.has(value)) {
        ev.target.style.borderColor = "#FF6B6B";
        error.hidden = false;
        error.innerText = `R должен быть одним из: ${[...possibleRs].join(", ")}`;
        ev.target.focus();
    } else {
        state.r = ev.target.value;
        ev.target.style.borderColor = "#4A90E2";
        error.hidden = true;
    }
});

document.getElementById("data-form").addEventListener("submit", async function (ev) {
    ev.preventDefault();
    
    try {
        validateState(state);
        
        const params = new URLSearchParams({
            x: state.x[0],
            y: state.y,
            r: state.r
        });

        const response = await fetch("/api/check-point?" + params.toString());

        const newRow = table.insertRow(-1);
        const rowX = newRow.insertCell(0);
        const rowY = newRow.insertCell(1);
        const rowR = newRow.insertCell(2);
        const rowTime = newRow.insertCell(3);
        const rowExecTime = newRow.insertCell(4);
        const rowResult = newRow.insertCell(5);

        if (response.ok) {
            error.hidden = true;
            const result = await response.json();
            
            rowX.innerText = state.x[0];
            rowY.innerText = state.y;
            rowR.innerText = state.r;
            rowTime.innerText = new Date(result.now).toLocaleString();
            rowExecTime.innerText = `${result.time} нс`;
            rowResult.innerText = result.result ? "Попадание" : "Промах";

            drawPoint(parseFloat(state.x[0]), parseFloat(state.y), parseFloat(state.r));
            
            const results = {
                x: state.x[0],
                y: state.y,
                r: state.r,
                execTime: `${result.time} нс`,
                time: new Date(result.now).toLocaleString(),
                result: result.result ? "Попадание" : "Промах"
            };
            
            const prevResults = JSON.parse(localStorage.getItem("results") || "[]");
            localStorage.setItem("results", JSON.stringify([...prevResults, results]));
            
        } else if (response.status === 400) {
            const result = await response.json();
            error.hidden = false;
            error.innerText = `Ошибка: ${result.reason}`;
            
            rowX.innerText = state.x[0];
            rowY.innerText = state.y;
            rowR.innerText = state.r;
            rowTime.innerText = new Date(result.now).toLocaleString();
            rowExecTime.innerText = "N/A";
            rowResult.innerText = `Ошибка: ${result.reason}`;
        } else {
            error.hidden = false;
            error.innerText = "Ошибка сервера";
            
            rowX.innerText = state.x[0];
            rowY.innerText = state.y;
            rowR.innerText = state.r;
            rowTime.innerText = "N/A";
            rowExecTime.innerText = "N/A";
            rowResult.innerText = "Ошибка сервера";
        }
        
    } catch (e) {
        ev.preventDefault();
    }
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
