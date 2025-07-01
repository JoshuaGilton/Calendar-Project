import json
import os
from pathlib import Path
from calendar import monthrange
from typing import Dict

import requests

# Example static data for demonstration
STATIC_NOTES = {
    "12345": {
        "2025-07-01": {"Line_1": "Bird migration peak", "Line_2": "Fishing: Trout season"},
        "2025-07-02": {"Line_1": "Wildflowers bloom", "Line_2": "Hunting: Deer archery"},
        # ... more days ...
    },
    # ... more zip codes ...
}

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
ZIP_SOURCES_PATH = DATA_DIR / "zip_sources.json"


def _load_zip_sources() -> Dict[str, str]:
    if ZIP_SOURCES_PATH.exists():
        try:
            with open(ZIP_SOURCES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _load_external_notes(source: str) -> Dict[str, Dict[str, str]]:
    """Load notes from a local JSON file or remote URL."""
    if source.startswith("http://") or source.startswith("https://"):
        try:
            resp = requests.get(source, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return {}
    else:
        path = Path(source)
        if not path.is_absolute():
            path = DATA_DIR / path
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
    return {}


def get_notes_for_zip(zip_code: str, month: int, year: int) -> Dict[str, Dict[str, str]]:
    """Returns a dict mapping YYYY-MM-DD to notes for each day."""

    notes: Dict[str, Dict[str, str]] = {}
    days_in_month = monthrange(year, month)[1]

    # Determine data source
    zip_sources = _load_zip_sources()
    zip_data = {}
    source = zip_sources.get(str(zip_code))
    if source:
        zip_data = _load_external_notes(source)
    if not zip_data:
        zip_data = STATIC_NOTES.get(str(zip_code), {})

    for day in range(1, days_in_month + 1):
        date_str = f"{year:04d}-{month:02d}-{day:02d}"
        day_note = zip_data.get(date_str, {})
        # Pin hunting/fishing to Line_2 if present
        line_1 = day_note.get("Line_1", "")
        line_2 = day_note.get("Line_2", "")
        if ("hunting" in line_1.lower() or "fishing" in line_1.lower()) and not line_2:
            line_2, line_1 = line_1, ""
        elif ("hunting" in line_2.lower() or "fishing" in line_2.lower()) and line_1:
            pass  # already in Line_2
        notes[date_str] = {"Line_1": line_1, "Line_2": line_2}
    return notes
