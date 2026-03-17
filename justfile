host := if os() == "macos" { "mac" } else if os() == "windows" { "windows" } else { "linux" }
export UV_NO_EDITABLE := "1"

@_default:
    @just --list

# install (re)-build pyqt6-qlementine
install-pyqt6: _clone install-qt
    uv sync --group pyqt6 --reinstall-package pyqt6-qlementine

# install (re)-build pyside6-qlementine
install-pyside6: _clone (install-qt "6.10.2")
    uv sync --group pyside6 --reinstall-package pyside6-qlementine

# Clean build artifacts
clean:
    rm -rf build dist wheelhouse Qt

# run demo widget
demo:
    uv run examples/demo.py

# build wheel (into ./wheelhouse)
build-wheel target="PyQt6":
    #!/usr/bin/env sh
    if echo "{{target}}" | grep -qi pyside; then
        export QT_VERSION=6.10.2
    else
        export QT_VERSION=6.8.1
    fi
    @just install-qt qt_version=$QT_VERSION
    uvx cibuildwheel --config-file pyproject.toml packages/{{target}}-Qlementine

install-qt qt_version="6.8.1":
    #!/usr/bin/env sh
    if [ -d "Qt/{{ qt_version }}" ]; then
        echo "Qt {{ qt_version }} already installed"
    else
        uvx --from aqtinstall aqt install-qt {{ host }} desktop {{ qt_version }} --outputdir Qt
    fi

_clone:
    git submodule update --init --recursive
