import sys

sys_impl_name_ = sys.implementation.name
on_circuitpython_ = sys_impl_name_ in ("circuitpython", "micropython")

# TODO: make widgets return DimSpecs and PosSpecs when dims and coords are not set yet

import random as _random

from .layout_classes import *
from .position_specifiers import *
from .dimension_specifiers import *


class NestingError(RuntimeError):
    pass


class PlacementError(RuntimeError):
    pass


class RenderError(RuntimeError):
    pass


_next_id = _random.randint(0, 11)


class Constant:
    def __init__(self, outer, name):
        self._name = name
        self._outer = outer

    def __repr__(self):
        return f"<Constant {self._outer._name}.{self._name}>"


class ConstantGroup:
    def __init__(self, name, subs):
        self._name = name
        self._subs = subs_dict = {
            sub_name: Constant(self, sub_name) for sub_name in subs
        }
        for name, sub in subs_dict.items():
            setattr(self, name, sub)

    def __repr__(self):
        return f"<ConstantGroup {self._name}>"


def uid():
    global _next_id
    id = _next_id
    _next_id += 1
    return id


def clip(lower, value, upper):
    return min(max(lower, value), upper)


align = ConstantGroup("align", ("leading", "center", "trailing"))


class color:
    # TODO: consider make ready only using proerties and lambdas vs performance
    _clear = None  # tentative
    red = 0xFF0000
    orange = 0xFFA500
    yellow = 0xFFFF00
    green = 0x00FF00
    blue = 0x0000FF
    purple = 0xCC8899

    white = 0xFFFFFF
    lightgray = 0xC4C4C4
    gray = 0x909090
    darkgray = 0x606060
    black = 0x000000


class Palette:
    def __init__(
        self,
        *,
        fill_color,
        text_color,
        selected_text,
        selected_fill,
        backfill,
    ):
        self.fill_color = fill_color
        self.selected_fill = selected_fill
        self.text_color = text_color
        self.selected_text = selected_text
        self.backfill = backfill


class Palettes:
    def __init__(self, *, primary, secondary):
        self.primary = primary
        self.secondary = secondary


class Defaults:
    def __init__(
        self,
        *,
        margin,
        radius,
        font_size,
        _fill_color_,
        _selected_fill_,
        _text_color_,
        _selected_text_,
    ):
        self.margin = margin
        self.radius = radius
        self.font_size = font_size

        self._fill_color_ = _fill_color_
        self._selected_fill_ = _selected_fill_
        self._text_color_ = _text_color_
        self._selected_text_ = _selected_text_


class Screen:
    def __init__(
        self,
        *,
        min_size,
        palettes: Palettes,
        default: Defaults,
        layout_class: LayoutCls,
        outer: "Screen" = None,
    ):
        self._id_ = uid()
        self.default = default
        self.layout_class = layout_class
        self.outer = outer

        self.min_size = min_size
        self.palettes = palettes

        self._pointables_ = []
        self._pressables_ = []
        self._altpressables_ = []

    def __repr__(self):
        return f"<{type(self).__name__} {self._id_}>"

    def __getattr__(self, name):
        # if name in self._kwargs:
        # return self._kwargs[name]
        if self.outer is not None:
            try:
                return getattr(self.outer, name)
            except:
                pass
        raise AttributeError(f"unable to get attribute `.{name}`")

    def on_widget_nest_in(self, wid: "Widget"):
        pass

    def on_widget_unnest_from(self, wid: "Widget"):
        pass

    def on_widget_render(self, wid: "Widget"):
        pass

    def on_widget_derender(self, wid: "Widget"):
        pass

    def on_container_place(self, wid: "Widget"):
        pass

    def on_container_pickup(self, wid: "Widget"):
        pass

    def on_container_render(_, widget: "Widget"):
        pass

    def on_container_derender(_, widget: "Widget"):
        pass


class Widget:

    _next_id = 0

    def __init__(
        self, *, superior=None, margin=None
    ):  # TODO: should use nest or superior kwarg?
        global Widget
        self._id_ = uid()

        self._superior_ = None  # type: Optional[superior]
        self._screen_ = None

        self._placement_ = None  # type: Optional[Tuple[x, y, width, height]]
        self._rel_placement_ = None
        self._phys_coord = None

        self._margin_ = margin

        self._rendered_ = False

        if superior is not None:
            superior._nest_(self)

    def __repr__(self):
        return f"<{type(self).__name__} {self._id_}>"

    def isnested(self):
        return self._superior_ is not None

    def isnestedin(self, maybe_superior):
        return self._superior_ is maybe_superior and self in maybe_superior._nested_

    def isplaced(self):
        return self._placement_ is not None  # and self.isnested()

    def isrendered(self):
        return self._rendered_

    def _nest_in_(self, superior):
        # nesting is permanent, this shoudl bbe called by the parent
        current = self._superior_
        if current is None:
            self._superior_ = superior
            self._screen_ = superior._screen_
            self._screen_.on_widget_nest_in(self)
        elif current is superior:  # if double nesting in same thing
            print(
                f"WARNING: {self} already nested in {current}, "
                + "double nesting in the same widget is not advisable"
            )
        else:
            raise ValueError(
                f"{self} already nested in {current}, " + f"cannot nest in {superior}"
            )

        self._on_nest_()

    def _unnest_from_(self, superior):
        if self._superior_ is superior:
            self._screen_.on_widget_unnest_from(self)
            self._screen_ = None
            self._superior_ = None
        else:
            raise RuntimeError(
                f"cannot unnest {self} from {superior}, nested in {self._superior_}"
            )

    def _on_nest_(self):
        pass

    def _on_unnest_(self):
        pass

    # auto nesting, only for layouts, etc
    # list, zstacks, and others will need to manually nest in their __init__s
    def __get__(self, owner, ownertype=None):
        #  def __get__(self, owner=None, ownertype=None):
        # print(f"self={self}, owner={owner}, ownertype={ownertype}")
        # this adds a side effect to getters
        # if __debug__: print('__get__', self, owner, f"self.isnested()={self.isnested()}")
        if not self.isnested():
            owner._nest_(self)
        return self

    # placement sugar, still in flux
    def __call__(self, coord, dims):
        self._place_(coord, dims)
        return self

    def _place_(self, coord, dims):
        # is there a diference between place and render? (yes, button state)
        assert self.isnested(), f"{self} must be nested to place it"
        # print(self)
        # assert not self.isplaced(), f"cannot doulbe place {self}, it must be pickup-ed first"

        was_on_screen = self.isrendered()
        if was_on_screen:  # if was_on_screen := self.isrendered()
            self._derender_()

        # get margin
        mar = self._margin_
        if mar is None:
            self._margin_ = mar = self._screen_.default.margin

        # format dims
        width, height = dims
        if isinstance(width, DimensionSpecifier):
            width = width._calc_dim_(self)
        if isinstance(height, DimensionSpecifier):
            height = height._calc_dim_(self)

        # make sure PositionSpecifiers have access to width/height
        self._placement_ = (None, None, width, height)

        # format coord
        if isinstance(coord, PositionSpecifier):
            x, y = coord._calc_coord_(self)
        else:
            x, y = coord

        if isinstance(x, PositionSpecifier):
            # print('x is posspec')
            x = x._calc_x_(self)
        if isinstance(y, PositionSpecifier):
            # print('y is posspec')
            y = y._calc_y_(self)

        if self._superior_ is None and (x < 0 or y < 0):
            raise ValueError(f"right aligned coord cannot be used with root widgets")

        # adjust
        if x < 0:
            x = self._superior_.width - width + 1 + x
        if y < 0:
            y = self._superior_.height - height + 1 + y

        # save
        self._placement_ = placement = x, y, w, h = (x, y, width, height)

        # calc relative placement
        self._rel_placement_ = rel_placement = (
            mar + x,
            mar + y,
            w - (2 * mar),
            h - (2 * mar),
        )
        rx, ry, rw, rh = rel_placement

        # calc absolute physical placement
        supx, supy = self._superior_._phys_coord_
        self._phys_coord_ = (supx + rx, supy + ry)
        self._phys_end_coord = (supx + rx + rw, supy + ry + rh)

        if was_on_screen:
            self._render_()

    def _pickup_(self):
        # only containers need to worry about when to cover vs replace
        self._placement_ = None
        self._rel_placement_ = None
        self._phys_coord_ = None
        if self.isrendered():
            # if it is on the screen biut is being pickup up it shoudl derender
            #   visually, generally everything should be derendered before it
            #   is pickedup
            self._derender_(True)

    def _render_(self):
        self._rendered_ = True
        screen = self._screen_
        screen.on_widget_render(self)
        if hasattr(self, "_selected_"):
            screen._pointables_.append(self)

    def _derender_(self):
        self._screen_.on_widget_derender(self)
        self._rendered_ = False

    def _rerender_(self):
        self._derender_()
        self._rerender_()

    def __del__(self):
        # remove double links
        self._superior_ = None
        self._screen_ = None
        # remove placement cache
        self._placement_ = None
        self._rel_placement_ = None
        self._phys_coord = None

    # coordinates and dimension getters
    coord = property(lambda self: self._placement_[0:2])
    _rel_coord_ = property(lambda self: self._rel_placement_[0:2])
    # uses raw exposed tuple # _phys_coord_ = property(lambda self: self._phys_coord)

    dims = property(lambda self: self._placement_[2:4])
    _phys_dims_ = property(lambda self: self._rel_placement_[2:4])

    x = property(lambda self: self._placement_[0])
    _rel_x_ = property(lambda self: self._rel_placement_[0])
    _phys_x_ = property(lambda self: self._phys_coord_[0])

    y = property(lambda self: self._placement_[1])
    _rel_y_ = property(lambda self: self._rel_placement_[1])
    _phys_y_ = property(lambda self: self._phys_coord_[1])

    width = property(lambda self: self._placement_[2])
    _phys_width_ = property(lambda self: self._rel_placement_[2])

    height = property(lambda self: self._placement_[3])
    _phys_height_ = property(lambda self: self._rel_placement_[3])


class Container(Widget):
    def __init__(self, superior=None):
        global Widget

        super().__init__(superior=superior, margin=0)

        self._nested_ = []

        self._setup_()

    @property
    def fill(self):
        return ((0, 0), self.dims)

    def _setup_(self):
        pass  # used for setting up of reuables contianers "compound widgets"

    def _nest_(self, widget: Widget):
        if widget not in self._nested_:
            self._nested_.append(widget)
            widget._nest_in_(self)

    def _unnest_(self, widget: Widget):
        # raise NotImplementedError("dev side not implemented")
        while widget in self._nested_:
            widget._unnest_from_(self)
            self._nested_.remove(widget)

    def _place_(self, coord, dims):
        super()._place_(coord, dims)
        self._place_nested_()
        self._screen_.on_container_place(self)

    def _pickup_(self, visual):
        self._screen_.on_container_pickup(self)
        self._pickup_nested_()
        super()._pickup_(visual)

    def _render_(self):
        super()._render_()
        self._render_nested_()

    def _derender_(self):
        super()._derender_()
        self._derender_nested_()

    def _render_nested_(self):
        raise NotImplementedError(
            f"{type(self).__name__}._render_nested_ not implemented"
        )

    def _derender_nested_(self):
        raise NotImplementedError(
            f"{type(self).__name__}._derender_nested_ not implemented"
        )

    def _place_nested_(self):
        raise NotImplementedError(
            f"{type(self).__name__}._place_nested_ not implemented"
        )

    def _pickup_nested_(self):
        raise NotImplementedError(
            f"{type(self).__name__}._pickup_nested_ not implemented"
        )

    def __del__(self):
        super().__del__()
        nested = self._nested_
        while len(nested):
            del nested[0]
