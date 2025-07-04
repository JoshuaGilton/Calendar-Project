from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from calendar import monthrange
import json
from pathlib import Path

# Load layout configuration
CONFIG_PATH = (
    Path(__file__).resolve().parents[1] / "templates" / "layout_config.json"
)
try:
    with open(CONFIG_PATH) as f:
        LAYOUT_CONFIG = json.load(f)
except FileNotFoundError:
    LAYOUT_CONFIG = {}


def build_calendar_pdf(notes, zip_code, month, year, filename=None):
    """
    Draws a 7x5 grid calendar PDF for the given notes dict.
    notes: dict of YYYY-MM-DD -> {Line_1, Line_2}
    """
    if filename is None:
        filename = f"calendar_{zip_code}_{year}_{month:02d}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    cfg = LAYOUT_CONFIG
    margin = cfg.get("page_margin", 40)
    header_height = cfg.get("header_height", 40)
    rows = cfg.get("rows", 5)
    cols = cfg.get("cols", 7)

    fonts_cfg = cfg.get("fonts", {})
    day_font = fonts_cfg.get(
        "day_name",
        {"name": "Helvetica-Bold", "size": 12},
    )
    date_font = fonts_cfg.get("date", {"name": "Helvetica-Bold", "size": 14})
    note_font = fonts_cfg.get("note", {"name": "Helvetica", "size": 10})
    icon_font = fonts_cfg.get(
        "icon",
        {"name": "Helvetica-Oblique", "size": 8},
    )

    grid_top = height - margin - header_height
    grid_left = margin
    grid_width = width - 2 * margin
    grid_height = height - 2 * margin - header_height

    cell_cfg = cfg.get("cell_size", {})
    cell_width = cell_cfg.get("width", grid_width / cols)
    cell_height = cell_cfg.get("height", grid_height / rows)
    if "width" in cell_cfg:
        grid_width = cell_width * cols
    if "height" in cell_cfg:
        grid_height = cell_height * rows

    # Draw day names
    for i, day in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
        c.setFont(day_font["name"], day_font["size"])
        c.drawCentredString(
            grid_left + cell_width * (i + 0.5),
            grid_top + 20,
            day,
        )

    # Get first weekday and number of days
    first_weekday, num_days = monthrange(year, month)
    day_counter = 1
    for row in range(rows):
        for col in range(cols):
            x = grid_left + col * cell_width
            y = grid_top - row * cell_height
            c.setStrokeColor(colors.black)
            c.rect(
                x,
                y - cell_height,
                cell_width,
                cell_height,
                stroke=1,
                fill=0,
            )
            # Only fill in valid days
            if (row == 0 and col < first_weekday) or day_counter > num_days:
                continue
            # Date string
            date_str = f"{year:04d}-{month:02d}-{day_counter:02d}"
            note = notes.get(date_str, {})
            # Bold date in top-left
            c.setFont(date_font["name"], date_font["size"])
            c.drawString(x + 5, y - 18, str(day_counter))
            # Notes below date
            c.setFont(note_font["name"], note_font["size"])
            if note.get("Line_1"):
                c.drawString(x + 5, y - 32, note["Line_1"])
            if note.get("Line_2"):
                c.drawString(x + 5, y - 44, note["Line_2"])
            # Reserve bottom right for icons (placeholder)
            c.setFont(icon_font["name"], icon_font["size"])
            c.setFillColor(colors.grey)
            c.drawRightString(
                x + cell_width - 5,
                y - cell_height + 14,
                "[icon]",
            )
            c.setFillColor(colors.black)
            day_counter += 1
    c.save()
    print(f"Saved calendar to {filename}")
