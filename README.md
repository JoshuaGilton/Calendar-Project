# Calendar Project

This project generates a PDF nature calendar for a given ZIP code. Notes for each ZIP code can come from local JSON files or remote URLs.

## Install dependencies

Before running `calendar_runner.py`, install the required packages:

```bash
pip install -r requirements.txt
```

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
