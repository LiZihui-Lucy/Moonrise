# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap


# ==================================================
# 1. Convert HH:MM into decimal hours
# ==================================================

def time_to_hour(value):
    if not value:
        return None

    hour, minute = value.split(":")
    return int(hour) + int(minute) / 60


# ==================================================
# 2. Read the CSV data
# ==================================================

DATA = Path("data/Moon_rise_set_2026.csv")
OUT = Path("out")

OUT.mkdir(exist_ok=True)

days = []
moonrise = []
transit = []
moonset = []


with open(DATA, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)

    for day_number, row in enumerate(reader, start=1):

        rise = time_to_hour(row["RISE"])
        trans = time_to_hour(row["TRAN."])
        setting = time_to_hour(row["SET"])

        days.append(day_number)
        moonrise.append(rise)
        transit.append(trans)
        moonset.append(setting)


# ==================================================
# 3. Break lines when data jumps across midnight
# ==================================================

def make_segments(x, y):

    segments = []
    current = []

    for i in range(len(x)):

        # Missing data
        if y[i] is None:

            if len(current) > 1:
                segments.append(current)

            current = []
            continue

        point = (x[i], y[i])

        # Check for a large jump in time
        if current:

            previous_y = current[-1][1]

            if abs(y[i] - previous_y) > 8:

                if len(current) > 1:
                    segments.append(current)

                current = []

        current.append(point)

    # Add final segment
    if len(current) > 1:
        segments.append(current)

    return segments


# ==================================================
# 4. Create figure
# ==================================================

fig, ax = plt.subplots(
    figsize=(17, 11)
)

fig.patch.set_facecolor("white")
ax.set_facecolor("white")


# ==================================================
# 5. Silver-blue gradient
# ==================================================

blue_gradient = LinearSegmentedColormap.from_list(
    "moon_blue",
    [
        "#DCE7EF",
        "#AFC4D3",
        "#7D9CAF",
        "#58758C",
    ],
)


# ==================================================
# 6. Draw a gradient data line
# ==================================================

def draw_wave(
    x,
    y,
    linewidth=1.8,
    alpha=0.9,
):

    segments = make_segments(x, y)

    for segment in segments:

        if len(segment) < 2:
            continue

        points = []

        for i in range(len(segment) - 1):

            x1, y1 = segment[i]
            x2, y2 = segment[i + 1]

            points.append(
                [
                    [x1, y1],
                    [x2, y2],
                ]
            )

        colors = [
            blue_gradient(
                i / max(1, len(points) - 1)
            )
            for i in range(len(points))
        ]

        collection = LineCollection(
            points,
            colors=colors,
            linewidths=linewidth,
            alpha=alpha,
        )

        ax.add_collection(collection)


# ==================================================
# 7. Main data waves
# ==================================================

# Moonrise
draw_wave(
    days,
    moonrise,
    linewidth=2.2,
    alpha=0.95,
)

# Transit
draw_wave(
    days,
    transit,
    linewidth=2.0,
    alpha=0.80,
)

# Moonset
draw_wave(
    days,
    moonset,
    linewidth=2.2,
    alpha=0.90,
)


# ==================================================
# 8. Subtle echo waves
# ==================================================
#
# These are only visual echoes.
# They do NOT represent additional measurements.
#

for offset in [-0.10, 0.10]:

    echo_rise = [
        value + offset
        if value is not None
        else None
        for value in moonrise
    ]

    echo_transit = [
        value + offset
        if value is not None
        else None
        for value in transit
    ]

    echo_set = [
        value + offset
        if value is not None
        else None
        for value in moonset
    ]

    draw_wave(
        days,
        echo_rise,
        linewidth=0.5,
        alpha=0.18,
    )

    draw_wave(
        days,
        echo_transit,
        linewidth=0.5,
        alpha=0.14,
    )

    draw_wave(
        days,
        echo_set,
        linewidth=0.5,
        alpha=0.18,
    )


# ==================================================
# 9. Actual data points
# ==================================================

ax.scatter(
    days,
    moonrise,
    s=5,
    color="#607D91",
    alpha=0.55,
    zorder=5,
)

ax.scatter(
    days,
    transit,
    s=4,
    color="#8CA5B6",
    alpha=0.45,
    zorder=5,
)

ax.scatter(
    days,
    moonset,
    s=5,
    color="#506D83",
    alpha=0.55,
    zorder=5,
)


# ==================================================
# 10. Month positions
# ==================================================

months = [
    ("JAN", 1),
    ("FEB", 32),
    ("MAR", 60),
    ("APR", 91),
    ("MAY", 121),
    ("JUN", 152),
    ("JUL", 182),
    ("AUG", 213),
    ("SEP", 244),
    ("OCT", 274),
    ("NOV", 305),
    ("DEC", 335),
]


for month, position in months:

    # Vertical month divider
    ax.axvline(
        position,
        linewidth=0.6,
        color="#DCE4E9",
        alpha=0.8,
        zorder=0,
    )

    # Month label above the chart
    ax.text(
        position + 2,
        25.15,
        month,
        fontsize=8,
        color="#6F8492",
        fontweight="bold",
        ha="left",
    )


# ==================================================
# 11. Horizontal time grid
# ==================================================

for hour in [0, 6, 12, 18, 24]:

    ax.axhline(
        hour,
        linewidth=0.6,
        color="#E5EBEF",
        alpha=0.8,
        zorder=0,
    )


# ==================================================
# 12. Axis range
# ==================================================

ax.set_xlim(
    1,
    365,
)

ax.set_ylim(
    0,
    25.8,
)


# ==================================================
# 13. Y-axis labels
# ==================================================

ax.set_xticks([])

ax.set_yticks(
    [
        0,
        6,
        12,
        18,
        24,
    ]
)

ax.set_yticklabels(
    [
        "00:00",
        "06:00",
        "12:00",
        "18:00",
        "24:00",
    ],
    fontsize=9,
    color="#6F8492",
)


# ==================================================
# 14. Main title
# ==================================================

ax.text(
    1,
    27.0,
    "MOONRISE / TRANSIT / MOONSET",
    fontsize=21,
    fontweight="bold",
    color="#405766",
)


# Subtitle
ax.text(
    1,
    26.45,
    "Hong Kong · 2026 · 365 days of lunar movement",
    fontsize=9,
    color="#8799A5",
)


# ==================================================
# 15. X-axis description
# ==================================================

ax.text(
    183,
    -1.45,
    "DAY OF YEAR  →",
    ha="center",
    fontsize=8,
    color="#8A9AA4",
)


# ==================================================
# 16. Legend
# ==================================================

ax.plot(
    [],
    [],
    color="#607D91",
    linewidth=2,
    label="Moonrise",
)

ax.plot(
    [],
    [],
    color="#8CA5B6",
    linewidth=2,
    label="Transit",
)

ax.plot(
    [],
    [],
    color="#506D83",
    linewidth=2,
    label="Moonset",
)


ax.legend(
    loc="upper left",
    bbox_to_anchor=(0, -0.08),
    ncol=3,
    frameon=False,
    fontsize=9,
    handlelength=2.5,
    columnspacing=2.5,
)


# ==================================================
# 17. Clean up the frame
# ==================================================

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_visible(False)


# Remove unnecessary tick marks
ax.tick_params(
    axis="both",
    length=0,
)


# ==================================================
# 18. Layout
# ==================================================

plt.tight_layout(
    rect=[
        0,
        0.05,
        1,
        0.96,
    ]
)


# ==================================================
# 19. Save
# ==================================================

output = OUT / "moonrise_new.png"

plt.savefig(
    output,
    dpi=200,
    bbox_inches="tight",
    facecolor="white",
)


# ==================================================
# 20. Display
# ==================================================

plt.show()


# ==================================================
# 21. Confirmation
# ==================================================

print()
print("==============================")
print("NEW MOONRISE PLOT CREATED")
print("==============================")
print(output.resolve())
print("==============================")