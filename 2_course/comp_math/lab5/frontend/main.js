const variantRows = [
  [1.10, 0.2234],
  [1.25, 1.2438],
  [1.40, 2.2644],
  [1.55, 3.2984],
  [1.70, 4.3222],
  [1.85, 5.3516],
  [2.00, 6.3867],
];

const methodLabels = {
  lagrange: "Лагранж",
  newton_finite: "Ньютон",
  gauss: "Гаусс",
};

const curveLabels = {
  newton: "Ньютон",
  gauss: "Гаусс",
  truth: "Истинная функция",
};

const allMethods = ["lagrange", "newton_finite", "gauss"];

const sourceFunctions = {
  sin: Math.sin,
  cos: Math.cos,
  exp: Math.exp,
  ln: Math.log,
  sqrt: Math.sqrt,
  quadratic: (x) => x * x + 2 * x + 1,
  rational: (x) => 1 / (1 + x * x),
};

const state = {
  mode: "variant",
  lastResponse: null,
  chartCurve: "newton",
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

const ui = {
  functionSelect: $("#functionSelect"),
  variantTableBody: $("#variantTableBody"),
  functionTableBody: $("#functionTableBody"),
  addRowButton: $("#addRowButton"),
  resetRowsButton: $("#resetRowsButton"),
  targetInput: $("#targetInput"),
  leftInput: $("#leftInput"),
  rightInput: $("#rightInput"),
  countInput: $("#countInput"),
  calculateButton: $("#calculateButton"),
  statusLine: $("#statusLine"),
  metricStrip: $("#metricStrip"),
  chartTabs: $("#chartTabs"),
  chart: $("#chart"),
  resultTable: $("#resultTable"),
  finiteTable: $("#finiteTable"),
};

function formatNumber(value, digits = 8) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "";
  const number = Number(value);
  if (!Number.isFinite(number)) return String(value);
  const maxDigits = Math.max(0, Math.min(20, Number(digits) || 0));
  const minDigits = Math.min(maxDigits, Math.abs(number) < 10 && number !== 0 ? 4 : 0);
  return number.toLocaleString("ru-RU", {
    maximumFractionDigits: maxDigits,
    minimumFractionDigits: minDigits,
  });
}

function inputValue(value, digits) {
  const number = Number(value);
  return Number.isFinite(number) ? number.toFixed(digits) : "";
}

function renderEditableTable(tbody, rows, options = {}) {
  tbody.innerHTML = rows
    .map(
      ([x, y], index) => `<tr>
        <td><input type="number" step="any" value="${inputValue(x, options.xDigits ?? 4)}" data-column="x" aria-label="x ${index + 1}" /></td>
        <td><input type="number" step="any" value="${inputValue(y, options.yDigits ?? 6)}" data-column="y" aria-label="y ${index + 1}" /></td>
        ${options.deletable ? `<td><button class="row-action" type="button" data-delete-row="${index}" aria-label="Удалить строку">-</button></td>` : ""}
      </tr>`,
    )
    .join("");
}

function renderVariantTable(rows) {
  renderEditableTable(ui.variantTableBody, rows, { xDigits: 2, yDigits: 4, deletable: true });

  $$("[data-delete-row]").forEach((button) => {
    button.addEventListener("click", () => {
      try {
        const rows = readVariantRows();
        if (rows.x.length <= 2) {
          ui.statusLine.textContent = "Нужно минимум две строки.";
          return;
        }
        const index = Number(button.dataset.deleteRow);
        const nextRows = rows.x.map((x, rowIndex) => [x, rows.y[rowIndex]]).filter((_, rowIndex) => rowIndex !== index);
        renderVariantTable(nextRows);
        calculate();
      } catch (error) {
        ui.statusLine.textContent = error.message;
      }
    });
  });
}

function readRows(tbody) {
  const rows = [...tbody.querySelectorAll("tr")].map((row, index) => {
    const x = Number(String(row.querySelector('[data-column="x"]').value).replace(",", "."));
    const y = Number(String(row.querySelector('[data-column="y"]').value).replace(",", "."));
    if (!Number.isFinite(x) || !Number.isFinite(y)) {
      throw new Error(`Строка ${index + 1}: x и y должны быть числами.`);
    }
    return [x, y];
  });

  if (rows.length < 2) {
    throw new Error("Нужно минимум две строки таблицы.");
  }

  return {
    x: rows.map(([x]) => x),
    y: rows.map(([, y]) => y),
  };
}

function readVariantRows() {
  return readRows(ui.variantTableBody);
}

function readFunctionRows() {
  const fn = sourceFunctions[ui.functionSelect.value];
  if (!fn) throw new Error("Функция не выбрана.");

  const rows = [...ui.functionTableBody.querySelectorAll("tr")].map((row, index) => {
    const x = Number(String(row.querySelector('[data-column="x"]').value).replace(",", "."));
    if (!Number.isFinite(x)) {
      throw new Error(`Строка ${index + 1}: x должен быть числом.`);
    }
    const y = fn(x);
    if (!Number.isFinite(y)) {
      throw new Error(`Строка ${index + 1}: функция не определена в этой точке.`);
    }
    return [x, y];
  });

  if (rows.length < 2) {
    throw new Error("Нужно минимум две строки таблицы.");
  }

  return {
    x: rows.map(([x]) => x),
    y: rows.map(([, y]) => y),
  };
}

function generateFunctionRows() {
  const fn = sourceFunctions[ui.functionSelect.value];
  const left = Number(String(ui.leftInput.value).replace(",", "."));
  const right = Number(String(ui.rightInput.value).replace(",", "."));
  const count = Number(ui.countInput.value);

  if (!fn) throw new Error("Функция не выбрана.");
  if (!Number.isFinite(left) || !Number.isFinite(right)) throw new Error("Границы интервала должны быть числами.");
  if (!Number.isInteger(count) || count < 2) throw new Error("n должно быть целым числом не меньше 2.");
  if (left === right) throw new Error("Границы интервала должны различаться.");

  const step = (right - left) / (count - 1);
  return Array.from({ length: count }, (_, index) => {
    const x = left + step * index;
    return [x, fn(x)];
  });
}

function renderFunctionTable(rows) {
  ui.functionTableBody.innerHTML = rows
    .map(
      ([x], index) => `<tr>
        <td><input type="number" step="any" value="${inputValue(x, 6)}" data-column="x" aria-label="x ${index + 1}" /></td>
      </tr>`,
    )
    .join("");
}

function rebuildFunctionTable() {
  try {
    renderFunctionTable(generateFunctionRows());
    if (state.mode === "function") calculate();
  } catch (error) {
    ui.statusLine.textContent = error.message;
  }
}

function setMode(mode) {
  state.mode = mode;
  $$(".mode-button").forEach((button) => button.classList.toggle("active", button.dataset.mode === mode));
  $$(".source-pane").forEach((pane) => pane.classList.toggle("active", pane.dataset.pane === mode));
}

async function loadMetadata() {
  const functions = await fetch("/api/functions").then((response) => response.json());

  ui.functionSelect.innerHTML = functions
    .map((fn) => `<option value="${fn.id}">${fn.label}</option>`)
    .join("");
}

function buildPayload() {
  const target = Number(String(ui.targetInput.value).replace(",", "."));
  if (!Number.isFinite(target)) throw new Error("Аргумент x должен быть числом.");

  const payload = {
    mode: state.mode === "variant" ? "table" : state.mode,
    target,
    methods: allMethods,
    options: {},
  };

  if (state.mode === "variant") {
    payload.points = readVariantRows();
  }

  if (state.mode === "function") {
    payload.function = ui.functionSelect.value;
    payload.left = Number(String(ui.leftInput.value).replace(",", "."));
    payload.right = Number(String(ui.rightInput.value).replace(",", "."));
    payload.count = Number(ui.countInput.value);
    payload.points = readFunctionRows();
  }

  return payload;
}

async function calculate() {
  ui.statusLine.textContent = "Расчет...";
  try {
    const payload = buildPayload();
    const response = await fetch("/api/interpolate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok || data.error) throw new Error(data.error || "Ошибка API.");
    state.lastResponse = data;
    render(data);
    ui.statusLine.textContent = "Готово";
  } catch (error) {
    ui.statusLine.textContent = error.message;
  }
}

function render(data) {
  renderMetrics(data.results);
  renderResults(data.results);
  renderFiniteTable(data.points, data.finiteDifferences);
  renderChartTabs(data);
  renderChart(data);
}

function renderMetrics(results) {
  const cards = Object.entries(results)
    .filter(([, result]) => !result.error)
    .slice(0, 5)
    .map(([key, result]) => {
      return `<div class="metric"><span>${methodLabels[key] || key}</span><strong>${formatNumber(result.value, 10)}</strong></div>`;
    });
  ui.metricStrip.innerHTML = cards.join("");
}

function resultRows(results, methods) {
  return methods
    .filter((key) => results[key])
    .map((key) => {
      const result = results[key];
      if (result.error) {
        return `<tr><td>${methodLabels[key] || key}</td><td class="error-cell" colspan="3">${result.error}</td></tr>`;
      }
      return `<tr>
        <td>${methodLabels[key] || key}</td>
        <td>${formatNumber(result.value, 12)}</td>
        <td>${formatNumber(result.q, 6)}</td>
        <td>${result.terms ? result.terms.length : "-"}</td>
      </tr>`;
    })
    .join("");
}

function buildResultTable(rows) {
  return `
    <thead><tr><th>Метод</th><th>f(x)</th><th>q</th><th>Слагаемых</th></tr></thead>
    <tbody>${rows || '<tr><td colspan="4">Нет результатов</td></tr>'}</tbody>
  `;
}

function renderResults(results) {
  ui.resultTable.innerHTML = buildResultTable(resultRows(results, allMethods));
}

function renderFiniteTable(points, levels) {
  if (!levels || levels.length === 0) {
    ui.finiteTable.innerHTML = "";
    return;
  }
  const headers = ["x", "y", ...levels.slice(1).map((_, index) => `Δ${index + 1}y`)];
  const body = points
    .map((point, rowIndex) => {
      const cells = [formatNumber(point.x, 6), ...levels.map((level) => formatNumber(level[rowIndex], 10))];
      return `<tr>${cells.map((cell) => `<td>${cell}</td>`).join("")}</tr>`;
    })
    .join("");

  ui.finiteTable.innerHTML = `
    <thead><tr>${headers.map((header) => `<th>${header}</th>`).join("")}</tr></thead>
    <tbody>${body}</tbody>
  `;
}

function factorial(n) {
  let value = 1;
  for (let i = 2; i <= n; i += 1) value *= i;
  return value;
}

function finiteLevels(ys) {
  const levels = [ys.map(Number)];
  while (levels[levels.length - 1].length > 1) {
    const previous = levels[levels.length - 1];
    levels.push(previous.slice(1).map((value, index) => value - previous[index]));
  }
  return levels;
}

function equalStep(xs) {
  if (xs.length < 2) return null;
  const h = xs[1] - xs[0];
  if (Math.abs(h) < 1e-12) return null;
  return xs.every((x, index) => index === 0 || Math.abs(x - xs[index - 1] - h) <= 1e-9) ? h : null;
}

function newtonFiniteAt(xs, ys, x) {
  const h = equalStep(xs);
  if (!h) return null;
  const levels = finiteLevels(ys);
  const second = x > (xs[0] + xs[xs.length - 1]) / 2;
  const q = second ? (x - xs[xs.length - 1]) / h : (x - xs[0]) / h;
  let total = second ? ys[ys.length - 1] : ys[0];
  let product = 1;

  for (let order = 1; order < xs.length; order += 1) {
    product *= second ? q + order - 1 : q - order + 1;
    const coefficient = product / factorial(order);
    const index = second ? xs.length - 1 - order : 0;
    total += coefficient * levels[order][index];
  }

  return Number.isFinite(total) ? total : null;
}

function gaussShifts(order, first) {
  if (first) {
    if (order % 2 === 0) {
      const radius = order / 2;
      return { shifts: Array.from({ length: order }, (_, index) => radius - 1 - index), indexShift: -radius };
    }
    const radius = (order - 1) / 2;
    return { shifts: Array.from({ length: order }, (_, index) => radius - index), indexShift: -radius };
  }
  if (order % 2 === 0) {
    const radius = order / 2;
    return { shifts: Array.from({ length: order }, (_, index) => -(radius - 1) + index), indexShift: -radius };
  }
  const radius = (order - 1) / 2;
  return { shifts: Array.from({ length: order }, (_, index) => -radius + index), indexShift: -(radius + 1) };
}

function gaussAt(xs, ys, x) {
  const h = equalStep(xs);
  if (!h) return null;
  const levels = finiteLevels(ys);
  let center = xs.findIndex((value, index) => index < xs.length - 1 && value <= x && x <= xs[index + 1]);
  if (center < 0) center = xs.reduce((best, value, index) => (Math.abs(value - x) < Math.abs(xs[best] - x) ? index : best), 0);
  if (center === xs.length - 1) center = xs.length - 2;

  const q = (x - xs[center]) / h;
  const first = q >= 0;
  let total = ys[center];

  for (let order = 1; order < xs.length; order += 1) {
    const spec = gaussShifts(order, first);
    const index = center + spec.indexShift;
    if (!levels[order] || index < 0 || index >= levels[order].length) break;
    const coefficient = spec.shifts.reduce((product, shift) => product * (q + shift), 1) / factorial(order);
    total += coefficient * levels[order][index];
  }

  return Number.isFinite(total) ? total : null;
}

function buildCurve(points, evaluator) {
  if (!points.length) return [];
  const xs = points.map((point) => point.x);
  const left = Math.min(...xs);
  const right = Math.max(...xs);
  return Array.from({ length: 180 }, (_, index) => {
    const x = left + ((right - left) * index) / 179;
    const y = evaluator(x);
    return Number.isFinite(y) ? { x, y } : null;
  }).filter(Boolean);
}

function buildLocalCurves(data) {
  const points = data.points || data.plot.nodes || [];
  const xs = points.map((point) => point.x);
  const ys = points.map((point) => point.y);
  const curves = {
    newton: buildCurve(points, (x) => newtonFiniteAt(xs, ys, x)),
    gauss: buildCurve(points, (x) => gaussAt(xs, ys, x)),
  };
  if (state.mode === "function" && sourceFunctions[ui.functionSelect.value]) {
    curves.truth = buildCurve(points, sourceFunctions[ui.functionSelect.value]);
  }
  return curves;
}

function getCurves(data) {
  const localCurves = buildLocalCurves(data);
  return { ...localCurves, ...(data.plot.curves || {}) };
}

function renderChartTabs(data) {
  const curves = getCurves(data);
  const keys = Object.keys(curves).filter((key) => curves[key]?.length);
  if (!keys.length) {
    ui.chartTabs.innerHTML = "";
    return;
  }
  if (!keys.includes(state.chartCurve)) {
    state.chartCurve = keys[0];
  }

  ui.chartTabs.innerHTML = keys
    .map(
      (key) =>
        `<button class="${state.chartCurve === key ? "active" : ""}" type="button" data-curve="${key}">${curveLabels[key] || key}</button>`,
    )
    .join("");

  $$("[data-curve]").forEach((button) => {
    button.addEventListener("click", () => {
      state.chartCurve = button.dataset.curve;
      renderChartTabs(data);
      renderChart(data);
    });
  });
}

function renderChart(data) {
  const width = 960;
  const height = 420;
  const pad = { left: 62, right: 28, top: 24, bottom: 48 };
  const curves = getCurves(data);
  const activeKey = curves[state.chartCurve]?.length ? state.chartCurve : Object.keys(curves)[0];
  const curve = curves[activeKey] || [];
  const nodes = data.plot.nodes;
  const allCurves = Object.values(curves).flat();
  const all = [...allCurves, ...nodes];
  if (!all.length) {
    ui.chart.innerHTML = "";
    return;
  }

  let minX = Math.min(...all.map((point) => point.x));
  let maxX = Math.max(...all.map((point) => point.x));
  let minY = Math.min(...all.map((point) => point.y));
  let maxY = Math.max(...all.map((point) => point.y));
  if (minY === maxY) {
    minY -= 1;
    maxY += 1;
  }
  const yMargin = (maxY - minY) * 0.12;
  minY -= yMargin;
  maxY += yMargin;

  const sx = (x) => pad.left + ((x - minX) / (maxX - minX || 1)) * (width - pad.left - pad.right);
  const sy = (y) => height - pad.bottom - ((y - minY) / (maxY - minY || 1)) * (height - pad.top - pad.bottom);
  const polyline = curve.map((point) => `${sx(point.x).toFixed(2)},${sy(point.y).toFixed(2)}`).join(" ");
  const xTicks = Array.from({ length: 6 }, (_, index) => minX + ((maxX - minX) * index) / 5);
  const yTicks = Array.from({ length: 5 }, (_, index) => minY + ((maxY - minY) * index) / 4);
  const targetX = sx(data.target);

  ui.chart.innerHTML = `
    <rect x="0" y="0" width="${width}" height="${height}" fill="transparent"></rect>
    ${yTicks
      .map(
        (tick) => `<line class="grid-line" x1="${pad.left}" x2="${width - pad.right}" y1="${sy(tick)}" y2="${sy(tick)}"></line>
          <text class="chart-label" x="14" y="${sy(tick) + 4}">${formatNumber(tick, 3)}</text>`,
      )
      .join("")}
    ${xTicks
      .map(
        (tick) => `<line class="grid-line" x1="${sx(tick)}" x2="${sx(tick)}" y1="${pad.top}" y2="${height - pad.bottom}"></line>
          <text class="chart-label" x="${sx(tick) - 18}" y="${height - 16}">${formatNumber(tick, 3)}</text>`,
      )
      .join("")}
    <line class="axis" x1="${pad.left}" x2="${width - pad.right}" y1="${height - pad.bottom}" y2="${height - pad.bottom}"></line>
    <line class="axis" x1="${pad.left}" x2="${pad.left}" y1="${pad.top}" y2="${height - pad.bottom}"></line>
    <line class="target-line" x1="${targetX}" x2="${targetX}" y1="${pad.top}" y2="${height - pad.bottom}"></line>
    <polyline class="curve ${activeKey}-curve" points="${polyline}"></polyline>
    ${nodes.map((point) => `<circle class="node" cx="${sx(point.x)}" cy="${sy(point.y)}" r="5"></circle>`).join("")}
  `;
}

function bindEvents() {
  $$(".mode-button").forEach((button) => {
    button.addEventListener("click", () => setMode(button.dataset.mode));
  });
  ui.addRowButton.addEventListener("click", () => {
    try {
      const rows = readVariantRows();
      const lastIndex = rows.x.length - 1;
      const h = rows.x.length > 1 ? rows.x[lastIndex] - rows.x[lastIndex - 1] : 0.15;
      const dy = rows.y.length > 1 ? rows.y[lastIndex] - rows.y[lastIndex - 1] : 1;
      renderVariantTable([...rows.x.map((x, index) => [x, rows.y[index]]), [rows.x[lastIndex] + h, rows.y[lastIndex] + dy]]);
      calculate();
    } catch (error) {
      ui.statusLine.textContent = error.message;
    }
  });
  ui.resetRowsButton.addEventListener("click", () => {
    renderVariantTable(variantRows);
    calculate();
  });
  [ui.functionSelect, ui.leftInput, ui.rightInput, ui.countInput].forEach((control) => {
    control.addEventListener("change", rebuildFunctionTable);
  });
  ui.calculateButton.addEventListener("click", calculate);
}

async function init() {
  renderVariantTable(variantRows);
  bindEvents();
  try {
    await loadMetadata();
    renderFunctionTable(generateFunctionRows());
    await calculate();
  } catch (error) {
    ui.statusLine.textContent = error.message;
  }
}

init();
