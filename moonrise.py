import csv


def time_to_hour(time):
    hour, minute = time.split(":")
    return int(hour) + int(minute) / 60


with open(
    "data/Moon_rise_set_2026.csv",
    newline="",
    encoding="utf-8-sig"
) as f:
    reader = csv.DictReader(f)

    for row in reader:
        if not row["RISE"]:
            continue

        rise = time_to_hour(row["RISE"])

        print(row["YYYY-MM-DD"], rise)