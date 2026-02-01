# Excel Data Comparison Tool

Compare two Excel files (old vs new) and see what's added, removed, or changed.

## Drug Head-to-Head Comparison (American Hospital GHD data)

For drug-level comparison with visualizations:

```bash
python drug_comparison.py "/path/to/old.xlsx" "/path/to/new.xlsx"
```

**Output:**
- `drug_comparison_head_to_head.xlsx` – Head-to-head table with Old, New, and Change columns per drug
- `drug_total_comparison.png` – Bar chart: Old vs New total patients per drug
- `drug_change_by_drug.png` – Horizontal bar chart: Change (New − Old) per drug
- `drug_metrics_comparison.png` – Multi-metric comparison charts

**For visualizations**, install matplotlib:
```bash
pip install matplotlib
```

## Design-inspired Dashboard (mobile-friendly)

Run the analytics-style dashboard (dark theme, progress rings, donuts, bar/line/scatter charts, timeline, maps):

```bash
streamlit run dashboard_ui.py
```

Open **http://localhost:8501**. Use your browser’s device toolbar (e.g. Chrome DevTools) to preview the mobile layout.

## GHD Medication Calculator

Convert **drug name** and **monthly consumption** (vials/units) to **estimated number of patients**. Uses the same GHD drug list as the Drug Comparison project.

```bash
streamlit run medication_calculator.py
```

Open **http://localhost:8501**. Select a drug, enter monthly consumption and (optionally) consumption per patient per month; the app shows the estimated patient count.

## Live Dashboard (GHD Drug Comparison)

Run the interactive Streamlit dashboard:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open **http://localhost:8501** in your browser. The dashboard includes:
- **Demo (sample data)** — bundled sample Excel files so the app works out of the box and on [Streamlit Community Cloud](https://share.streamlit.io)
- Other hospitals (e.g. American Hospital) — use your local Excel paths or **Custom upload** in the sidebar
- Interactive Plotly charts (zoom, hover, pan), summary metrics, head-to-head data table, Overview + Details tabs

**Deploy on Streamlit Community Cloud:** Push this repo to GitHub, then at [share.streamlit.io](https://share.streamlit.io) create a new app from the repo with **Main file path:** `app.py`. The default **Demo (sample data)** option uses files in `sample_data/` so the deployed app has data without local files.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

1. **Place your Excel files** in this directory (e.g. `old_data.xlsx`, `new_data.xlsx`).

2. **Run the comparison:**

   ```bash
   python compare_excel.py old_data.xlsx new_data.xlsx
   ```

3. **Output:** Results are saved to `comparison_results.xlsx` with sheets:
   - **Added** – Rows only in the new file
   - **Removed** – Rows only in the old file
   - **Changed** – Rows in both with different values
   - **Unchanged** – Rows identical in both files

### Options

- **Match by a key column** (e.g. ID) instead of row order:

  ```bash
  python compare_excel.py old.xlsx new.xlsx --key ID
  ```

  For multiple key columns:

  ```bash
  python compare_excel.py old.xlsx new.xlsx --key ID,Name
  ```

- **Specific sheet** (by name or index):

  ```bash
  python compare_excel.py old.xlsx new.xlsx --sheet "Sheet2"
  ```

## Python / Jupyter

You can also import and use the comparison logic directly:

```python
from compare_excel import load_excel, compare_excel_files

result = compare_excel_files("old.xlsx", "new.xlsx", key_columns=["ID"])
print(result["summary"])
# result["added"], result["removed"], result["changed"], result["unchanged"]
```
