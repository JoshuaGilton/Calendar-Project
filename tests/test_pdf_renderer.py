import os
import tempfile

from src.pdf_renderer import build_calendar_pdf


def test_build_calendar_pdf_creates_file(tmp_path):
    notes = {"2024-01-01": {"Line_1": "Note", "Line_2": ""}}
    pdf_path = tmp_path / "out.pdf"
    build_calendar_pdf(notes, zip_code="00000", month=1, year=2024, filename=str(pdf_path))
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 0
