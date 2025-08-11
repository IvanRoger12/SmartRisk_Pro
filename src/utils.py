# -- crée src/__init__.py et src/utils.py
from pathlib import Path

Path("src").mkdir(parents=True, exist_ok=True)
Path("src/__init__.py").write_text("", encoding="utf-8")

utils_code = r'''
import numpy as np
import pandas as pd
from typing import Tuple

# -------- Qualité des données
def quality_report(df: pd.DataFrame) -> pd.DataFrame:
    out = []
    n = len(df)
    for c in df.columns:
        s = df[c]
        dtype = str(s.dtype)
        na = int(s.isna().sum())
        na_pct = round(na / n * 100, 2) if n else 0.0
        nunique = int(s.nunique(dropna=True))
        zero_var = (s.nunique(dropna=True) <= 1)
        n_inf = int(np.isinf(s.replace({np.inf: np.nan, -np.inf: np.nan})).sum()) if np.issubdtype(s.dtype, np.number) else 0
        out.append({
            "feature": c,
            "dtype": dtype,
            "missing_cnt": na,
            "missing_pct": na_pct,
            "nunique": nunique,
            "zero_variance": bool(zero_var),
            "n_infinite": n_inf,
        })
    rep = pd.DataFrame(out).sort_values(["missing_pct","feature"], ascending=[False, True]).reset_index(drop=True)
    return rep

# -------- PSI (Population Stability Index)
def _psi_for_arrays(base: np.ndarray, cur: np.ndarray, bins: int = 10) -> float:
    base = base[~np.isnan(base)]
    cur  = cur[~np.isnan(cur)]
    if base.size == 0 or cur.size == 0:
        return 0.0
    # bornes = quantiles de la base
    qs = np.linspace(0, 1, bins + 1)
    try:
        edges = np.unique(np.quantile(base, qs))
    except Exception:
        return 0.0
    if edges.size < 3:  # pas assez de variabilité
        return 0.0
    # histogrammes normalisés
    base_hist, _ = np.histogram(base, bins=edges)
    cur_hist,  _ = np.histogram(cur,  bins=edges)
    base_ratio = base_hist / np.maximum(base_hist.sum(), 1)
    cur_ratio  = cur_hist  / np.maximum(cur_hist.sum(), 1)
    # epsilon pour éviter /0 et log(0)
    eps = 1e-6
    base_ratio = np.clip(base_ratio, eps, None)
    cur_ratio  = np.clip(cur_ratio,  eps, None)
    psi = np.sum((base_ratio - cur_ratio) * np.log(base_ratio / cur_ratio))
    return float(psi)

def psi_frame(base_df: pd.DataFrame, cur_df: pd.DataFrame, bins: int = 10) -> pd.DataFrame:
    common = [c for c in base_df.columns if c in cur_df.columns]
    rows = []
    for c in common:
        if pd.api.types.is_numeric_dtype(base_df[c]) and pd.api.types.is_numeric_dtype(cur_df[c]):
            psi = _psi_for_arrays(base_df[c].to_numpy(dtype=float), cur_df[c].to_numpy(dtype=float), bins=bins)
            rows.append({"feature": c, "psi": round(psi, 4)})
    return pd.DataFrame(rows).sort_values("psi", ascending=False).reset_index(drop=True)

# -------- Seuil & profit
def compute_profit(y_true: np.ndarray, proba: np.ndarray, thr: float, revenue_ok: float, loss_bad: float) -> Tuple[float,int,int,int]:
    y_true = np.asarray(y_true).astype(int)
    proba  = np.asarray(proba, dtype=float)
    # Règle: on ACCEPTE si proba défaut < seuil
    accept_mask = proba < thr
    n_accept = int(accept_mask.sum())
    n_ok_accepted  = int(((y_true == 0) & accept_mask).sum())
    n_bad_accepted = int(((y_true == 1) & accept_mask).sum())
    profit = n_ok_accepted * float(revenue_ok) - n_bad_accepted * float(loss_bad)
    return float(profit), n_ok_accepted, n_bad_accepted, n_accept

def find_best_threshold(y_true: np.ndarray, proba: np.ndarray, revenue_ok: float, loss_bad: float) -> Tuple[float, float]:
    grid = np.linspace(0.01, 0.99, 199)
    best_thr, best_profit = 0.5, -1e18
    for t in grid:
        p, *_ = compute_profit(y_true, proba, float(t), revenue_ok, loss_bad)
        if p > best_profit:
            best_profit, best_thr = p, float(t)
    return best_thr, best_profit
'''
Path("src/utils.py").write_text(utils_code.strip() + "\n", encoding="utf-8")
print("✅ src/utils.py créé")
