#!/usr/bin/env python3
"""
Create dashboard SQLite DB from schema and seed with sample data
matching the dashboard layout (gauges, donuts, scatter, bars, timeline, pyramid).
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "dashboard.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

COLORS = ["#ec4899", "#7dd3fc", "#86efac", "#a78bfa", "#eab308", "#94a3b8"]


def create_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_PATH.read_text())
    conn.commit()
    return conn


def seed(conn: sqlite3.Connection):
    c = conn.cursor()

    # Chart registry (optional)
    charts = [
        ("gauge_1", "Metric 1", "gauge", 1),
        ("gauge_2", "Metric 2", "gauge", 2),
        ("gauge_3", "Metric 3", "gauge", 3),
        ("gauge_4", "Metric 4", "gauge", 4),
        ("donut_main", "Distribution", "donut", 5),
        ("donut_secondary", "Distribution 2", "donut", 6),
        ("scatter_trend", "Scatter trend", "scatter", 7),
        ("segmented_bars", "Segmented bars", "segmented_bar", 8),
        ("percentage_bars", "Percentage bars", "percentage_bar", 9),
        ("area_series", "Area chart", "area", 10),
        ("pie_main", "Pie", "pie", 11),
        ("monthly_bars", "Monthly", "monthly_bar", 12),
        ("stacked_bars", "Stacked", "stacked_bar", 13),
        ("grouped_bars", "Grouped bars", "grouped_bar", 14),
        ("timeline_main", "Timeline", "timeline", 15),
        ("vertical_pct", "Vertical %", "percentage_bar", 16),
        ("pyramid_main", "Pyramid", "pyramid", 17),
        ("map_usa", "USA", "map", 18),
    ]
    c.executemany(
        "INSERT OR REPLACE INTO dashboard_charts (chart_key, title, chart_type, sort_order) VALUES (?,?,?,?)",
        charts,
    )

    # Gauges: 80, 75, 50, 25
    for i, (val, color) in enumerate([(80, COLORS[0]), (75, COLORS[1]), (50, COLORS[4]), (25, "#f8fafc")]):
        c.execute(
            "INSERT INTO metrics (chart_key, metric_key, value, unit, color_hex, sort_order) VALUES (?,?,?,?,?,?)",
            (f"gauge_{i+1}", f"metric_{i+1}", val, "%", color, i),
        )

    # Donut main: ONE, TWO, THREE, FOUR
    for i, (label, val) in enumerate([("ONE", 25), ("TWO", 30), ("THREE", 25), ("FOUR", 20)]):
        c.execute(
            "INSERT INTO distribution_segments (chart_key, label, value, color_hex, sort_order) VALUES (?,?,?,?,?)",
            ("donut_main", label, val, COLORS[i % 4], i),
        )
    # Donut secondary: ONE, TWO, Other
    for i, (label, val) in enumerate([("ONE", 45), ("TWO", 35), ("Other", 20)]):
        c.execute(
            "INSERT INTO distribution_segments (chart_key, label, value, color_hex, sort_order) VALUES (?,?,?,?,?)",
            ("donut_secondary", label, val, [COLORS[0], COLORS[1], COLORS[4]][i], i),
        )

    # Scatter (sample trend)
    import math
    for i in range(30):
        x = i * 70 / 29
        y = 0.5 * x + 5 * math.sin(i * 0.3)
        c.execute(
            "INSERT INTO scatter_points (chart_key, x_value, y_value, sort_order) VALUES (?,?,?,?)",
            ("scatter_trend", x, y, i),
        )

    # Segmented bars: A,B,C,D × 4 segments
    cats = ["A", "B", "C", "D"]
    for ci, cat in enumerate(cats):
        for si in range(4):
            v = 15 + (ci + si) * 5
            c.execute(
                "INSERT INTO segmented_bar_data (chart_key, category_label, segment_label, value, segment_order) VALUES (?,?,?,?,?)",
                ("segmented_bars", cat, f"Seg {si+1}", v, si),
            )

    # Percentage bars: 85, 42, 26
    for i, (label, val) in enumerate([("Metric 1", 85), ("Metric 2", 42), ("Metric 3", 26)]):
        c.execute(
            "INSERT INTO percentage_metrics (chart_key, metric_label, value, color_hex, sort_order) VALUES (?,?,?,?,?)",
            ("percentage_bars", label, val, [COLORS[0], COLORS[1], COLORS[2]][i], i),
        )

    # Area series (two series, 50 points)
    for i in range(50):
        x = i * 5 / 49
        c.execute(
            "INSERT INTO time_series_points (chart_key, series_name, x_value, y_value, sort_order) VALUES (?,?,?,?,?)",
            ("area_series", "Series 1", x, 2 + math.sin(x) * 1.5, i),
        )
        c.execute(
            "INSERT INTO time_series_points (chart_key, series_name, x_value, y_value, sort_order) VALUES (?,?,?,?,?)",
            ("area_series", "Series 2", x, 1.5 + math.cos(x * 1.2) * 1.2, i),
        )

    # Pie (same as donut_main)
    for i, (label, val) in enumerate([("ONE", 25), ("TWO", 30), ("THREE", 25), ("FOUR", 20)]):
        c.execute(
            "INSERT INTO distribution_segments (chart_key, label, value, color_hex, sort_order) VALUES (?,?,?,?,?)",
            ("pie_main", label, val, COLORS[i % 4], i),
        )

    # Monthly bars: JAN–JUN
    for i, (m, v) in enumerate([("JAN", 2), ("FEB", 3), ("MAR", 4), ("APR", 3), ("MAY", 5), ("JUN", 5)]):
        c.execute(
            "INSERT INTO monthly_series (chart_key, month_label, value, sort_order) VALUES (?,?,?,?)",
            ("monthly_bars", m, v, i),
        )

    # Stacked bars: 10 x categories, 4 series
    import random
    random.seed(42)
    for x in range(10):
        for si in range(4):
            c.execute(
                "INSERT INTO monthly_series (chart_key, month_label, value, series_name, sort_order) VALUES (?,?,?,?,?)",
                ("stacked_bars", str(x), random.randint(5, 15), f"Cat {si+1}", x * 4 + si),
            )

    # Grouped bars: JAN–JUL, series A and B
    months7 = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL"]
    ya = [3, 2, 4, 3, 5, 4, 5]
    yb = [2, 3, 3, 4, 3, 5, 4]
    for i, m in enumerate(months7):
        c.execute(
            "INSERT INTO monthly_series (chart_key, month_label, value, series_name, sort_order) VALUES (?,?,?,?,?)",
            ("grouped_bars", m, ya[i], "A", i),
        )
        c.execute(
            "INSERT INTO monthly_series (chart_key, month_label, value, series_name, sort_order) VALUES (?,?,?,?,?)",
            ("grouped_bars", m, yb[i], "B", len(months7) + i),
        )

    # Timeline: 2005, 2012, 2020
    for i, (yr, label) in enumerate([(2005, "2005"), (2012, "2012"), (2020, "2020")]):
        c.execute(
            "INSERT INTO timeline_events (chart_key, event_year, label, color_hex, sort_order) VALUES (?,?,?,?,?)",
            ("timeline_main", yr, label, [COLORS[0], COLORS[1], COLORS[2]][i], i),
        )

    # Vertical %: ONE 50, TWO 80, THREE 35, FOUR 70
    for i, (label, val) in enumerate([("ONE", 50), ("TWO", 80), ("THREE", 35), ("FOUR", 70)]):
        c.execute(
            "INSERT INTO percentage_metrics (chart_key, metric_label, value, color_hex, sort_order) VALUES (?,?,?,?,?)",
            ("vertical_pct", label, val, COLORS[i % 4], i),
        )

    # Pyramid: levels 1–5, values 100,80,60,40,20
    for i, (label, val) in enumerate([("1", 100), ("2", 80), ("3", 60), ("4", 40), ("5", 20)]):
        c.execute(
            "INSERT INTO pyramid_levels (chart_key, level_label, value, color_hex, level_order) VALUES (?,?,?,?,?)",
            ("pyramid_main", label, val, COLORS[i % 5] if i < 4 else COLORS[4], i),
        )

    # Geo: minimal sample (a few states)
    for code, name, val in [("CA", "California", 100), ("TX", "Texas", 80), ("NY", "New York", 60), ("FL", "Florida", 70)]:
        c.execute(
            "INSERT INTO geo_data (chart_key, region_code, region_name, value) VALUES (?,?,?,?)",
            ("map_usa", code, name, val),
        )

    conn.commit()


def main():
    Path(DB_PATH).unlink(missing_ok=True)
    conn = create_db()
    seed(conn)
    conn.close()
    print(f"Created and seeded: {DB_PATH}")


if __name__ == "__main__":
    main()
