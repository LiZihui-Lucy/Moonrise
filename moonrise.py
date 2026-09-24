import csv

with open("data/Moon_rise_set_2026.csv", newline="") as f:
    reader = csv.DictReader(f)

    row = next(reader)

    print(row)
    print(row["RISE"])
    print(type(row["RISE"]))