# Calendar Generator

Generate SVG or PDF wall-calendar layouts (continuous, grid, or weekday) for a given year.

## Requirements

- Python >= 3.14
- `uv`

## Usage

Install dependencies:

```bash
uv sync
```

Generate an SVG calendar:

```bash
uv run python generate_calendar.py --year 2026
```

Generate a PDF in A4 size:

```bash
uv run python generate_calendar.py --year 2026 --pdf --a4
```

Generate a grid layout with bleed (mm):

```bash
uv run python generate_calendar.py --year 2026 --layout grid --bleed 3 --a4
```

Generate a weekday layout with one row per weekday and one column per week:

```bash
uv run python generate_calendar.py --year 2026 --layout weekday
```

Run `uv run python generate_calendar.py --help` for full options.
