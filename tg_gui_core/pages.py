from .stateful import State
from .base import Container, Widget


class PageState(State):
    def __set__(self, owner, value):
        if isinstance(value, Widget):
            for page_key, page_value in owner._pages.items():
                if value is page_value:
                    value = page_key
        self.update(value)


class Pages(Container):
    def __init__(self, show=None, pages=None, _buffered=True, **kwargs):
        super().__init__(**kwargs)

        # assert isinstance(show, State)
        # self._page_key_src = page_key_src = show

        # scan for class attrs
        if pages is None and show is None:
            cls = type(self)
            pageattrs = []
            for attrname in dir(cls):
                attr = getattr(cls, attrname)
                if isinstance(attr, Widget):
                    pageattrs.append(attr)
                    # pages[attr] = attr
                elif isinstance(attr, type) and issubclass(attr, Widget):
                    raise NotImplementedError(
                        "Pages widgets don't support types as pages (yet?), "
                        + f"found {attr}"
                    )
                else:
                    pass
            else:
                pageattrs.sort(key=lambda item: item._id_)
                pages = {
                    index: widget for index, widget in enumerate(pageattrs)
                }
            if show is None:
                if hasattr(cls, "page"):
                    show = getattr(cls, "page")
                    assert isinstance(show, PageState), f"found {show}"
                else:
                    raise TypeError(
                        f"{cls} has no attribute page, a `Pages` subclass must "
                        + "have a `.page` attribute. `page = PageState(0)`"
                    )
                # find the widget with the lowest id (as they are chronological)
                # show = State(0)
            else:
                raise TypeError(
                    "when 'pages' is not specified show must not be either, "
                    + f"found {show}"
                )
        elif isinstance(pages, (tuple, list)):
            pages = dict(enumerate(pages))
        elif isinstance(pages, dict):
            pass
        else:
            raise TypeError(
                "argument pages must be a tuple, dict, or None, "
                + f"found {type(self)}"
            )

        if _buffered is None and hasattr(self, "_buffered_"):
            self._buffered = self._buffered_
        else:
            self._buffered = _buffered

        self._page_key_src = show
        self._pages = pages
        self._page_key = None

    def set_page(self, value):
        if isinstance(value, AttributeError):
            value = value.get_attribute(self)
        self._page_key_src.update(value)

    def _on_nest_(self):
        for page in self._pages.values():
            self._nest_(page)

    def _place_(self, coord, dims):
        Widget._place_(self, coord, dims)
        if self._buffered is True:
            for page in self._pages.values():
                page._place_((0, 0), self.dims)
        self._screen_.on_container_place(self)

    def _pickup_(self):
        self._screen_.on_container_pickup(self)
        for page in self._pages:
            page._pickup_()
        Widget._pickup_(self)

    def _render_(self):
        Widget._render_(self)
        self._page_key = page_key = self._page_key_src.getvalue(
            self, self._rerender_pages
        )
        page = self._pages[page_key]
        if self._buffered is False:
            if not page.isplaced():
                page._place_((0, 0), self.dims)
        page._render_()
        self._screen_.on_container_render(self)

    def _derender_(self):
        page = self._pages[self._page_key]
        page._derender_()
        # page._pickup_()
        Widget._derender_(self)
        self._screen_.on_container_derender(self)

    def _rerender_pages(self):
        self._screen_.on_container_derender(self)
        page = self._pages[self._page_key]
        page._derender_()
        # page._pickup_()
        self._page_key = page_key = self._page_key_src.getvalue(
            self, self._rerender_pages
        )
        page = self._pages[page_key]
        if self._buffered is False:
            if not page.isplaced():
                page._place_((0, 0), self.dims)
        page._render_()
        self._screen_.on_container_render(self)
