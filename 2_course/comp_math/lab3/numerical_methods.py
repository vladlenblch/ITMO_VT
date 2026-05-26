def f1(x):
    return 4 * x**3 - 5 * x**2 + 6 * x - 7

def f2(x):
    return 3 * x**3 - 2 * x**2 - 7 * x - 8

def f3(x):
    return 2 * x**3 - 3 * x**2 + 5 * x - 9

FUNCTIONS = {
    "f1": {
        "func": f1,
        "name": "f₁(x) = 4x³ - 5x² + 6x - 7",
        "default_a": 0.0,
        "default_b": 2.0,
        "exact": lambda a, b: (
            (x := b) and (b**4 - (5 / 3) * b**3 + 3 * b**2 - 7 * b)
        ) - (
            (x := a) and (a**4 - (5 / 3) * a**3 + 3 * a**2 - 7 * a)
        ),
    },
    "f2": {
        "func": f2,
        "name": "f₂(x) = 3x³ - 2x² - 7x - 8",
        "default_a": 2.0,
        "default_b": 3.0,
        "exact": lambda a, b: (
            (3 / 4) * (b**4 - a**4)
            - (2 / 3) * (b**3 - a**3)
            - (7 / 2) * (b**2 - a**2)
            - 8 * (b - a)
        ),
    },
    "f3": {
        "func": f3,
        "name": "f₃(x) = 2x³ - 3x² + 5x - 9",
        "default_a": 1.0,
        "default_b": 2.0,
        "exact": lambda a, b: (
            0.5 * (b**4 - a**4)
            - (b**3 - a**3)
            + 2.5 * (b**2 - a**2)
            - 9 * (b - a)
        ),
    },
}

def rectangle_left(f, a, b, n):
    h = (b - a) / n
    s = 0.0
    x = a
    for _ in range(n):
        s += f(x)
        x += h
    return s * h

def rectangle_right(f, a, b, n):
    h = (b - a) / n
    s = 0.0
    x = a + h
    for _ in range(n):
        s += f(x)
        x += h
    return s * h

def rectangle_middle(f, a, b, n):
    h = (b - a) / n
    s = 0.0
    x = a + h / 2
    for _ in range(n):
        s += f(x)
        x += h
    return s * h

def trapezoid(f, a, b, n):
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    x = a + h
    for _ in range(1, n):
        s += f(x)
        x += h
    return s * h

def simpson(f, a, b, n):
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    x = a + h
    for i in range(1, n):
        coeff = 4 if i % 2 == 1 else 2
        s += coeff * f(x)
        x += h
    return s * h / 3

METHODS = {
    "rect_left": {
        "name": "Метод прямоугольников (левые)",
        "func": rectangle_left,
        "order": 2,
    },
    "rect_right": {
        "name": "Метод прямоугольников (правые)",
        "func": rectangle_right,
        "order": 2,
    },
    "rect_mid": {
        "name": "Метод прямоугольников (средние)",
        "func": rectangle_middle,
        "order": 2,
    },
    "trapezoid": {
        "name": "Метод трапеций",
        "func": trapezoid,
        "order": 2,
    },
    "simpson": {
        "name": "Метод Симпсона",
        "func": simpson,
        "order": 4,
    },
}

def integrate_with_runge(f, a, b, method_key, eps, n0=4, n_max=4 * 1024 * 1024):
    method_info = METHODS[method_key]
    method = method_info["func"]
    p = method_info["order"]

    n = max(1, n0)
    i_n = method(f, a, b, n)

    while n * 2 <= n_max:
        n2 = n * 2
        i_n2 = method(f, a, b, n2)
        err = abs(i_n2 - i_n) / (2**p - 1)
        if err < eps:
            return i_n2, n2, err
        n, i_n = n2, i_n2

    return i_n, n, None
