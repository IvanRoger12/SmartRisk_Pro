import streamlit as st, pandas as pd, numpy as np, joblib
import plotly.graph_objects as go
import shap
import matplotlib.pyplot as plt

from i18n.strings import tr
from src.ui import use_global_css, get_lang  # CSS global + langue

# --- Style global + langue (toujours en haut) ---
use_global_css()
lang = get_lang()

st.header(tr("nav_score", lang) or "Notation individuelle")

# --- Chargement modèle (cache) ---
@st.cache_resource(show_spinner=True)
def load_model():
    return joblib.load("models/pipeline.joblib")

try:
    pipe = load_model()
except Exception:
    st.error(tr("needs_model", lang) or "Modèle introuvable. Entraînez via src/train.py puis relancez.")
    st.stop()

# Colonnes attendues (ordre identique à l’entraînement) si dispo
expected_cols = getattr(pipe.named_steps.get("impute", pipe), "feature_names_in_", None)

def align_columns(df: pd.DataFrame) -> pd.DataFrame:
    if expected_cols is None:
        return df
    # ajoute colonnes manquantes et réordonne
    out = df.copy()
    for c in expected_cols:
        if c not in out.columns:
            out[c] = np.nan
    return out[list(expected_cols)]

with st.form("form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        MonthlyIncome = st.number_input("MonthlyIncome", min_value=0, max_value=200_000, value=3000, step=100)
        DebtRatio = st.number_input("DebtRatio", min_value=0.0, max_value=5.0, value=0.35, step=0.01, format="%.2f")
        age = st.number_input("Age", min_value=18, max_value=100, value=35, step=1)
    with col2:
        N30 = st.number_input("NumberOfTime30-59DaysPastDueNotWorse", min_value=0, max_value=50, value=0)
        N60 = st.number_input("NumberOfTime60-89DaysPastDueNotWorse", min_value=0, max_value=50, value=0)
        N90 = st.number_input("NumberOfTimes90DaysLate", min_value=0, max_value=50, value=0)
    with col3:
        Util = st.number_input("RevolvingUtilizationOfUnsecuredLines", min_value=0.0, max_value=5.0, value=0.25, step=0.01, format="%.2f")
        NOpen = st.number_input("NumberOfOpenCreditLinesAndLoans", min_value=0, max_value=80, value=6)
        NRE = st.number_input("NumberRealEstateLoansOrLines", min_value=0, max_value=50, value=1)
        NDeps = st.number_input("NumberOfDependents", min_value=0, max_value=20, value=0)
    go_btn = st.form_submit_button(tr("score_btn", lang) or "Scorer")

if go_btn:
    x = pd.DataFrame([{
        "MonthlyIncome": MonthlyIncome,
        "DebtRatio": DebtRatio,
        "age": age,
        "NumberOfTime30-59DaysPastDueNotWorse": N30,
        "NumberOfTime60-89DaysPastDueNotWorse": N60,
        "NumberOfTimes90DaysLate": N90,
        "RevolvingUtilizationOfUnsecuredLines": Util,
        "NumberOfOpenCreditLinesAndLoans": NOpen,
        "NumberRealEstateLoansOrLines": NRE,
        "NumberOfDependents": NDeps
    }])
    x = align_columns(x)

    # Prédiction
    try:
        pd_hat = float(pipe.predict_proba(x)[:, 1][0])
    except Exception as e:
        st.error(f"Erreur de prédiction : {e}")
        st.stop()

    score = int((1 - pd_hat) * 100)

    c1, c2 = st.columns([1.2, 1])
    with c1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": tr("score", lang) or "Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"thickness": 0.35},
                "steps": [
                    {"range": [0, 40], "color": "#fdecea"},
                    {"range": [40, 70], "color": "#fff4cc"},
                    {"range": [70, 100], "color": "#e6f4ea"},
                ],
            },
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"{tr('defprob', lang) or 'Probabilité de défaut'} : {pd_hat:.3f}")

    with c2:
        # Démo simple de limite "safe" (à adapter selon ton métier)
        exp_loss_rate = pd_hat
        gross_margin_rate = 0.18
        safe_limit = max(0, int((gross_margin_rate / max(exp_loss_rate, 1e-6)) * 1000))
        st.markdown(tr("proposal", lang) or "Proposition")
        st.write(f"{tr('limit', lang) or 'Limite indicative'} : {safe_limit} €")
        tips = []
        if DebtRatio > 0.4:
            tips.append(tr("tip_debt", lang) or "Réduire le DebtRatio sous 40%.")
        if (N30 + N60 + N90) > 0:
            tips.append(tr("tip_late", lang) or "Supprimer les retards de paiement.")
        if Util > 0.6:
            tips.append(tr("tip_util", lang) or "Baisser l'utilisation du revolving <60%.")
        st.info(("; ".join(tips)) if tips else (tr("healthy", lang) or "Profil sain à ce stade."))

    # What-if (variation sur DebtRatio)
    st.subheader(tr("what_if", lang) or "What-if")
    delta_debt = st.slider(tr("what_if_debt", lang) or "Variation de DebtRatio", -0.3, 0.3, -0.05, step=0.01)
    x2 = x.copy()
    x2["DebtRatio"] = np.clip(x2["DebtRatio"] + delta_debt, 0, 5)
    pd2 = float(pipe.predict_proba(x2)[:, 1][0])
    score2 = int((1 - pd2) * 100)
    st.write(f"{tr('what_if_result', lang) or 'Si DebtRatio change de'} {delta_debt:+.2f} → {tr('score', lang) or 'score'} {score2} (PD {pd2:.3f})")

    # Explications locales (SHAP)
    st.subheader(tr("explain_local", lang) or "Explications locales")
    try:
        @st.cache_resource(show_spinner=False)
        def get_explainer(clf):
            return shap.TreeExplainer(clf)

        clf = pipe.named_steps.get("clf", None)
        impute = pipe.named_steps.get("impute", None)
        if clf is None or impute is None:
            raise RuntimeError("Pipeline inattendu (pas d'étapes 'impute' et 'clf').")

        x_imp = pd.DataFrame(impute.transform(x), columns=expected_cols if expected_cols is not None else x.columns)
        explainer = get_explainer(clf)
        sv = explainer(x_imp)
        shap.plots.bar(sv[0], show=False)
        st.pyplot(plt.gcf(), clear_figure=True)
    except Exception:
        st.caption(tr("shap_unavailable", lang) or "Explications SHAP indisponibles ici.")
