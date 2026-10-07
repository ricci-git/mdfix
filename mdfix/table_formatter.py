from .elements import Table


def format_table(table: Table) -> str:
    column_count = len(table.headers)

    if any(len(row) > column_count for row in table.rows):
        raise ValueError("more cells than headers")

    normalized_rows = [
        row + [""] * (column_count - len(row))
        for row in table.rows
    ]

    widths = [
        max(
            len(table.headers[index]),
            *(len(row[index]) for row in normalized_rows),
            3,
        )
        for index in range(column_count)
    ]

    header = "| " + " | ".join(
        cell.ljust(width)
        for cell, width in zip(table.headers, widths)
    ) + " |"

    separator = "| " + " | ".join(
        "-" * width
        for width in widths
    ) + " |"

    rows = [
        "| " + " | ".join(
            cell.ljust(width)
            for cell, width in zip(row, widths)
        ) + " |"
        for row in normalized_rows
    ]

    return "\n".join([header, separator, *rows])
