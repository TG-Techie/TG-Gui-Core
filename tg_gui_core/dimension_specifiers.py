# The MIT License (MIT)
#
# Copyright (c) 2021 Jonah Yolles-Murphy (TG-Techie)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
This file is under active development.
"""


class DimensionSpecifier:
    pass


class _calc_Based(DimensionSpecifier):
    def __init__(self, _for_superior=False):
        self._for_superior = _for_superior
        self._ops = []

    def _base_dim(self, inst):
        raise NotImplementedError()

    def _calc_dim_(self, inst):
        dim = self._base_dim(inst)
        for op, val in self._ops:
            if isinstance(val, DimensionSpecifier):
                val = val._calc_dim_(inst)
            if op == "+":
                dim += val
            elif op == "-":
                dim -= val
            elif op == "*":
                dim *= val
            elif op == "//":
                dim //= val
            else:
                raise NotImplementedError(
                    f"{repr(op)} not supported for dimension specifiers"
                )
        return dim

    def __add__(self, value):
        self._ops.append(("+", value))
        return self

    def __sub__(self, value):
        self._ops.append(("-", value))
        return self

    def __rsub__(self, value):
        self._ops.append(("r-", value))
        return self

    def __mul__(self, value):
        self._ops.append(("*", value))
        return self

    def __rmul__(self, value):
        self._ops.append(("*", value))
        return self

    def __floordiv__(self, value):
        self._ops.append(("//", value))
        return self


class WidthForwardSpecifier(_calc_Based):
    def _base_dim(self, inst):
        if self._for_superior:
            return inst._superior_.width
        else:
            return inst.width


class HeightForwardSpecifier(_calc_Based):
    def _base_dim(self, inst):
        if self._for_superior:
            return inst._superior_.height
        else:
            return inst.height


# WidthSpecifier
class width(_calc_Based):
    def __init__(self, ref):
        super().__init__()
        self._ref = ref

    def _base_dim(self, inst):
        return self._ref.width


# HeightSpecifier
class height(_calc_Based):
    def __init__(self, ref):
        super().__init__()
        self._ref = ref

    def _base_dim(self, inst):
        return self._ref.height
