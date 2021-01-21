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


class PositionSpecifier:
    def __init__(self, ref):
        self._ref = ref

    def _calc_coord_(self, inst):
        return (self._calc_x_(inst), self._calc_y_(inst))

    def _calc_x_(self, inst):
        # default to centered
        ref = self._ref
        return ref.x + ref.width//2 - inst.width//2

    def _calc_y_(self, inst):
        # default to centered
        return ref.y + ref.height//2 - inst.height//2

class centerto(PositionSpecifier):
    pass

class leftof(PositionSpecifier):

    def _calc_x_(self, inst):
        return self._ref.x - inst.width

class rightof(PositionSpecifier):

    def _calc_x_(self, inst):
        return self._ref.x + self._ref.width

class below(PositionSpecifier):

    def _calc_y_(self, inst):
        return self._ref.y + self._ref.height

class above(PositionSpecifier):

    def _calc_y_(self, inst):
        return self._ref.y - inst.height

class XSpecifier(PositionSpecifier):

    def _calc_x_(self, inst):
        return self._ref.x

    def _calc_y_(self, inst):
        raise ValueError(f"XSpecifiers cannot be used for y coordinates")


class YSpecifier(PositionSpecifier):

    def _calc_x_(self, inst):
        raise ValueError(f"YSpecifiers cannot be used for y coordinates")

    def _calc_y_(self, inst):
        return self._ref.y


class _SuperiorCenter(PositionSpecifier):
    def __init__(self):
        pass

    def _calc_x_(self, inst):
        return inst._superior_.width // 2 - inst.width // 2

    def _calc_y_(self, inst):
        return inst._superior_.height // 2 - inst.height // 2


class ConstantPosition(PositionSpecifier):
    def __init__(self, x, y, *, name=None):
        self._name = name
        self._x = x
        self._y = y

    def __repr__(self):
        if self._name is None:
            x = str(self._x) if self._x is not None else "_"
            y = str(self._y) if self._y is not None else "_"
            return f"<{type(self).__name__} ({x}, {y})>"
        else:
            return f"<{type(self).__name__} {self._name}>"

    def _calc_x_(self, inst):
        if self._x is None:
            raise ValueError(f"{self} cannot be used to specify x coordinates")
        return self._x

    def _calc_y_(self, inst):
        if self._y is None:
            raise ValueError(f"{self} cannot be used to specify y coordinates")
        return self._y


center = _SuperiorCenter()

top = ConstantPosition(None, 0, name="top")
bottom = ConstantPosition(None, -1, name="bottom")

left = ConstantPosition(0, None, name="left")
right = ConstantPosition(-1, None, name="right")
