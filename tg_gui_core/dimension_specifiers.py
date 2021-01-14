
class DimensionSpecifier():
    pass

class _calc_Based (DimensionSpecifier):

    def __init__(self):
        self._ops = []

    def _base_dim(self):
        raise NotImplementedError()

    def _calc_dim_(self):
        dim = self._base_dim()
        for op, val in self._ops:
            if isinstance(val, DimensionSpecifier):
                val = val._calc_dim_()
            if   op == '+': dim += val
            elif op == '-': dim -= val
            elif op == '*': dim *= val
            elif op == '//': dim //= val
            else: raise ValueError(
                f"{repr(op)} not supported for dimension specifiers"
            )

    def __add__(self, value):
        self._ops.append(('+', value))

    def __sub__(self, value):
        self._ops.append(('-', value))

    def __mul__(self, value):
        self._ops.append(('*', value))

    def __floordiv__(self, value):
        self._ops.append(('//', value))

def _Infer(DimensionSpecifier):
    pass

# infer = _Infer()
