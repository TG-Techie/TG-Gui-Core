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

from . import dimension_specifiers
from . import position_specifiers

_singleton = lambda cls: cls()


class SpecifierConstructor:
    def __init__(self, *, name, for_superior):
        self._for_superior = for_superior
        self._name = name

    def __repr__(self):
        return f"<Specifier constructor {repr(self._name)}>"

    @property
    def width(self):
        global dimension_specifiers
        return dimension_specifiers.WidthForwardSpecifier(
            _for_superior=self._for_superior
        )

    @property
    def height(self):
        global dimension_specifiers
        return dimension_specifiers.HeightForwardSpecifier(
            _for_superior=self._for_superior
        )

    def __getattr__(self, name):
        global AttributeSpecifier
        return AttributeSpecifier(name, _for_superior=self._for_superior)


self = SpecifierConstructor(name="self", for_superior=False)
# superior = SpecifierConstructor(name="superior", for_superior=True)


class AttributeSpecifier:
    def __init__(self, name, _for_superior=False):
        self._for_superior = _for_superior
        self._name = name
        self._attr = None

    def get_attribute(self, widget):
        attr = self._attr
        if self._attr is not None:
            return attr
        else:
            if self._for_superior:  # for the continer's superior
                widgetfrom = widget._superior_._superior_
            else:  # for the container
                widgetfrom = widget._superior_
            self._attr = attr = getattr(widgetfrom, self._name)
            return attr
