#!/usr/bin/env python3
"""
Create sample Excel files for GHD app (overview + details sheets).
Run from project root: python create_sample_data.py
Output: sample_data/old.xlsx, sample_data/new.xlsx
"""

import pandas as pd
from pathlib import Path

SAMPLE_DIR = Path(__file__).parent / "sample_data"
SAMPLE_DIR.mkdir(exist_ok=True)

# Overview: first sheet — header "Drug" + metric columns
OVERVIEW_METRICS = [
    "Total patients treated in the last 12 months",
    "Newly diagnosed patients received drug treatments in the last 12 months",
    "Follow up patients and received drug treatments in the last 12 months",
    "Active patients (Received treatment in the last 12 months)",
]
DRUGS_OVERVIEW = [
    "Genotropin (Pfizer)",
    "Norditropin (Novo Nordisk)",
    "Omnitrope (Sandoz)",
    "Saizen (Merck Serono)",
    "Ngenla (Pfizer)",
]


def write_overview_sheet(writer, sheet_name: str, drug_values: dict):
    """drug_values: list of (drug_name, [metric1, metric2, ...]) or dict drug -> list of values."""
    rows = [["Drug"] + OVERVIEW_METRICS]
    for drug, values in drug_values.items():
        rows.append([drug] + list(values))
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df.to_excel(writer, sheet_name=sheet_name, index=False)


def write_details_sheet(writer, sheet_name: str, rows_data: list):
    """rows_data: list of (type_label, metric1, metric2, ...). Section headers have type_label like 'pGHD', data rows have drug names."""
    # Header row: Type + metric names
    DETAIL_METRICS = [
        "Total patients treated in the last 12 months",
        "Newly diagnosed patients received drug treatments in the last 12 months",
        "Follow up patients and received drug treatments in the last 12 months",
    ]
    rows = [["Type"] + DETAIL_METRICS] + rows_data
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df.to_excel(writer, sheet_name=sheet_name, index=False)


def build_details_rows(old_period: bool):
    """Build details sheet rows: section headers (pGHD, etc.) and data rows with numbers."""
    mult = 1.0 if old_period else 0.85  # Slightly different for "new" period
    rows = []
    # pGHD section
    rows.append(["Pediatric Growth Hormone Deficiency (pGHD)", "", "", ""])
    rows.append(["Total patients (UNIQUE)", 120 * mult, 30 * mult, 90 * mult])
    rows.append(["Genotropin (Pfizer)", 35 * mult, 8 * mult, 27 * mult])
    rows.append(["Norditropin (Novo Nordisk)", 25 * mult, 6 * mult, 19 * mult])
    rows.append(["Omnitrope (Sandoz)", 20 * mult, 5 * mult, 15 * mult])
    rows.append(["Saizen (Merck Serono)", 28 * mult, 7 * mult, 21 * mult])
    rows.append(["Ngenla (Pfizer)", 12 * mult, 4 * mult, 8 * mult])
    # SGA section
    rows.append(["Small for Gestational Age (SGA)", "", "", ""])
    rows.append(["Total patients (UNIQUE)", 80 * mult, 15 * mult, 65 * mult])
    rows.append(["Genotropin (Pfizer)", 22 * mult, 4 * mult, 18 * mult])
    rows.append(["Norditropin (Novo Nordisk)", 18 * mult, 3 * mult, 15 * mult])
    rows.append(["Omnitrope (Sandoz)", 15 * mult, 3 * mult, 12 * mult])
    rows.append(["Saizen (Merck Serono)", 15 * mult, 3 * mult, 12 * mult])
    rows.append(["Ngenla (Pfizer)", 10 * mult, 2 * mult, 8 * mult])
    return rows


def main():
    # Old period (12 mo)
    old_overview = {
        "Genotropin (Pfizer)": [52, 12, 40, 52],
        "Norditropin (Novo Nordisk)": [0, 0, 0, 0],
        "Omnitrope (Sandoz)": [0, 0, 0, 0],
        "Saizen (Merck Serono)": [76, 18, 58, 76],
        "Ngenla (Pfizer)": [26, 6, 20, 26],
    }
    old_details = build_details_rows(old_period=True)

    # New period (6 mo)
    new_overview = {
        "Genotropin (Pfizer)": [48, 10, 38, 48],
        "Norditropin (Novo Nordisk)": [8, 2, 6, 8],
        "Omnitrope (Sandoz)": [12, 3, 9, 12],
        "Saizen (Merck Serono)": [65, 16, 49, 65],
        "Ngenla (Pfizer)": [23, 5, 18, 23],
    }
    new_details = build_details_rows(old_period=False)

    with pd.ExcelWriter(SAMPLE_DIR / "old.xlsx", engine="openpyxl") as w:
        write_overview_sheet(w, "Questionnaire - overview", old_overview)
        write_details_sheet(w, "Questionnaire - details", old_details)

    with pd.ExcelWriter(SAMPLE_DIR / "new.xlsx", engine="openpyxl") as w:
        write_overview_sheet(w, "Questionnaire - overview", new_overview)
        write_details_sheet(w, "Questionnaire - details", new_details)

    print(f"Created {SAMPLE_DIR / 'old.xlsx'} and {SAMPLE_DIR / 'new.xlsx'}")


if __name__ == "__main__":
    main()
