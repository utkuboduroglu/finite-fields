def extendedGCD(x, y):
    if x < y:
        x, y = y, x
    div = lambda x, y: (x//y, x%y)
    factors = []

    # this is totally unnecessary, it just felt appropriate to relabel
    # the variables in a form similar to the DA: n = pq + r
    n, q = x, y

    while q > 0:
        fac, rem = div(n, q)
        factors.append(fac)
        n = q
        q = rem

    return n, factors

def pairBezout(x, y):
    coef = lambda P, c: (P[1], P[0] - P[1] * c)
    maxSorted = x < y
    d, factors = extendedGCD(x, y)

    # we throw out the last factor as we do not need it for divisibility
    factors = factors[::-1][1:]

    bezout = (0, 1)
    for fac in factors:
        bezout = coef(bezout, fac)

    if maxSorted:
        bezout = (bezout[1], bezout[0])

    return bezout

def is_prime(n):
    from math import sqrt, ceil
    # we only need to check whether primes up to faclimit divide n, as some
    # factor needs to be smaller than faclimit (can be proven by
    # contradiction!) in fact, we can check whether any number in this range
    # divides n: this is way more expensive but for small numbers we don't have
    # to worry about finding primes inside the range 
    faclimit = ceil(sqrt(n))

    # we can divide the search in half just by testing for 2 and
    # limiting ourselves to odd primes
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for q in range(3, faclimit + 1, 2):
        if n % q == 0:
            return False

    return True

    
class FiniteIntegerRing:
    def __init__(self, n):
        if n == 0:
            raise ValueError("Do not specify 0! Use normal operations instead!")
        elif n < 0:
            n = -n

        self._n = n
    
    def add(self, a, b):
        return (a + b) % self._n

    def sub(self, a, b):
        return self.add(a, -b)

    def id(self, a):
        return self.add(a, 0)

    def add_inv(self, a):
        return self.add(-a, 0)

    def mult(self, a, b):
        return (a * b) % self._n

    # Note that every ring has repeated multiplication, but in
    # the case of the integers, we can also think of it as exponentiation!
    def pow(self, b, e):
        c = 1
        for f in range(e):
            f += 1
            c = self.mult(b, c)
        return c
        

class FiniteField(FiniteIntegerRing):
    def __init__(self, p):
        if not is_prime(p):
            raise ValueError("Specified value {} should be prime!".format(p))
        self._n = p

    def mult_inv(self, a):
        if a == 0:
            raise ZeroDivisionError

        b, _ = pairBezout(self.id(a), self._n)
        return self.id(b)

    def div(self, a, b):
        return self.mult(a, self.mult_inv(b))
