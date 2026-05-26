import math
from numerical_methods import integrate_with_runge, METHODS

class ImproperIntegral:
    def __init__(self, func, a, b, singular_points, name, description, power=0.5):
        self.func = func
        self.a = a
        self.b = b
        self.singular_points = singular_points
        self.name = name
        self.description = description
        self.power = power

def g1(x):
    if x <= 0:
        return float("inf")
    return 1.0 / math.sqrt(x)

def g2(x):
    if x >= 1:
        return float("inf")
    return 1.0 / math.sqrt(1.0 - x)

def g3(x):
    if x == 0.5:
        return float("inf")
    return 1.0 / math.sqrt(abs(x - 0.5))

def g4(x):
    if x <= 0:
        return float("inf")
    return 1.0 / (x ** 1.5)

def g5(x):
    if x >= 1:
        return float("inf")
    return 1.0 / ((1.0 - x) ** 1.5)

def g6(x):
    if x == 0.5:
        return float("inf")
    return 1.0 / (abs(x - 0.5) ** 1.5)

IMPROPER_INTEGRALS = {
    "g1": ImproperIntegral(
        func=g1, a=0.0, b=1.0, singular_points=(0.0,),
        name="g₁(x) = 1/√x",
        description="Несобственный интеграл 2 рода: разрыв в левой границе (a)",
        power=0.5
    ),
    "g2": ImproperIntegral(
        func=g2, a=0.0, b=1.0, singular_points=(1.0,),
        name="g₂(x) = 1/√(1-x)",
        description="Несобственный интеграл 2 рода: разрыв в правой границе (b)",
        power=0.5
    ),
    "g3": ImproperIntegral(
        func=g3, a=0.0, b=1.0, singular_points=(0.5,),
        name="g₃(x) = 1/√|x-0.5|",
        description="Несобственный интеграл 2 рода: разрыв внутри отрезка",
        power=0.5
    ),
    "g4": ImproperIntegral(
        func=g4, a=0.0, b=1.0, singular_points=(0.0,),
        name="g₄(x) = 1/x^{3/2}",
        description="Несобственный интеграл 2 рода: разрыв в левой границе (a)",
        power=1.5
    ),
    "g5": ImproperIntegral(
        func=g5, a=0.0, b=1.0, singular_points=(1.0,),
        name="g₅(x) = 1/(1-x)^{3/2}",
        description="Несобственный интеграл 2 рода: разрыв в правой границе (b)",
        power=1.5
    ),
    "g6": ImproperIntegral(
        func=g6, a=0.0, b=1.0, singular_points=(0.5,),
        name="g₆(x) = 1/|x-0.5|^{3/2}",
        description="Несобственный интеграл 2 рода: разрыв внутри отрезка",
        power=1.5
    ),
}

def check_convergence_and_compute(f, a, b, singular_point, method_key, eps, n0=4):
    tolerance = 1e-9
    is_singular_at_a = abs(singular_point - a) < tolerance
    is_singular_at_b = abs(singular_point - b) < tolerance
    is_singular_inside = (a + tolerance < singular_point < b - tolerance)
    
    if not (is_singular_at_a or is_singular_at_b or is_singular_inside):
        try:
            val, n, err = integrate_with_runge(f, a, b, method_key, eps, n0)
            if math.isinf(val) or math.isnan(val):
                return False, None, 0
            return True, val, n
        except Exception:
            return False, None, 0

    eps_sing = 1e-2
    min_eps_sing = 1e-12
    values_history = []
    eps_history = []
    max_iterations = 25
    
    for i in range(max_iterations):
        current_eps = eps_sing * (0.5 ** i)
        if current_eps < min_eps_sing:
            break
            
        try:
            if is_singular_at_a:
                start = a + current_eps
                end = b
            elif is_singular_at_b:
                start = a
                end = b - current_eps
            else:
                left, _, _ = integrate_with_runge(f, a, singular_point - current_eps, method_key, eps, n0)
                right, _, _ = integrate_with_runge(f, singular_point + current_eps, b, method_key, eps, n0)
                val = left + right
                values_history.append(val)
                eps_history.append(current_eps)
                
                if len(values_history) >= 5:
                    result = analyze_convergence(values_history, eps_history, eps)
                    if result is not None:
                        return result
                continue

            val, _, _ = integrate_with_runge(f, start, end, method_key, eps, n0)
            values_history.append(val)
            eps_history.append(current_eps)
            
            if len(values_history) >= 5:
                result = analyze_convergence(values_history, eps_history, eps)
                if result is not None:
                    return result
                    
        except Exception as e:
            break

    if len(values_history) >= 3:
        result = analyze_convergence(values_history, eps_history, eps, final=True)
        if result is not None:
            return result
    
    if len(values_history) >= 1 and abs(values_history[-1]) < 1e6:
        return True, values_history[-1], len(values_history)
    
    return False, None, len(values_history)

def analyze_convergence(values, epsilons, eps, final=False):
    if len(values) < 5 and not final:
        return None
    
    n = len(values)
    last_vals = values[-5:] if n >= 5 else values
    
    if any(abs(v) > 1e7 for v in last_vals):
        return False, None, n
    
    if n >= 5:
        growth_count = 0
        for i in range(1, len(last_vals)):
            if abs(last_vals[i]) > abs(last_vals[i-1]) * 1.1:
                growth_count += 1
        
        if growth_count >= 4:
            return False, None, n
    
    if n >= 5:
        max_val = max(abs(v) for v in last_vals)
        if max_val < 1e-10:
            return True, values[-1], n
        
        rel_diff = abs(last_vals[-1] - last_vals[-2]) / max_val
        
        if rel_diff < eps * 1000:
            if n >= 6:
                prev_diff = abs(last_vals[-2] - last_vals[-3]) / max_val
                if rel_diff <= prev_diff:
                    return True, values[-1], n
            else:
                return True, values[-1], n
    
    if not final:
        return None
    
    if abs(values[-1]) < 1e5:
        return True, values[-1], n
    
    return False, None, n

def improper_integral_numeric(key, method_key, eps, n0=4, a_override=None, b_override=None):
    info = IMPROPER_INTEGRALS[key]
    a = info.a if a_override is None else a_override
    b = info.b if a_override is None else a_override
    b = info.b if b_override is None else b_override
    f = info.func

    if a >= b:
        return None, 0, False, "Некорректные пределы интегрирования (a >= b)"

    if len(info.singular_points) != 1:
        return None, 0, False, "Поддерживается только одна особая точка"

    c = info.singular_points[0]
    
    convergent, value, iterations = check_convergence_and_compute(
        f, a, b, c, method_key, eps, n0
    )

    if not convergent:
        return None, iterations, False, "Интеграл не существует (расходится)"
    
    if value is None or math.isnan(value) or math.isinf(value):
        return None, iterations, False, "Интеграл не существует (расходится)"
    
    return value, iterations, True, None
