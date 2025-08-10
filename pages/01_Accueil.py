import streamlit as st
from i18n.strings import tr

lang = st.session_state.get("lang","FR")
st.header(tr("nav_home", lang))
st.write("""
- 🎯 Objectif : prédire la probabilité de défaut client (score 0–100) et fournir des recommandations actionnables.
- 🧱 Stack : Streamlit, scikit-learn, LightGBM, Plotly, SHAP.
- 🧪 Données : Kaggle *Give Me Some Credit* (2011).
- 🔍 Explications : importance globale & locale (SHAP).
- 📦 Fonctions : scoring **individuel** et **batch**, dashboard **métriques**, contexte **macro** (API), **OCDE**.
- 🌍 Langues : FR / EN / ES / IT / ZH.
""")
st.success("Disclaimer : projet démonstratif. Données anonymisées, aucune donnée utilisateur stockée.")
