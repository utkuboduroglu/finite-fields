def extensiveGCD(x, y):
    if x < y:
        x, y = y, x
    div = lambda x, y: (x//y, x%y)
    factors = []

    n, q = x, y

    while q > 0:
        fac, rem = div(n, q)
        factors.append(fac)
        n = q
        q = rem

    # we throw out the last factor as we do not need it for divisibility
    factors = factors[::-1][1:]

    return n, factors

def pairBezout(x, y):
    coef = lambda P, c: (P[1], P[0] - P[1] * c)
    maxSorted = x < y
    d, factors = extensiveGCD(x, y)

    bezout = (0, 1)
    for fac in factors:
        bezout = coef(bezout, fac)

    if maxSorted:
        bezout = (bezout[1], bezout[0])

    return bezout

def testValidBezout(x, y):
    d, _ = extensiveGCD(x, y)
    p, q = pairBezout(x, y)
    left = (p == 0) or (p * x % y == d)
    right = (q == 0) or (q * y % x == d)
    return all([left, right])


def is_prime(n):
    from math import sqrt, ceil
    # we only need to check whether primes up to faclimit divide n, as some
    # factor needs to be smaller than faclimit (can be proven by
    # contradiction!) in fact, we can check whether any number in this range
    # divides n: this is way more expensive but for small numbers we don't have
    # to worry about finding primes inside the range 
    faclimit = ceil(sqrt(n))

    for q in range(2, faclimit + 1):
        if n % q == 0:
            return False

    return True

class FiniteField:
    def __init__(self, p):
        if not is_prime(p):
            raise ValueError("Specified value {} should be prime!".format(p))
        self._p = p

    def add(self, a, b):
        return (a + b) % self._p

    def sub(self, a, b):
        return self.add(a, -b)

    def add_inv(self, a):
        return self.sub(0, a)

    def mult(self, a, b):
        return (a * b) % self._p

    def mult_inv(self, a):
        if a == 0:
            raise ZeroDivisionError
        b, _ = pairBezout(a, self._p)
        return self.add(b, 0)

    def div(self, a, b):
        return self.mult(a, self.mult_inv(b))

