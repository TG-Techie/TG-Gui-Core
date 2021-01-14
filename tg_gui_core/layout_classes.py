
def isvariant(obj, cls):
    if obj._is_single_varnt:
        return obj is cls
    else:
        print(f"(obj, cls)={(obj, cls)}")
        return isinstance(obj, cls)

def _enum_single_varnt(outercls):
    def _enum_nester(subcls):
        assert issubclass(subcls, outercls)
        subcls._is_single_varnt = True
        inst = subcls()
        setattr(outercls, subcls.__name__, inst)
        return inst
    return _enum_nester

def _enum_data_varnt(outercls):
    def _enum_nester(subcls):
        assert issubclass(subcls, outercls)
        subcls._is_single_varnt = False
        setattr(outercls, subcls.__name__, subcls)
        return subcls
    return _enum_nester

# puedo enums
class SizeClass:
    pass

@_enum_single_varnt(SizeClass)
class regular(SizeClass):
    pass

@_enum_single_varnt(SizeClass)
class compact(SizeClass):
    pass

class LayoutCls:
    pass

@_enum_single_varnt(LayoutCls)
class wearable(LayoutCls):
    pass

@_enum_data_varnt(LayoutCls)
class mobile(LayoutCls):
    # width: SizeClass
    # height: SizeClass

    def __init__(self, width, height):
        global SizeClass
        assert isinstance(width, SizeClass)
        assert isinstance(height, SizeClass)
        self.width = width
        self.height = height

# others
