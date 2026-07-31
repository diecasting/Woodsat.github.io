"""Generate static/favicon.ico (32x32) — a speaker-driver mark in Woodsat wood tones.
Pure stdlib: writes a 32-bit BGRA ICO by hand, no image libraries required.
"""
import os
import struct

SIZE = 32
WOOD = (0x6B, 0x44, 0x23)   # RGB wood brown, background
CREAM = (0xE8, 0xDC, 0xC8)  # surround ring
CONE = (0x3A, 0x24, 0x12)   # dark cone centre

cx = cy = (SIZE - 1) / 2.0


def pixel(x, y):
    dx, dy = x - cx, y - cy
    d = (dx * dx + dy * dy) ** 0.5
    if d <= 4.5:
        return CONE
    if d <= 12.0:
        return CREAM
    if d <= 13.6:
        return CONE
    return WOOD


# XOR bitmap is stored bottom-up, BGRA
xor = bytearray()
for y in range(SIZE - 1, -1, -1):
    for x in range(SIZE):
        r, g, b = pixel(x, y)
        xor += bytes((b, g, r, 255))

# AND mask: fully opaque, rows padded to 4 bytes
and_mask = bytes((SIZE // 8) * SIZE)

info_header = struct.pack(
    "<IiiHHIIiiII",
    40,            # biSize
    SIZE,          # biWidth
    SIZE * 2,      # biHeight (XOR + AND)
    1,             # biPlanes
    32,            # biBitCount
    0,             # biCompression
    len(xor) + len(and_mask),
    0, 0, 0, 0,
)

image = info_header + bytes(xor) + and_mask
ico = struct.pack("<HHH", 0, 1, 1)
ico += struct.pack("<BBBBHHII", SIZE, SIZE, 0, 0, 1, 32, len(image), 6 + 16)
ico += image

os.makedirs("static", exist_ok=True)
with open(os.path.join("static", "favicon.ico"), "wb") as f:
    f.write(ico)
print("wrote static/favicon.ico", len(ico), "bytes")

svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
    '<rect width="32" height="32" rx="6" fill="#6B4423"/>'
    '<circle cx="16" cy="16" r="13" fill="#3A2412"/>'
    '<circle cx="16" cy="16" r="11.5" fill="#E8DCC8"/>'
    '<circle cx="16" cy="16" r="4.5" fill="#3A2412"/>'
    "</svg>"
)
with open(os.path.join("static", "favicon.svg"), "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote static/favicon.svg")
