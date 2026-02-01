-- Analytics Dashboard — Database Schema (SQLite)
-- Aligned with DATABASE_DESIGN.md and dashboard layout (gauges, donuts, scatter, bars, area, timeline, pyramid, maps)

-- Optional chart registry
CREATE TABLE IF NOT EXISTS dashboard_charts (
    chart_key   TEXT PRIMARY KEY,
    title       TEXT,
    chart_type  TEXT NOT NULL,
    sort_order  INTEGER DEFAULT 0,
    created_at  TEXT DEFAULT (datetime('now'))
);

-- Progress rings / single KPIs
CREATE TABLE IF NOT EXISTS metrics (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key   TEXT NOT NULL,
    metric_key  TEXT NOT NULL,
    value       REAL NOT NULL,
    unit        TEXT DEFAULT '%',
    color_hex   TEXT,
    sort_order  INTEGER DEFAULT 0,
    updated_at  TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_metrics_chart ON metrics(chart_key);

-- Donuts / pies (ONE, TWO, THREE, FOUR)
CREATE TABLE IF NOT EXISTS distribution_segments (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key   TEXT NOT NULL,
    label       TEXT NOT NULL,
    value       REAL NOT NULL,
    color_hex   TEXT,
    sort_order  INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_distribution_chart ON distribution_segments(chart_key);

-- Scatter / trend (x, y, optional series)
CREATE TABLE IF NOT EXISTS scatter_points (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key   TEXT NOT NULL,
    x_value     REAL NOT NULL,
    y_value     REAL NOT NULL,
    series_name TEXT,
    sort_order  INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_scatter_chart ON scatter_points(chart_key);

-- Horizontal stacked bars (category × segment)
CREATE TABLE IF NOT EXISTS segmented_bar_data (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key       TEXT NOT NULL,
    category_label  TEXT NOT NULL,
    segment_label   TEXT NOT NULL,
    value           REAL NOT NULL,
    segment_order   INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_segmented_chart ON segmented_bar_data(chart_key);

-- Horizontal percentage bars (85%, 42%, 26%)
CREATE TABLE IF NOT EXISTS percentage_metrics (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key    TEXT NOT NULL,
    metric_label TEXT NOT NULL,
    value        REAL NOT NULL,
    color_hex    TEXT,
    sort_order   INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_percentage_chart ON percentage_metrics(chart_key);

-- Area / line time series
CREATE TABLE IF NOT EXISTS time_series_points (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key   TEXT NOT NULL,
    series_name TEXT NOT NULL,
    x_value     REAL NOT NULL,
    y_value     REAL NOT NULL,
    sort_order  INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_timeseries_chart ON time_series_points(chart_key);

-- Monthly bars (single or grouped)
CREATE TABLE IF NOT EXISTS monthly_series (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key   TEXT NOT NULL,
    month_label TEXT NOT NULL,
    value       REAL NOT NULL,
    series_name TEXT,
    sort_order  INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_monthly_chart ON monthly_series(chart_key);

-- Timeline events (2005, 2012, 2020)
CREATE TABLE IF NOT EXISTS timeline_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key   TEXT NOT NULL,
    event_year  INTEGER NOT NULL,
    label       TEXT,
    description TEXT,
    color_hex   TEXT,
    sort_order  INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_timeline_chart ON timeline_events(chart_key);

-- Pyramid levels (1–5)
CREATE TABLE IF NOT EXISTS pyramid_levels (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key    TEXT NOT NULL,
    level_label  TEXT NOT NULL,
    value        REAL NOT NULL,
    color_hex    TEXT,
    level_order  INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_pyramid_chart ON pyramid_levels(chart_key);

-- Choropleth (USA / Europe)
CREATE TABLE IF NOT EXISTS geo_data (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key    TEXT NOT NULL,
    region_code  TEXT NOT NULL,
    region_name  TEXT,
    value        REAL NOT NULL,
    updated_at   TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_geo_chart ON geo_data(chart_key);
