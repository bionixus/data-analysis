#!/usr/bin/env python3
"""
Compare two Excel files (old vs new) and output differences.
"""

import pandas as pd
import sys
from pathlib import Path


def load_excel(filepath: str, sheet: int | str = 0) -> pd.DataFrame:
    """Load an Excel file into a DataFrame."""
    return pd.read_excel(filepath, sheet_name=sheet)


def compare_excel_files(
    old_file: str,
    new_file: str,
    key_columns: list[str] | None = None,
    sheet: int | str = 0,
) -> dict:
    """
    Compare two Excel files and return differences.
    
    Args:
        old_file: Path to the old Excel file
        new_file: Path to the new Excel file
        key_columns: Optional list of columns to use for matching rows (e.g. ["ID"])
                     If None, rows are matched by index.
        sheet: Sheet name or index (default: first sheet)
    
    Returns:
        Dict with 'added', 'removed', 'changed', and 'unchanged' DataFrames
    """
    df_old = load_excel(old_file, sheet)
    df_new = load_excel(new_file, sheet)
    
    if key_columns is None:
        # Match by index
        key_columns = []
        use_index = True
    else:
        use_index = False
        for col in key_columns:
            if col not in df_old.columns or col not in df_new.columns:
                raise ValueError(f"Key column '{col}' not found in both files")
    
    if use_index:
        # Compare by row index
        min_len = min(len(df_old), len(df_new))
        max_len = max(len(df_old), len(df_new))
        
        # Rows only in new (added)
        added = df_new.iloc[min_len:] if len(df_new) > min_len else pd.DataFrame()
        
        # Rows only in old (removed)
        removed = df_old.iloc[min_len:] if len(df_old) > min_len else pd.DataFrame()
        
        # Compare overlapping rows for changes
        df_old_sub = df_old.iloc[:min_len].reset_index(drop=True)
        df_new_sub = df_new.iloc[:min_len].reset_index(drop=True)
        
        # Use only common columns (files may have different column structure)
        common_cols = [c for c in df_old_sub.columns if c in df_new_sub.columns]
        
        if not common_cols:
            # No common columns - treat all overlapping rows as changed
            changed = pd.concat(
                [df_old_sub.add_suffix("_old"), df_new_sub.add_suffix("_new")],
                axis=1,
            )
            unchanged = pd.DataFrame()
        else:
            # Compare only common columns, handle NaN correctly
            old_vals = df_old_sub[common_cols].fillna("__NA__")
            new_vals = df_new_sub[common_cols].fillna("__NA__")
            diff_mask = (old_vals != new_vals).any(axis=1)
            
            changed_old = df_old_sub.loc[diff_mask]
            changed_new = df_new_sub.loc[diff_mask]
            unchanged = df_old_sub.loc[~diff_mask]
            # Combine for display: add suffixes (use common cols for alignment)
            if len(changed_old) == 0:
                changed = pd.DataFrame()
            else:
                changed = pd.concat(
                    [changed_old[common_cols].add_suffix("_old").reset_index(drop=True),
                     changed_new[common_cols].add_suffix("_new").reset_index(drop=True)],
                    axis=1,
                )
    else:
        # Compare by key columns
        keys_old = set(df_old[key_columns].drop_duplicates().apply(tuple, axis=1))
        keys_new = set(df_new[key_columns].drop_duplicates().apply(tuple, axis=1))
        
        added_keys = keys_new - keys_old
        removed_keys = keys_old - keys_new
        common_keys = keys_old & keys_new
        
        # Build key lookup
        df_old["_key"] = df_old[key_columns].apply(tuple, axis=1)
        df_new["_key"] = df_new[key_columns].apply(tuple, axis=1)
        
        added = df_new[df_new["_key"].isin(added_keys)].drop(columns=["_key"])
        removed = df_old[df_old["_key"].isin(removed_keys)].drop(columns=["_key"])
        
        # Find changed rows among common keys
        changed_rows = []
        unchanged_rows = []
        
        for key in common_keys:
            row_old = df_old[df_old["_key"] == key].drop(columns=["_key"])
            row_new = df_new[df_new["_key"] == key].drop(columns=["_key"])
            
            compare_cols = [c for c in row_old.columns if c in row_new.columns]
            if not row_old[compare_cols].equals(row_new[compare_cols]):
                merged = pd.concat(
                    [row_old.add_suffix("_old"), row_new.add_suffix("_new")],
                    axis=1,
                )
                changed_rows.append(merged)
            else:
                unchanged_rows.append(row_old)
        
        changed = pd.concat(changed_rows, ignore_index=True) if changed_rows else pd.DataFrame()
        unchanged = pd.concat(unchanged_rows, ignore_index=True) if unchanged_rows else pd.DataFrame()
    
    return {
        "added": added,
        "removed": removed,
        "changed": changed,
        "unchanged": unchanged,
        "summary": {
            "old_rows": len(df_old),
            "new_rows": len(df_new),
            "added_rows": len(added),
            "removed_rows": len(removed),
            "changed_rows": len(changed),
            "unchanged_rows": len(unchanged),
        },
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python compare_excel.py <old_file.xlsx> <new_file.xlsx> [--key ID,Name] [--sheet 0]")
        print("\nPlace your Excel files in this directory, then run:")
        print("  python compare_excel.py old_data.xlsx new_data.xlsx")
        print("\nOptional: Use --key to specify columns for row matching (e.g. --key ID)")
        sys.exit(1)
    
    old_file = sys.argv[1]
    new_file = sys.argv[2]
    key_columns = None
    sheet = 0
    
    # Parse optional args
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--key" and i + 1 < len(sys.argv):
            key_columns = [k.strip() for k in sys.argv[i + 1].split(",")]
            i += 2
        elif sys.argv[i] == "--sheet" and i + 1 < len(sys.argv):
            try:
                sheet = int(sys.argv[i + 1])
            except ValueError:
                sheet = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    if not Path(old_file).exists():
        print(f"Error: Old file not found: {old_file}")
        sys.exit(1)
    if not Path(new_file).exists():
        print(f"Error: New file not found: {new_file}")
        sys.exit(1)
    
    result = compare_excel_files(old_file, new_file, key_columns=key_columns, sheet=sheet)
    
    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    s = result["summary"]
    print(f"Old file rows:  {s['old_rows']}")
    print(f"New file rows:  {s['new_rows']}")
    print(f"Added rows:     {s['added_rows']}")
    print(f"Removed rows:   {s['removed_rows']}")
    print(f"Changed rows:   {s['changed_rows']}")
    print(f"Unchanged rows: {s['unchanged_rows']}")
    print("=" * 60)
    
    # Save results to Excel
    output_file = "comparison_results.xlsx"
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        result["added"].to_excel(writer, sheet_name="Added", index=False)
        result["removed"].to_excel(writer, sheet_name="Removed", index=False)
        result["changed"].to_excel(writer, sheet_name="Changed", index=False)
        result["unchanged"].to_excel(writer, sheet_name="Unchanged", index=False)
    
    print(f"\nDetailed results saved to: {output_file}")
    print("  - Added:   Rows that appear only in the new file")
    print("  - Removed: Rows that appear only in the old file")
    print("  - Changed: Rows that exist in both but have different values")
    print("  - Unchanged: Rows that are identical in both files")


if __name__ == "__main__":
    main()
