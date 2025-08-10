
import pandas as pd

GMSC_COLUMNS = [
    "RevolvingUtilizationOfUnsecuredLines",
    "age",
    "NumberOfTime30-59DaysPastDueNotWorse",
    "DebtRatio",
    "MonthlyIncome",
    "NumberOfOpenCreditLinesAndLoans",
    "NumberOfTimes90DaysLate",
    "NumberRealEstateLoansOrLines",
    "NumberOfTime60-89DaysPastDueNotWorse",
    "NumberOfDependents",
]
TARGET_COL = "SeriousDlqin2yrs"

def load_raw_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    return df

def select_features(df: pd.DataFrame) -> pd.DataFrame:
    keep = [c for c in GMSC_COLUMNS if c in df.columns]
    return df[keep].copy()

def get_target(df: pd.DataFrame) -> pd.Series:
    if TARGET_COL not in df.columns:
        raise ValueError(f"Colonne cible '{TARGET_COL}' absente du CSV.")
    return df[TARGET_COL].astype(int)
