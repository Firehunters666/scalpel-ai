import streamlit as st
import pandas as pd
from io import BytesIO
from openai import OpenAI

# ======================== PAGE CONFIG ========================
st.set_page_config(page_title="Scalpel AI", layout="wide")
st.title("Scalpel AI Accounting Engine")
st.markdown("### Deterministic Engine Test")


# ======================== HELPER FUNCTIONS ========================
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


def download_excel(trial_balance, pl):
    """Export Trial Balance and P&L as separate sheets."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        trial_balance.to_excel(writer, sheet_name='Trial Balance', index=False)
        pl.to_excel(writer, sheet_name='Profit & Loss', index=False)
    return output.getvalue()


# ======================== AI FUNCTION (Groq) ========================
def ask_scalpel_ai(question, context):
    """Use Groq API (free tier) – requires GROQ_API_KEY in secrets."""
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        return "⚠️ API key not found. Please add GROQ_API_KEY to .streamlit/secrets.toml"

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )
    # Using a reliable, fast model from Groq (free)
    model_name = "llama-3.3-70b-versatile"  # or "mixtral-8x7b-32768"

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system",
                 "content": "You are a senior accountant. Answer based only on the provided financial data. Do not invent numbers."},
                {"role": "user",
                 "content": f"Here is the P&L and Trial Balance (as text):\n{context}\n\nQuestion: {question}"}
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI error: {e}"


# ======================== MAIN APP ========================
uploaded_file = st.file_uploader("Upload General Ledger (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success(f"Loaded {len(df)} rows")

    # Global balance check
    is_balanced, total_debits, total_credits = validate_global_balance(df)
    if not is_balanced:
        st.error(f"❌ Global debits ({total_debits:.2f}) ≠ credits ({total_credits:.2f})")
        st.stop()
    else:
        st.success(f"✅ Global balance verified (Debits = Credits = {total_debits:.2f})")

    # Generate reports
    tb = generate_trial_balance(df)
    pl = generate_pl(tb)

    # ========== TABS ==========
    tab_tb, tab_pl, tab_ai = st.tabs(["📊 Trial Balance", "📈 P&L Statement", "🤖 Scalpel AI"])

    with tab_tb:
        st.subheader("Trial Balance")
        st.dataframe(tb, use_container_width=True)

    with tab_pl:
        st.subheader("Profit & Loss Statement")
        st.dataframe(pl, use_container_width=True)

    with tab_ai:
        st.subheader("Ask Scalpel AI")
        st.markdown(
            "Ask questions about the financial data (e.g., *What is total operating expense?*, *Why is net income negative?*)")
        user_question = st.text_input("Your question:", key="ai_question")

        # Prepare context: P&L and TB as text
        context = f"P&L:\n{pl.to_string(index=False)}\n\nTrial Balance:\n{tb.to_string(index=False)}"

        if st.button("Ask Scalpel AI"):
            if not user_question:
                st.warning("Please enter a question.")
            else:
                with st.spinner("Scalpel AI is thinking..."):
                    answer = ask_scalpel_ai(user_question, context)
                st.success("Scalpel AI says:")
                st.write(answer)

    # ========== DOWNLOAD BUTTON ==========
    st.markdown("---")
    excel_data = download_excel(tb, pl)
    st.download_button(
        label="📥 Download Financial Statements (Excel)",
        data=excel_data,
        file_name="scalpel_financials.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Please upload your balanced general ledger Excel file to begin.")