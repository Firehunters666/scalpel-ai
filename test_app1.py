import streamlit as st
import pandas as pd
from aura_engine import AuraFinanceEngine

st.set_page_config(page_title="Aura Finance – Deterministic P&L", layout="wide")
st.title("Scalpel AI Accounting System")
st.markdown("### Deterministic Accounting Engine Testing")

uploaded_file = st.file_uploader("Upload General Ledger (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success(f"Loaded {len(df)} rows")

    engine = AuraFinanceEngine(df)

    # Global balance check
    if not engine.validate_global_balance():
        st.error("❌ Global debits ≠ credits. Please check your data.")
        st.stop()
    else:
        st.success("✅ Global balance verified (Total Debits = Total Credits).")

    # Trial Balance
    tb = engine.generate_trial_balance()
    st.subheader("📊 Trial Balance")
    st.dataframe(tb, use_container_width=True)

    # P&L
    pl = engine.generate_pl()
    st.subheader("📈 Profit & Loss Statement")
    st.dataframe(pl, use_container_width=True)

    # Export
    if st.button("Export P&L to Excel"):
        pl.to_excel("pl_output.xlsx", index=False)
        st.success("Exported as pl_output.xlsx")
else:
    st.info("Please upload your Excel file to begin.")