# Utility functions to draw supplemental charts and icons on the calendar
from calendar import monthrange
from math import sin, pi
from reportlab.lib import colors
from reportlab.lib.units import inch


def _placeholder_sun_data(num_days):
    """Return simple sine-wave sunrise and sunset times for demo."""
    sunrise = [6 + 0.5 * sin(2 * pi * (d - 1) / num_days) for d in range(1, num_days + 1)]
    sunset = [18 - 0.5 * sin(2 * pi * (d - 1) / num_days) for d in range(1, num_days + 1)]
    return sunrise, sunset


def draw_calendar_chart(c, x, y, width, height, month, year, iss_days=None):
    """Draw a small chart of sunrise/sunset times and optional ISS passes."""
    num_days = monthrange(year, month)[1]
    sunrise, sunset = _placeholder_sun_data(num_days)
    iss_days = iss_days or [5, 15, 25]

    min_time, max_time = 4, 20  # hour range to display

    def day_to_x(day):
        return x + (day - 1) / (num_days - 1) * width

    def time_to_y(t):
        return y + (t - min_time) / (max_time - min_time) * height

    # Border
    c.setStrokeColor(colors.black)
    c.rect(x, y, width, height, stroke=1, fill=0)
    c.setFont("Helvetica", 7)
    c.drawString(x + 2, y + height + 2, "Sunrise/Sunset")

    # Sunrise line
    c.setStrokeColor(colors.orange)
    c.setLineWidth(1)
    for d in range(1, num_days):
        c.line(day_to_x(d), time_to_y(sunrise[d - 1]),
               day_to_x(d + 1), time_to_y(sunrise[d]))

    # Sunset line
    c.setStrokeColor(colors.red)
    for d in range(1, num_days):
        c.line(day_to_x(d), time_to_y(sunset[d - 1]),
               day_to_x(d + 1), time_to_y(sunset[d]))

    # ISS passes (simple markers)
    c.setFillColor(colors.blue)
    for d in iss_days:
        if 1 <= d <= num_days:
            c.circle(day_to_x(d), time_to_y(21), 1.5, fill=1, stroke=0)
    c.setFillColor(colors.black)


def parse_icons(note):
    """Return a list of icon names based on note text."""
    icons = []
    text = f"{note.get('Line_1','')} {note.get('Line_2','')}".lower()
    if "fish" in text:
        icons.append("fish")
    if "hunt" in text or "deer" in text:
        icons.append("deer")
    if "bird" in text:
        icons.append("bird")
    if "iss" in text:
        icons.append("iss")
    return icons


def draw_icon(c, icon_type, x, y, size=8):
    """Draw a very simple vector icon."""
    c.setLineWidth(1)
    if icon_type == "fish":
        c.line(x - size / 2, y, x + size / 2, y)
        c.line(x + size / 2, y, x, y + size / 2)
        c.line(x + size / 2, y, x, y - size / 2)
    elif icon_type == "deer":
        c.circle(x, y, size / 2, stroke=1, fill=0)
        c.line(x, y + size / 2, x, y + size)
    elif icon_type == "bird":
        c.circle(x, y, size / 2, stroke=1, fill=0)
        c.line(x - size / 2, y, x + size / 2, y + size / 2)
        c.line(x - size / 2, y, x + size / 2, y - size / 2)
    elif icon_type == "iss":
        c.setFont("Helvetica", size)
        c.drawCentredString(x, y - size / 2, "★")
    else:
        c.setFont("Helvetica", size)
        c.drawCentredString(x, y - size / 2, icon_type[0].upper())


def draw_icons(c, icons, x, y, size=8, gap=3):
    """Draw multiple icons stacked horizontally ending at (x, y)."""
    offset = 0
    for icon in reversed(icons):
        draw_icon(c, icon, x - offset, y, size)
        offset += size + gap
