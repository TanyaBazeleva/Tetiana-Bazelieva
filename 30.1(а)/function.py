"""
Doctest
>>> from function import function
>>> function(0, 0.1)
0
>>> function(0.9, 0.0001) > function(0.8, 0.0001)
True
>>> from math import log
>>> abs(function(0.9, 0.0001) - log(1.9)) < 0.0002
True
"""

def function(x, eps):
    assert abs(x) < 1
    assert eps > 0

    a = x
    s = a
    i = 1
    while abs(a) > eps:
        a *= -x * i / (i + 1)
        s += a
        i += 1
    return s
