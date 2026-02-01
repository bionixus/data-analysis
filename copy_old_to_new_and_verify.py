#!/usr/bin/env python3
"""
Copy Old American details to New American second sheet, then re-read and print values to verify.
"""
import pandas as pd
from pathlib import Path
from drug_comparison import (
    get_second_tab_sheet_names,
    get_details_sheet_row_col_map,
    parse_details_sheet,
    details_old_to_new_columns,
    fill_details_sheet_to_excel,
)

OLD_PATH = "/Users/selim/Documents/BioNixus Market Research Reports/GHD /Updated Old American.xlsx"
NEW_PATH = "/Users/selim/Downloads/New American Hospital data.xlsx"

def main():
    if not Path(OLD_PATH).exists():
        print("Old file not found:", OLD_PATH)
        return
    if not Path(NEW_PATH).exists():
        print("New file not found:", NEW_PATH)
        return

    so, sn = get_second_tab_sheet_names(OLD_PATH, NEW_PATH)
    sheet_name = sn or "Questionnaire - details"
    print("Sheet name:", sheet_name)

    old_details = parse_details_sheet(OLD_PATH, so or "Questionnaire - details")
    print("Old details shape:", old_details.shape)
    print("Old details sample (first row, first 3 cols):")
    if not old_details.empty:
        first_key = old_details.index[0]
        for c in list(old_details.columns)[:3]:
            print(f"  {c}: {old_details.loc[first_key, c]}")

    old_renamed = details_old_to_new_columns(old_details)
    print("Old renamed columns:", list(old_renamed.columns))

    print("\nWriting to New file...")
    try:
        n_written = fill_details_sheet_to_excel(NEW_PATH, old_renamed, sheet_name=sheet_name)
        print("Cells written:", n_written)
    except Exception as e:
        print("Write failed:", e)
        return

    # Read one cell with openpyxl to verify write
    import openpyxl
    wb = openpyxl.load_workbook(NEW_PATH, data_only=True)
    ws = wb[sheet_name]
    # First data row for Genotropin (Pfizer) is Excel row 7, first metric column is B=2
    cell_val = ws.cell(row=7, column=2).value
    print("Excel cell(7,2) after write:", cell_val)
    wb.close()

    print("\nRe-reading New file second sheet with pandas...")
    new_after = parse_details_sheet(NEW_PATH, sheet_name)
    print("New details shape after write:", new_after.shape)
    if not new_after.empty:
        print("New details sample (first row, first 3 cols):")
        first_key = new_after.index[0]
        for c in list(new_after.columns)[:3]:
            print(f"  {c}: {new_after.loc[first_key, c]}")
        print("Sum of first numeric column:", new_after.iloc[:, 0].sum())
    else:
        print("New details is empty after read!")

if __name__ == "__main__":
    main()
