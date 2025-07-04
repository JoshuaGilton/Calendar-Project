from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import pdf_renderer


def test_build_calendar_pdf_creates_file(tmp_path):
    notes = {
        "2025-07-01": {"Line_1": "A", "Line_2": "B"},
        "2025-07-02": {"Line_1": "", "Line_2": ""},
    }
    outfile = tmp_path / "calendar.pdf"
    pdf_renderer.build_calendar_pdf(notes, "12345", 7, 2025, filename=str(outfile))
    assert outfile.exists()
    assert outfile.stat().st_size > 0
