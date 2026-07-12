"""
Turn a photo of yourself into ASCII art sized for the profile SVG.

Usage:
    pip install pillow
    python generate_ascii.py path/to/photo.jpg

It prints ready-to-paste <tspan> lines. Copy them over the ASCII block
(the lines between <text x="15" ...> and </text>) in BOTH dark_mode.svg
and light_mode.svg.

Tips for a good result:
  - Use a high-contrast, head-and-shoulders photo with a plain background.
  - A square-ish crop works best.
"""
import sys

# Ramp from empty -> dense. On the dark-theme SVG the text is light ink on a dark
# background, so BRIGHT pixels (your lit face) should become dense characters and
# DARK pixels (background) should fade to spaces. If your photo has a light
# background instead, pass "invert" as a 2nd arg to flip the ramp.
CHARS = " .:-=+*#%@"
COLS = 42          # width in characters (fits the left column of the SVG)
CHAR_ASPECT = 0.5  # monospace glyphs are ~2x taller than wide


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    try:
        from PIL import Image
    except ImportError:
        print("Pillow is required:  pip install pillow")
        sys.exit(1)

    invert = len(sys.argv) > 2 and sys.argv[2].lower() == "invert"
    ramp = CHARS[::-1] if invert else CHARS

    img = Image.open(sys.argv[1]).convert("L")  # greyscale
    w, h = img.size
    rows = int(COLS * (h / w) * CHAR_ASPECT)
    img = img.resize((COLS, rows))
    pixels = img.getdata()

    lines = []
    for r in range(rows):
        row_chars = []
        for c in range(COLS):
            lum = pixels[r * COLS + c]          # 0..255
            idx = int((lum / 255) * (len(ramp) - 1))
            row_chars.append(ramp[idx])
        lines.append("".join(row_chars))

    # Emit <tspan> lines starting at y=30, stepping 20px (matches the SVG grid).
    print("\n--- paste these lines into the <text x=\"15\"> block of both SVGs ---\n")
    y = 30
    for line in lines:
        safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        print(f'<tspan x="15" y="{y}">{safe}</tspan>')
        y += 20


if __name__ == "__main__":
    main()
