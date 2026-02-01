#!/usr/bin/env python3
"""
Read Growth Hormone AJCH Excel file, sum consumption by drug, convert to patients.
Uses same vials-per-patient defaults as medication_calculator.py.
"""

import pandas as pd
from pathlib import Path

# Match medication_calculator defaults (pens/cartridges per patient per month)
# Ngenla: 1 pen = 1 month; rest: 2 pens or cartridges per month
VIALS_PER_PATIENT_MONTH = {
    "Genotropin (Pfizer)": 2.0,
    "Norditropin (Novo Nordisk)": 2.0,
    "Nutropin (Genentech)": 2.0,
    "Omnitrope (Sandoz)": 2.0,
    "Saizen (Merck Serono)": 2.4,
    "Humatrope (Eli Lilly)": 2.0,
    "Ngenla (Pfizer)": 1.0,
    "Zomacton (Ferring)": 2.0,
}

# Map Excel "Item Description" substrings to canonical drug name
ITEM_TO_DRUG = [
    ("GENOTROPIN", "Genotropin (Pfizer)"),
    ("Genotropin", "Genotropin (Pfizer)"),
    ("SAIZEN", "Saizen (Merck Serono)"),
    ("Saizen", "Saizen (Merck Serono)"),
    ("NGENLA", "Ngenla (Pfizer)"),
    ("Ngenla", "Ngenla (Pfizer)"),
    ("OMNITROPE", "Omnitrope (Sandoz)"),
    ("Omnitrope", "Omnitrope (Sandoz)"),
    ("NORDITROPIN", "Norditropin (Novo Nordisk)"),
    ("Norditropin", "Norditropin (Novo Nordisk)"),
    ("NUTROPIN", "Nutropin (Genentech)"),
    ("Humatrope", "Humatrope (Eli Lilly)"),
    ("Zomacton", "Zomacton (Ferring)"),
]


def map_item_to_drug(desc: str) -> str | None:
    if pd.isna(desc) or not str(desc).strip():
        return None
    s = str(desc).strip()
    for keyword, drug in ITEM_TO_DRUG:
        if keyword in s:
            return drug
    return None


def main(filepath: str, months: float = 6.0):
    path = Path(filepath)
    if not path.exists():
        print(f"File not found: {filepath}")
        return

    df = pd.read_excel(path, sheet_name=0, header=0)
    df.columns = [str(c).strip() for c in df.columns]

    item_col = None
    qty_col = None
    for c in df.columns:
        if "item" in c.lower() or "description" in c.lower():
            item_col = c
        if "qty" in c.lower() or "delivered" in c.lower():
            qty_col = c
    if not item_col or not qty_col:
        print("Could not find Item Description and Qty Delivered columns.")
        return

    df["_drug"] = df[item_col].apply(map_item_to_drug)
    df = df.dropna(subset=["_drug"])
    df[qty_col] = pd.to_numeric(df[qty_col], errors="coerce").fillna(0)

    totals = df.groupby("_drug", as_index=False).agg({qty_col: "sum"})
    totals.columns = ["Drug", "Total vials"]

    print("=" * 60)
    print("Growth Hormone — AJCH 07 to 12 - 2025")
    print("=" * 60)
    print(f"Period: {months} months")
    print()

    total_vials_all = 0
    total_patients_all = 0.0

    print(f"{'Drug':<30} {'Total vials':>12} {'Vials/pat/mo':>12} {'Patients':>10}")
    print("-" * 66)

    for _, row in totals.iterrows():
        drug = row["Drug"]
        vials = row["Total vials"]
        vpp = VIALS_PER_PATIENT_MONTH.get(drug, 1.0)
        patients = vials / (vpp * months) if months > 0 and vpp > 0 else 0
        total_vials_all += vials
        total_patients_all += patients
        print(f"{drug:<30} {vials:>12.0f} {vpp:>12.1f} {patients:>10.1f}")

    print("-" * 66)
    print(f"{'TOTAL (sum of vials)':<30} {total_vials_all:>12.0f} {'—':>12} {'—':>10}")
    print(f"{'TOTAL patient-equivalents':<30} {'—':>12} {'—':>12} {total_patients_all:>10.1f}")
    print()
    print("Patient-equivalents = total vials ÷ (vials per patient per month × number of months).")
    print("Total patient-equivalents is the sum of per-drug estimates (not unique patients).")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "/Users/selim/Desktop/Growth Hormone -AJCH 07 to 12 - 2025.xlsx"
    months = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0
    main(path, months)
