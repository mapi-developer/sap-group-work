from pathlib import Path

import pandas as pd

ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "environment.yml").exists())
RAW = ROOT / "resources"
PROC = ROOT / "data" / "processed"
FIG = ROOT / "reports" / "figures"
PROC.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

PURCH_ORG = "US00"
COMPANY_CODE = "US00"
PERIOD_START = pd.Timestamp("2025-10-01")
PERIOD_END = pd.Timestamp("2026-10-01")


TABLES = {
    "ekko": ("EKKO_3.xlsx", [
        "Purchasing Document", "Purch. Doc. Category", "Purchasing Doc. Type",
        "Supplier", "Company Code", "Purch. Organization.1", "Purchasing Group",
        "Document Date", "Created On", "Created By", "Currency", "Exchange Rate"]),
    "ekpo": ("EKPO_2026.xlsx", [
        "Purchasing Document", "Item", "Purch. Doc. Category", "Deletion Indicator",
        "Material", "Short Text", "Material Group", "Material Type", "Plant",
        "Company Code", "Order Quantity", "Order Unit", "Net Order Price",
        "Price unit", "Net Order Value", "Gross order value"]),
    "lfa1": ("LFA1_2026.xlsx", [
        "Supplier", "Name 1", "Country/Region Key", "Region", "City",
        "Postal Code", "Account group", "Created On"]),
    "ekbe": ("EKBE_2026.xlsx", [
        "Purchasing Document", "Item", "Trans./event type", "Material Doc. Year",
        "Material Document", "Material Doc.Item", "PO History Category",
        "Movement Type", "Debit/Credit ind", "Posting Date", "Quantity",
        "Amount", "Currency", "Material", "Plant"]),
}

RENAME = {"Purch. Organization.1": "Purch. Organization"}


def load(name: str, refresh: bool = False) -> pd.DataFrame:
    file, cols = TABLES[name]
    pq = PROC / f"{name}.parquet"
    if pq.exists() and not refresh:
        df = pd.read_parquet(pq)
        if list(df.columns) == cols:
            return _tidy(df)
    df = pd.read_excel(RAW / file, usecols=cols)[cols]
    df.to_parquet(pq)
    return _tidy(df)


def load_raw(name: str) -> pd.DataFrame:
    return pd.read_excel(RAW / TABLES[name][0])


def _tidy(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=RENAME)
    if "Supplier" in df:
        df["Supplier"] = df["Supplier"].astype("string").str.strip()
    return df
