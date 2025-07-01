from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from calendar import month_name, monthrange


def build_calendar_pdf(notes, zip_code, month, year, filename=None):
    """
    Draws a 7x5 grid calendar PDF for the given notes dict.
    notes: dict of YYYY-MM-DD -> {Line_1, Line_2}
    """
    if filename is None:
        filename = f"calendar_{zip_code}_{year}_{month:02d}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    margin = 40
    grid_top = height - margin - 40
    grid_left = margin
    grid_width = width - 2 * margin
    grid_height = height - 2 * margin - 40
    cell_width = grid_width / 7
    cell_height = grid_height / 5

    # Title at the top center
    month_str = month_name[month]
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - margin / 2, f"{month_str} {year}")

    # Draw day names
    for i, day in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(grid_left + cell_width * (i + 0.5), grid_top + 20, day)

    # Get first weekday and number of days
    first_weekday, num_days = monthrange(year, month)
    day_counter = 1
    for row in range(5):
        for col in range(7):
            x = grid_left + col * cell_width
            y = grid_top - row * cell_height
            c.setStrokeColor(colors.black)
            c.rect(x, y - cell_height, cell_width, cell_height, stroke=1, fill=0)
            # Only fill in valid days
            if (row == 0 and col < first_weekday) or day_counter > num_days:
                continue
            # Date string
            date_str = f"{year:04d}-{month:02d}-{day_counter:02d}"
            note = notes.get(date_str, {})
            # Bold date in top-left
            c.setFont("Helvetica-Bold", 14)
            c.drawString(x + 5, y - 18, str(day_counter))
            # Notes below date
            c.setFont("Helvetica", 10)
            if note.get("Line_1"):
                c.drawString(x + 5, y - 32, note["Line_1"])
            if note.get("Line_2"):
                c.drawString(x + 5, y - 44, note["Line_2"])
            # Reserve bottom right for icons (placeholder)
            c.setFont("Helvetica-Oblique", 8)
            c.setFillColor(colors.grey)
            c.drawRightString(x + cell_width - 5, y - cell_height + 14, "[icon]")
            c.setFillColor(colors.black)
            day_counter += 1
    c.save()
    print(f"Saved calendar to {filename}")
