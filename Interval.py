from numpy import inf

class Interval:
    def __init__(self, lb, ub):
        if isinstance((lb, ub), (int, float)) and lb > ub:
            raise ValueError(f"Lower bound {lb} can't be greater than upper bound {ub}")
        self.lb = lb
        self.ub = ub

    def _add(self, other):
        l1, u1 = self
        if isinstance(other, Interval):
            l2, u2 = other
            lb = l1 + l2
            ub = u1 + u2
        elif isinstance(other, (int, float)):
            lb = l1 + other
            ub = u1 + other
        else:
            raise TypeError(f"Unsupported operand type(s) for +: '{type(self)}' and '{type(other)}'")
        return lb, ub

    def __add__(self, other):
        return Interval(*self._add(other))

    __radd__ = __add__

    def __iadd__(self, other):
        self.lb, self.ub = self._add(other)
        return self

    def __neg__(self):
        return Interval(-self.ub, -self.lb)

    def _sub(self, other):
        if isinstance(other, (Interval, int, float)):
            return self._add(-other)
        else:
            raise TypeError(f"Unsupported operand type(s) for -: '{type(self)}' and '{type(other)}'")

    def __sub__(self, other):
        return Interval(*self._sub(other))

    def __isub__(self, other):
        self.lb, self.ub = self._sub(other)
        return self

    def _mul(self, other):
        l1, u1 = self
        if isinstance(other, Interval):
            l2, u2 = other 
            lb = min(l1*l2, l1*u2, u1*l2, u1*u2)
            ub = max(l1*l2, l1*u2, u1*l2, u1*u2)
        elif isinstance(other, (int, float)):
            if other >= 0:
                lb = l1 * other
                ub = u1 * other
            else:
                lb = u1 * other
                ub = l1 * other
        else:
            raise TypeError(f"Unsupported operand types(s) for *: '{type(self)}' and '{type(other)}'")

        return lb, ub

    def __mul__(self, other):
        return Interval(*self._mul(other))

    __rmul__ = __mul__

    def __imul__(self, other):
        self.lb, self.ub = self._mul(other)
        return self

    # Not robust
    def __pow__(self, other):
        res = Interval(self.lb, self.ub)
        while other := other - 1:
            res *= res
        return res

    def _truediv(self, other):
        if isinstance(other, Interval):
            l1, u1 = self
            l2, u2 = other

            if 0 not in other:
                other = Interval(1 / u2, 1 / l2)
                return self._mul(other)

            else:
                if 0 in self:
                    return -inf, inf
                elif l2 == u2 == 0:
                    return None, None                   # Empty interval 
                elif u1 < 0:
                    if u2 == 0:
                        return u1 / l2, inf
                    if l2 < 0 < u2:
                        return -inf, inf                # [-inf, u1 / u2] U [u1 / l2, inf]
                    if l2 == 0:
                        return -inf, u1 / u2
                elif 0 < l1:
                    if u2 == 0:
                        return -inf, l1 / l2
                    if l2 < 0 < u2:
                        return -inf, inf                # [-inf, l1 / l2] U [l1 / u2, inf]
                    if l2 == 0:
                        return l1 / u2, inf

        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError(f"Interval division by zero: {self} / {other}")
            else:
                other = 1 / other
                return self._mul(other)
        else:
            raise TypeError(f"Unsupported operand type(s) for /: '{type(self)}' and '{type(other)}'")

    def __truediv__(self, other):
        return Interval(*self._truediv(other))

    def __itruediv__(self, other):
        self.lb, self.ub = self._truediv(other)
        return self

    def __repr__(self):
        return f"Interval({self.lb}, {self.ub})"

    def __str__(self):
        return f"[{self.lb}, {self.ub}]"

    def __contains__(self, item):
        return self.lb <= item and item <= self.ub

    def __iter__(self):
        return iter((self.lb, self.ub))
