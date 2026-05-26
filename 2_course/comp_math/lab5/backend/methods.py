from math import factorial, isfinite


class InterpolationError(ValueError):
    pass


def _term(order, coefficient, difference, value, index=None, label=None):
    return {
        "order": order,
        "coefficient": coefficient,
        "difference": difference,
        "value": value,
        "index": index,
        "label": label,
    }


def normalize_points(xs, ys):
    x_list = list(xs)
    y_list = list(ys)
    if len(x_list) != len(y_list):
        raise InterpolationError("The x and y arrays must have the same length.")

    points = [(float(x), float(y)) for x, y in zip(x_list, y_list)]
    if len(points) < 2:
        raise InterpolationError("Need at least two interpolation nodes.")

    for x, y in points:
        if not isfinite(x) or not isfinite(y):
            raise InterpolationError("All node coordinates must be finite numbers.")

    points.sort(key=lambda point: point[0])
    for left, right in zip(points, points[1:]):
        if abs(left[0] - right[0]) < 1e-12:
            raise InterpolationError("Interpolation nodes must have distinct x values.")

    return [point[0] for point in points], [point[1] for point in points]


def _require_equal_step(xs, tolerance=1e-9):
    h = xs[1] - xs[0]
    if abs(h) < tolerance:
        raise InterpolationError("Step must be non-zero.")

    for left, right in zip(xs, xs[1:]):
        if abs((right - left) - h) > tolerance:
            raise InterpolationError("This method requires equally spaced x values.")
    return h


def finite_differences(ys):
    levels = [[float(y) for y in ys]]
    if len(levels[0]) < 2:
        raise InterpolationError("Need at least two y values.")

    while len(levels[-1]) > 1:
        previous = levels[-1]
        levels.append([previous[i + 1] - previous[i] for i in range(len(previous) - 1)])
    return levels


def interpolate_lagrange(xs, ys, target):
    x_values, y_values = normalize_points(xs, ys)
    x_target = float(target)
    if not isfinite(x_target):
        raise InterpolationError("Target x must be finite.")

    total = 0.0
    terms = []
    for i, x_i in enumerate(x_values):
        basis = 1.0
        for j, x_j in enumerate(x_values):
            if i != j:
                basis *= (x_target - x_j) / (x_i - x_j)
        value = y_values[i] * basis
        terms.append({"index": i, "x": x_i, "y": y_values[i], "basis": basis, "value": value})
        total += value

    return {"method": "lagrange", "value": total, "terms": terms}


def interpolate_newton_finite(xs, ys, target, formula="auto"):
    x_values, y_values = normalize_points(xs, ys)
    h = _require_equal_step(x_values)
    diffs = finite_differences(y_values)
    x_target = float(target)
    n = len(x_values)

    if formula == "auto":
        formula = "first" if x_target <= (x_values[0] + x_values[-1]) / 2 else "second"
    if formula not in {"first", "second"}:
        raise InterpolationError("Newton formula must be auto, first or second.")

    if formula == "first":
        q = (x_target - x_values[0]) / h
        total = y_values[0]
        product = 1.0
        terms = [_term(0, 1.0, y_values[0], y_values[0], 0)]
        for order in range(1, n):
            product *= q - (order - 1)
            coefficient = product / factorial(order)
            difference = diffs[order][0]
            value = coefficient * difference
            total += value
            terms.append(_term(order, coefficient, difference, value, 0))
    else:
        q = (x_target - x_values[-1]) / h
        total = y_values[-1]
        product = 1.0
        terms = [_term(0, 1.0, y_values[-1], y_values[-1], n - 1)]
        for order in range(1, n):
            product *= q + (order - 1)
            coefficient = product / factorial(order)
            index = n - 1 - order
            difference = diffs[order][index]
            value = coefficient * difference
            total += value
            terms.append(_term(order, coefficient, difference, value, index))

    return {
        "method": "newton_finite",
        "value": total,
        "q": q,
        "h": h,
        "table": diffs,
        "terms": terms,
    }


def _gauss_term_specs(order, formula):
    if formula == "first":
        if order % 2 == 0:
            radius = order // 2
            return list(range(radius - 1, -radius - 1, -1)), -radius
        radius = (order - 1) // 2
        return list(range(radius, -radius - 1, -1)), -radius

    if order % 2 == 0:
        radius = order // 2
        return list(range(-(radius - 1), radius + 1)), -radius
    radius = (order - 1) // 2
    return list(range(-radius, radius + 1)), -(radius + 1)


def _valid_difference(levels, order, index):
    return 0 <= order < len(levels) and 0 <= index < len(levels[order])


def _product(values):
    result = 1.0
    for value in values:
        result *= value
    return result


def interpolate_gauss(xs, ys, target, formula="auto", center_index=None):
    x_values, y_values = normalize_points(xs, ys)
    h = _require_equal_step(x_values)
    diffs = finite_differences(y_values)
    x_target = float(target)
    n = len(x_values)

    if center_index is None:
        if formula == "second":
            center_index = min(range(n), key=lambda i: (abs(x_values[i] - x_target), -i))
        else:
            candidates = [i for i in range(n - 1) if x_values[i] <= x_target <= x_values[i + 1]]
            center_index = candidates[-1] if candidates else min(range(n), key=lambda i: abs(x_values[i] - x_target))
            if center_index == n - 1:
                center_index = n - 2

    if not 0 <= center_index < n:
        raise InterpolationError("Center index is out of range.")

    q = (x_target - x_values[center_index]) / h
    if formula == "auto":
        formula = "first" if q >= 0 else "second"
    if formula not in {"first", "second"}:
        raise InterpolationError("Gauss formula must be auto, first or second.")

    total = y_values[center_index]
    terms = [_term(0, 1.0, y_values[center_index], y_values[center_index], center_index)]
    for order in range(1, n):
        shifts, index_shift = _gauss_term_specs(order, formula)
        index = center_index + index_shift
        if not _valid_difference(diffs, order, index):
            break
        coefficient = _product(q + shift for shift in shifts) / factorial(order)
        difference = diffs[order][index]
        value = coefficient * difference
        total += value
        terms.append(_term(order, coefficient, difference, value, index))

    return {
        "method": "gauss",
        "value": total,
        "q": q,
        "h": h,
        "centerIndex": center_index,
        "table": diffs,
        "terms": terms,
    }
