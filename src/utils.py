# utils métier & monitoring — écrit “comme Ivan”
from __future__ import annotations
import numpy as np, pandas as pd

def compute_profit(y_true: np.ndarray, proba: np.ndarray, thresh: float, revenue_ok: float, loss_bad: float):
    y_pred = (proba >= thresh).astype(int)  # 1 = risque => on refuse
    accept = (y_pred == 0)
    nb_ok  = int(((y_true == 0) & accept).sum())
    nb_bad = int(((y_true == 1) & accept).sum())
    profit = nb_ok * revenue_ok - nb_bad * loss_bad
    return profit, nb_ok, nb_bad, int(accept.sum())

def find_best_threshold(y_true: np.ndarray, proba: np.ndarray, revenue_ok: float, loss_bad: float, grid: int = 101):
    t_grid = np.linspace(0.01, 0.99, grid)
    scores = [compute_profit(y_true, proba, t, revenue_ok, loss_bad)[0] for t in t_grid]
    i = int(np.argmax(scores))
    return float(t_grid[i]), float(scores[i])

def quality_report(df: pd.DataFrame) -> pd.DataFrame:
    rep = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "missing_pct": df.isna().mean() * 100,
        "inf_count": np.isinf(df.select_dtypes(include=[float,int])).sum() if len(df) else 0,
        "n_unique": df.nunique(),
        "std": df.select_dtypes(include=[float,int]).std()
    })
    rep["zero_var"] = rep["std"].fillna(0).eq(0)
    return rep.sort_values("missing_pct", ascending=False)

def psi(expected: pd.Series, actual: pd.Series, bins: int = 10) -> float:
    exp = expected.dropna().astype(float); act = actual.dropna().astype(float)
    if exp.empty or act.empty: return np.nan
    # bins sur les quantiles du jeu “expected”
    q = np.linspace(0, 1, bins + 1)
    cuts = np.unique(np.quantile(exp, q))
    exp_counts = np.histogram(exp, bins=cuts)[0]; act_counts = np.histogram(act, bins=cuts)[0]
    exp_pct = np.clip(exp_counts / max(exp_counts.sum(), 1), 1e-6, 1)
    act_pct = np.clip(act_counts / max(act_counts.sum(), 1), 1e-6, 1)
    return float(np.sum((act_pct - exp_pct) * np.log(act_pct / exp_pct)))

def psi_frame(expected_df: pd.DataFrame, actual_df: pd.DataFrame, bins: int = 10) -> pd.DataFrame:
    cols = [c for c in expected_df.columns if c in actual_df.columns]
    res = []
    for c in cols:
        if pd.api.types.is_numeric_dtype(expected_df[c]) and pd.api.types.is_numeric_dtype(actual_df[c]):
            res.append({"feature": c, "psi": psi(expected_df[c], actual_df[c], bins)})
    out = pd.DataFrame(res).sort_values("psi", ascending=False)
    out["severity"] = pd.cut(out["psi"], bins=[-np.inf, 0.1, 0.25, np.inf], labels=["OK", "Alerte", "Fort"])
    return out
