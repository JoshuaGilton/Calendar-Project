# Calendar Project

This project generates a PDF nature calendar for a given ZIP code. Notes for each ZIP code can come from local JSON files or remote URLs.

## `data/zip_sources.json`

`zip_sources.json` maps ZIP codes to the JSON file or URL that contains the calendar notes. Relative paths are resolved from the `data` directory.

Example:

```json
{
  "12345": "sample_notes_12345.json",
  "98765": "https://example.com/notes/98765.json"
}
```

## Notes file format

Each notes file is a JSON object where keys are `YYYY-MM-DD` strings and values contain two fields:

```json
{
  "2025-07-01": {"Line_1": "Bird migration peak", "Line_2": "Fishing: Trout season"},
  "2025-07-02": {"Line_1": "Wildflowers bloom", "Line_2": "Hunting: Deer archery"}
}
```

`Line_1` is an optional general note. `Line_2` is used for hunting or fishing information and will always appear on the second line in the calendar.

See `data/sample_notes_12345.json` for a complete example.

## Generating a calendar

Run:

```bash
python calendar_runner.py --zip 12345 --month 7 --year 2025
```

This will read notes for ZIP code `12345` from the configured source and output a PDF calendar.

## `templates/layout_config.json`

The PDF layout is controlled by `templates/layout_config.json`. The file
defines page margins, header height, grid dimensions, cell sizes and the fonts
used for different parts of the calendar. Editing this JSON allows you to
change the look of the generated calendar.

Example snippet of the default configuration:

```json
{
  "page_margin": 40,
  "header_height": 40,
  "rows": 5,
  "cols": 7,
  "cell_size": {"width": 76, "height": 134},
  "fonts": {
    "day_name": {"name": "Helvetica-Bold", "size": 12},
    "date": {"name": "Helvetica-Bold", "size": 14},
    "note": {"name": "Helvetica", "size": 10},
    "icon": {"name": "Helvetica-Oblique", "size": 8}
  }
}
```

To use different fonts or adjust cell dimensions, modify the file like so:

```json
{
  "fonts": {
    "day_name": {"name": "Courier-Bold", "size": 12},
    "date": {"name": "Courier-Bold", "size": 16}
  },
  "cell_size": {"width": 90, "height": 150}
}
```

After saving your changes, run `calendar_runner.py` again to generate a calendar
with the new layout.
