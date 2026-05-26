function $(selector) {
  return document.querySelector(selector);
}

function printIntegralResult(target, results) {
  const prefix = "&gt; ";

  const methodNames = {
    "rect_left": "Метод прямоугольников (левые)",
    "rect_right": "Метод прямоугольников (правые)",
    "rect_mid": "Метод прямоугольников (средние)",
    "trapezoid": "Метод трапеций",
    "simpson": "Метод Симпсона"
  };

  const lines = [];
  for (const [methodKey, data] of Object.entries(results)) {
    if (!data.ok) {
      lines.push(`${prefix}<span class="error">${methodNames[methodKey]}: ошибка - ${data.error}</span>`);
      continue;
    }

    lines.push(`${prefix}${methodNames[methodKey]}:`);
    lines.push(`${prefix}  значение ≈ <span class="accent">${data.result}</span>`);
    if (data.n) {
      lines.push(`${prefix}  разбиений n = ${data.n}`);
    }
    if (data.runge_error !== null) {
      lines.push(`${prefix}  оценка погрешности по Рунге ≈ ${data.runge_error}`);
    } else {
      lines.push(`${prefix}  оценка погрешности: точность не достигнута`);
    }
    if (data.exact_value !== null) {
      lines.push(`${prefix}  точное значение = ${data.exact_value}`);
    }
    if (data.exact_error !== null) {
      lines.push(`${prefix}  |погрешность| = ${data.exact_error}`);
    }
    lines.push("");
  }

  target.innerHTML = lines.join("\n");
}

function printImproperResult(target, results) {
  const prefix = "> ";

  const methodNames = {
    "rect_left": "Метод прямоугольников (левые)",
    "rect_right": "Метод прямоугольников (правые)",
    "rect_mid": "Метод прямоугольников (средние)",
    "trapezoid": "Метод трапеций",
    "simpson": "Метод Симпсона"
  };

  const lines = [];
  for (const [methodKey, data] of Object.entries(results)) {
    if (!data.ok) {
      lines.push(`${prefix}<span class="error">${methodNames[methodKey]}: ошибка - ${data.error}</span>`);
      continue;
    }

    if (!data.exists) {
      lines.push(`${prefix}${methodNames[methodKey]}: сходимость: интеграл не существует (расходится)`);
      lines.push(prefix);
      lines.push("");
      continue;
    }

    lines.push(`${prefix}${methodNames[methodKey]}: сходимость: интеграл существует (сходится)`);
    lines.push(`${prefix}значение ≈ <span class="accent">${data.value}</span>`);
    lines.push("");
  }

  target.innerHTML = lines.join("\n");
}

window.addEventListener("DOMContentLoaded", () => {
  const fnSelect = $("#function_key");
  const aInput = $("#a");
  const bInput = $("#b");
  const epsInput = $("#eps");
  const integralOutput = $("#integral-output");
  const improperOutput = $("#improper-output");
  const improperAInput = $("#improper_a");
  const improperBInput = $("#improper_b");

  function applyDefaults() {
    const opt = fnSelect.options[fnSelect.selectedIndex];
    aInput.value = opt.getAttribute("data-a");
    bInput.value = opt.getAttribute("data-b");
  }

  applyDefaults();

  fnSelect.addEventListener("change", applyDefaults);

  function applyDefaultsImproper() {
    const opt = $("#improper_key").options[$("#improper_key").selectedIndex];
    if (!opt) return;
    improperAInput.value = opt.getAttribute("data-a");
    improperBInput.value = opt.getAttribute("data-b");
  }

  applyDefaultsImproper();

  $("#improper_key").addEventListener("change", applyDefaultsImproper);

  $("#integral-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const methods = ["rect_left", "rect_right", "rect_mid", "trapezoid", "simpson"];
    const results = {};

    const basePayload = {
      function_key: fnSelect.value,
      a: aInput.value,
      b: bInput.value,
      eps: epsInput.value,
    };

    const promises = methods.map(async (methodKey) => {
      const payload = { ...basePayload, method_key: methodKey };
      try {
        const res = await fetch("/api/integrate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        results[methodKey] = data;
      } catch (err) {
        results[methodKey] = {
          ok: false,
          error: `ошибка сети: ${err}`,
        };
      }
    });

    await Promise.all(promises);
    printIntegralResult(integralOutput, results);
  });

  $("#improper-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const methods = ["rect_left", "rect_right", "rect_mid", "trapezoid", "simpson"];
    const results = {};

    const basePayload = {
      key: $("#improper_key").value,
      eps: $("#improper_eps").value,
      a: improperAInput.value,
      b: improperBInput.value,
    };

    const promises = methods.map(async (methodKey) => {
      const payload = { ...basePayload, method_key: methodKey };
      try {
        const res = await fetch("/api/improper", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        results[methodKey] = data;
      } catch (err) {
        results[methodKey] = {
          ok: false,
          error: `ошибка сети: ${err}`,
        };
      }
    });

    await Promise.all(promises);
    printImproperResult(improperOutput, results);
  });
});
