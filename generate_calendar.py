#!/usr/bin/env python3
"""Generate an SVG calendar in the style of calendar-2025.pdf"""

import calendar
from datetime import date, timedelta


def add_crop_marks(svg_parts: list[str], bleed: float, total_width: float, total_height: float,
                   border_color: str) -> None:
    """Add crop marks around the printable page."""
    if bleed <= 0:
        return

    crop_mark_length = 10
    crop_mark_offset = 5
    # Top-left
    svg_parts.append(f'<line x1="{bleed - crop_mark_offset}" y1="{bleed}" x2="{bleed - crop_mark_offset - crop_mark_length}" y2="{bleed}" stroke="{border_color}" stroke-width="0.5"/>')
    svg_parts.append(f'<line x1="{bleed}" y1="{bleed - crop_mark_offset}" x2="{bleed}" y2="{bleed - crop_mark_offset - crop_mark_length}" stroke="{border_color}" stroke-width="0.5"/>')
    # Top-right
    svg_parts.append(f'<line x1="{total_width - bleed + crop_mark_offset}" y1="{bleed}" x2="{total_width - bleed + crop_mark_offset + crop_mark_length}" y2="{bleed}" stroke="{border_color}" stroke-width="0.5"/>')
    svg_parts.append(f'<line x1="{total_width - bleed}" y1="{bleed - crop_mark_offset}" x2="{total_width - bleed}" y2="{bleed - crop_mark_offset - crop_mark_length}" stroke="{border_color}" stroke-width="0.5"/>')
    # Bottom-left
    svg_parts.append(f'<line x1="{bleed - crop_mark_offset}" y1="{total_height - bleed}" x2="{bleed - crop_mark_offset - crop_mark_length}" y2="{total_height - bleed}" stroke="{border_color}" stroke-width="0.5"/>')
    svg_parts.append(f'<line x1="{bleed}" y1="{total_height - bleed + crop_mark_offset}" x2="{bleed}" y2="{total_height - bleed + crop_mark_offset + crop_mark_length}" stroke="{border_color}" stroke-width="0.5"/>')
    # Bottom-right
    svg_parts.append(f'<line x1="{total_width - bleed + crop_mark_offset}" y1="{total_height - bleed}" x2="{total_width - bleed + crop_mark_offset + crop_mark_length}" y2="{total_height - bleed}" stroke="{border_color}" stroke-width="0.5"/>')
    svg_parts.append(f'<line x1="{total_width - bleed}" y1="{total_height - bleed + crop_mark_offset}" x2="{total_width - bleed}" y2="{total_height - bleed + crop_mark_offset + crop_mark_length}" stroke="{border_color}" stroke-width="0.5"/>')


def generate_calendar_svg_grid(year: int, page_width: float = None, page_height: float = None,
                               bleed: float = 0) -> str:
    """Generate grid-style SVG calendar where all months start at column 1."""

    # Configuration
    base_cell_width = 80
    base_cell_height = 80
    month_label_width = 60
    header_height = 40
    margin = 20
    max_days = 31  # Maximum days in any month

    # Colors
    weekend_color = "#E6F3FF"  # Light blue for weekends
    weekday_color = "#FFFFFF"  # White for weekdays
    border_color = "#000000"
    text_color = "#000000"

    # Day of week letters
    dow_letters = ['M', 'T', 'W', 'T', 'F', 'S', 'S']

    # Month names
    month_names = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                   'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    # Calculate calendar data
    cal = calendar.Calendar(firstweekday=0)  # Monday = 0

    # Build the SVG
    svg_parts = []

    # Calculate scale factor if fitting to page
    if page_width and page_height:
        # Calculate natural calendar size
        natural_width = margin + month_label_width + (max_days * base_cell_width) + margin
        natural_height = margin + header_height + (12 * base_cell_height) + margin

        # Calculate scale to fit page (maintaining aspect ratio)
        available_width = page_width
        available_height = page_height
        scale_w = available_width / natural_width
        scale_h = available_height / natural_height
        scale = min(scale_w, scale_h, 1.0)  # Don't scale up, only down if needed

        cell_width = base_cell_width * scale
        cell_height = base_cell_height * scale
        month_label_width_scaled = month_label_width * scale
        header_height_scaled = header_height * scale
        margin_scaled = margin * scale
    else:
        cell_width = base_cell_width
        cell_height = base_cell_height
        month_label_width_scaled = month_label_width
        header_height_scaled = header_height
        margin_scaled = margin
        scale = 1.0

    # Calculate calendar dimensions with scaled values
    calendar_width = margin_scaled + month_label_width_scaled + (max_days * cell_width) + margin_scaled
    calendar_height = margin_scaled + header_height_scaled + (12 * cell_height) + margin_scaled

    # If page dimensions provided, use them; otherwise use calendar dimensions
    if page_width and page_height:
        total_width = page_width + (2 * bleed)
        total_height = page_height + (2 * bleed)
        # Center horizontally, align to top
        offset_x = bleed + (page_width - calendar_width) / 2
        offset_y = bleed  # Start at top of page (after bleed)
    else:
        total_width = calendar_width
        total_height = calendar_height
        offset_x = 0
        offset_y = 0

    # Add day number headers at the top (1-31)
    dow_x = offset_x + margin_scaled + month_label_width_scaled
    dow_y = offset_y + margin_scaled + (20 * scale)
    font_size_header = max(8, int(12 * scale))

    for day_num in range(1, max_days + 1):
        x = dow_x + ((day_num - 1) * cell_width)
        svg_parts.append(
            f'<text x="{x + cell_width/2}" y="{dow_y}" '
            f'text-anchor="middle" font-size="{font_size_header}" fill="{text_color}">{day_num}</text>'
        )

    # Start position for months
    y_pos = margin_scaled + header_height_scaled

    # Generate each month
    for month_idx, month_name in enumerate(month_names):
        month_num = month_idx + 1

        # Month label
        font_size_month = max(10, int(14 * scale))
        svg_parts.append(
            f'<text x="{offset_x + margin_scaled}" y="{offset_y + y_pos + cell_height/2 + (5 * scale)}" '
            f'font-size="{font_size_month}" fill="{text_color}">{month_name}</text>'
        )

        # Get all days in this month with their weekdays
        month_days = list(cal.itermonthdays2(year, month_num))

        # Create a mapping of day_number -> weekday for this month
        day_to_weekday = {}
        for day, weekday in month_days:
            if day != 0:
                day_to_weekday[day] = weekday

        # Draw cells for each day number (1-31)
        x_pos = offset_x + margin_scaled + month_label_width_scaled

        for day_num in range(1, max_days + 1):
            if day_num in day_to_weekday:
                weekday = day_to_weekday[day_num]
                # Determine background color (weekend vs weekday)
                bg_color = weekend_color if weekday >= 5 else weekday_color

                # Draw cell background
                svg_parts.append(
                    f'<rect x="{x_pos}" y="{offset_y + y_pos}" '
                    f'width="{cell_width}" height="{cell_height}" '
                    f'fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>'
                )

                # Draw day-of-week letter in upper right corner
                font_size_letter = max(4, min(10, cell_width / 8))
                padding = max(2, cell_width * 0.08)
                y_offset = max(font_size_letter * 1.1, cell_height * 0.15)
                svg_parts.append(
                    f'<text x="{x_pos + cell_width - padding}" y="{offset_y + y_pos + y_offset}" '
                    f'text-anchor="end" font-size="{font_size_letter:.1f}" fill="{text_color}">{dow_letters[weekday]}</text>'
                )
            # If day doesn't exist in this month, leave it empty (no cell)

            x_pos += cell_width

        # Move to next month row
        y_pos += cell_height

    add_crop_marks(svg_parts, bleed, total_width, total_height, border_color)

    # Build complete SVG
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{total_width}pt" height="{total_height}pt"
     viewBox="0 0 {total_width} {total_height}">
  <style>
    text {{ font-family: Arial, sans-serif; }}
  </style>
  <rect width="{total_width}" height="{total_height}" fill="white"/>
  {''.join(svg_parts)}
</svg>'''

    return svg


def generate_calendar_svg(year: int, page_width: float = None, page_height: float = None,
                          bleed: float = 0) -> str:
    """Generate continuous-style SVG calendar for the specified year."""

    # Configuration
    base_cell_width = 80
    base_cell_height = 80
    month_label_width = 60
    header_height = 40
    margin = 20

    # Colors
    weekend_color = "#E6F3FF"  # Light blue for weekends
    weekday_color = "#FFFFFF"  # White for weekdays
    border_color = "#000000"
    text_color = "#000000"

    # Month names
    month_names = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                   'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    # Day of week labels
    dow_labels = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    # Calculate calendar data
    cal = calendar.Calendar(firstweekday=0)  # Monday = 0

    # Build the SVG
    svg_parts = []

    # Start position
    y_pos = margin + header_height

    # Calculate the maximum width needed by checking each month
    max_cells_needed = 0
    for month_idx in range(12):
        month_num = month_idx + 1
        month_days = list(cal.itermonthdays2(year, month_num))

        # Find first and last day
        first_weekday = None
        last_day_num = 0
        for day, weekday in month_days:
            if day != 0:
                if first_weekday is None:
                    first_weekday = weekday
                last_day_num = day

        # Calculate cells needed: starting position + number of days
        if first_weekday is not None:
            cells_needed = first_weekday + last_day_num
            max_cells_needed = max(max_cells_needed, cells_needed)

    # Calculate scale factor if fitting to page
    if page_width and page_height:
        # Calculate natural calendar size
        natural_width = margin + month_label_width + (max_cells_needed * base_cell_width) + margin
        natural_height = margin + header_height + (12 * base_cell_height) + margin

        # Calculate scale to fit page (maintaining aspect ratio)
        available_width = page_width
        available_height = page_height
        scale_w = available_width / natural_width
        scale_h = available_height / natural_height
        scale = min(scale_w, scale_h, 1.0)  # Don't scale up, only down if needed

        cell_width = base_cell_width * scale
        cell_height = base_cell_height * scale
        month_label_width_scaled = month_label_width * scale
        header_height_scaled = header_height * scale
        margin_scaled = margin * scale
    else:
        cell_width = base_cell_width
        cell_height = base_cell_height
        month_label_width_scaled = month_label_width
        header_height_scaled = header_height
        margin_scaled = margin
        scale = 1.0

    # Calculate calendar dimensions with scaled values
    calendar_width = margin_scaled + month_label_width_scaled + (max_cells_needed * cell_width) + margin_scaled
    calendar_height = margin_scaled + header_height_scaled + (12 * cell_height) + margin_scaled

    # If page dimensions provided, use them; otherwise use calendar dimensions
    if page_width and page_height:
        total_width = page_width + (2 * bleed)
        total_height = page_height + (2 * bleed)
        # Center horizontally, align to top
        offset_x = bleed + (page_width - calendar_width) / 2
        offset_y = bleed  # Start at top of page (after bleed)
    else:
        total_width = calendar_width
        total_height = calendar_height
        offset_x = 0
        offset_y = 0

    # Add day of week headers at the top
    # Repeat the headers multiple times to cover the width
    dow_x = offset_x + margin_scaled + month_label_width_scaled
    dow_y = offset_y + margin_scaled + (20 * scale)
    font_size_dow = max(8, int(12 * scale))

    # Only add headers for cells that will actually be used
    for cell_idx in range(max_cells_needed):
        dow_idx = cell_idx % 7
        x = dow_x + (cell_idx * cell_width)
        svg_parts.append(
            f'<text x="{x + cell_width/2}" y="{dow_y}" '
            f'text-anchor="middle" font-size="{font_size_dow}" fill="{text_color}">{dow_labels[dow_idx]}</text>'
        )

    # Start position for months
    y_pos = margin_scaled + header_height_scaled

    # Generate each month
    for month_idx, month_name in enumerate(month_names):
        month_num = month_idx + 1

        # Month label
        font_size_month = max(10, int(14 * scale))
        svg_parts.append(
            f'<text x="{offset_x + margin_scaled}" y="{offset_y + y_pos + cell_height/2 + (5 * scale)}" '
            f'font-size="{font_size_month}" fill="{text_color}">{month_name}</text>'
        )

        # Get all days in this month
        month_days = list(cal.itermonthdays2(year, month_num))

        # Starting x position for first day
        x_pos = offset_x + margin_scaled + month_label_width_scaled

        # Find the first non-zero day to determine starting position
        first_day_weekday = None
        for day, weekday in month_days:
            if day != 0:
                first_day_weekday = weekday
                break

        # Adjust x_pos based on the first day's weekday
        if first_day_weekday is not None:
            x_pos += first_day_weekday * cell_width

        # Draw each day
        day_x = x_pos
        for day, weekday in month_days:
            if day != 0:  # Skip days from previous/next month
                # Determine background color (weekend vs weekday)
                # weekday: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
                bg_color = weekend_color if weekday >= 5 else weekday_color

                # Draw cell background
                svg_parts.append(
                    f'<rect x="{day_x}" y="{offset_y + y_pos}" '
                    f'width="{cell_width}" height="{cell_height}" '
                    f'fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>'
                )

                # Draw day number in upper right corner
                # Scale font size relative to cell size, with minimum of 4pt
                font_size_day = max(4, min(10, cell_width / 8))
                # Padding should be proportional to cell size
                padding = max(2, cell_width * 0.08)
                # Vertical position - use font height + extra padding for smaller cells
                y_offset = max(font_size_day * 1.1, cell_height * 0.15)
                svg_parts.append(
                    f'<text x="{day_x + cell_width - padding}" y="{offset_y + y_pos + y_offset}" '
                    f'text-anchor="end" font-size="{font_size_day:.1f}" fill="{text_color}">{day}</text>'
                )

                day_x += cell_width

        # Move to next month row
        y_pos += cell_height

    add_crop_marks(svg_parts, bleed, total_width, total_height, border_color)

    # Build complete SVG
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{total_width}pt" height="{total_height}pt"
     viewBox="0 0 {total_width} {total_height}">
  <style>
    text {{ font-family: Arial, sans-serif; }}
  </style>
  <rect width="{total_width}" height="{total_height}" fill="white"/>
  {''.join(svg_parts)}
</svg>'''

    return svg


def generate_calendar_svg_weekday(year: int, page_width: float = None, page_height: float = None,
                                  bleed: float = 0) -> str:
    """Generate SVG calendar with one row per weekday and one column per week."""

    # Configuration
    base_cell_width = 80
    base_cell_height = 80
    row_label_width = 60
    header_height = 40
    margin = 20

    # Colors
    border_color = "#000000"
    text_color = "#000000"
    month_line_color = "#666666"
    month_colors = [
        "#F6D6D6", "#F6E2D6", "#F6F0D6", "#E8F6D6",
        "#D6F6E3", "#D6F1F6", "#D6E3F6", "#E1D6F6",
        "#F1D6F6", "#F6D6E7", "#E6E6E6", "#DDE7D7",
    ]

    # Labels
    dow_labels = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    month_names = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                   'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    year_start = date(year, 1, 1)
    year_end = date(year, 12, 31)
    grid_start = year_start - timedelta(days=year_start.weekday())
    grid_end = year_end + timedelta(days=(6 - year_end.weekday()))
    total_weeks = ((grid_end - grid_start).days + 1) // 7

    if page_width and page_height:
        natural_width = margin + row_label_width + (total_weeks * base_cell_width) + margin
        natural_height = margin + header_height + (7 * base_cell_height) + margin

        scale_w = page_width / natural_width
        scale_h = page_height / natural_height
        scale = min(scale_w, scale_h, 1.0)

        cell_width = base_cell_width * scale
        cell_height = base_cell_height * scale
        row_label_width_scaled = row_label_width * scale
        header_height_scaled = header_height * scale
        margin_scaled = margin * scale
    else:
        cell_width = base_cell_width
        cell_height = base_cell_height
        row_label_width_scaled = row_label_width
        header_height_scaled = header_height
        margin_scaled = margin
        scale = 1.0

    calendar_width = margin_scaled + row_label_width_scaled + (total_weeks * cell_width) + margin_scaled
    calendar_height = margin_scaled + header_height_scaled + (7 * cell_height) + margin_scaled

    if page_width and page_height:
        total_width = page_width + (2 * bleed)
        total_height = page_height + (2 * bleed)
        offset_x = bleed + (page_width - calendar_width) / 2
        offset_y = bleed
    else:
        total_width = calendar_width
        total_height = calendar_height
        offset_x = 0
        offset_y = 0

    svg_parts = []

    header_y = offset_y + margin_scaled + (20 * scale)
    font_size_day = max(4, min(10, cell_width / 8))
    font_size_month = max(8, int(12 * scale))
    font_size_row = max(10, int(14 * scale))
    padding = max(2, cell_width * 0.08)
    day_y_offset = max(font_size_day * 1.1, cell_height * 0.15)

    # Week columns and month markers
    month_starts = {
        date(year, month_num, 1): month_names[month_num - 1]
        for month_num in range(1, 13)
    }
    for week_idx in range(total_weeks):
        week_start = grid_start + timedelta(days=week_idx * 7)
        x = offset_x + margin_scaled + row_label_width_scaled + (week_idx * cell_width)

        for day_offset in range(7):
            current_day = week_start + timedelta(days=day_offset)
            if current_day in month_starts:
                label_x = x + (cell_width / 2)
                svg_parts.append(
                    f'<text x="{label_x}" y="{header_y}" '
                    f'text-anchor="middle" font-size="{font_size_month}" fill="{text_color}">{month_starts[current_day]}</text>'
                )
                svg_parts.append(
                    f'<line x1="{x}" y1="{offset_y + margin_scaled + header_height_scaled * 0.35}" '
                    f'x2="{x}" y2="{offset_y + margin_scaled + header_height_scaled + (7 * cell_height)}" '
                    f'stroke="{month_line_color}" stroke-width="0.75"/>'
                )
                break

    y_pos = margin_scaled + header_height_scaled
    for weekday_idx, label in enumerate(dow_labels):
        row_y = offset_y + y_pos + (weekday_idx * cell_height)

        svg_parts.append(
            f'<text x="{offset_x + margin_scaled}" y="{row_y + cell_height/2 + (5 * scale)}" '
            f'font-size="{font_size_row}" fill="{text_color}">{label}</text>'
        )

        for week_idx in range(total_weeks):
            current_day = grid_start + timedelta(days=(week_idx * 7) + weekday_idx)
            x = offset_x + margin_scaled + row_label_width_scaled + (week_idx * cell_width)

            if year_start <= current_day <= year_end:
                bg_color = month_colors[current_day.month - 1]
                svg_parts.append(
                    f'<rect x="{x}" y="{row_y}" width="{cell_width}" height="{cell_height}" '
                    f'fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>'
                )
                svg_parts.append(
                    f'<text x="{x + cell_width - padding}" y="{row_y + day_y_offset}" '
                    f'text-anchor="end" font-size="{font_size_day:.1f}" fill="{text_color}">{current_day.day}</text>'
                )

    add_crop_marks(svg_parts, bleed, total_width, total_height, border_color)

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{total_width}pt" height="{total_height}pt"
     viewBox="0 0 {total_width} {total_height}">
  <style>
    text {{ font-family: Arial, sans-serif; }}
  </style>
  <rect width="{total_width}" height="{total_height}" fill="white"/>
  {''.join(svg_parts)}
</svg>'''

    return svg


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate SVG calendar')
    parser.add_argument('--year', type=int, default=2026,
                        help='Year for the calendar (default: 2026)')
    parser.add_argument('--output', type=str, default=None,
                        help='Output filename (default: calendar-YEAR.svg or .pdf)')
    parser.add_argument('--pdf', action='store_true',
                        help='Generate PDF output')
    parser.add_argument('--a2', action='store_true',
                        help='Format for A2 landscape printing (594mm × 420mm)')
    parser.add_argument('--a4', action='store_true',
                        help='Format for A4 landscape printing (297mm × 210mm)')
    parser.add_argument('--bleed', type=float, default=None,
                        help='Bleed area in mm (default: 3mm for PDF with --a2/--a4, 0 otherwise)')
    parser.add_argument('--layout', type=str, default='continuous',
                        choices=['continuous', 'grid', 'weekday'],
                        help='Calendar layout: continuous (default, days flow by weekday), grid (all months start at column 1, show day-of-week letters), or weekday (one row per weekday, one column per week)')

    args = parser.parse_args()

    # Paper dimensions in points (1 point = 1/72 inch, 1mm = 2.83465 points)
    if args.a2:
        page_width = 1683.78  # 594mm
        page_height = 1190.55  # 420mm
        # Default 3mm bleed for PDF print, unless explicitly set
        if args.bleed is None:
            bleed_points = 3 * 2.83465 if args.pdf else 0
        else:
            bleed_points = args.bleed * 2.83465
        page_name = 'a2'
    elif args.a4:
        page_width = 841.89  # 297mm (A4 landscape)
        page_height = 595.28  # 210mm
        # Default 3mm bleed for PDF print, unless explicitly set
        if args.bleed is None:
            bleed_points = 3 * 2.83465 if args.pdf else 0
        else:
            bleed_points = args.bleed * 2.83465
        page_name = 'a4'
    else:
        page_width = None
        page_height = None
        bleed_points = args.bleed * 2.83465 if args.bleed and args.bleed > 0 else 0
        page_name = None

    # Determine output filename
    if args.output:
        output_file = args.output
    else:
        ext = 'pdf' if args.pdf else 'svg'
        suffix = f'-{page_name}' if page_name else ''
        layout_suffix = '' if args.layout == 'continuous' else f'-{args.layout}'
        output_file = f'calendar-{args.year}{suffix}{layout_suffix}.{ext}'

    # Generate calendar with the chosen layout
    if args.layout == 'grid':
        svg_content = generate_calendar_svg_grid(args.year, page_width, page_height, bleed_points)
    elif args.layout == 'weekday':
        svg_content = generate_calendar_svg_weekday(args.year, page_width, page_height, bleed_points)
    else:
        svg_content = generate_calendar_svg(args.year, page_width, page_height, bleed_points)

    if args.pdf:
        # Generate PDF
        try:
            import cairosvg
            svg_path = output_file.replace('.pdf', '.svg')
            # Save SVG first
            with open(svg_path, 'w') as f:
                f.write(svg_content)
            # Convert to PDF (cairosvg will use the SVG's native dimensions)
            cairosvg.svg2pdf(bytestring=svg_content.encode('utf-8'),
                           write_to=output_file)
            print(f"PDF generated: {output_file}")
            if svg_path != output_file:
                print(f"SVG saved: {svg_path}")
        except ImportError:
            print("Error: cairosvg not installed. Install with: uv add cairosvg")
            return
    else:
        # Generate SVG
        with open(output_file, 'w') as f:
            f.write(svg_content)
        print(f"Calendar generated: {output_file}")


if __name__ == '__main__':
    main()
