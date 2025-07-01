# Example static data for demonstration
STATIC_NOTES = {
    "12345": {
        "2025-07-01": {"Line_1": "Bird migration peak", "Line_2": "Fishing: Trout season"},
        "2025-07-02": {"Line_1": "Wildflowers bloom", "Line_2": "Hunting: Deer archery"},
        # ... more days ...
    },
    # ... more zip codes ...
}

def get_notes_for_zip(zip_code, month, year):
    """
    Returns a dict mapping YYYY-MM-DD to a dict of notes for each day.
    Ensures hunting/fishing notes are always in Line_2.
    """
    from calendar import monthrange
    notes = {}
    days_in_month = monthrange(year, month)[1]
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
