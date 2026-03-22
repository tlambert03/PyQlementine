"""Qlementine utility functions."""


def _init():
    from . import PySide6Qlementine as _ql

    bridge = _ql.UtilsBridge
    ns = globals()
    _excluded = frozenset({"appStyle"})
    for name in dir(bridge):
        if name.startswith("_") or name in _excluded:
            continue
        ns[name] = getattr(bridge, name)


_init()
del _init
