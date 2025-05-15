def f_sum(x, eps):
    if abs(x) >= 1:
        return 0, 1
    if eps <= 0:
        return 0, 2
    term = 1.0
    total = term
    k = 1
    num = 1  # чисельник (1, 1*3, 1*3*5, ...)
    denom = 1  # знаменник (1, 2*4, 2*4*6, ...)
    sign = -1
    while abs(term) >= eps:
        num *= (2 * k - 1)
        denom *= (2 * k)
        term = sign * (num / denom) * (x ** k)
        total += term
        sign *= -1
        k += 1
    return total, 0
