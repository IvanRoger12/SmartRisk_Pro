import streamlit as st, pandas as pd, joblib, plotly.graph_objects as go
import shap, numpy as np

lang = st.session_state.get("lang","FR")
st.header("Scoring individuel")

@st.cache_resource
def load_model(): return joblib.load("models/pipeline.joblib")

try:
    pipe = load_model()
except Exception:
    st.error("Modèle introuvable. Lance d'abord : python src/train.py")
    st.stop()

with st.form("form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        MonthlyIncome = st.number_input("MonthlyIncome", 0, 100000, 3000, step=100)
        DebtRatio = st.number_input("DebtRatio", 0.0, 5.0, 0.35, step=0.01)
        age = st.number_input("age", 18, 100, 35)
    with col2:
        N30 = st.number_input("NumberOfTime30-59DaysPastDueNotWorse", 0, 50, 0)
        N60 = st.number_input("NumberOfTime60-89DaysPastDueNotWorse", 0, 50, 0)
        N90 = st.number_input("NumberOfTimes90DaysLate", 0, 50, 0)
    with col3:
        Util = st.number_input("RevolvingUtilizationOfUnsecuredLines", 0.0, 5.0, 0.25, step=0.01)
        NOpen = st.number_input("NumberOfOpenCreditLinesAndLoans", 0, 80, 6)
        NRE = st.number_input("NumberRealEstateLoansOrLines", 0, 50, 1)
        NDeps = st.number_input("NumberOfDependents", 0, 20, 0)
    go_btn = st.form_submit_button("Scorer")

if not go_btn: st.stop()

row = pd.DataFrame([{
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

p = pipe.predict_proba(row)[:,1][0]
score = int((1 - p)*100)

st.metric("Score (0–100)", score)
st.caption(f"Probabilité de défaut : {p:.3f}")

fig = go.Figure(go.Indicator(mode="gauge+number", value=score, title={"text":"Score (0–100)"},
    gauge={'axis': {'range': [0, 100]}, 'bar': {'thickness': 0.3},
           'steps': [{'range':[0,40],'color':'#fce8e6'},{'range':[40,70],'color':'#fff4cc'},{'range':[70,100],'color':'#e6f4ea'}]}))
st.plotly_chart(fig, use_container_width=True)

tips=[]
if DebtRatio>0.4: tips.append("Réduire DebtRatio < 40%")
if N30>0 or N60>0 or N90>0: tips.append("Éviter les retards de paiement")
if Util>0.6: tips.append("Baisser l'utilisation du crédit renouvelable")
st.info("Recommandations : " + ("; ".join(tips) if tips else "Profil sain"))

# SHAP local (explication individuelle)
try:
    clf = pipe.named_steps["clf"]
    background = np.zeros((1, row.shape[1]))  # baseline neutre
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(row)[1] if isinstance(explainer.shap_values(row), list) else explainer.shap_values(row)
    st.subheader("Explication locale (SHAP)")
    shap.initjs()
    st.pyplot(shap.force_plot(explainer.expected_value[1] if isinstance(explainer.expected_value, list) else explainer.expected_value,
                               shap_values, row, matplotlib=True, show=False, figsize=(8,1.8)))
except Exception:
    st.warning("SHAP local indisponible dans cet environnement. Teste en local si besoin.")
