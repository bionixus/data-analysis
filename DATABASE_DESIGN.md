# Database Design — Analytics Dashboard

Design aligned with the dashboard layout (progress rings, donuts, scatter, segmented bars, percentage bars, area chart, pie, monthly/stacked/grouped bars, timeline, pyramid, maps).

---

## 1. Overview

- **Purpose:** Store all data backing the dashboard visualizations (gauges, donuts, bar charts, time series, timeline, pyramid, maps).
- **Scope:** One schema supports every chart type in the reference design.
- **Conventions:** Each chart is identified by a `chart_key`. Tables are normalized; optional `dashboard_charts` table links chart keys to titles and chart types.

---

## 2. Entity Relationship (High Level)

```
dashboard_charts (optional registry)
       │
       ├── metrics ..................... progress rings / single KPIs
       ├── distribution_segments ...... donuts / pies (label + value)
       ├── scatter_points ............. scatter (x, y, optional series)
       ├── segmented_bar_data ......... horizontal stacked bars (category × segment)
       ├── percentage_metrics ......... horizontal % bars (label + value)
       ├── time_series_points ......... area / line (x, y, series)
       ├── monthly_series ............. monthly bars (single or grouped)
       ├── timeline_events ............ timeline (year + label)
       ├── pyramid_levels ............. pyramid (level + value)
       └── geo_data ................... choropleth (region + value)
```

---

## 3. Table Definitions

### 3.1 `dashboard_charts` (optional)

Registry of charts for UI and data binding.

| Column       | Type         | Description                    |
|-------------|--------------|--------------------------------|
| chart_key   | TEXT PK      | Unique key (e.g. `gauge_1`, `donut_main`) |
| title       | TEXT         | Display title                  |
| chart_type   | TEXT         | `gauge`, `donut`, `pie`, `scatter`, `segmented_bar`, `percentage_bar`, `area`, `monthly_bar`, `stacked_bar`, `grouped_bar`, `timeline`, `pyramid`, `map` |
| sort_order  | INTEGER      | Order on dashboard             |
| created_at  | TEXT (ISO)   | Creation timestamp             |

---

### 3.2 `metrics` — Progress rings / single KPIs

One row per gauge or KPI.

| Column     | Type    | Description                |
|------------|---------|----------------------------|
| id         | INTEGER PK | Auto                       |
| chart_key  | TEXT    | Links to chart             |
| metric_key | TEXT    | e.g. `metric_1`, `metric_2` |
| value      | REAL    | Current value (e.g. 80 for 80%) |
| unit       | TEXT    | e.g. `%`, `count`          |
| color_hex  | TEXT    | e.g. `#ec4899`             |
| sort_order | INTEGER | Display order               |
| updated_at | TEXT    | Last update (ISO)           |

---

### 3.3 `distribution_segments` — Donuts / Pies

One row per segment (ONE, TWO, THREE, FOUR).

| Column     | Type    | Description     |
|------------|---------|-----------------|
| id         | INTEGER PK | Auto        |
| chart_key  | TEXT    | Chart id        |
| label      | TEXT    | Segment label   |
| value      | REAL    | Segment value   |
| color_hex  | TEXT    | Fill color      |
| sort_order | INTEGER | Order in chart   |

---

### 3.4 `scatter_points` — Scatter / trend

One row per point; optional series for multiple lines.

| Column      | Type    | Description   |
|-------------|---------|----------------|
| id          | INTEGER PK | Auto      |
| chart_key   | TEXT    | Chart id       |
| x_value     | REAL    | X              |
| y_value     | REAL    | Y              |
| series_name | TEXT    | Optional group |
| sort_order  | INTEGER | Point order    |

---

### 3.5 `segmented_bar_data` — Horizontal stacked bars

Category × segment (e.g. A/B/C/D × Seg1–4).

| Column        | Type    | Description    |
|---------------|---------|----------------|
| id            | INTEGER PK | Auto       |
| chart_key     | TEXT    | Chart id       |
| category_label| TEXT    | Row (e.g. A)   |
| segment_label | TEXT    | Segment name   |
| value         | REAL    | Segment value  |
| segment_order | INTEGER | Stack order    |

---

### 3.6 `percentage_metrics` — Horizontal % bars (85%, 42%, 26%)

| Column     | Type    | Description   |
|------------|---------|---------------|
| id         | INTEGER PK | Auto      |
| chart_key  | TEXT    | Chart id      |
| metric_label| TEXT   | e.g. Metric 1 |
| value      | REAL    | 0–100         |
| color_hex  | TEXT    | Bar color     |
| sort_order | INTEGER | Row order     |

---

### 3.7 `time_series_points` — Area / line charts

| Column      | Type    | Description   |
|-------------|---------|---------------|
| id          | INTEGER PK | Auto      |
| chart_key   | TEXT    | Chart id      |
| series_name | TEXT    | Series label  |
| x_value     | REAL    | X (e.g. time) |
| y_value     | REAL    | Y             |
| sort_order  | INTEGER | Point order   |

---

### 3.8 `monthly_series` — Monthly bars (single or grouped)

| Column      | Type    | Description        |
|-------------|---------|--------------------|
| id          | INTEGER PK | Auto           |
| chart_key   | TEXT    | Chart id           |
| month_label | TEXT    | JAN, FEB, …        |
| value       | REAL    | Bar value          |
| series_name | TEXT    | NULL = single bar; else grouped series |
| sort_order  | INTEGER | Order              |

---

### 3.9 `timeline_events` — Timeline (2005, 2012, 2020)

| Column     | Type    | Description   |
|------------|---------|---------------|
| id         | INTEGER PK | Auto      |
| chart_key  | TEXT    | Chart id      |
| event_year | INTEGER | Year           |
| label      | TEXT    | Short label    |
| description| TEXT    | Optional text  |
| color_hex  | TEXT    | Marker color   |
| sort_order | INTEGER | Order          |

---

### 3.10 `pyramid_levels` — Pyramid (levels 1–5)

| Column      | Type    | Description   |
|-------------|---------|---------------|
| id          | INTEGER PK | Auto      |
| chart_key   | TEXT    | Chart id      |
| level_label | TEXT    | 1, 2, 3, …    |
| value       | REAL    | Level width   |
| color_hex   | TEXT    | Level color   |
| level_order | INTEGER | Top to bottom |

---

### 3.11 `geo_data` — Choropleth (USA / Europe)

| Column      | Type    | Description   |
|-------------|---------|---------------|
| id          | INTEGER PK | Auto      |
| chart_key   | TEXT    | e.g. `map_usa`, `map_europe` |
| region_code | TEXT    | State/country code (e.g. CA, PL) |
| region_name | TEXT    | Display name  |
| value       | REAL    | Color value   |
| updated_at  | TEXT    | Last update   |

---

## 4. Chart Key Convention

Suggested keys for the reference layout:

| Chart           | chart_key        |
|-----------------|------------------|
| Progress ring 1 | gauge_1          |
| Progress ring 2 | gauge_2          |
| Progress ring 3 | gauge_3          |
| Progress ring 4 | gauge_4          |
| Donut (4 seg)   | donut_main       |
| Donut (2 seg)   | donut_secondary  |
| Scatter         | scatter_trend     |
| Segmented bars  | segmented_bars   |
| Percentage bars | percentage_bars  |
| Area chart      | area_series      |
| Pie             | pie_main         |
| Monthly bars    | monthly_bars     |
| Stacked bars    | stacked_bars    |
| Grouped bars    | grouped_bars    |
| Timeline        | timeline_main   |
| Vertical %      | vertical_pct    |
| Pyramid         | pyramid_main   |
| USA map         | map_usa        |
| Europe map      | map_europe     |

---

## 5. Indexes (for SQL implementation)

- All tables: index on `chart_key`.
- `time_series_points`: index on `(chart_key, series_name, sort_order)`.
- `monthly_series`: index on `(chart_key, series_name, sort_order)`.
- `geo_data`: index on `(chart_key, region_code)`.

---

## 6. Usage with Dashboard

1. Dashboard UI selects chart by `chart_key` (or by `dashboard_charts.sort_order`).
2. For each chart type, query the corresponding table filtered by `chart_key`.
3. Map `color_hex` to Plotly/dashboard palette when present.

This design supports the full set of visualizations from the reference picture and keeps the schema simple and extensible.

---

## 7. Quick start

```bash
# Create SQLite DB and load schema
sqlite3 dashboard.db < schema.sql

# Or create and seed in one step (Python)
python seed_dashboard_db.py
```

This creates `dashboard.db` with sample data for every chart type. The dashboard UI can later be wired to read from this DB instead of hardcoded values.
