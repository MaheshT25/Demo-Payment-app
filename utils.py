import pandas as pd
from io import BytesIO

def generate_summary(df):
    return {
        "total": len(df),
        "matched": len(df[df["status"] == "MATCHED"]),
        "mismatched": len(df[df["status"] == "MISMATCH"]),
        "missing": len(df[df["status"] == "MISSING"]),
    }

def download_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Results")
    return output.getvalue()
