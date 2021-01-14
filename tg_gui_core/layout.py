from .base import Container, Widget
from .layout_classes import *

class Layout(Container):

    def _render_(self):
        Widget._render_(self)
        for wid in self._nested_:
            if wid.isplaced():
                wid._render_()

    def _derender_(self):
        for wid in self._nested_:
            if wid.isplaced():
                wid._derender_()
        Widget._derender_(self)

    def _place_(self, coord, dims):
        Widget._place_(self, coord, dims)

        layoutcls = self._screen_.layout_class

        if layoutcls is LayoutCls.wearable:
            self._wearable_()
        elif isinstance(layoutcls, LayoutCls.mobile):
            self._mobile_(layoutcls.width, layoutcls.height)
        else:
            raise ValueError(f"unknown LayoutCls variant or object, {type(layoutcls)}")

        self._screen_.on_container_place(self)

    def _pickup_(self):
        self._screen_.on_container_pickup(self)
        for wid in self._nested_:
            wid._pickup_()
        Widget._pickup_(self)

    def _relayout_proto_(self):
        self._layout_()
        self._unlayout_()

    def _any_(self):
        raise NotImplementedError(f"layout methods must be written for subclasses of layout")

    def _wearable_(self):
        self._any_()

    def _mobile_(self, width:SizeClass, height:SizeClass):
        self._any_()
