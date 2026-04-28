# Scalpel AI – Deterministic Accounting Engine

**A professional, investor‑ready finance operating system that transforms raw general ledger data into accurate financial statements (P&L, Balance Sheet, Trial Balance), detailed transaction ledgers, monthly analytics, and downloadable Excel reports – all with a clean Streamlit UI.**

---

## Features

- **Deterministic validation** – Automatically checks that total debits equal total credits.
- **Multi‑format input** – Accepts raw journal entries (`account`, `debit`, `credit`) or trial balance exports.
- **Detailed P&L** – Shows every revenue and COGS line, plus grouped operating expenses (Payroll, Facilities, Admin).
- **Balance Sheet** – Lists assets, liabilities, and equity, with automatic inclusion of net income.
- **Account ledgers** – Drill down into any account to see individual transactions with totals.
- **Monthly analysis** – Seasonal trends if your data contains effective dates.
- **Styled Excel download** – Multi‑sheet workbook with bold headers and auto‑adjusted columns.
- **Optional AI chat** – (Scalpel AI) uses Groq (free) or Claude to answer questions about your financial data.

---

## Quick Start (for beginners)

### 1. Prerequisites
- **Python 3.9 or later** installed on your computer.
- A general ledger file in Excel format (`.xlsx` or `.xls`) containing at least these columns:  
  `account`, `debit`, `credit` (and preferably `account_description`, `effective_date`).

### 2. Download or clone the repository
```bash
git clone https://github.com/your-username/scalpel-ai-finance.git
cd scalpel-ai-finance
```

### 3. Install required packages
```bash
pip install -r requirements.txt
```



### 4. Run the app
```bash
streamlit run main_consolidated.py
```
(The main file may be `app.py` or `main_consolidated.py` – use the name you see in the repository.)

A local browser tab will open at `http://localhost:8501` (often a different port, e.g. `8505`).  
Upload your Excel file and explore the reports.

---

## 📁 Repository Structure

| File                    | Purpose                                                                 |
|-------------------------|-------------------------------------------------------------------------|
| `main_consolidated.py`  | **Main Streamlit app** – contains all UI and logic.                     |
| `aura_engine.py`        | Core accounting engine (classification, trial balance, P&L generation). |
| `test_app1.py` / `test_app2.py` | Tests and earlier prototypes (ignore for normal use).              |
| `pl_output.xlsx`        | Example output – can be deleted.                                       |
| `.gitignore`            | Excludes unnecessary files from version control.                       |

> **Note:** The app now is fully contained in `main_consolidated.py`. The other files are kept for reference.

---

## 🖥️ How to Use the App

1. **Upload your file** – click the “Browse files” button and select your ledger Excel.
2. **Validation** – the app automatically checks global balance and shows a success message.
3. **Navigate tabs**:
   - **Account Ledgers** – pick an account, see every transaction.
   - **Trial Balance** – all accounts with debits, credits, and balance.
   - **P&L (Detailed)** – revenue breakdown, COGS breakdown, operating expenses by category.
   - **Balance Sheet** – assets, liabilities, equity.
   - **Monthly Analysis** – (if your data has dates) trends over time.
   - **Scalpel AI** – optional chat (requires API keys).
4. **Download** – click the button at the bottom to get a full Excel report with multiple sheets.

---

## 🔧 Customising Account Classification

The app uses **account number ranges** and **keywords** to decide if an account is Revenue, COGS, OpEx, Asset, or Liability.  
If your accounts are mis‑classified, edit the `classify_account()` function inside `aura_engine.py` or directly in `main_consolidated.py` (look for the function near the top).  
You can add more keywords or change number ranges to match your chart of accounts.

---

## 🧪 Testing with Sample Data

If you don’t have your own ledger, you can use the sample files provided in the original repository (or create a small test Excel with at least two rows: one debit, one credit).

---

## 🌐 Deploying to the Cloud (Share with Investors)

### Option A: Streamlit Community Cloud (easiest)
1. Push your code to **GitHub** (you already have).
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud), sign in with GitHub.
3. Click **New app**, select your repo, branch, and the main file (`main_consolidated.py`).
4. Click **Deploy**. Your app will be live at `https://your-app.streamlit.app`.

### Option B: Hugging Face Spaces
- Create a new Space → choose **Streamlit** SDK.
- Upload `main_consolidated.py` and `requirements.txt`.  
- The Space will build automatically.

---

## 🤖 Enabling the AI Chat (Scalpel AI)

By default the AI tab shows a mock response. To enable real AI:
- **Groq (free)** – sign up at [console.groq.com](https://console.groq.com), get an API key.
- **Claude (pro)** – add credits at [console.anthropic.com](https://console.anthropic.com).
- **Add the key** to Streamlit Cloud’s **Secrets** (or Hugging Face **Repository Secrets**) using the names:
  ```toml
  GROQ_API_KEY = "gsk_..."
  ANTHROPIC_API_KEY = "sk-ant-..."
  ```

The app will then answer natural language questions about your current P&L and Trial Balance.

---

## ❓ Troubleshooting

| Problem                                  | Likely fix                                                             |
|------------------------------------------|------------------------------------------------------------------------|
| `ModuleNotFoundError`                    | Run `pip install -r requirements.txt` again.                           |
| Uploaded file gives “Missing columns”    | Ensure your Excel has columns named exactly `account`, `debit`, `credit`. Use lowercase. |
| Balance sheet doesn’t balance            | Check if you have any **Equity** accounts (e.g., Retained Earnings). The app adds net income to equity, but you may need to add an opening balance. |
| P&L shows negative COGS                  | This happens if your file contains credit entries on COGS accounts (inventory reclassifications). The app **only uses debit amounts for COGS** – that’s correct for a P&L. |

---

## 📄 License

This project is open‑source and available under the MIT License.

---

## 🙌 Acknowledgements

Built with Streamlit, pandas, and Plotly. Inspired by modern, deterministic accounting engines.

**Made for investors who want to see a real, working finance automation platform.**
```
