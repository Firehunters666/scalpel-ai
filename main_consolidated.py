import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Scalpel AI", layout="wide")
st.title("Scalpel AI Accounting Enging")
st.markdown("### Deterministic Engine Test")


# ---------------------------
# Helper functions
# ---------------------------
def validate_global_balance(df):
    total_debits = df["Debit"].sum()
    total_credits = df["Credit"].sum()
    return abs(total_debits - total_credits) < 0.01, total_debits, total_credits


def generate_trial_balance(df):
    tb = df.groupby(['AccountNumber', 'AccountName']).agg({
        'Debit': 'sum',
        'Credit': 'sum'
    }).reset_index()
    tb['Balance'] = tb['Debit'] - tb['Credit']
    return tb


def generate_pl(trial_balance):
    rev_accounts = [4000, 4010]
    cogs_accounts = [5000]
    opex_accounts = [6000, 5010]

    revenue = trial_balance[trial_balance['AccountNumber'].isin(rev_accounts)]['Credit'].sum()
    cogs = trial_balance[trial_balance['AccountNumber'].isin(cogs_accounts)]['Debit'].sum()
    gross_profit = revenue - cogs
    opex = trial_balance[trial_balance['AccountNumber'].isin(opex_accounts)]['Debit'].sum()
    net_income = gross_profit - opex

    pl_df = pd.DataFrame([
        ["Revenue", revenue],
        ["COGS", cogs],
        ["Gross Profit", gross_profit],
        ["Operating Expenses", opex],
        ["Net Income", net_income]
    ], columns=["Account", "Amount"])
    return pl_df


def generate_ledger_detail(df):
    """Show all transactions, sorted by account, then date."""
    return df[['TxnDate', 'AccountNumber', 'AccountName', 'Debit', 'Credit', 'Description', 'Dept', 'CostCenter',
               'Currency']].sort_values(['AccountNumber', 'TxnDate'])


def download_excel(ledger_detail, trial_balance, pl):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        ledger_detail.to_excel(writer, sheet_name='Ledger Detail', index=False)
        trial_balance.to_excel(writer, sheet_name='Trial Balance', index=False)
        pl.to_excel(writer, sheet_name='Profit & Loss', index=False)
    return output.getvalue()


# ---------------------------
# Main App
# ---------------------------
uploaded_file = st.file_uploader("Upload General Ledger (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success(f"Loaded {len(df)} rows")

    # Validation
    is_balanced, total_debits, total_credits = validate_global_balance(df)
    if not is_balanced:
        st.error(f"❌ Global debits ({total_debits:.2f}) ≠ credits ({total_credits:.2f}). Please fix data.")
        st.stop()
    else:
        st.success(f"✅ Global balance verified (Total Debits = Total Credits = {total_debits:.2f})")

    # Generate outputs
    tb = generate_trial_balance(df)
    pl = generate_pl(tb)
    ledger_detail = generate_ledger_detail(df)

    # ---- Tabs for different views ----
    tab1, tab2, tab3 = st.tabs(["📋 Ledger Detail", "📊 Trial Balance", "📈 Profit & Loss"])

    with tab1:
        st.subheader("All Journal Entries (by Account)")
        st.dataframe(ledger_detail, use_container_width=True)

    with tab2:
        st.subheader("Trial Balance")
        st.dataframe(tb, use_container_width=True)

    with tab3:
        st.subheader("Profit & Loss Statement")
        st.dataframe(pl, use_container_width=True)

    # ---- Download button ----
    st.markdown("---")
    excel_data = download_excel(ledger_detail, tb, pl)
    st.download_button(
        label="📥 Download All Statements (Excel)",
        data=excel_data,
        file_name="aura_financial_statements.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Please upload your Excel file (Balanced_General_Ledger.xlsx) to begin.")