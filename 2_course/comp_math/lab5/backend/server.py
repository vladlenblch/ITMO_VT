import json
import math
import mimetypes
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from methods import (
    InterpolationError,
    finite_differences,
    interpolate_gauss,
    interpolate_lagrange,
    interpolate_newton_finite,
    normalize_points,
)


ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend"
VARIANT_FILE = Path(__file__).resolve().parent / "variant8.json"

FUNCTIONS = {
    "sin": ("sin(x)", math.sin),
    "cos": ("cos(x)", math.cos),
    "exp": ("exp(x)", math.exp),
    "ln": ("ln(x)", math.log),
    "sqrt": ("sqrt(x)", math.sqrt),
    "quadratic": ("x^2 + 2x + 1", lambda x: x * x + 2 * x + 1),
    "rational": ("1 / (1 + x^2)", lambda x: 1 / (1 + x * x)),
}

METHODS = {
    "lagrange": lambda xs, ys, x, options: interpolate_lagrange(xs, ys, x),
    "newton_finite": lambda xs, ys, x, options: interpolate_newton_finite(xs, ys, x),
    "gauss": lambda xs, ys, x, options: interpolate_gauss(xs, ys, x),
}

DEFAULT_METHODS = ["lagrange", "newton_finite", "gauss"]


def _read_json(handler):
    length = int(handler.headers.get("Content-Length", "0"))
    if length <= 0:
        return {}
    return json.loads(handler.rfile.read(length).decode("utf-8"))


def _variant_points():
    data = json.loads(VARIANT_FILE.read_text(encoding="utf-8"))
    return data["points"]["x"], data["points"]["y"]


def _points_from_payload(payload):
    target = float(payload.get("target", 0))
    source_function = None

    if payload.get("mode") == "function":
        function_id = payload.get("function", "sin")
        if function_id not in FUNCTIONS:
            raise InterpolationError("Unknown function.")
        source_function = function_id
        points = payload.get("points")
        if points:
            xs = points.get("x", [])
            ys = points.get("y", [])
        else:
            left = float(payload.get("left", 0))
            right = float(payload.get("right", 1))
            count = int(payload.get("count", 7))
            if count < 2 or left == right:
                raise InterpolationError("Function mode needs at least two nodes and a non-zero interval.")
            step = (right - left) / (count - 1)
            fn = FUNCTIONS[function_id][1]
            xs = [left + i * step for i in range(count)]
            ys = [float(fn(x)) for x in xs]
    else:
        points = payload.get("points")
        if points:
            xs = points.get("x", [])
            ys = points.get("y", [])
        else:
            xs, ys = _variant_points()

    xs, ys = normalize_points(xs, ys)
    return xs, ys, target, source_function


def _curve_points(xs, evaluator):
    left = min(xs)
    right = max(xs)
    points = []
    for i in range(180):
        x = left + (right - left) * i / 179
        try:
            points.append({"x": x, "y": float(evaluator(x))})
        except (InterpolationError, ValueError, OverflowError):
            pass
    return points


def _plot(xs, ys, source_function):
    curves = {
        "newton": _curve_points(xs, lambda x: interpolate_newton_finite(xs, ys, x)["value"]),
        "gauss": _curve_points(xs, lambda x: interpolate_gauss(xs, ys, x)["value"]),
    }
    if source_function:
        fn = FUNCTIONS[source_function][1]
        curves["truth"] = _curve_points(xs, fn)
    return curves


def _analyze(payload):
    xs, ys, target, source_function = _points_from_payload(payload)
    results = {}

    for method in payload.get("methods", DEFAULT_METHODS):
        if method not in METHODS:
            results[method] = {"method": method, "error": "Unknown method."}
            continue
        try:
            results[method] = METHODS[method](xs, ys, target, {})
        except InterpolationError as exc:
            results[method] = {"method": method, "error": str(exc)}

    return {
        "points": [{"x": x, "y": y} for x, y in zip(xs, ys)],
        "target": target,
        "finiteDifferences": finite_differences(ys),
        "results": results,
        "plot": {
            "nodes": [{"x": x, "y": y} for x, y in zip(xs, ys)],
            "curves": _plot(xs, ys, source_function),
        },
    }


class LabRequestHandler(BaseHTTPRequestHandler):
    server_version = "Lab5Interpolation/1.0"

    def _json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._json({})

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            self._json({"status": "ok"})
        elif path == "/api/functions":
            self._json([{"id": key, "label": value[0]} for key, value in FUNCTIONS.items()])
        else:
            self._static(path)

    def do_POST(self):
        if urlparse(self.path).path != "/api/interpolate":
            self._json({"error": "Unknown endpoint."}, 404)
            return
        try:
            self._json(_analyze(_read_json(self)))
        except (InterpolationError, ValueError, OverflowError) as exc:
            self._json({"error": str(exc)}, 400)

    def _static(self, path):
        if path in {"", "/"}:
            path = "/index.html"
        file_path = (FRONTEND_DIR / unquote(path).lstrip("/")).resolve()
        if not file_path.is_file() or FRONTEND_DIR.resolve() not in [file_path, *file_path.parents]:
            self.send_error(404)
            return

        body = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(str(file_path))[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main():
    host = "127.0.0.1"
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer((host, port), LabRequestHandler)
    print(f"Serving backend and frontend at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
