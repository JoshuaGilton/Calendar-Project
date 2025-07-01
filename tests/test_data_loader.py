import builtins
import importlib

import pytest

import src.data_loader as dl


def test_get_notes_for_zip_rearranges_notes(monkeypatch):
    test_data = {
        "99999": {
            "2024-01-01": {"Line_1": "Go skiing", "Line_2": ""},
            "2024-01-02": {"Line_1": "Hunting: Bear", "Line_2": ""},
            "2024-01-03": {"Line_1": "Bird watching", "Line_2": "Fishing: Bass"},
        }
    }
    monkeypatch.setattr(dl, "STATIC_NOTES", test_data)
    notes = dl.get_notes_for_zip("99999", 1, 2024)
    assert len(notes) == 31
    assert notes["2024-01-01"] == {"Line_1": "Go skiing", "Line_2": ""}
    assert notes["2024-01-02"] == {"Line_1": "", "Line_2": "Hunting: Bear"}
    assert notes["2024-01-03"] == {"Line_1": "Bird watching", "Line_2": "Fishing: Bass"}
