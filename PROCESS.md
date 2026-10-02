# Process

## Tools

- Hong Kong Observatory Open Data — used as the data source for the 2026 moonrise, lunar transit, and moonset times in Hong Kong. The data was provided as a CSV file.
- **VS Code** — used to inspect the CSV file and write and run the Python scripts.
- **Python `csv` module** — used to read the raw CSV file and process the data.
- **Matplotlib** — used to create the final visualization and export it as a PNG.
- **uv** — used to run the Python scripts and manage the dependencies specified in the script metadata.
- Git / GitHub— used to version and publish the project.

I also used AI to help write and iterate on parts of the Python visualization code. I tested the code locally, checked the output, and changed the visualization based on what the data actually showed.

## Kept

I kept the basic idea of using day of year on the x-axis and time of day on the y-axis.

The original data contains three times for each day: moonrise, lunar transit, and moonset. At first I experimented with several different visual forms, including a normal line chart, a circular moonrise chart, and a more radial/spiral visualization.

The circular versions made the data difficult to read. They looked more decorative than informative, and the relationship between the actual moonrise times and the days of the year was not clear.

I therefore kept the Cartesian time-series structure in the final version:

- X = day of year
- Y = time of day
- three waves = moonrise, transit, and moonset

I also kept the midnight-crossing behaviour as part of the visualization instead of simply treating it as an error. Some moonrise and moonset times move from late evening to just after midnight, which creates apparent jumps in a normal time plot. The final script breaks the line at large jumps so that it does not draw a misleading vertical connection across midnight.

The final visualization also keeps the actual data points visible while using the wave-like lines to create a larger overall pattern. This made the image more visually coherent without completely hiding the underlying data.

## Rejected

I rejected the early circular / radial visualization.

I first mapped the day of the year around a circle and mapped the moonrise time to a radius. Later I also experimented with connecting the moonrise, transit, and moonset data into circular and spiral patterns.

These versions looked visually interesting, but they did not communicate the numerical data clearly. The circular mapping made the chart look like a fan or a set of concentric rings, and it became difficult to tell which position represented which actual time.

I also rejected the first simple line-chart version as the final design. It showed the data clearly, but the midnight crossings created large jumps in the lines. The chart was readable, but it did not express the continuous lunar movement that I wanted to explore visually.

During the data-processing stage, I also found that the CSV values were initially strings rather than numbers. For example, `15:28` was reported as `<class 'str'>`. I converted the time values into decimal hours before plotting them. The CSV also contained some missing values, so these were kept as missing rather than inventing values for them.

One technical issue I had to correct was the CSV's UTF-8 BOM. The first column was initially read incorrectly, which caused a `KeyError` when accessing `YYYY-MM-DD`. I changed the file reading to use `encoding="utf-8-sig"` so that the original CSV could be parsed correctly.