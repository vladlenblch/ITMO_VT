from __future__ import annotations

import math
from dataclasses import dataclass

from flask import Flask, jsonify, render_template, request

from numerical_methods import FUNCTIONS, METHODS, integrate_with_runge
from improper_integrals import IMPROPER_INTEGRALS, improper_integral_numeric

app = Flask(__name__)

@dataclass
class IntegrationRequest:
    function_key: str
    method_key: str
    a: float
    b: float
    eps: float

def parse_float(value, field_name):
    if value is None or str(value).strip() == "":
        return None
    try:
        cleaned_value = str(value).strip().replace(',', '.')
        return float(cleaned_value)
    except ValueError:
        raise ValueError(f"Поле '{field_name}' должно содержать число")

def parse_integration_request(data):
    try:
        function_key = str(data["function_key"])
        method_key = str(data["method_key"])
        
        a = parse_float(data.get("a"), "a")
        if a is None:
            raise ValueError("Поле 'a' не заполнено")
        if not math.isfinite(a):
            raise ValueError("Нижний предел a должен быть конечным числом")
        
        b = parse_float(data.get("b"), "b")
        if b is None:
            raise ValueError("Поле 'b' не заполнено")
        if not math.isfinite(b):
            raise ValueError("Верхний предел b должен быть конечным числом")
        
        eps = parse_float(data.get("eps"), "eps")
        if eps is None:
            raise ValueError("Поле 'eps' не заполнено")
        if not math.isfinite(eps):
            raise ValueError("Точность eps должна быть конечным числом")
        if eps <= 0:
            raise ValueError("Точность должна быть положительной")
        
        if a >= b:
            raise ValueError("Нижний предел a должен быть меньше верхнего предела b")
        
    except (KeyError, TypeError):
        raise ValueError("Некорректные входные данные")

    return IntegrationRequest(function_key, method_key, a, b, eps)

@app.route("/")
def index():
    return render_template(
        "index.html",
        functions=FUNCTIONS,
        methods=METHODS,
        improper_integrals=IMPROPER_INTEGRALS,
    )

@app.route("/api/integrate", methods=["POST"])
def api_integrate():
    try:
        data = request.get_json(force=True)
        params = parse_integration_request(data)

        f_info = FUNCTIONS[params.function_key]
        f = f_info["func"]

        result, n, err = integrate_with_runge(
            f, params.a, params.b, params.method_key, params.eps
        )

        if err is None:
            raise ValueError("Точность не достигнута: превышено максимальное число разбиений (n_max = 4194304)")

        if not math.isfinite(result):
            raise ValueError("Не удалось вычислить интеграл (результат бесконечен или не определен)")

        if math.isnan(err):
            err = None

        exact_value = None
        exact_error = None
        if (exact := f_info.get("exact")) is not None:
            exact_value = exact(params.a, params.b)
            if math.isfinite(exact_value):
                exact_error = abs(result - exact_value)
                if not math.isfinite(exact_error):
                    exact_error = None
            else:
                exact_value = None

        return jsonify(
            {
                "ok": True,
                "result": result,
                "n": n,
                "runge_error": err,
                "exact_value": exact_value,
                "exact_error": exact_error,
            }
        )
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

@app.route("/api/improper", methods=["POST"])
def api_improper():
    try:
        data = request.get_json(force=True)
        
        key = str(data.get("key", "").strip())
        if not key:
            raise ValueError("Поле 'key' не заполнено")
        
        method_key = str(data.get("method_key", "").strip())
        if not method_key:
            raise ValueError("Поле 'method_key' не заполнено")
        
        eps = parse_float(data.get("eps"), "eps")
        if eps is None:
            raise ValueError("Поле 'eps' не заполнено")
        if eps <= 0:
            raise ValueError("Точность должна быть положительной")
        
        a_override = parse_float(data.get("a"), "a")
        b_override = parse_float(data.get("b"), "b")
        
        if a_override is not None and not math.isfinite(a_override):
            raise ValueError("Предел a должен быть конечным числом")
        if b_override is not None and not math.isfinite(b_override):
            raise ValueError("Предел b должен быть конечным числом")
        
        info = IMPROPER_INTEGRALS[key]
        
        a = info.a if a_override is None else a_override
        b = info.b if b_override is None else b_override
        
        if a >= b:
            raise ValueError("Нижний предел a должен быть меньше верхнего предела b")
        
        value, iterations, convergent, error_message = improper_integral_numeric(
            key,
            method_key,
            eps,
            a_override=a_override,
            b_override=b_override,
        )
        
        if not convergent:
            return jsonify(
                {
                    "ok": True,
                    "exists": False,
                    "message": error_message or "Интеграл не существует (расходится)",
                }
            )

        return jsonify(
            {
                "ok": True,
                "exists": True,
                "value": value,
                "iterations": iterations,
            }
        )
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
