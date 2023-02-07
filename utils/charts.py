color_palette = [
    "#9774d5",
    "#55efc4",
    "#81ecec",
    "#a29bfe",
    "#ffeaa7",
    "#fab1a0",
    "#fd79a8",
]
color_danger = "#ff7675"


def generate_color_palette(amount):
    palette = []

    i = 0
    while i < len(color_palette) and len(palette) < amount:
        palette.append(color_palette[i])
        i += 1
        if i == len(color_palette) and len(palette) < amount:
            i = 0

    return palette
