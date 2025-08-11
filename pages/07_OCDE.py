# pages/07_Qualite_et_Drift_PSI.py
import streamlit as st, pandas as pd
from src.ui import use_global_css, get_lang
from i18n.strings import tr
from src.utils import quality_report, psi_frame

# Style global + langue
use_global_css()
lang = get_lang()

st.header(tr("nav_psi", lang) or "Qualité des données & Drift (PSI)")
st.caption(tr("psi_intro", lang) or
           "Comparaison du jeu courant au baseline d'entraînement pour détecter le drift (PSI) et les problèmes qualité.")

BASELINE = "models/baseline_sample.parquet"

@st.cache_data(show_spinner=False)
def load_baseline(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)

# Chargement baseline
try:
    base = load_baseline(BASELINE)
except Exception:
    st.error(tr("psi_missing_base", lang) or
             "Baseline PSI introuvable. Ré-entraînez (src/train.py) pour générer models/baseline_sample.parquet.")
    st.stop()

# Upload du jeu courant
uploaded = st.file_uploader(tr("psi_upload", lang) or
                            "Jeu courant (CSV, mêmes colonnes numériques que le training)", type=["csv"])
if not uploaded:
    st.info(tr("psi_hint", lang) or "Chargez un fichier pour lancer l'analyse.")
    st.stop()

@st.cache_data(show_spinner=False)
def load_csv(f) -> pd.DataFrame:
    return pd.read_csv(f)

cur = load_csv(uploaded)

# Intersection sur colonnes numériques
cur_num_cols = cur.select_dtypes(include=["number"]).columns
inter_cols = [c for c in cur_num_cols if c in base.columns]
if not inter_cols:
    st.error(tr("psi_no_common", lang) or
             "Aucune colonne numérique commune entre votre fichier et le baseline. Vérifiez le schéma et les noms de colonnes.")
    st.stop()

cur_num = cur[inter_cols]
base_num = base[inter_cols]

# Qualité des données
st.subheader(tr("psi_quality", lang) or "Qualité des données")
qr = quality_report(cur)
st.dataframe(qr, use_container_width=True)
st.download_button(
    tr("download_quality", lang) or "Télécharger rapport qualité (CSV)",
    qr.to_csv(index=False).encode("utf-8"),
    file_name="data_quality_report.csv",
    mime="text/csv",
)

# Drift PSI
st.subheader("Drift — Population Stability Index (PSI)")
psi_df = psi_frame(base_num, cur_num, bins=10)
st.dataframe(psi_df, use_container_width=True)

if not psi_df.empty:
    st.bar_chart(psi_df.set_index("feature")["psi"])

st.download_button(
    tr("download_psi", lang) or "Télécharger rapport PSI (CSV)",
    psi_df.to_csv(index=False).encode("utf-8"),
    file_name="psi_report.csv",
    mime="text/csv",
)

# ---- Alertes sans icône (markdown + CSS)
alert = psi_df.query("psi >= 0.1 and psi < 0.25")
strong = psi_df.query("psi >= 0.25")

if not strong.empty:
    msg = (tr("psi_strong", lang) or "Drift fort sur : ") + ", ".join(strong["feature"])
    st.markdown(f'<div class="alert error">{msg}</div>', unsafe_allow_html=True)
elif not alert.empty:
    msg = (tr("psi_watch", lang) or "Drift à surveiller sur : ") + ", ".join(alert["feature"])
    st.markdown(f'<div class="alert warn">{msg}</div>', unsafe_allow_html=True)
else:
    msg = tr("psi_ok", lang) or "Aucun drift significatif (PSI < 0.1)"
    st.markdown(f'<div class="alert ok">{msg}</div>', unsafe_allow_html=True)

st.caption(tr("psi_rules", lang) or "Règles usuelles PSI : < 0.1 OK, 0.1–0.25 Alerte, > 0.25 Fort.")
