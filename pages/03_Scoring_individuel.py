import streamlit as st, pandas as pd, numpy as np, joblib, plotly.graph_objects as go
import shap
from i18n.strings import tr
lang = st.session_state.get("lang","FR")

st.header(tr("nav_score", lang))

@st.cache_resource
def load_model():
    return joblib.load("models/pipeline.joblib")
try:
    pipe = load_model()
except Exception:
    st.error(tr("needs_model", lang)); st.stop()

with st.form("form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        MonthlyIncome = st.number_input("MonthlyIncome", 0, 200000, 3000, step=100)
        DebtRatio = st.number_input("DebtRatio", 0.0, 5.0, 0.35, step=0.01)
        age = st.number_input("Age", 18, 100, 35)
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

if go_btn:
    x = pd.DataFrame([{
        "MonthlyIncome": MonthlyIncome, "DebtRatio": DebtRatio, "age": age,
        "NumberOfTime30-59DaysPastDueNotWorse": N30, "NumberOfTime60-89DaysPastDueNotWorse": N60,
        "NumberOfTimes90DaysLate": N90, "RevolvingUtilizationOfUnsecuredLines": Util,
        "NumberOfOpenCreditLinesAndLoans": NOpen, "NumberRealEstateLoansOrLines": NRE,
        "NumberOfDependents": NDeps
    }])

    pd_hat = float(pipe.predict_proba(x)[:,1][0])
    score = int((1 - pd_hat)*100)

    c1, c2 = st.columns([1.2,1])
    with c1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=score, title={"text": tr("score", lang)},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'thickness': 0.35},
                   'steps': [{'range':[0,40],'color':'#fdecea'},
                             {'range':[40,70],'color':'#fff4cc'},
                             {'range':[70,100],'color':'#e6f4ea'}]}))
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"{tr('defprob', lang)} : {pd_hat:.3f}")

    with c2:
        exp_loss_rate = pd_hat
        gross_margin_rate = 0.18
        safe_limit = max(0, int((gross_margin_rate / max(exp_loss_rate,1e-6)) * 1000))
        st.markdown("Proposition")
        st.write(f"Limite indicative: {safe_limit} € (démo)")
        tips=[]
        if DebtRatio>0.4: tips.append("Réduire le DebtRatio sous 40%.")
        if N30+N60+N90>0: tips.append("Supprimer les retards de paiement.")
        if Util>0.6: tips.append("Baisser l'utilisation du revolving <60%.")
        st.info(("; ".join(tips)) if tips else tr("healthy", lang))

    st.subheader("What-if")
    delta_debt = st.slider("Variation de DebtRatio", -0.3, 0.3, -0.05, step=0.01)
    x2 = x.copy(); x2["DebtRatio"] = np.clip(x2["DebtRatio"] + delta_debt, 0, 5)
    pd2 = float(pipe.predict_proba(x2)[:,1][0]); score2 = int((1-pd2)*100)
    st.write(f"Si DebtRatio change de {delta_debt:+.2f} → score {score2} (PD {pd2:.3f})")

    try:
        explainer = shap.TreeExplainer(pipe.named_steps["clf"])
        x_imp = pd.DataFrame(pipe.named_steps["impute"].transform(x), columns=x.columns)
        sv = explainer(x_imp)
        shap.plots.bar(sv[0], show=False)
        st.pyplot(bbox_inches="tight")
    except Exception:
        st.caption("Explications locales indisponibles ici (SHAP).")
