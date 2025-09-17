from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Pre-measured Y coordinates for duty rows
ROWS = {
    "off_duty": 150,
    "sleeper": 220,
    "driving": 290,
    "on_duty": 360,
}


def generate_blank_log():
    """Generate a clean blank log sheet (white paper with grid)."""
    im = Image.new("RGB", (1200, 500), "white")
    draw = ImageDraw.Draw(im)
    fnt = ImageFont.load_default()

    # Grid X coords
    x0, x1 = 70, im.width - 70
    w = (x1 - x0) / 24.0

    # Vertical hour lines + labels
    for h in range(25):
        x = int(x0 + h * w)
        draw.line([(x, ROWS["off_duty"]), (x, ROWS["on_duty"])], fill="gray", width=1)
        if h < 24:
            draw.text((x - 5, ROWS["on_duty"] + 20), f"{h}", font=fnt, fill="black")

    # Horizontal duty status lines
    for name, y in ROWS.items():
        draw.line([(x0, y), (x1, y)], fill="black", width=2)
        draw.text((20, y - 10), name.replace("_", " ").title(), font=fnt, fill="black")

    # Border box
    draw.rectangle([(x0, ROWS["off_duty"]), (x1, ROWS["on_duty"])], outline="black", width=2)

    return im


def render_log(segments, date_label="2025-09-16", carrier="Demo Carrier", driver="Driver"):
    """Draw duty segments on a generated blank log sheet."""
    im = generate_blank_log().convert("RGBA")
    draw = ImageDraw.Draw(im)
    fnt = ImageFont.load_default()

    # Grid X coords
    x0, x1 = 70, im.width - 70
    w = (x1 - x0) / 24.0

    def x_at(time_str):
        t = datetime.strptime(time_str, "%H:%M")
        hour = t.hour + t.minute / 60
        return int(x0 + hour * w)

    # Draw duty lines
    for seg in segments:
        y = ROWS.get(seg["status"], ROWS["off_duty"])
        xs, xe = x_at(seg["start"]), x_at(seg["end"])
        draw.line([(xs, y), (xe, y)], fill="black", width=4)
        # connectors
        draw.line([(xs, y - 20), (xs, y + 20)], fill="black", width=2)
        draw.line([(xe, y - 20), (xe, y + 20)], fill="black", width=2)

    # Header info
    draw.text((80, 20), f"Date: {date_label}", font=fnt, fill="black")
    draw.text((300, 20), f"Carrier: {carrier}", font=fnt, fill="black")
    draw.text((600, 20), f"Driver: {driver}", font=fnt, fill="black")

    return im
