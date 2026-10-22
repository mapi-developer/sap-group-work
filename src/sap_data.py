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


def load_scope() -> pd.DataFrame:
    """In-scope PO items (US00, category F, not deleted, reporting window), built by eda/scope_eda.ipynb."""
    return pd.read_parquet(PROC / "po_scope.parquet")


# Material codes are created per student (CHLO1072, CHLK1003T, ...), so one product has
# hundreds of codes. Product family is derived from Short Text, then the material prefix.
FAMILY_TEXT = [
    ("Chain lock", r"chain|lokk"),
    ("Water bottle cage", r"cage"),
    ("Water bottle", r"bottle"),
    ("Socket head bolt", r"bolt"),
    ("T-shirt", r"shirt"),
    ("Spelt flour", r"nköly|onkoly|liszt|búza|buza"),
    ("Touring bike", r"touring bike"),
    ("Off-road handle bar", r"handle ?bar"),
]
FAMILY_PREFIX = {"CH": "Chain lock", "BOTL": "Water bottle", "BOLT": "Socket head bolt",
                 "SH": "T-shirt", "TK": "Spelt flour", "CA": "Water bottle cage"}
FAMILY_CATEGORY = {
    "Chain lock": "Accessories", "Water bottle": "Accessories",
    "Water bottle cage": "Accessories", "T-shirt": "Accessories",
    "Socket head bolt": "Components", "Off-road handle bar": "Components",
    "Touring bike": "Finished bikes", "Spelt flour": "Non-bike (exercise item)",
}


def product_family(df: pd.DataFrame) -> pd.Series:
    text = df["Short Text"].fillna("").str.lower()
    fam = pd.Series("Other", index=df.index)
    for name, pattern in reversed(FAMILY_TEXT):
        fam = fam.mask(text.str.contains(pattern), name)
    for prefix, name in FAMILY_PREFIX.items():
        fam = fam.mask((fam == "Other") & df["Material"].fillna("").str.startswith(prefix), name)
    return fam
