"""
Live Drug Comparison Dashboard — McKinsey Elite Style
All styling is in mckinsey_style.py so any new hospital dashboard can import the same setup.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

from drug_comparison import (
    parse_american_hospital_excel,
    parse_details_sheet,
    compare_drugs,
    compare_details,
    get_details_sheet_common,
    get_second_tab_sheet_names,
)
from mckinsey_style import (
    M,
    PLOTLY_LAYOUT,
    PLOTLY_LAYOUT_PIE,
    STREAMLIT_CSS_LIGHT,
    STREAMLIT_CSS_DARK,
    PIE_PALETTE,
    CHART_TITLE_FONT,
    PIE_TEXTFONT,
    PIE_MARKER_LINE,
    PIE_TITLE_PAD,
    FONT_SIZE_TITLE,
    FONT_SIZE_BODY,
)

# Path to sample data (bundled in repo for Streamlit Cloud / when local files are missing)
_SAMPLE_DIR = Path(__file__).resolve().parent / "sample_data"
_SAMPLE_OLD = _SAMPLE_DIR / "old.xlsx"
_SAMPLE_NEW = _SAMPLE_DIR / "new.xlsx"

# Hospital config: one entry per hospital (Old vs New data). Demo first so deployed app has data.
HOSPITALS = [
    {
        "name": "Demo (sample data)",
        "old_path": str(_SAMPLE_OLD),
        "new_path": str(_SAMPLE_NEW),
    },
    {
        "name": "American Hospital",
        "old_path": "/Users/selim/Documents/BioNixus Market Research Reports/GHD /Updated Old American.xlsx",
        "new_path": "/Users/selim/Downloads/New American Hospital data.xlsx",
    },
    # Add more hospitals, e.g.:
    # {"name": "Hospital B", "old_path": "/path/to/old.xlsx", "new_path": "/path/to/new.xlsx"},
]

CUSTOM_UPLOAD_LABEL = "Custom upload (choose files in sidebar)"

st.set_page_config(page_title="Drug Comparison | GHD Analysis", page_icon="▣", layout="wide", initial_sidebar_state="collapsed")

# Theme: persist in session state, toggle button in header
if "theme" not in st.session_state:
    st.session_state.theme = "light"
# Apply theme CSS first so the rest of the page uses it
st.markdown(
    STREAMLIT_CSS_DARK if st.session_state.theme == "dark" else STREAMLIT_CSS_LIGHT,
    unsafe_allow_html=True,
)

# Header row: title + theme toggle
header_col1, header_col2 = st.columns([6, 1])
with header_col1:
    st.title("▣ GHD Drug Comparison")
with header_col2:
    theme_label = "Dark" if st.session_state.theme == "light" else "White"
    icon = "🌙" if st.session_state.theme == "light" else "☀️"
    if st.button(f"{icon} {theme_label}", key="theme_toggle", use_container_width=True):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()

# Main dashboard filter: hospital dropdown
hospital_options = [h["name"] for h in HOSPITALS] + [CUSTOM_UPLOAD_LABEL]
selected = st.selectbox(
    "Select hospital (Old vs New data)",
    options=hospital_options,
    index=0,
    key="hospital_select",
)
# Caption will show selected hospital labels after they're set below

# Resolve paths and labels from selection or custom upload
old_path = None
new_path = None
LABEL_OLD = "Old data"
LABEL_NEW = "New data"

if selected == CUSTOM_UPLOAD_LABEL:
    st.sidebar.header("Data sources")
    st.sidebar.caption("Custom upload selected above.")
    old_file = st.sidebar.file_uploader("Old period Excel", type=["xlsx", "xls"])
    new_file = st.sidebar.file_uploader("New period Excel", type=["xlsx", "xls"])
    old_path = "/tmp/old_upload.xlsx" if old_file else None
    new_path = "/tmp/new_upload.xlsx" if new_file else None
    if old_file:
        with open("/tmp/old_upload.xlsx", "wb") as f:
            f.write(old_file.getvalue())
    if new_file:
        with open("/tmp/new_upload.xlsx", "wb") as f:
            f.write(new_file.getvalue())
    LABEL_OLD = "Old data"
    LABEL_NEW = "New data"
else:
    h = next((x for x in HOSPITALS if x["name"] == selected), None)
    if h:
        old_path = h["old_path"]
        new_path = h["new_path"]
        LABEL_OLD = f"{h['name']} — Old"
        LABEL_NEW = f"{h['name']} — New"
    st.sidebar.header("Data sources")
    st.sidebar.caption(f"**Hospital:** {selected}")
    if old_path and new_path and (not Path(old_path).exists() or not Path(new_path).exists()):
        st.sidebar.warning("One or both files not found for this hospital. Use Custom upload to provide files.")
        missing = []
        if not Path(old_path).exists():
            missing.append("Old")
        if not Path(new_path).exists():
            missing.append("New")
        st.sidebar.caption(f"Missing: {', '.join(missing)}")

st.caption(f"**{LABEL_OLD}** (12 mo) vs **{LABEL_NEW}** (6 mo)")

if old_path and new_path and Path(old_path).exists() and Path(new_path).exists():
    with st.spinner("Loading both sheets..."):
        xl_old = pd.ExcelFile(old_path)
        xl_new = pd.ExcelFile(new_path)
        old_df = parse_american_hospital_excel(old_path)
        new_df = parse_american_hospital_excel(new_path)
        comp_df = compare_drugs(old_df, new_df)
        # Details: compare the second tab in both files (same instructions as overview)
        second_old, second_new = get_second_tab_sheet_names(old_path, new_path)
        if second_old is not None and second_new is not None:
            has_details = True
            details_sheet_name = second_old  # for tab label
            new_details_sheet_name = second_new  # new file's details sheet for write
            old_details = parse_details_sheet(old_path, second_old)
            new_details = parse_details_sheet(new_path, second_new)
        else:
            details_sheet_name_old, details_sheet_name_new = get_details_sheet_common(old_path, new_path)
            has_details = bool(details_sheet_name_old and details_sheet_name_new)
            details_sheet_name = details_sheet_name_old or details_sheet_name_new or "—"
            new_details_sheet_name = details_sheet_name_new
            old_details = parse_details_sheet(old_path, details_sheet_name_old) if details_sheet_name_old else pd.DataFrame()
            new_details = parse_details_sheet(new_path, details_sheet_name_new) if details_sheet_name_new else pd.DataFrame()
        comp_details = compare_details(old_details, new_details) if has_details and not (old_details.empty and new_details.empty) else pd.DataFrame()

    # Summary
    st.subheader("Executive summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(f"{LABEL_OLD} drugs", len(old_df))
    with col2:
        st.metric(f"{LABEL_NEW} drugs", len(new_df))
    with col3:
        st.metric("Unique drugs (overview)", len(comp_df))
    with col4:
        change_cols = [c for c in comp_df.columns if c.endswith("_change")] if not comp_df.empty else []
        total_col = next((c for c in change_cols if "Total" in c), change_cols[0] if change_cols else None)
        delta = comp_df[total_col].sum() if total_col and not comp_df.empty else 0
        st.metric("Δ Total patients (overview)", f"{delta:+.0f}")

    # Sheet-level tabs: Overview vs Details
    used_second_tab = second_old is not None and second_new is not None
    details_tab_label = f"▸ Details (second tab: {details_sheet_name or '—'})" if used_second_tab else f"▸ Details ({details_sheet_name or '—'})"
    sheet_tab1, sheet_tab2 = st.tabs(["▸ Overview (Questionnaire - overview)", details_tab_label])

    old_cols = [c for c in comp_df.columns if c.endswith("_old")]
    new_cols = [c for c in comp_df.columns if c.endswith("_new")]
    change_cols = [c for c in comp_df.columns if c.endswith("_change")]
    total_old = next((c for c in old_cols if "Total" in c), old_cols[0] if old_cols else None)
    total_new = next((c for c in new_cols if "Total" in c), new_cols[0] if new_cols else None)
    total_change = next((c for c in change_cols if "Total" in c), change_cols[0] if change_cols else None)
    drugs = comp_df.index.tolist()

    def short_name(d):
        return str(d).replace("(Pfizer)", "").replace("(Novo Nordisk)", "").replace("(Merck)", "").replace("(Sandoz)", "").strip()[:22]

    # --- Overview tab ---
    with sheet_tab1:
        tab1, tab2, tab3, tab4 = st.tabs(["▸ Charts", "▸ Data table", f"▸ {LABEL_OLD} vs {LABEL_NEW}", "▸ Export"])
        with tab1:
            st.subheader("Visual analysis")
            if total_old and total_new:
                fig1 = go.Figure()
                fig1.add_trace(go.Bar(
                    name=f"{LABEL_OLD} (12 mo)", x=[short_name(d) for d in drugs],
                    y=[comp_df.loc[d, total_old] if pd.notna(comp_df.loc[d, total_old]) else 0 for d in drugs],
                    marker_color=M["teal"], marker_line_width=0,
                ))
                fig1.add_trace(go.Bar(
                    name=f"{LABEL_NEW} (6 mo)", x=[short_name(d) for d in drugs],
                    y=[comp_df.loc[d, total_new] if pd.notna(comp_df.loc[d, total_new]) else 0 for d in drugs],
                    marker_color=M["navy"], marker_line_width=0,
                ))
                fig1.update_layout(
                    **PLOTLY_LAYOUT,
                    barmode="group", bargap=0.15, bargroupgap=0.05,
                    title=dict(text="Total patients by drug — prior vs current period", font=CHART_TITLE_FONT),
                    xaxis_tickangle=-40, height=420,
                )
                st.plotly_chart(fig1, use_container_width=True)

            # Market share pie charts (Old vs New) — McKinsey style
            if total_old and total_new:
                old_vals = comp_df[total_old].fillna(0)
                new_vals = comp_df[total_new].fillna(0)
                labels_pie = [short_name(d) for d in drugs]
                drug_colors = [PIE_PALETTE[i % len(PIE_PALETTE)] for i in range(len(drugs))]
                fig_pie_old = go.Figure(go.Pie(
                    labels=labels_pie,
                    values=old_vals.values,
                    hole=0.45,
                    textinfo="label+percent",
                    textposition="outside",
                    textfont=PIE_TEXTFONT,
                    hovertemplate="%{label}<br>Patients: %{value:,.0f}<br>Share: %{percent}<extra></extra>",
                    marker=dict(colors=drug_colors, line=PIE_MARKER_LINE),
                ))
                fig_pie_old.update_layout(
                    **PLOTLY_LAYOUT_PIE,
                    title=dict(text=f"{LABEL_OLD} — Market share (12 mo)", font=CHART_TITLE_FONT, pad=PIE_TITLE_PAD),
                    height=400,
                    showlegend=True,
                )
                fig_pie_new = go.Figure(go.Pie(
                    labels=labels_pie,
                    values=new_vals.values,
                    hole=0.45,
                    textinfo="label+percent",
                    textposition="outside",
                    textfont=PIE_TEXTFONT,
                    hovertemplate="%{label}<br>Patients: %{value:,.0f}<br>Share: %{percent}<extra></extra>",
                    marker=dict(colors=drug_colors, line=PIE_MARKER_LINE),
                ))
                fig_pie_new.update_layout(
                    **PLOTLY_LAYOUT_PIE,
                    title=dict(text=f"{LABEL_NEW} — Market share (6 mo)", font=CHART_TITLE_FONT, pad=PIE_TITLE_PAD),
                    height=400,
                    showlegend=True,
                )
                pie_c1, pie_c2 = st.columns(2)
                with pie_c1:
                    st.plotly_chart(fig_pie_old, use_container_width=True, key="pie_old")
                with pie_c2:
                    st.plotly_chart(fig_pie_new, use_container_width=True, key="pie_new")

            if total_change:
                change_data = comp_df[total_change].fillna(0)
                colors = [M["increase"] if v >= 0 else M["decrease"] for v in change_data]
                fig2 = go.Figure(go.Bar(
                    y=[short_name(d) for d in change_data.index],
                    x=change_data.values,
                    orientation="h",
                    marker_color=colors,
                    marker_line_width=0,
                    text=[f"{v:+.0f}" for v in change_data.values],
                    textposition="outside",
                    textfont={"size": 11, "color": M["navy"]},
                ))
                fig2.add_vline(x=0, line_dash="solid", line_color=M["charcoal"], line_width=1.2)
                fig2.update_layout(
                    **PLOTLY_LAYOUT,
                    title=dict(text="Δ Total patients by drug", font=CHART_TITLE_FONT),
                    height=400,
                )
                fig2.update_xaxes(title_text="Change (current − prior)", title_font=dict(color=M["navy"], size=FONT_SIZE_BODY))
                st.plotly_chart(fig2, use_container_width=True)
            metric_pairs = list(zip(old_cols[:4], new_cols[:4]))[:4]
            # Short titles for Metrics comparison subplots (McKinsey style)
            def _metric_subplot_title(col_name: str) -> str:
                s = str(col_name).replace("_old", "").replace("_new", "").strip()
                if "Total" in s and ("12" in s or "12mo" in s):
                    return "Total patients"
                if "Newly diagnosed" in s:
                    return "Newly diagnosed"
                if "Follow up" in s and "received" in s:
                    return "Follow up (received treatment)"
                if "Follow up" in s:
                    return "Follow up"
                return s[:28] if len(s) > 28 else s
            subplot_titles = [_metric_subplot_title(oc) for oc, _ in metric_pairs]
            if metric_pairs:
                fig3 = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=subplot_titles,
                    vertical_spacing=0.18, horizontal_spacing=0.12,
                )
                for idx, (oc, nc) in enumerate(metric_pairs):
                    row, col = idx // 2 + 1, idx % 2 + 1
                    show_legend = (idx == 0)
                    fig3.add_trace(
                        go.Bar(name=LABEL_OLD, x=[short_name(d) for d in drugs],
                               y=[comp_df.loc[d, oc] if pd.notna(comp_df.loc[d, oc]) else 0 for d in drugs],
                               marker_color=M["teal"], marker_line_width=0,
                               showlegend=show_legend),
                        row=row, col=col,
                    )
                    fig3.add_trace(
                        go.Bar(name=LABEL_NEW, x=[short_name(d) for d in drugs],
                               y=[comp_df.loc[d, nc] if pd.notna(comp_df.loc[d, nc]) else 0 for d in drugs],
                               marker_color=M["navy"], marker_line_width=0,
                               showlegend=show_legend),
                        row=row, col=col,
                    )
                fig3.update_layout(
                    **PLOTLY_LAYOUT,
                    height=600,
                    title=dict(text="Metrics comparison", font=CHART_TITLE_FONT),
                    showlegend=True,
                )
                fig3.update_annotations(font=CHART_TITLE_FONT)
                fig3.update_xaxes(tickangle=-40, tickfont={"size": 9, "color": M["navy"]})
                fig3.update_yaxes(tickfont={"size": 9, "color": M["navy"]})
                st.plotly_chart(fig3, use_container_width=True)

        with tab2:
            st.subheader("Head-to-head comparison (overview)")
            change_subset = [c for c in comp_df.columns if "_change" in c]
            styled = comp_df.fillna(0).style.format("{:.0f}", na_rep="0")
            if change_subset:
                styled = styled.background_gradient(subset=change_subset, cmap="RdYlGn", axis=None, vmin=-50, vmax=50)
            st.dataframe(styled, use_container_width=True, height=400)

        with tab3:
            st.subheader(f"{LABEL_OLD} (overview)")
            st.dataframe(old_df, use_container_width=True)
            st.subheader(f"{LABEL_NEW} (overview)")
            st.dataframe(new_df, use_container_width=True)

        with tab4:
            st.subheader("Export overview")
            st.download_button("Download overview comparison (CSV)", comp_df.fillna(0).to_csv(), file_name="ghd_overview_comparison.csv", mime="text/csv")

    # --- Details tab ---
    with sheet_tab2:
        if has_details and not comp_details.empty:
            st.subheader(f"Details comparison — {LABEL_OLD} vs {LABEL_NEW} (by Indication × Type)")
            comp_display = comp_details.fillna(0).reset_index()

            # Data table
            st.subheader("Details — data table")
            numeric_cols_d = [c for c in comp_display.columns if c not in ("Indication", "Type") and pd.api.types.is_numeric_dtype(comp_display[c])]
            change_subset_d = [c for c in numeric_cols_d if "_change" in c]
            styled_d = comp_display.style
            if numeric_cols_d:
                styled_d = styled_d.format({c: "{:.0f}" for c in numeric_cols_d}, na_rep="0")
            if change_subset_d:
                styled_d = styled_d.background_gradient(subset=change_subset_d, cmap="RdYlGn", axis=None, vmin=-50, vmax=50)
            st.dataframe(styled_d, use_container_width=True, height=500)
            st.subheader(f"{LABEL_OLD} — details")
            old_display = old_details.fillna(0).reset_index()
            st.dataframe(old_display, use_container_width=True)

            # New details section (anchor: #american-hospital-new-details when LABEL_NEW is "American Hospital — New")
            st.subheader(f"{LABEL_NEW} — details", anchor="american-hospital-new-details")
            new_display = new_details.fillna(0).reset_index()
            if new_details.empty:
                st.info("New details sheet has no data yet (empty or not parsed). Use **Fill details into New American Excel** after adding data, or copy values from Old details above.")
                if not old_details.empty:
                    # Preview: show Old details with 6-month column names so user can copy
                    _col_12_to_6 = {
                        "Total patients treated in the last 12 months": "Total patients treated in the last 6 months",
                        "Newly diagnosed patients received drug treatments in the last 12 months": "Newly diagnosed patients received drug treatments in the last 6 months",
                        "Follow up patients and received drug treatments in the last 12 months": "Follow up patients and received drug treatments in the last 6 months",
                    }
                    old_preview = old_details.rename(columns=_col_12_to_6).fillna(0).reset_index()
                    st.caption("Preview (from Old details, 12mo→6mo): copy these into the New Excel second sheet if needed.")
                    st.dataframe(old_preview, use_container_width=True)
            else:
                _num_cols = new_display.select_dtypes(include=["number"]).columns
                if len(_num_cols) and (new_display[_num_cols].fillna(0) == 0).all().all():
                    st.caption("New details sheet has structure but all values are zero. Edit the Excel manually or copy from Old details above.")
                st.dataframe(new_display, use_container_width=True)
            st.download_button("Download details comparison (CSV)", comp_display.to_csv(index=False), file_name="ghd_details_comparison.csv", mime="text/csv", key="details_csv")
        else:
            # Specific reason for no details
            n_old, n_new = len(xl_old.sheet_names), len(xl_new.sheet_names)
            if not has_details:
                if n_old < 2 and n_new < 2:
                    reason = f"Both files have only 1 tab ({LABEL_OLD}: {n_old}, {LABEL_NEW}: {n_new}). Add a second sheet in each file for details."
                elif n_old < 2:
                    reason = f"{LABEL_OLD} file has only 1 tab (need 2). {LABEL_NEW} has {n_new}."
                elif n_new < 2:
                    reason = f"{LABEL_NEW} file has only 1 tab (need 2). {LABEL_OLD} has {n_old}."
                else:
                    reason = "Both have 2+ tabs but no common details sheet name. Use the same sheet name (e.g. 'Questionnaire - details') in both files."
            else:
                reason = "Details sheet found but parsed to no rows. Ensure the second tab has a row with 'Type' and numeric data rows below."
            st.info(f"No details data: {reason}")
            st.caption(f"**{LABEL_OLD} file sheets:** {', '.join(xl_old.sheet_names) or '—'}")
            st.caption(f"**{LABEL_NEW} file sheets:** {', '.join(xl_new.sheet_names) or '—'}")
            st.caption(f"Details compare the **second tab** in each file (same layout as overview: {LABEL_OLD} vs {LABEL_NEW}, export).")
            # Fallback: show overview data so the tab is still useful
            st.subheader(f"{LABEL_OLD} (overview)")
            st.dataframe(old_df, use_container_width=True)
            st.subheader(f"{LABEL_NEW} (overview)")
            st.dataframe(new_df, use_container_width=True)

else:
    st.info("Select a hospital above and ensure its data files exist, or choose **Custom upload** and provide both Old and New Excel files in the sidebar.")
