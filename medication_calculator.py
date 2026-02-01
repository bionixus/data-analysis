#!/usr/bin/env python3
"""
Medication Calculator — GHD drugs
Convert monthly consumption (e.g. vials/units) to estimated number of patients.
Uses the same drug list as the GHD Drug Comparison project.
"""

import streamlit as st
from drug_comparison import GHD_DRUGS

st.set_page_config(
    page_title="Medication Calculator | GHD",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Default consumption per patient per month (pens/cartridges per patient per month).
# Ngenla: 1 pen = 1 month; rest: 2 pens or cartridges per month.
DEFAULT_CONSUMPTION_PER_PATIENT = {
    "Genotropin (Pfizer)": 2.0,
    "Norditropin (Novo Nordisk)": 2.0,
    "Nutropin (Genentech)": 2.0,
    "Omnitrope (Sandoz)": 2.0,
    "Saizen (Merck Serono)": 2.4,
    "Humatrope (Eli Lilly)": 2.0,
    "Ngenla (Pfizer)": 1.0,
    "Zomacton (Ferring)": 2.0,
}

st.title("💊 GHD Medication Calculator")
st.caption("Convert monthly consumption to estimated number of patients (drugs from GHD project)")

drug_options = ["— Select drug —"] + sorted(GHD_DRUGS)
drug_choice = st.selectbox("Drug", options=drug_options, key="drug")

if drug_choice == "— Select drug —":
    st.info("Select a drug to continue.")
    st.stop()

# Normalize in case of custom input later
drug_name = drug_choice
consumption_per_patient_default = DEFAULT_CONSUMPTION_PER_PATIENT.get(
    drug_name, 1.0
)

monthly_consumption = st.number_input(
    "Monthly consumption (vials)",
    min_value=0.0,
    value=100.0,
    step=1.0,
    format="%.1f",
    key="monthly",
)
consumption_per_patient = st.number_input(
    "Vials per patient per month",
    min_value=0.01,
    value=float(consumption_per_patient_default),
    step=0.1,
    format="%.2f",
    key="per_patient",
    help="Typical pens/cartridges per patient per month (e.g. Ngenla: 1, Saizen: 2.4).",
)

if consumption_per_patient <= 0:
    st.error("Consumption per patient must be positive.")
    st.stop()

estimated_patients = monthly_consumption / consumption_per_patient

st.divider()
st.metric(
    "Estimated number of patients",
    f"{estimated_patients:,.1f}",
    help="Monthly consumption ÷ consumption per patient per month",
)
st.caption(f"Formula: {monthly_consumption:,.1f} vials ÷ {consumption_per_patient:,.2f} vials/patient = {estimated_patients:,.1f} patients")
