from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from pathlib import Path

# Use absolute path so Django always finds it
BASE_DIR = Path(__file__).resolve().parent.parent
SHEET = BASE_DIR / "logs" / "static" / "blank-paper-log.png"

ROWS = {
    "off_duty": 210,
    "sleeper": 260,
    "driving": 310,
    "on_duty": 360,
}

def render_log(segments, date_label="2025-09-16", carrier="Demo Carrier", driver="Driver"):
    im = Image.open(SHEET).convert("RGBA")
    draw = ImageDraw.Draw(im)

    # grid X coords
    x0, x1 = 70, im.width - 70
    w = (x1 - x0) / 24.0

    def x_at(time_str):
        t = datetime.strptime(time_str, "%H:%M")
        hour = t.hour + t.minute / 60  # ✅ fix
        return int(x0 + hour * w)

    # draw duty lines
    for seg in segments:
        y = ROWS.get(seg["status"], ROWS["off_duty"])
        xs, xe = x_at(seg["start"]), x_at(seg["end"])
        draw.line([(xs, y), (xe, y)], fill="black", width=4)
        # connectors
        draw.line([(xs, y - 20), (xs, y + 20)], fill="black", width=2)
        draw.line([(xe, y - 20), (xe, y + 20)], fill="black", width=2)

    # header text
    fnt = ImageFont.load_default()
    draw.text((80, 20), f"Date: {date_label}", font=fnt, fill="black")
    draw.text((300, 20), f"Carrier: {carrier}", font=fnt, fill="black")
    draw.text((600, 20), f"Driver: {driver}", font=fnt, fill="black")

    return im
