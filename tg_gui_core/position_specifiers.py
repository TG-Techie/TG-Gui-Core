#def under(wid):
#    return wid.y + wid.height

# TODO: add xReference and yreferecne so that (top, left) can be switched around

class PositionSpecifier():

    def __init__(self, ref):
        self._ref = ref

    def _calc_coord_(self, inst):
        return (self._calc_x_(inst), self._calc_y_(inst))

    def _calc_x_(self, inst):
        raise NotImplementedError("cannot use a raw PositionSpecifier for x")

    def _calc_y_(self, inst):
        raise NotImplementedError("cannot use a raw PositionSpecifier for y")

class leftof(PositionSpecifier):

    def _calc_x_(self, inst):
        return self._ref.x - inst.width

    def _calc_y_(self, inst):
        return self._ref.y


class rightof(PositionSpecifier):

    def _calc_x_(self, inst):
        ref = self._ref
        return ref.x + ref.width

    def _calc_y_(self, inst):
        return self._ref.y

class below(PositionSpecifier):

    def _calc_x_(self, inst):
        return self._ref.x

    def _calc_y_(self, inst):
        ref = self._ref
        return ref.y + ref.height

class above(PositionSpecifier):

    def _calc_x_(self, inst):
        return self._ref.x

    def _calc_y_(self, inst):
        ref = self._ref
        return ref.y - inst.height

class _Center(PositionSpecifier):

    def __init__(self):
        pass

    def _calc_x_(self, inst):
        return inst._superior_.width//2 - inst.width//2

    def _calc_y_(self, inst):
        return inst._superior_.height//2 - inst.height//2

class ConstantPosition(PositionSpecifier):

    def __init__(self, x, y, *, name=None):
        self._name = name
        self._x = x
        self._y = y

    def __repr__(self):
        if self._name is None:
            x = str(self._x) if self._x is not None else '_'
            y = str(self._y) if self._y is not None else '_'
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

center = _Center()

top     = ConstantPosition(None, 0, name='top')
bottom  = ConstantPosition(None, -1, name='bottom')

left    = ConstantPosition(0, None, name='left')
right   = ConstantPosition(-1, None, name='right')

top_left     = (left, top)
top_right    = (right, top)
bottom_left  = (left, bottom)
bottom_right = (right, bottom)
