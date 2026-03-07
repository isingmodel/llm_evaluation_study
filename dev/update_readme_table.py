from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
README_PATH = ROOT / "README.md"
CSV_PATH = ROOT / "dev" / "study_table.csv"
START_MARKER = "<!-- STUDY_TABLE:START -->"
END_MARKER = "<!-- STUDY_TABLE:END -->"
HEADERS = ("Index", "주제", "논문/자료", "발표자", "발표자료 & 영상")
FIELD_NAMES = ("index", "topic", "papers", "presenter", "materials")


def escape_markdown_cell(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", "<br>")


def build_table() -> str:
    lines = [
        "| " + " | ".join(HEADERS) + " |",
        "| :- | :--- | :--- | :--- | :--- |",
    ]

    with CSV_PATH.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        missing = [field for field in FIELD_NAMES if field not in (reader.fieldnames or [])]
        if missing:
            missing_text = ", ".join(missing)
            raise ValueError(f"CSV header is missing required columns: {missing_text}")

        for row in reader:
            cells = [escape_markdown_cell(row.get(field, "").strip()) for field in FIELD_NAMES]
            lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


def update_readme() -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    if START_MARKER not in readme or END_MARKER not in readme:
        raise ValueError("README.md is missing table markers.")

    start = readme.index(START_MARKER) + len(START_MARKER)
    end = readme.index(END_MARKER)
    table_block = "\n\n" + build_table() + "\n\n"
    updated = readme[:start] + table_block + readme[end:]
    README_PATH.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    update_readme()
