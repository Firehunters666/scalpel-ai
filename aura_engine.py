import pandas as pd


class AuraFinanceEngine:
    def __init__(self, df_journal):
        self.df_journal = df_journal
        self.trial_balance = None

    def validate_global_balance(self):
        total_debits = self.df_journal["Debit"].sum()
        total_credits = self.df_journal["Credit"].sum()
        return abs(total_debits - total_credits) < 0.01

    def generate_trial_balance(self):
        tb = self.df_journal.groupby(['AccountNumber', 'AccountName']).agg({
            'Debit': 'sum',
            'Credit': 'sum'
        }).reset_index()
        tb['Balance'] = tb['Debit'] - tb['Credit']
        self.trial_balance = tb
        return self.trial_balance

    def generate_pl(self):
        if self.trial_balance is None:
            self.generate_trial_balance()

        rev_accounts = [4000, 4010]
        cogs_accounts = [5000]
        opex_accounts = [6000, 5010]

        pl_data = {}
        pl_data['Revenue'] = self.trial_balance[self.trial_balance['AccountNumber'].isin(rev_accounts)]['Credit'].sum()
        pl_data['COGS'] = self.trial_balance[self.trial_balance['AccountNumber'].isin(cogs_accounts)]['Debit'].sum()
        pl_data['Gross Profit'] = pl_data['Revenue'] - pl_data['COGS']
        pl_data['Operating Expenses'] = self.trial_balance[self.trial_balance['AccountNumber'].isin(opex_accounts)][
            'Debit'].sum()
        pl_data['Net Income'] = pl_data['Gross Profit'] - pl_data['Operating Expenses']

        return pd.DataFrame(list(pl_data.items()), columns=['Account', 'Amount'])