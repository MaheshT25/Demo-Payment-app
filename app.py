import streamlit as st
import pandas as pd
from engine import run_reconciliation_df
from utils import generate_summary, download_excel

st.set_page_config(layout="wide")
st.title("💰 Reconciliation Dashboard")

# ─────────────────────────────────────────────
# Upload Section
# ─────────────────────────────────────────────
st.sidebar.header("Upload Data")

bank_file = st.sidebar.file_uploader("Upload Bank CSV", type=["csv"])
system_file = st.sidebar.file_uploader("Upload System CSV", type=["csv"])

tolerance = st.sidebar.number_input("Tolerance", value=0.05)

# ─────────────────────────────────────────────
# Process Data
# ─────────────────────────────────────────────
if bank_file and system_file:
    bank_df = pd.read_csv(bank_file)
    system_df = pd.read_csv(system_file)

    st.success("Files uploaded successfully!")

    # Run reconciliation
    result_df = run_reconciliation_df(bank_df, system_df, tolerance)

    # ─────────────────────────────────────────
    # KPIs
    # ─────────────────────────────────────────
    summary = generate_summary(result_df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", summary["total"])
    col2.metric("Matched", summary["matched"])
    col3.metric("Mismatched", summary["mismatched"])
    col4.metric("Missing", summary["missing"])

    # ─────────────────────────────────────────
    # Charts
    # ─────────────────────────────────────────
    st.subheader("📊 Status Distribution")
    chart_data = result_df["status"].value_counts()
    st.bar_chart(chart_data)

    # ─────────────────────────────────────────
    # Filters
    # ─────────────────────────────────────────
    st.subheader("🔍 Filter Results")

    status_filter = st.multiselect(
        "Select Status",
        options=result_df["status"].unique(),
        default=result_df["status"].unique()
    )

    filtered_df = result_df[result_df["status"].isin(status_filter)]

    # ─────────────────────────────────────────
    # Drill Down Table
    # ─────────────────────────────────────────
    st.subheader("📋 Reconciliation Results")
    st.dataframe(filtered_df, use_container_width=True)

    # ─────────────────────────────────────────
    # Exception View
    # ─────────────────────────────────────────
    st.subheader("⚠️ Exceptions")

    exceptions = filtered_df[filtered_df["status"] != "MATCHED"]

    if not exceptions.empty:
        st.dataframe(exceptions, use_container_width=True)
    else:
        st.success("No exceptions found!")

    # ─────────────────────────────────────────
    # Download
    # ─────────────────────────────────────────
    st.subheader("⬇️ Export Results")

    excel_data = download_excel(filtered_df)

    st.download_button(
        label="Download Excel",
        data=excel_data,
        file_name="reconciliation_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("Upload both files to start reconciliation")
