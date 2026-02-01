"""
Data Visualization Dashboard — Inspired by modern analytics UI.
Dark theme, pink/blue/green/purple palette, mobile-friendly.
Data loaded from dashboard.db when present; falls back to hardcoded sample data.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path

# Database path (next to this script)
DB_PATH = Path(__file__).parent / "dashboard.db"


@st.cache_data(ttl=60)
def load_dashboard_data():
    """Load all chart data from dashboard.db. Returns dict of DataFrames/lists; empty dict if DB missing."""
    if not DB_PATH.exists():
        return {}
    try:
        conn = sqlite3.connect(DB_PATH)
        out = {}
        # Gauges (gauge_1..4)
        df = pd.read_sql("SELECT chart_key, value, unit, color_hex FROM metrics WHERE chart_key LIKE 'gauge_%' ORDER BY sort_order", conn)
        if not df.empty:
            out["gauges"] = df
        # Donuts
        out["donut_main"] = pd.read_sql("SELECT label, value, color_hex FROM distribution_segments WHERE chart_key = 'donut_main' ORDER BY sort_order", conn)
        out["donut_secondary"] = pd.read_sql("SELECT label, value, color_hex FROM distribution_segments WHERE chart_key = 'donut_secondary' ORDER BY sort_order", conn)
        # Scatter
        out["scatter"] = pd.read_sql("SELECT x_value, y_value FROM scatter_points WHERE chart_key = 'scatter_trend' ORDER BY sort_order", conn)
        # Segmented bars
        out["segmented"] = pd.read_sql("SELECT category_label, segment_label, value, segment_order FROM segmented_bar_data WHERE chart_key = 'segmented_bars' ORDER BY category_label, segment_order", conn)
        # Percentage bars (horizontal)
        out["pct_bars"] = pd.read_sql("SELECT metric_label, value, color_hex FROM percentage_metrics WHERE chart_key = 'percentage_bars' ORDER BY sort_order", conn)
        # Area series
        out["area"] = pd.read_sql("SELECT series_name, x_value, y_value FROM time_series_points WHERE chart_key = 'area_series' ORDER BY series_name, sort_order", conn)
        # Pie
        out["pie"] = pd.read_sql("SELECT label, value, color_hex FROM distribution_segments WHERE chart_key = 'pie_main' ORDER BY sort_order", conn)
        # Monthly bars (single series)
        out["monthly"] = pd.read_sql("SELECT month_label, value FROM monthly_series WHERE chart_key = 'monthly_bars' AND (series_name IS NULL OR series_name = '') ORDER BY sort_order", conn)
        if out["monthly"].empty:
            out["monthly"] = pd.read_sql("SELECT month_label, value FROM monthly_series WHERE chart_key = 'monthly_bars' ORDER BY sort_order", conn)
        # Stacked bars
        out["stacked"] = pd.read_sql("SELECT month_label, value, series_name FROM monthly_series WHERE chart_key = 'stacked_bars' ORDER BY sort_order", conn)
        # Grouped bars
        out["grouped"] = pd.read_sql("SELECT month_label, value, series_name FROM monthly_series WHERE chart_key = 'grouped_bars' ORDER BY series_name, sort_order", conn)
        # Timeline
        out["timeline"] = pd.read_sql("SELECT event_year, label, color_hex FROM timeline_events WHERE chart_key = 'timeline_main' ORDER BY sort_order", conn)
        # Vertical %
        out["vertical_pct"] = pd.read_sql("SELECT metric_label, value, color_hex FROM percentage_metrics WHERE chart_key = 'vertical_pct' ORDER BY sort_order", conn)
        # Pyramid
        out["pyramid"] = pd.read_sql("SELECT level_label, value, color_hex FROM pyramid_levels WHERE chart_key = 'pyramid_main' ORDER BY level_order", conn)
        # Geo (map_usa)
        out["geo"] = pd.read_sql("SELECT region_code, region_name, value FROM geo_data WHERE chart_key = 'map_usa'", conn)
        conn.close()
        return out
    except Exception:
        return {}

# Palette from design
PINK = "#ec4899"
LIGHT_BLUE = "#7dd3fc"
LIGHT_GREEN = "#86efac"
PURPLE = "#a78bfa"
DARK_BLUE = "#1e3a5f"
BG_DARK = "#0f172a"
CARD_BG = "#1e293b"
GRID_COLOR = "#334155"
WHITE = "#f8fafc"
GREY = "#94a3b8"

COLORS = [PINK, LIGHT_BLUE, LIGHT_GREEN, PURPLE]

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Mobile-friendly dark theme CSS
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp { background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%); min-height: 100vh; }
    .block-container { padding: 1rem 1rem 2rem; max-width: 100%; }
    h1, h2, h3, p, span, label { color: #f8fafc !important; font-family: 'Inter', sans-serif !important; }
    .stMetric { background: rgba(30, 41, 59, 0.8); padding: 1rem; border-radius: 12px; border: 1px solid #334155; }
    .stMetric label { color: #94a3b8 !important; font-size: 0.7rem !important; text-transform: uppercase; }
    .stMetric [data-testid="stMetricValue"] { color: #f8fafc !important; }
    div[data-testid="stVerticalBlock"] > div { padding: 0.25rem 0; }
    [data-testid="stVerticalBlock"] > div { width: 100%; }
    @media (max-width: 768px) {
        .block-container { padding: 0.75rem; }
        [data-testid="column"] { width: 100% !important; min-width: 100% !important; }
        .js-plotly-plot .svg-container { width: 100% !important; }
    }
    section[data-testid="stSidebar"] { background: #0f172a; }
    section[data-testid="stSidebar"] .stMarkdown { color: #f8fafc; }
</style>
""", unsafe_allow_html=True)

# Plotly dark layout
def dark_layout(title=""):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=WHITE, size=11),
        title=dict(text=title, font=dict(size=14, color=WHITE)),
        margin=dict(t=40, r=20, b=40, l=40),
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False, tickfont=dict(color=GREY)),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False, tickfont=dict(color=GREY)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=WHITE)),
        showlegend=True,
    )

# Load data from DB (or empty dict → use fallbacks)
data = load_dashboard_data()

st.title("◉ Analytics Dashboard")
st.caption("Data visualization — responsive layout" + (" · loaded from database" if data else " · sample data"))

# --- Row 1: Progress rings ---
st.subheader("Key metrics")
gauges_df = data.get("gauges")
gauge_vals = gauges_df["value"].tolist() if gauges_df is not None and not gauges_df.empty else [80, 75, 50, 25]
_default_gauge_colors = [PINK, LIGHT_BLUE, GREY, WHITE]
gauge_colors = (gauges_df["color_hex"].fillna(PINK).tolist() if gauges_df is not None and not gauges_df.empty and "color_hex" in gauges_df.columns else _default_gauge_colors)[:4]
r1c1, r1c2, r1c3, r1c4 = st.columns(4)
for i, col in enumerate([r1c1, r1c2, r1c3, r1c4]):
    val = gauge_vals[i] if i < len(gauge_vals) else [80, 75, 50, 25][i]
    clr = gauge_colors[i] if i < len(gauge_colors) else [PINK, LIGHT_BLUE, GREY, WHITE][i]
    with col:
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=val, number=dict(suffix="%"),
            gauge=dict(axis=dict(range=[0, 100], tickcolor=WHITE), bar=dict(color=clr),
                       bgcolor=CARD_BG, borderwidth=0),
        ))
        fig.update_layout(dark_layout(""), height=180, margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True, config=dict(displayModeBar=False))

# --- Row 2: Donuts + Scatter ---
st.subheader("Distribution & trends")
c2a, c2b, c2c = st.columns([1, 1, 2])
df_d1 = data.get("donut_main")
labels1 = df_d1["label"].tolist() if df_d1 is not None and not df_d1.empty else ["ONE", "TWO", "THREE", "FOUR"]
values1 = df_d1["value"].tolist() if df_d1 is not None and not df_d1.empty else [25, 30, 25, 20]
colors1 = df_d1["color_hex"].fillna(PINK).tolist() if df_d1 is not None and "color_hex" in df_d1.columns else COLORS
with c2a:
    fig_donut = go.Figure(data=[go.Pie(labels=labels1, values=values1, hole=0.6, marker=dict(colors=colors1[: len(labels1)] or COLORS), textinfo="label")])
    fig_donut.update_layout(dark_layout(""), height=280, showlegend=False)
    st.plotly_chart(fig_donut, use_container_width=True, config=dict(displayModeBar=False))
df_d2 = data.get("donut_secondary")
labels2 = df_d2["label"].tolist() if df_d2 is not None and not df_d2.empty else ["ONE", "TWO", "Other"]
values2 = df_d2["value"].tolist() if df_d2 is not None and not df_d2.empty else [45, 35, 20]
colors2 = df_d2["color_hex"].fillna(PINK).tolist() if df_d2 is not None and "color_hex" in df_d2.columns else [PINK, LIGHT_BLUE, GREY]
with c2b:
    fig_donut2 = go.Figure(data=[go.Pie(labels=labels2, values=values2, hole=0.6, marker=dict(colors=colors2[: len(labels2)] or [PINK, LIGHT_BLUE, GREY]), textinfo="label")])
    fig_donut2.update_layout(dark_layout(""), height=280, showlegend=False)
    st.plotly_chart(fig_donut2, use_container_width=True, config=dict(displayModeBar=False))
df_scatter = data.get("scatter")
if df_scatter is not None and not df_scatter.empty:
    x_s, y_s = df_scatter["x_value"].values, df_scatter["y_value"].values
else:
    np.random.seed(42)
    x_s = np.linspace(0, 70, 30)
    y_s = 0.5 * x_s + np.random.randn(30) * 5
with c2c:
    fig_scatter = go.Figure(go.Scatter(x=x_s, y=y_s, mode="markers", marker=dict(color=PINK, size=10)))
    fig_scatter.update_layout(dark_layout("Scatter trend"), height=280)
    st.plotly_chart(fig_scatter, use_container_width=True, config=dict(displayModeBar=False))

# --- Row 3: Horizontal bars + Line/area ---
r3c1, r3c2 = st.columns(2)
df_seg = data.get("segmented")
if df_seg is not None and not df_seg.empty:
    categories = df_seg["category_label"].unique().tolist()
    seg_labels = df_seg["segment_label"].unique().tolist()
    fig_hbar = go.Figure()
    for i, seg in enumerate(seg_labels):
        sub = df_seg[df_seg["segment_label"] == seg]
        vals = [sub[sub["category_label"] == c]["value"].sum() for c in categories]
        fig_hbar.add_trace(go.Bar(y=categories, x=vals, orientation="h", marker_color=COLORS[i % len(COLORS)], name=seg, legendgroup="g"))
else:
    categories = ["A", "B", "C", "D"]
    seg_vals = np.random.randint(15, 35, (4, 4))
    fig_hbar = go.Figure()
    for i, color in enumerate(COLORS):
        fig_hbar.add_trace(go.Bar(y=categories, x=seg_vals[:, i], orientation="h", marker_color=color, name=f"Seg {i+1}", legendgroup="g"))
with r3c1:
    fig_hbar.update_layout(dark_layout("Segmented bars"), barmode="stack", height=220, xaxis=dict(range=[0, 120]))
    st.plotly_chart(fig_hbar, use_container_width=True, config=dict(displayModeBar=False))
df_pct = data.get("pct_bars")
if df_pct is not None and not df_pct.empty:
    fig_pct = go.Figure()
    for _, row in df_pct.iterrows():
        lbl, val = row["metric_label"], row["value"]
        clr = row.get("color_hex", PINK)
        fig_pct.add_trace(go.Bar(y=[lbl], x=[val], orientation="h", marker_color=clr, text=f"{int(val)}%", textposition="outside"))
else:
    fig_pct = go.Figure()
    for lbl, val, clr in [("Metric 1", 85, PINK), ("Metric 2", 42, LIGHT_BLUE), ("Metric 3", 26, LIGHT_GREEN)]:
        fig_pct.add_trace(go.Bar(y=[lbl], x=[val], orientation="h", marker_color=clr, text=f"{val}%", textposition="outside"))
with r3c2:
    fig_pct.update_layout(dark_layout("Percentage bars"), height=220, xaxis=dict(range=[0, 100]), showlegend=False)
    st.plotly_chart(fig_pct, use_container_width=True, config=dict(displayModeBar=False))

# --- Row 4: Line area chart ---
df_area = data.get("area")
if df_area is not None and not df_area.empty:
    fig_area = go.Figure()
    for name in df_area["series_name"].unique():
        sub = df_area[df_area["series_name"] == name].sort_values("x_value")
        clr = PINK if "1" in str(name) else LIGHT_BLUE
        fig_area.add_trace(go.Scatter(x=sub["x_value"], y=sub["y_value"], fill="tozeroy", name=name, line=dict(color=clr)))
else:
    x_line = np.linspace(0, 5, 50)
    y1 = 2 + np.sin(x_line) * 1.5
    y2 = 1.5 + np.cos(x_line * 1.2) * 1.2
    fig_area = go.Figure()
    fig_area.add_trace(go.Scatter(x=x_line, y=y1, fill="tozeroy", name="Series 1", line=dict(color=PINK)))
    fig_area.add_trace(go.Scatter(x=x_line, y=y2, fill="tozeroy", name="Series 2", line=dict(color=LIGHT_BLUE)))
fig_area.update_layout(dark_layout("Area chart"), height=280)
st.plotly_chart(fig_area, use_container_width=True, config=dict(displayModeBar=False))

# --- Row 5: Pie + Bar charts ---
st.subheader("Breakdown by category")
r5c1, r5c2, r5c3 = st.columns(3)
df_pie = data.get("pie")
pie_labels = df_pie["label"].tolist() if df_pie is not None and not df_pie.empty else ["ONE", "TWO", "THREE", "FOUR"]
pie_vals = df_pie["value"].tolist() if df_pie is not None and not df_pie.empty else [25, 30, 25, 20]
pie_colors = (df_pie["color_hex"].fillna(PINK).tolist() if df_pie is not None and "color_hex" in df_pie.columns else COLORS)[: len(pie_labels)]
with r5c1:
    fig_pie = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_vals, marker=dict(colors=pie_colors or COLORS))])
    fig_pie.update_layout(dark_layout("Pie"), height=280, legend=dict(orientation="h"))
    st.plotly_chart(fig_pie, use_container_width=True, config=dict(displayModeBar=False))
df_monthly = data.get("monthly")
if df_monthly is not None and not df_monthly.empty:
    months, m_vals = df_monthly["month_label"].tolist(), df_monthly["value"].tolist()
else:
    months, m_vals = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN"], [2, 3, 4, 3, 5, 5]
with r5c2:
    fig_bar = go.Figure(go.Bar(x=months, y=m_vals, marker_color=PINK))
    fig_bar.update_layout(dark_layout("Monthly"), height=280)
    st.plotly_chart(fig_bar, use_container_width=True, config=dict(displayModeBar=False))
df_stacked = data.get("stacked")
if df_stacked is not None and not df_stacked.empty and "series_name" in df_stacked.columns:
    fig_stacked = go.Figure()
    for (name, color) in zip(df_stacked["series_name"].unique(), COLORS):
        sub = df_stacked[df_stacked["series_name"] == name].sort_values("month_label")
        fig_stacked.add_trace(go.Bar(x=sub["month_label"].tolist(), y=sub["value"].tolist(), name=name, marker_color=color))
else:
    fig_stacked = go.Figure()
    for i, color in enumerate(COLORS):
        fig_stacked.add_trace(go.Bar(x=list(range(10)), y=np.random.randint(5, 15, 10), name=f"Cat {i+1}", marker_color=color))
with r5c3:
    fig_stacked.update_layout(dark_layout("Stacked"), barmode="stack", height=280)
    st.plotly_chart(fig_stacked, use_container_width=True, config=dict(displayModeBar=False))

# --- Row 6: Grouped bars + Timeline ---
st.subheader("Time series & timeline")
r6c1, r6c2 = st.columns(2)
df_grp = data.get("grouped")
if df_grp is not None and not df_grp.empty and "series_name" in df_grp.columns:
    months7 = df_grp["month_label"].unique().tolist()
    fig_grp = go.Figure()
    series_colors = [PINK, LIGHT_BLUE]
    for (name, color) in zip(df_grp["series_name"].unique(), series_colors):
        sub = df_grp[df_grp["series_name"] == name].sort_values("month_label")
        fig_grp.add_trace(go.Bar(x=sub["month_label"].tolist(), y=sub["value"].tolist(), name=name, marker_color=color))
else:
    months7 = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL"]
    fig_grp = go.Figure()
    fig_grp.add_trace(go.Bar(x=months7, y=[3, 2, 4, 3, 5, 4, 5], name="A", marker_color=PINK))
    fig_grp.add_trace(go.Bar(x=months7, y=[2, 3, 3, 4, 3, 5, 4], name="B", marker_color=LIGHT_BLUE))
with r6c1:
    fig_grp.update_layout(dark_layout("Grouped bars"), barmode="group", height=280)
    st.plotly_chart(fig_grp, use_container_width=True, config=dict(displayModeBar=False))
df_tl = data.get("timeline")
if df_tl is not None and not df_tl.empty:
    years = df_tl["event_year"].tolist()
    labels_tl = df_tl["label"].fillna(df_tl["event_year"].astype(str)).tolist()
    colors_tl = df_tl["color_hex"].fillna(PINK).tolist() if "color_hex" in df_tl.columns else [PINK, LIGHT_BLUE, LIGHT_GREEN]
else:
    years, labels_tl, colors_tl = [2005, 2012, 2020], ["2005", "2012", "2020"], [PINK, LIGHT_BLUE, LIGHT_GREEN]
with r6c2:
    fig_timeline = go.Figure()
    fig_timeline.add_trace(go.Scatter(x=years, y=[1] * len(years), mode="markers+lines", marker=dict(size=16, color=colors_tl[: len(years)]), line=dict(color=GREY, width=2)))
    for x, lbl in zip(years, labels_tl):
        fig_timeline.add_annotation(x=x, y=1, text=str(lbl), showarrow=False, yshift=25, font=dict(color=WHITE))
    fig_timeline.update_layout(dark_layout("Timeline"), height=280, yaxis=dict(visible=False, range=[0.8, 1.2]), xaxis=dict(range=[min(years) - 2, max(years) + 5]))
    st.plotly_chart(fig_timeline, use_container_width=True, config=dict(displayModeBar=False))

# --- Row 7: Vertical percentage bars + Pyramid ---
r7c1, r7c2 = st.columns(2)
df_vpct = data.get("vertical_pct")
if df_vpct is not None and not df_vpct.empty:
    vpct_labels = df_vpct["metric_label"].tolist()
    vpct_vals = df_vpct["value"].tolist()
    vpct_colors = df_vpct["color_hex"].fillna(PINK).tolist() if "color_hex" in df_vpct.columns else COLORS
else:
    vpct_labels, vpct_vals = ["ONE", "TWO", "THREE", "FOUR"], [50, 80, 35, 70]
    vpct_colors = COLORS
with r7c1:
    fig_vpct = go.Figure()
    fig_vpct.add_trace(go.Bar(x=vpct_labels, y=vpct_vals, marker_color=vpct_colors[: len(vpct_labels)] or COLORS, text=vpct_vals, textposition="outside"))
    fig_vpct.update_layout(dark_layout("Vertical %"), height=280, yaxis=dict(range=[0, 100]))
    st.plotly_chart(fig_vpct, use_container_width=True, config=dict(displayModeBar=False))
df_pyr = data.get("pyramid")
if df_pyr is not None and not df_pyr.empty:
    pyr_levels = df_pyr["level_label"].tolist()
    pyr_vals = df_pyr["value"].tolist()
    pyr_colors = df_pyr["color_hex"].fillna(PINK).tolist() if "color_hex" in df_pyr.columns else (COLORS + ["#eab308"])
else:
    pyr_levels, pyr_vals = ["1", "2", "3", "4", "5"], [100, 80, 60, 40, 20]
    pyr_colors = COLORS + ["#eab308"]
with r7c2:
    fig_pyramid = go.Figure()
    fig_pyramid.add_trace(go.Bar(y=pyr_levels, x=pyr_vals, orientation="h", marker_color=pyr_colors[: len(pyr_levels)] or (COLORS + ["#eab308"])))
    fig_pyramid.update_layout(dark_layout("Pyramid"), height=280, xaxis=dict(range=[0, max(pyr_vals) * 1.2 if pyr_vals else 120]))
    st.plotly_chart(fig_pyramid, use_container_width=True, config=dict(displayModeBar=False))

# --- Row 8: Maps (simplified choropleth) ---
st.subheader("Regional view")
df_geo = data.get("geo")
if df_geo is not None and not df_geo.empty and "region_code" in df_geo.columns and "value" in df_geo.columns:
    fig_usa = px.choropleth(
        df_geo, locations="region_code", locationmode="USA-states", color="value",
        scope="usa", color_continuous_scale=["#1e293b", LIGHT_BLUE, PINK],
    )
    fig_usa.update_layout(geo=dict(bgcolor="rgba(0,0,0,0)", lakecolor=CARD_BG), paper_bgcolor="rgba(0,0,0,0)", font=dict(color=WHITE), height=350, margin=dict(t=0))
    st.plotly_chart(fig_usa, use_container_width=True, config=dict(displayModeBar=False))
else:
    try:
        df_usa = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv")
        fig_usa = px.choropleth(
            df_usa, locations="code", locationmode="USA-states", color="total exports",
            scope="usa", color_continuous_scale=["#1e293b", LIGHT_BLUE, PINK],
        )
        fig_usa.update_layout(geo=dict(bgcolor="rgba(0,0,0,0)", lakecolor=CARD_BG), paper_bgcolor="rgba(0,0,0,0)", font=dict(color=WHITE), height=350, margin=dict(t=0))
        st.plotly_chart(fig_usa, use_container_width=True, config=dict(displayModeBar=False))
    except Exception:
        st.info("Map data unavailable. Connect to the internet or seed dashboard.db with geo_data.")
        fig_placeholder = go.Figure(go.Scatter(x=[], y=[]))
        fig_placeholder.update_layout(dark_layout("Map (connect or use DB)"), height=300)
        st.plotly_chart(fig_placeholder, use_container_width=True, config=dict(displayModeBar=False))

st.markdown("---")
st.caption("Dashboard inspired by modern analytics UI · Mobile-friendly layout")
