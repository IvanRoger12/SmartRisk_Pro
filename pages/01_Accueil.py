import streamlit as st
from i18n.strings import tr
from src.ui import use_global_css, get_lang  # ← ajout

use_global_css()                             # ← ajout
lang = get_lang()                            # ← ajout

st.header(tr("nav_home", lang) or "Accueil")

st.markdown("""
**Objectif.** Prédire la probabilité de défaut (score 0–100) et fournir des recommandations actionnables.  
**Stack.** Streamlit, scikit-learn, LightGBM, Plotly, SHAP.  
**Données.** Kaggle « Give Me Some Credit » (2011).  
**Explications.** Importance globale et locale (SHAP).  
**Fonctions.** Scoring individuel et batch, métriques & seuil, contexte macro (API), OCDE.  
**Langues.** FR / EN / ES / IT / ZH.
""")

st.success("Disclaimer : projet démonstratif. Données anonymisées, aucune donnée utilisateur stockée.")
