"""
McKinsey Elite style — single source of truth for all dashboards.
Import this module in any hospital comparison app to apply the same fonts, colors, and layout.
"""

from drug_comparison import MCKINSEY_STYLE

# Alias for charts and layout
M = MCKINSEY_STYLE

# --- Fonts (use everywhere: Plotly titles, labels, Streamlit) ---
FONT_FAMILY = "Helvetica Neue, Arial, sans-serif"
FONT_SIZE_BODY = 11
FONT_SIZE_TICK = 10
FONT_SIZE_TITLE = 14

# Plotly chart title font dict (McKinsey blue)
CHART_TITLE_FONT = dict(size=FONT_SIZE_TITLE, color=M["navy"], family=FONT_FAMILY)

# Pie chart text and marker (McKinsey blue for labels/percent)
PIE_TEXTFONT = dict(size=FONT_SIZE_BODY, color=M["navy"], family=FONT_FAMILY)
PIE_MARKER_LINE = dict(color=M["bg"], width=1.5)

# Palette for multi-series (e.g. pie slices, one color per drug) — same order as bar charts
PIE_PALETTE = [
    M["navy"],
    M["teal"],
    M["slate"],
    M["charcoal"],
    M["accent_blue"],
    M["accent_teal"],
]

# --- Plotly layout (use with fig.update_layout(**PLOTLY_LAYOUT)) — chart text in McKinsey blue ---
PLOTLY_LAYOUT = {
    "paper_bgcolor": M["bg"],
    "plot_bgcolor": "#fafafa",
    "font": {"family": FONT_FAMILY, "size": FONT_SIZE_BODY, "color": M["navy"]},
    "margin": {"t": 50, "r": 30, "b": 60, "l": 60},
    "xaxis": {
        "showgrid": True,
        "gridcolor": M["grid"],
        "zeroline": False,
        "showline": True,
        "linecolor": M["grid"],
        "tickfont": {"size": FONT_SIZE_TICK, "color": M["navy"]},
        "title_font": {"color": M["navy"]},
    },
    "yaxis": {
        "showgrid": True,
        "gridcolor": M["grid"],
        "zeroline": False,
        "showline": True,
        "linecolor": M["grid"],
        "tickfont": {"size": FONT_SIZE_TICK, "color": M["navy"]},
        "title_font": {"color": M["navy"]},
    },
    "legend": {
        "orientation": "h",
        "yanchor": "bottom",
        "y": 1.02,
        "xanchor": "right",
        "x": 1,
        "bgcolor": "rgba(0,0,0,0)",
        "font": {"color": M["navy"]},
    },
    "hoverlabel": {
        "bgcolor": M["bg"],
        "font_size": FONT_SIZE_BODY,
        "bordercolor": M["grid"],
        "font": {"family": FONT_FAMILY, "color": M["navy"]},
    },
}

# Pie/donut charts: extra top margin so title and legend don't feel cramped above the ring
PLOTLY_LAYOUT_PIE = {
    **PLOTLY_LAYOUT,
    "margin": {**PLOTLY_LAYOUT["margin"], "t": 100},
}
# Title padding for pie charts (more space below title before the chart)
PIE_TITLE_PAD = dict(t=15, b=45)

# --- Streamlit CSS (use with st.markdown(STREAMLIT_CSS, unsafe_allow_html=True)) ---
# Colors below match MCKINSEY_STYLE: navy #1a365d, teal #2c7a7b, slate #4a5568
STREAMLIT_CSS_LIGHT = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap');
    .stApp { background-color: #ffffff; }
    /* Catch-all: anything written in the app — McKinsey blue #1a365d */
    .stApp, .stApp *, .stApp p, .stApp span, .stApp label, .stApp div, .stApp a, .stApp small {
        color: #1a365d !important;
    }
    .stApp .stMarkdown, .stApp div[data-testid="stMarkdown"] {
        color: #1a365d !important;
    }
    h1, h2, h3 {
        font-family: 'Source Sans Pro', Helvetica, sans-serif !important;
        font-weight: 700 !important;
        color: #1a365d !important;
        letter-spacing: -0.02em;
    }
    /* Tab labels */
    div[data-testid="stTabs"] button,
    div[data-testid="stTabs"] button span,
    div[data-testid="stTabs"] label,
    div[data-testid="stTabs"] p {
        color: #1a365d !important;
    }
    /* Selectbox and section labels — blue */
    [data-testid="stHorizontalBlock"] label,
    [data-testid="column"] label,
    p.stCaptionContainer,
    .stCaptionContainer p {
        color: #1a365d !important;
    }
    /* Dropdown (selectbox) text only — white on dark */
    [data-testid="stSelectbox"] label,
    [data-testid="stSelectbox"] div,
    [data-testid="stSelectbox"] span,
    [data-testid="stSelectbox"] p,
    [data-baseweb="select"] div,
    [data-baseweb="select"] span {
        color: #ffffff !important;
    }
    [data-testid="stSelectbox"] [role="listbox"],
    [data-baseweb="select"] [role="listbox"] {
        background-color: #1a365d !important;
    }
    [data-baseweb="select"] > div {
        background-color: #1a365d !important;
        color: #ffffff !important;
    }
    /* Buttons (download, etc.) — keep text blue */
    .stApp button, .stApp button span, .stApp button label {
        color: #1a365d !important;
    }
    /* Theme toggle button: white text on dark background */
    div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="column"]:last-child button,
    div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="column"]:last-child button span,
    div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="column"]:last-child button label {
        color: #ffffff !important;
        background-color: #1a365d !important;
    }
    /* Streamlit header menu (Deploy, Rerun, File change, Datasource) — white text */
    [data-testid="stHeader"], [data-testid="stHeader"] *,
    [data-testid="stToolbar"], [data-testid="stToolbar"] *,
    header, header *,
    [data-testid="stMainMenu"], [data-testid="stMainMenu"] *,
    [data-testid="stStatusWidget"], [data-testid="stStatusWidget"] * {
        color: #ffffff !important;
    }
    .stMetric {
        background: #f7fafc;
        padding: 1rem 1.25rem;
        border-radius: 4px;
        border-left: 3px solid #2c7a7b;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .stMetric label {
        color: #1a365d !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"],
    .stMetric [data-testid="stMetricValue"],
    .stMetric div[data-testid="stMetricValue"],
    .stMetric span {
        color: #1a365d !important;
    }
    /* DataFrames: header and cell text */
    .stDataFrame { border: 1px solid #e2e8f0; border-radius: 4px; overflow: hidden; }
    .stDataFrame th, .stDataFrame td, .stDataFrame label {
        color: #1a365d !important;
    }
    div[data-testid="stTabs"] { margin-top: 1.5rem; }
    .css-1r6slb0 { background-color: #f7fafc !important; }
</style>
"""

# Dark theme: dark background, all text white so nothing is black on dark
STREAMLIT_CSS_DARK = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap');
    .stApp { background-color: #0e1117; }
    /* Any text on dark background — white */
    .stApp, .stApp *, .stApp p, .stApp span, .stApp label, .stApp div, .stApp a, .stApp small {
        color: #ffffff !important;
    }
    h1, h2, h3 {
        font-family: 'Source Sans Pro', Helvetica, sans-serif !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.02em;
    }
    p, span, label, .stMarkdown, .stApp div[data-testid="stMarkdown"] {
        color: #ffffff !important;
    }
    div[data-testid="stTabs"] button,
    div[data-testid="stTabs"] button span,
    div[data-testid="stTabs"] label,
    div[data-testid="stTabs"] p {
        color: #ffffff !important;
    }
    .stMetric {
        background: #1e293b;
        padding: 1rem 1.25rem;
        border-radius: 4px;
        border-left: 3px solid #2c7a7b;
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    .stMetric label,
    .stMetric [data-testid="stMetricValue"],
    .stMetric span {
        color: #ffffff !important;
    }
    .stDataFrame { border: 1px solid #334155; border-radius: 4px; overflow: hidden; }
    .stDataFrame th, .stDataFrame td, .stDataFrame label {
        color: #ffffff !important;
    }
    .stApp button, .stApp button span, .stApp button label {
        color: #ffffff !important;
    }
    /* Theme toggle + Streamlit menu (Dark, Deploy, Rerun, File change, Datasource) — white */
    div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="column"]:last-child button,
    div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="column"]:last-child button span,
    [data-testid="stHeader"], [data-testid="stHeader"] *,
    [data-testid="stToolbar"], [data-testid="stToolbar"] *,
    header, header *,
    [data-testid="stMainMenu"], [data-testid="stMainMenu"] *,
    [data-testid="stStatusWidget"], [data-testid="stStatusWidget"] * {
        color: #ffffff !important;
    }
    p.stCaptionContainer, .stCaptionContainer p {
        color: #ffffff !important;
    }
    [data-testid="stSelectbox"] label,
    [data-testid="stSelectbox"] div,
    [data-testid="stSelectbox"] span,
    [data-baseweb="select"] div,
    [data-baseweb="select"] span {
        color: #ffffff !important;
    }
    div[data-testid="stTabs"] { margin-top: 1.5rem; }
    .css-1r6slb0 { background-color: #1e293b !important; }
    [data-testid="stSidebar"] { background-color: #0e1117; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    [data-baseweb="select"] { background-color: #1e293b !important; }
</style>
"""

# Default (light) — keep for backward compatibility
STREAMLIT_CSS = STREAMLIT_CSS_LIGHT

# --- Instructions / conventions (for docs or new hospital setup) ---
STYLE_INSTRUCTIONS = """
McKinsey Elite style — usage:
- Bar charts: Old period = M["teal"], New period = M["navy"]
- Change/delta: positive = M["increase"], negative = M["decrease"]
- Pie/donut: use PIE_PALETTE (same color per entity in both pies), PIE_TEXTFONT, PIE_MARKER_LINE
- All Plotly figures: fig.update_layout(**PLOTLY_LAYOUT) then set title/height as needed
- Streamlit: st.markdown(STREAMLIT_CSS, unsafe_allow_html=True) once at app start
- Chart titles: title=dict(text="...", font=CHART_TITLE_FONT)
"""
