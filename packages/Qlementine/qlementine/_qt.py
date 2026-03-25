"""Qt backend abstraction shim.

Imports from PyQt6 first, falls back to PySide6. All other modules in this
package should import Qt symbols from here rather than directly from a backend.
"""

from __future__ import annotations

try:
    from PyQt6 import QtCore, QtGui, QtWidgets  # type: ignore[import-not-found]
    from PyQt6.QtCore import pyqtSignal as Signal  # type: ignore[import-not-found]

    BACKEND = "PyQt6"
except ImportError:
    from PySide6 import QtCore, QtGui, QtWidgets  # type: ignore[import-not-found]
    from PySide6.QtCore import Signal  # type: ignore[import-not-found]

    BACKEND = "PySide6"

__all__ = ["BACKEND", "QtCore", "QtGui", "QtWidgets", "Signal"]
