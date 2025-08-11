# pages/07_🛡️_Qualité_&_Drift_(PSI).py

import streamlit as st
import pandas as pd
from src.utils import quality_report, psi_frame

st.set_page_config(layout="wide")
st.header("🛡️ Qualité des données & Drift (PSI)")

st.caption(
    "Comparaison du jeu **courant** au **baseline d'entraînement** pour détecter le drift (PSI) "
    "et les problèmes qualité (valeurs manquantes, variances nulles, inf)."
)

# Baseline sauvegardée au training
BASELINE = "models/baseline_sample.parquet"
try:
    base = pd.read_parquet(BASELINE)
except Exception:
    st.error(
        "Baseline PSI introuvable. Ré-entraînez (src/train.py) pour générer "
        "`models/baseline_sample.parquet`."
    )
    st.stop()

uploaded = st.file_uploader(
    "Jeu courant (CSV, mêmes colonnes numériques que le training)", type=["csv"]
)
if not uploaded:
    st.info("Chargez un fichier pour lancer l'analyse.")
    st.stop()

cur = pd.read_csv(uploaded)

# Sous-ensembles numériques avec intersection des colonnes
cur_num_cols = cur.select_dtypes(include=["number"]).columns
inter_cols = [c for c in cur_num_cols if c in base.columns]
if not inter_cols:
    st.error(
        "Aucune colonne numérique commune entre votre fichier et le baseline. "
        "Vérifiez le schéma et les noms de colonnes."
    )
    st.stop()

cur_num = cur[inter_cols]
base_num = base[inter_cols]

# ---- Qualité des données
st.subheader("Qualité des données")
qr = quality_report(cur)
st.dataframe(qr, use_container_width=True)
st.download_button(
    "Télécharger rapport qualité (CSV)",
    qr.to_csv(index=False),
    file_name="data_quality_report.csv",
    mime="text/csv",
)

# ---- Drift PSI
st.subheader("Drift — Population Stability Index (PSI)")
psi_df = psi_frame(base_num, cur_num, bins=10)
st.dataframe(psi_df, use_container_width=True)

# petit graphe barre PSI
if not psi_df.empty:
    st.bar_chart(psi_df.set_index("feature")["psi"])

st.download_button(
    "Télécharger rapport PSI (CSV)",
    psi_df.to_csv(index=False),
    file_name="psi_report.csv",
    mime="text/csv",
)

# ---- Alertes lisibles
alerte = psi_df.query("psi >= 0.1 and psi < 0.25")
fort   = psi_df.query("psi >= 0.25")

if not fort.empty:
    st.error("🔴 Drift FORT sur : " + ", ".join(fort["feature"].tolist()))
elif not alerte.empty:
    st.warning("🟠 Drift à surveiller sur : " + ", ".join(alerte["feature"].tolist()))
else:
    st.success("🟢 Aucun drift significatif (PSI < 0.1)")

st.caption("Règles usuelles PSI : < 0.1 OK, 0.1–0.25 Alerte, > 0.25 Fort.")
