from .base import *

# TODO: add derived states

class State():

    def __init__(self, value, repr=repr):
        self._id_ = uid()
        self._value = value
        self._registered = []
        self._repr = repr

    # #@micropython.native
    def __get__(self, owner, ownertype):
        return self._value

    # #@micropython.native
    def __set__(self, owner, value):
        self.update(value)

    # #@micropython.native
    def update(self, value):
        previous = self._value
        if value != previous:
            self._value = value
            self._alert_registered()

    def __repr__(self):
        return f"<{type(self).__name__}:{self._id_} ({self._repr(self._value)})>"

    # #@micropython.native
    def getvalue(self, widget, handler):
        self._register_handler(widget, handler)
        return self._value

    # #@micropython.native
    def _alert_registered(self):
        registered = self._registered
        self._registered = []
        while len(registered):
            widget, handler = registered.pop(0)
            handler()

    # #@micropython.native
    def _register_handler(self, widget, handler):
        self._registered.append((widget, handler))

    def derived(self, fn):
        return DerivedState(self, fn)

class DerivedState(State):

    def __init__(self, state, fn):

        self._state = state
        self._fn = fn
        # register and get the new value
        start_value = fn(state.getvalue(self, self._on_src_update))

        super().__init__(
            value=start_value,
        )

    def __repr__(self):
        return f"<DerivedState:{self._id_} ({self._state})>"

    # #@micropython.native
    def _on_src_update(self):
        value_src = self._state.getvalue(self, self._on_src_update)
        self._value = self._fn(value_src)

        self._alert_registered()

    def update(self, value):
        raise TypeError(f"you cannot set the state of {self}, tried to set to {value}")


class StatefulAttribute():

    def __init__(self, initfn, *, private_name=None, _updatefn=None):
        global uid

        self._id_ = id = uid()

        if private_name is None:
            private_name = f"_stateful_attr_{id}_"

        self._initfn = initfn
        self._privname = private_name
        self._updatefn = _updatefn

    def __call__(self, fn):
        if self._updatefn is None:
            self._updatefn = fn
            self._privname = f"_stateful_attr_{fn.__name__}"
        else:
            raise ValueError(f"{self} alreayd has an update function {self._updatefn}, got {fn}")
        return self

    def __get__(self, owner, ownertype):
        return self._get_val(owner)

    def _get_val(self, owner):
        privname = self._privname
        if not hasattr(owner, privname):
            value = self._initfn(owner)
            setattr(owner, privname, value)
        else:
            value = getattr(owner, privname)
        return value

    def __set__(self, owner, value):
        # print('__set__', self, owner, value)
        if value != self._get_val(owner):
            setattr(owner, self._privname, value)
            if self._updatefn is not None:
                self._updatefn(owner)

def src_to_value(*, src, widget, handler, default):
    if src is None:
        val = default
    elif isinstance(src, State):
        val = src.getvalue(widget, handler)
    else:
        val = src
    return val
