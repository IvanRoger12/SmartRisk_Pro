import streamlit as st, pandas as pd, numpy as np, joblib
from i18n.strings import tr
from src.ui import use_global_css, get_lang

# --- Style global + langue ---
use_global_css()
lang = get_lang()

st.header(tr("nav_batch", lang) or "Lot de notation")

# --- Modèle en cache ---
@st.cache_resource(show_spinner=True)
def load_model():
    return joblib.load("models/pipeline.joblib")

try:
    pipe = load_model()
except Exception:
    st.error(tr("needs_model", lang) or "Modèle introuvable. Entraînez via src/train.py puis relancez.")
    st.stop()

# Colonnes attendues (si le pipeline expose feature_names_in_)
expected_cols = getattr(pipe.named_steps.get("impute", pipe), "feature_names_in_", None)

def align_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Aligne df sur l'ordre/jeu de colonnes attendu; ajoute les manquantes en NaN."""
    if expected_cols is None:
        return df
    out = df.copy()
    for c in expected_cols:
        if c not in out.columns:
            out[c] = np.nan
    return out[list(expected_cols)]

@st.cache_data(show_spinner=False)
def load_csv(_uploaded) -> pd.DataFrame:
    return pd.read_csv(_uploaded, low_memory=False)

file = st.file_uploader(tr("upload", lang) or "Fichier CSV (mêmes colonnes que l’entraînement)", type=["csv"])

with st.expander(tr("batch_options", lang) or "Options"):
    prob_threshold = st.slider(tr("prob_thresh", lang) or "Seuil probabilité de défaut (refus si > seuil)",
                               0.05, 0.90, 0.30, step=0.01)
    margin_rate = st.number_input(tr("margin_rate", lang) or "Marge brute unitaire (taux)",
                                  min_value=0.0, max_value=1.0, value=0.18, step=0.01, format="%.2f")
    loss_unit = st.number_input(tr("loss_unit", lang) or "Perte unitaire en cas de défaut (€)",
                                min_value=0.0, value=300.0, step=50.0, format="%.2f")
    batch_size = st.number_input(tr("batch_size", lang) or "Taille de lot (prédictions par batch)",
                                 min_value=5_000, max_value=200_000, value=50_000, step=5_000)

if file:
    df_raw = load_csv(file)
    st.write("Dimensions :", df_raw.shape)
    st.dataframe(df_raw.head(10), use_container_width=True)

    # Alignement des colonnes
    X = align_columns(df_raw.select_dtypes(include="number").copy()) if expected_cols is not None else df_raw.copy()

    # Prédiction par lot pour gros fichiers
    n = len(X)
    probs = np.empty(n, dtype=float)
    start = 0
    while start < n:
        end = min(start + batch_size, n)
        try:
            probs[start:end] = pipe.predict_proba(X.iloc[start:end])[:, 1]
        except Exception as e:
            st.error(f"Erreur de prédiction entre lignes {start}–{end}: {e}")
            st.stop()
        start = end

    out = df_raw.copy()
    out["default_proba"] = probs
    out["score_0_100"] = ((1.0 - probs) * 100).round(0).astype(int)

    # Décision simple orientée risque
    out["decision"] = np.where(out["default_proba"] > prob_threshold, "refus", "accord")

    # Profit espéré (démo) : profit = marge - prob*perte
    out["expected_profit"] = (margin_rate * 1000.0) - (out["default_proba"] * loss_unit)

    st.subheader(tr("pred_preview", lang) or "Aperçu des prédictions")
    st.dataframe(out.head(25), use_container_width=True)

    # KPI rapides
    acc_rate = (out["decision"] == "accord").mean()
    st.write(tr("kpi_accept", lang) or "Taux d’accord :", f"{acc_rate:.1%}")
    st.write(tr("kpi_mean_pd", lang) or "PD moyenne :", f"{out['default_proba'].mean():.3f}")
    st.write(tr("kpi_profit", lang) or "Profit espéré moyen (€) :", f"{out['expected_profit'].mean():.2f}")

    # Export
    csv_bytes = out.to_csv(index=False).encode("utf-8")
    st.download_button(tr("download", lang) or "Télécharger les prédictions",
                       csv_bytes, file_name="predictions.csv", mime="text/csv")
else:
    st.caption(tr("batch_hint", lang) or "Chargez un CSV contenant les colonnes du dataset d’entraînement.")
