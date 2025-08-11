import streamlit as st, pandas as pd, numpy as np, joblib
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, auc, confusion_matrix
import plotly.graph_objects as go
from i18n.strings import tr
from src.utils import find_best_threshold, compute_profit
lang = st.session_state.get("lang","FR")

st.header(tr("nav_metrics", lang))

@st.cache_resource
def load_model():
    return joblib.load("models/pipeline.joblib")
try:
    pipe = load_model()
except Exception:
    st.error(tr("needs_model", lang)); st.stop()

uploaded = st.file_uploader(tr("val_csv", lang), type=["csv"])
if not uploaded:
    st.caption("Uploadez un CSV contenant la colonne SeriousDlqin2yrs."); st.stop()

df = pd.read_csv(uploaded)
if "SeriousDlqin2yrs" not in df.columns:
    st.error("Colonne cible 'SeriousDlqin2yrs' manquante."); st.stop()

y = df["SeriousDlqin2yrs"].astype(int).values
X = df.drop(columns=["SeriousDlqin2yrs"])
proba = pipe.predict_proba(X)[:,1]
auc_roc = roc_auc_score(y, proba)
st.metric("AUC ROC", f"{auc_roc:.3f}")

# paramètres métier
colA, colB = st.columns(2)
with colA:  revenue = st.number_input("Marge par client sain (€)", 0, 10000, 400)
with colB:  loss    = st.number_input("Perte si défaut (€)", 0, 20000, 2000)

# seuil optimal (profit)
t_opt, best_profit = find_best_threshold(y, proba, revenue, loss)
st.success(f"Seuil optimal (profit): {t_opt:.2f} | Profit estimé: {best_profit:,.0f} €".replace(",", " "))

thresh = st.slider("Seuil d'acceptation (1=plus strict)", 0.0, 1.0, float(t_opt), step=0.01)

# métriques + profit au seuil choisi
profit, nb_ok, nb_bad, accepted = compute_profit(y, proba, thresh, revenue, loss)
tn, fp, fn, tp = confusion_matrix(y, (proba>=thresh).astype(int)).ravel()
c1,c2,c3,c4 = st.columns(4)
c1.metric("Acceptés", accepted); c2.metric("OK acceptés", nb_ok); c3.metric("Bad acceptés", nb_bad)
c4.metric("Profit estimé", f"{profit:,.0f} €".replace(",", " "))

# courbes
fpr,tpr,_=roc_curve(y, proba)
fig = go.Figure()
fig.add_trace(go.Scatter(x=fpr, y=tpr, name=f"ROC AUC={auc_roc:.2f}"))
fig.add_trace(go.Scatter(x=[0,1],y=[0,1],mode="lines",name="Chance",line=dict(dash="dash")))
fig.update_layout(xaxis_title="FPR", yaxis_title="TPR"); st.plotly_chart(fig, use_container_width=True)

prec, rec, _ = precision_recall_curve(y, proba)
pr_auc = auc(rec, prec)
fig2 = go.Figure(go.Scatter(x=rec, y=prec, name=f"PR AUC={pr_auc:.2f}"))
fig2.update_layout(xaxis_title="Recall", yaxis_title="Precision"); st.plotly_chart(fig2, use_container_width=True)

grid = np.linspace(0.01, 0.99, 60)
profits=[]
for t in grid:
    profits.append(compute_profit(y, proba, float(t), revenue, loss)[0])
fig3 = go.Figure(go.Scatter(x=grid, y=profits, mode="lines+markers", name="Profit"))
fig3.add_vline(x=thresh, line_dash="dash", annotation_text=f"Seuil {thresh:.2f}")
fig3.update_layout(xaxis_title="Seuil (plus élevé = plus strict)", yaxis_title="Profit estimé (€)")
st.plotly_chart(fig3, use_container_width=True)
