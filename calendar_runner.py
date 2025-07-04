import argparse
from src.generator import generate_calendar


def main():
    parser = argparse.ArgumentParser(
        description="Generate a ZIP-specific nature calendar."
    )
    parser.add_argument(
        "-z",
        "--zip",
        type=str,
        default="63901",
        help="5-digit ZIP code (default: 63901)",
    )
    parser.add_argument(
        "-m",
        "--month",
        type=int,
        help="Month as number (1–12)",
    )
    parser.add_argument(
        "-y",
        "--year",
        type=int,
        help="Year as 4-digit number (e.g. 2025)",
    )
    args = parser.parse_args()

    generate_calendar(
        zip_code=args.zip,
        month=args.month,
        year=args.year,
    )
    print("✅ Calendar generation complete.")


if __name__ == "__main__":
    main()
