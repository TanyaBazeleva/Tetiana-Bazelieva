def f_ln(x, eps):
    """
    Обчислює суму всіх доданків при заданому x, що за абсолютною величиною не перевищують заданого eps > 0.
    """
    try:
        if abs(x) >= 1:
            s = None; Err = 1
            raise ValueError
        elif eps <= 0 or eps >= 1:
            s = None; Err = 2
            raise ValueError
        else:
            Err = 0
            s = 0; mx = -x; h = -1; z = 0
            while True:
                z += 1; h *= mx; a = h / z
                if abs(a) < eps: break
                s += a
    except ValueError:
        if Err == 1:
            print("f_LN: Помилка: Значення abs(x) >=1 !")
        elif Err == 2:
            print("f_LN: Помилка: значення eps не ∈ (0,1) !")
    return Err
