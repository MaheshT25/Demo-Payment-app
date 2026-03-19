import pandas as pd

def run_reconciliation_df(bank_df, system_df, tolerance):
    merged = pd.merge(
        bank_df,
        system_df,
        on="transaction_id",
        how="outer",
        suffixes=("_bank", "_system"),
        indicator=True
    )

    def get_status(row):
        if row["_merge"] != "both":
            return "MISSING"

        diff = abs(row["amount_bank"] - row["amount_system"])

        if diff <= tolerance:
            return "MATCHED"
        else:
            return "MISMATCH"

    merged["status"] = merged.apply(get_status, axis=1)

    return merged
