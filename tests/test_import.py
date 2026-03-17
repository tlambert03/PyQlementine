from __future__ import annotations

import warnings

import pytest

try:
    import PyQt6Qlementine as Qlementine

    print("Using PyQt6Qlementine for tests.")
except ImportError:
    try:
        import PySide6Qlementine as Qlementine

        print("Using PySide6Qlementine for tests.")
    except ImportError:
        raise ImportError(
            "Neither PyQt6Qlementine nor PySide6Qlementine could be imported. "
            "Please install one of them to run the tests."
        )


_qapp_instance = None


@pytest.fixture(scope="session")
def qapp(pytestconfig):
    """Fixture that creates the QApplication instance that will be used by tests."""
    try:
        from PyQt6.QtWidgets import QApplication as qapp_cls
    except ImportError:
        from PySide6.QtWidgets import QApplication as qapp_cls

    if (app := qapp_cls.instance()) is None:
        global _qapp_instance
        _qapp_instance = qapp_cls([])
        name = pytestconfig.getini("qt_qapp_name")
        _qapp_instance.setApplicationName(name)
        return _qapp_instance
    else:
        if not isinstance(app, qapp_cls):
            warnings.warn(
                f"Existing QApplication {app} is not an instance of qapp_cls: "
                f"{qapp_cls}"
            )
        return app


def test_import():
    assert Qlementine.QlementineStyle is not None


def test_create_style(qapp: QApplication):
    style = Qlementine.QlementineStyle()
    assert style is not None
    assert style.animationsEnabled() is True


def test_enums():
    assert Qlementine.ColorRole.Primary is not None
    assert Qlementine.MouseState.Hovered is not None
    assert Qlementine.Status.Error is not None
    assert Qlementine.TextRole.H1 is not None


def test_widgets(qapp: QApplication):
    switch = Qlementine.Switch()
    assert switch is not None
    label = Qlementine.Label("Hello")
    assert label is not None
    line_edit = Qlementine.LineEdit()
    assert line_edit is not None
    spinner = Qlementine.LoadingSpinner()
    assert spinner is not None
