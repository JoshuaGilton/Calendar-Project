# Calendar Project

This project generates a printable PDF calendar populated with nature-related notes for a specified US ZIP code. It uses a small static dataset for demonstration but can be extended to pull notes from other sources.

## Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd Calendar-Project
   ```
2. **Create a virtual environment (optional but recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the command line script to create a PDF calendar. By default it uses ZIP code `63901` and the current month/year.

```bash
python calendar_runner.py
```

You can specify the ZIP code, month, and year:

```bash
python calendar_runner.py -z 12345 -m 7 -y 2025
```

The generated file will be named `calendar_<zip>_<year>_<month>.pdf` in the project directory.

## Project Goals

- Demonstrate PDF calendar generation with [ReportLab](https://www.reportlab.com/).
- Provide a starting point for ZIP‑specific wildlife, fishing, and hunting notes.
- Offer a simple structure that can be expanded with dynamic data sources and additional styling options.

Contributions and suggestions are welcome!
