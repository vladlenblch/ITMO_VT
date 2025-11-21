"use strict";

(function () {
    const BASE_R = 150; // canvas radius when r = MAX_R (5)
    const MAX_R = 5;
    let graphInitialized = false;
    let pfCallbacksAttached = false;
    let pfUpdateFn = null;
    let updateGraphRef = null;
    const LAST_R_KEY = "graph:lastR";
    let lastKnownR = loadLastKnownR();
    window.skipValidationMessages = window.skipValidationMessages || false;

    function loadLastKnownR() {
        try {
            const stored = window.localStorage.getItem(LAST_R_KEY);
            const num = parseFloat(stored);
            return Number.isFinite(num) && num > 0 ? num : null;
        } catch (e) {
            return null;
        }
    }

    function persistLastKnownR(newR) {
        if (!Number.isFinite(newR) || newR <= 0) return;
        lastKnownR = newR;
        try {
            window.localStorage.setItem(LAST_R_KEY, String(newR));
        } catch (e) {
        }
    }

    function getDataTable() {
        return document.getElementById("data-form:result-table") ||
               document.getElementById("result-table") ||
               document.querySelector('[id$="result-table"]');
    }

    function getRHidden() {
        return document.getElementById("data-form:rHidden") ||
               document.querySelector('input[id*="rHidden"]');
    }

    function getRValue() {
        const rHidden = getRHidden();
        if (!rHidden) {
            return lastKnownR;
        }
        const val = parseFloat(rHidden.value);
        if (Number.isFinite(val) && val > 0) {
            persistLastKnownR(val);
            return val;
        }
        return lastKnownR;
    }

    function parseLatestPoint() {
        const table = getDataTable();
        if (!table) return null;
        const rows = table.querySelectorAll("tbody tr");
        if (!rows || rows.length === 0) return null;
        const cells = rows[0].querySelectorAll("td");
        if (cells.length < 5) return null;
        const x = parseFloat(cells[0].innerText);
        const y = parseFloat(cells[1].innerText);
        const r = parseFloat(cells[2].innerText);
        const hitText = cells[4].innerText.toLowerCase();
        const hit = hitText.includes("попад") || hitText.includes("hit");
        if ([x, y, r].some((v) => Number.isNaN(v))) return null;
        persistLastKnownR(r);
        return { x, y, r, hit };
    }

    function drawArea(ctx, width, height, centerX, centerY, r) {
        const effectiveR = r || MAX_R;
        const scaleFactor = effectiveR / MAX_R;
        const scaledR = BASE_R * scaleFactor;
        const scaledHalfR = scaledR / 2;

        ctx.clearRect(0, 0, width, height);
        ctx.fillStyle = "#2c3e50";
        ctx.fillRect(0, 0, width, height);

        ctx.fillStyle = "rgba(100, 181, 246, 0.3)";

        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(centerX - scaledHalfR, centerY);
        ctx.lineTo(centerX, centerY - scaledR);
        ctx.closePath();
        ctx.fill();

        ctx.beginPath();
        ctx.rect(centerX - scaledR, centerY, scaledR, scaledR);
        ctx.fill();

        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        // quarter circle strictly in bottom-right (x >= 0, y <= 0)
        ctx.lineTo(centerX + scaledR, centerY);
        ctx.arc(centerX, centerY, scaledR, 0, Math.PI / 2, false);
        ctx.lineTo(centerX, centerY);
        ctx.closePath();
        ctx.fill();

        ctx.beginPath();
        ctx.moveTo(centerX, 0);
        ctx.lineTo(centerX, height);
        ctx.moveTo(0, centerY);
        ctx.lineTo(width, centerY);
        ctx.strokeStyle = "#64B5F6";
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.strokeStyle = "rgba(100, 181, 246, 0.25)";
        ctx.lineWidth = 1;
        for (let i = 1; i <= 4; i++) {
            const offset = (BASE_R / 2) * i;
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
        ctx.fillText("2.5", centerX - BASE_R / 2 - 12, centerY - 6);
        ctx.fillText("5", centerX - BASE_R - 10, centerY - 6);
        ctx.fillText("-2.5", centerX + 6, centerY + BASE_R / 2 + 14);
        ctx.fillText("-5", centerX + 6, centerY + BASE_R + 10);
        ctx.fillText("2.5", centerX + BASE_R / 2 - 12, centerY - 6);
        ctx.fillText("5", centerX + BASE_R - 10, centerY - 6);
    }

    function updateGraph(ctx, width, height, centerX, centerY) {
        const r = getRValue();
        const drawR = r || lastKnownR || MAX_R;
        const rHidden = getRHidden();
        if (rHidden && (!rHidden.value || rHidden.value.trim() === "") && lastKnownR) {
            rHidden.value = lastKnownR;
        }
        persistLastKnownR(drawR);
        drawArea(ctx, width, height, centerX, centerY, drawR);
        drawLatestPoint(ctx, centerX, centerY);
    }

    function drawLatestPoint(ctx, centerX, centerY) {
        const latest = parseLatestPoint();
        if (!latest) return;
        const scaleFactor = latest.r / MAX_R;
        const effectiveRpx = BASE_R * scaleFactor;
        const pxPerUnit = effectiveRpx / latest.r;
        const canvasX = centerX + latest.x * pxPerUnit;
        const canvasY = centerY - latest.y * pxPerUnit;
        ctx.fillStyle = latest.hit ? "#2ecc71" : "#e74c3c";
        ctx.beginPath();
        ctx.arc(canvasX, canvasY, 5, 0, Math.PI * 2);
        ctx.fill();
    }

    function attachRObserver(callback) {
        const rHidden = getRHidden();
        if (!rHidden) {
            return;
        }
        const observer = new MutationObserver(callback);
        observer.observe(rHidden, { attributes: true, attributeFilter: ["value"] });
        rHidden.addEventListener("change", callback);
        rHidden.addEventListener("input", callback);
    }

    function hookPrimeFaces(updateFn) {
        if (typeof updateFn === "function") {
            pfUpdateFn = updateFn;
        }
        if (pfCallbacksAttached) return;
        const pfQueue = window.PrimeFaces && window.PrimeFaces.ajax && (window.PrimeFaces.ajax.Queue || window.PrimeFaces.ajax.RequestQueue);
        if (pfQueue && pfQueue.addOnComplete) {
            pfQueue.addOnComplete(function () {
                if (typeof pfUpdateFn === "function") {
                    setTimeout(pfUpdateFn, 20);
                    setTimeout(pfUpdateFn, 140);
                } else {
                    forceReinitSoon();
                }
            });
            pfCallbacksAttached = true;
            return;
        }
        if (pfQueue && pfQueue.addOnQueueEmptyCallback) {
            pfQueue.addOnQueueEmptyCallback(function () {
                if (typeof pfUpdateFn === "function") {
                    setTimeout(pfUpdateFn, 20);
                    setTimeout(pfUpdateFn, 140);
                } else {
                    forceReinitSoon();
                }
            });
            pfCallbacksAttached = true;
        }
    }

    function hookRButtons() {
        const buttons = document.querySelectorAll(".panel-group-r .ui-commandlink, .panel-group-r a");
        buttons.forEach((btn) => {
            btn.removeEventListener("click", handleRButtonClick, false);
            btn.addEventListener("click", handleRButtonClick, false);
        });
    }

    function handleRButtonClick(event) {
        const source = (event && event.currentTarget) || event.target;
        const val = parseFloat((source && source.textContent) || "");
        if (Number.isFinite(val)) {
            persistLastKnownR(val);
        }
        setTimeout(() => {
            graphInitialized = false;
            initGraph();
        }, 200);
    }

    function forceReinitSoon() {
        persistLastKnownR(getRValue());
        graphInitialized = false;
        setTimeout(initGraph, 30);
    }

    window.captureCurrentR = function () {
        const current = getRValue();
        if (current) {
            persistLastKnownR(current);
        }
    };

    window.reinitGraph = function (delayMs = 0) {
        persistLastKnownR(getRValue());
        graphInitialized = false;
        setTimeout(() => {
            initGraph();
            setTimeout(() => {
                if (typeof updateGraphRef === "function") {
                    updateGraphRef();
                    setTimeout(updateGraphRef, 140);
                    setTimeout(updateGraphRef, 260);
                }
            }, 100);
        }, delayMs);
    };

    window.redrawGraphAfterAjax = function () {
        if (typeof updateGraphRef === "function") {
            updateGraphRef();
            setTimeout(updateGraphRef, 80);
            setTimeout(updateGraphRef, 200);
        } else {
            reinitGraph(0);
        }
    };

    function initGraph() {
        if (graphInitialized) {
            return;
        }

        const canvas = document.getElementById("graph");
        if (!canvas) {
            setTimeout(initGraph, 100);
            return;
        }

        const ctx = canvas.getContext("2d");
        if (!ctx) {
            return;
        }

        graphInitialized = true;

        const width = canvas.width;
        const height = canvas.height;
        const centerX = width / 2;
        const centerY = height / 2;

        const updateGraphFn = () => updateGraph(ctx, width, height, centerX, centerY);
        updateGraphRef = updateGraphFn;

        canvas.addEventListener("click", function (event) {
            const r = getRValue();
            const effectiveR = r || lastKnownR || MAX_R;
            const rect = canvas.getBoundingClientRect();
            const localX = event.clientX - rect.left;
            const localY = event.clientY - rect.top;
            const px = localX - centerX;
            const py = centerY - localY;
            const scale = (BASE_R * (effectiveR / MAX_R)) / effectiveR;

            const modelX = px / scale;
            const modelY = py / scale;

            const clampedX = Math.max(-4.999, Math.min(4.999, modelX));
            const clampedY = Math.max(-4.9, Math.min(4.9, modelY));

            const xInput = document.getElementById("data-form:x");
            if (xInput) {
                xInput.value = clampedX.toFixed(3);
                xInput.dispatchEvent(new Event("change"));
            }

            const yInput = document.querySelector("#data-form\\:y input");
            if (yInput) {
                yInput.value = clampedY.toFixed(1);
                yInput.dispatchEvent(new Event("change"));
            }

            setTimeout(function () {
                if (typeof submitPointFromCanvas === "function" && (r || lastKnownR)) {
                    const ensuredR = r || lastKnownR;
                    persistLastKnownR(ensuredR);
                    const rHidden = getRHidden();
                    if (rHidden && (!rHidden.value || rHidden.value.trim() === "")) {
                        rHidden.value = ensuredR;
                    }
                    submitPointFromCanvas();
                }
            }, 100);
        });

        attachRObserver(updateGraphFn);
        updateGraphFn();
        setTimeout(updateGraphFn, 60);
        setTimeout(updateGraphFn, 160);

        hookPrimeFaces(updateGraphFn);
        hookRButtons();

        const form = document.getElementById("data-form");
        if (form) {
            form.removeEventListener("submit", forceReinitSoon, false);
            form.addEventListener("submit", forceReinitSoon, false);
        }

        persistLastKnownR(getRValue());
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", function () {
            setTimeout(initGraph, 100);
        });
    } else {
        setTimeout(initGraph, 100);
    }

    setTimeout(initGraph, 500);
})();
