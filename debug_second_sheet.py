#!/usr/bin/env python3
"""Print raw structure of the second sheet so we can fix the parser."""

import pandas as pd
from pathlib import Path

NEW_PATH = "/Users/selim/Downloads/New American Hospital data.xlsx"

def main():
    if not Path(NEW_PATH).exists():
        print(f"File not found: {NEW_PATH}")
        return
    xl = pd.ExcelFile(NEW_PATH)
    print("Sheet names:", xl.sheet_names)
    if len(xl.sheet_names) < 2:
        print("Only one sheet.")
        return
    name = xl.sheet_names[1]
    df = pd.read_excel(NEW_PATH, sheet_name=name, header=None)
    print(f"\nSecond sheet: '{name}'")
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print("\nFirst 25 rows (all columns), raw values:")
    pd.set_option("display.max_columns", 20)
    pd.set_option("display.width", 200)
    pd.set_option("display.max_colwidth", 40)
    print(df.head(25).to_string())
    print("\n--- Column dtypes ---")
    print(df.dtypes)

if __name__ == "__main__":
    main()
