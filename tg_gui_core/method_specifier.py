

_singleton = lambda cls: cls()

@_singleton
class self():

    def __repr__(self):
        return "<MethodSpecifier constructor 'self'>"

    def __getattr__(self, name):
        global MethodSpecifier
        return MethodSpecifier(name)

class MethodSpecifier():

    def __init__(self, name):
        self._name = name
        self._method = None

    def getmethod(self, widget):
        method = self._method
        if self._method is not None:
            return method
        else:
            self._method = method = getattr(widget._superior_, self._name)
            return method
