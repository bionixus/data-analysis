#!/usr/bin/env python3
"""Fill Details tab data into the second sheet of the New American Excel file."""

from pathlib import Path
from drug_comparison import (
    get_second_tab_sheet_names,
    parse_details_sheet,
    fill_details_sheet_to_excel,
)

NEW_PATH = "/Users/selim/Downloads/New American Hospital data.xlsx"
OLD_PATH = "/Users/selim/Documents/BioNixus Market Research Reports/GHD /Updated Old American.xlsx"

def main():
    if not Path(NEW_PATH).exists():
        print(f"File not found: {NEW_PATH}")
        return
    second_old, second_new = get_second_tab_sheet_names(OLD_PATH, NEW_PATH)
    sheet_name = second_new
    if not sheet_name:
        from drug_comparison import get_details_sheet_common
        _, sheet_name = get_details_sheet_common(OLD_PATH, NEW_PATH)
    if not sheet_name:
        print("Could not determine second sheet name.")
        return
    new_details = parse_details_sheet(NEW_PATH, sheet_name)
    if new_details.empty:
        print("No details data parsed from the second sheet.")
        return
    fill_details_sheet_to_excel(NEW_PATH, new_details, sheet_name=sheet_name)
    print(f"Filled {len(new_details)} drug rows into the second sheet of the New American file.")

if __name__ == "__main__":
    main()
