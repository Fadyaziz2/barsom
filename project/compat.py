"""Compatibility helpers for third-party packages."""
from __future__ import annotations

import sys
from types import ModuleType


def _patch_entry_points(module: ModuleType) -> None:
    entry_points = getattr(module, "entry_points", None)
    if not callable(entry_points):
        return

    try:
        entry_points(group="__compat_test__")
    except TypeError:
        original = entry_points

        def _patched_entry_points(*args, **kwargs):
            kwargs_copy = dict(kwargs)
            group = kwargs_copy.pop("group", None)
            name = kwargs_copy.pop("name", None)
            result = original(*args, **kwargs_copy)
            if group is None and name is None:
                return result

            selector = getattr(result, "select", None)
            if callable(selector):
                return selector(group=group, name=name)

            filtered = [
                entry
                for entry in result
                if (group is None or getattr(entry, "group", None) == group)
                and (name is None or getattr(entry, "name", None) == name)
            ]
            return type(result)(filtered) if isinstance(result, (list, tuple)) else filtered

        module.entry_points = _patched_entry_points


def patch_importlib_entry_points() -> None:
    for module_name in ("importlib.metadata", "importlib_metadata"):
        module = sys.modules.get(module_name)
        if module is None:
            try:
                module = __import__(module_name)
            except ImportError:
                continue
        _patch_entry_points(module)


patch_importlib_entry_points()
