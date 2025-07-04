import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import data_loader


def test_load_external_notes_local(tmp_path):
    data = {"day": {"Line_1": "note"}}
    file = tmp_path / "notes.json"
    file.write_text(json.dumps(data))
    result = data_loader._load_external_notes(str(file))
    assert result == data


def test_load_external_notes_remote(monkeypatch):
    returned = {"x": {"Line_2": "remote"}}

    class DummyResp:
        def raise_for_status(self):
            pass

        def json(self):
            return returned

    def mock_get(url, timeout=10):
        assert url == "http://example.com/data.json"
        return DummyResp()

    monkeypatch.setattr(data_loader.requests, "get", mock_get)
    result = data_loader._load_external_notes("http://example.com/data.json")
    assert result == returned


def test_get_notes_for_zip_swaps_lines(monkeypatch):
    sample = {"2025-07-01": {"Line_1": "Fishing event"}}

    monkeypatch.setattr(data_loader, "_load_zip_sources", lambda: {"11111": "foo"})
    monkeypatch.setattr(data_loader, "_load_external_notes", lambda source: sample)

    notes = data_loader.get_notes_for_zip("11111", 7, 2025)
    swapped = notes["2025-07-01"]
    assert swapped["Line_1"] == ""
    assert swapped["Line_2"] == "Fishing event"
    assert len(notes) == 31
