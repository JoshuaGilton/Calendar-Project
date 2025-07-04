from datetime import date
from src.data_loader import get_notes_for_zip
from src.pdf_renderer import build_calendar_pdf


def generate_calendar(zip_code, month=None, year=None):
    today = date.today()
    month = month or today.month
    year = year or today.year

    notes = get_notes_for_zip(zip_code, month, year)
    build_calendar_pdf(notes, zip_code, month, year)
