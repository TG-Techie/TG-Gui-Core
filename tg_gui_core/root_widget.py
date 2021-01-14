import gc
from .base import *

class RootWrapper(Container):

    def __init__(self, *,
        screen:Screen,
        size,
        startup=False,
        **kwargs
    ):
        assert len(size) == 2, f"expected two dimensions found, {size}"

        Widget.__init__(self)

        self._superior_ = None
        self._screen_ = screen

        self._nested_ = []

        self._screen_ = screen
        self._inst_kwargs = kwargs
        self._size = size
        self._startup = startup

    def __call__(self, cls):
        # self._std_startup_(cls)
        self._root_wid_inst = root_wid_inst = cls()
        self._nest_(root_wid_inst)
        return root_wid_inst

    @property
    def _phys_coord_(self):
        return (0, 0)

    @property
    def wrapped(self):
        return self._root_wid_inst

    def _place_(self, coord:int, dims:int):
        assert dims > (0, 0), f"root's dims must be > (0, 0), found {dims}"

        was_on_screen = self.isrendered()
        if was_on_screen: #if was_on_screen := self.isrendered()
            self._derender_()

        self._placement_ = self._rel_placement_ = (0, 0) + dims
        self._abs_coord = (0, 0)

        #self._root_wid_inst._place_(*self.fill)

        self._place_nested_()

        if was_on_screen:
            self._render_()

    def _pickup_(self):
        self._pickup_nested_()
        Widget._pickup_(self)

    def _render_(self):
        self._rendered_ = True
        self._render_nested_()

    def _derender_(self):
        self._rendered_ = False
        self._derender_nested_()

    def _place_nested_(self):
        self._root_wid_inst(*self.fill)

    def _pickup_nested_(self):
        self._root_wid_inst._pickup_()

    def _render_nested_(self):
        self._root_wid_inst._render_()

    def _derender_nested_(self):
        self._root_wid_inst._derender_()

    def isnested(self):
        raise TypeError(f"roots cannot be nested (decorated with @RootWidget(...))")

    def _std_startup_(self):
        #self._root_wid_inst = root_wid = cls()
        self._nest_(self._root_wid_inst)
        self._place_((0, 0), self._size)
        self._render_()

    # possible future api
    def change_layoutcls(self, layoutcls):
        raise NotImplementedError()
