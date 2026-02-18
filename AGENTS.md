<INSTRUCTIONS>
## Project Overview
This repo generates printable calendar layouts (SVG/PDF) for a given year.
Core script: `generate_calendar.py`.

## How to Run
- Use `uv` for dependencies and execution.
- Install deps: `uv sync`
- Generate SVG: `uv run python generate_calendar.py --year 2026`
- Generate PDF: `uv run python generate_calendar.py --year 2026 --pdf --a4`
- Grid layout with bleed (mm): `uv run python generate_calendar.py --year 2026 --layout grid --bleed 3 --a4`

## Outputs
- The script writes output files in the repo root, named like:
  - `calendar-2026.svg`
  - `calendar-2026-grid.svg`
  - `calendar-2026-a4.pdf`
- Only commit output files when explicitly requested; otherwise keep the repo clean.

## Change Guidance
- Keep layout logic and CLI behavior in `generate_calendar.py`.
- Update `README.md` when changing usage or dependencies.
- Avoid introducing non-ASCII characters unless already present.
</INSTRUCTIONS>
