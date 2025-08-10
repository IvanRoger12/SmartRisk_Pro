import streamlit as st, pandas as pd, joblib
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, auc, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

st.header("Métriques & Explications (globales)")

@st.cache_resource
def load_model(): return joblib.load("models/pipeline.joblib")

try:
    pipe = load_model()
except Exception:
    st.error("Modèle introuvable. Lance d'abord : python src/train.py")
    st.stop()

uploaded = st.file_uploader("Jeu de validation (avec colonne SeriousDlqin2yrs)", type=["csv"])
thr = st.slider("Seuil de décision (sur score 0–100)", 0, 100, 60)

if not uploaded:
    st.caption("Charge un CSV avec la cible SeriousDlqin2yrs pour afficher les métriques.")
    st.stop()

df = pd.read_csv(uploaded)
if "SeriousDlqin2yrs" not in df.columns:
    st.error("Colonne cible 'SeriousDlqin2yrs' manquante.")
    st.stop()

y = df["SeriousDlqin2yrs"].astype(int)
X = df.drop(columns=["SeriousDlqin2yrs"])
proba = pipe.predict_proba(X)[:,1]
auc_roc = roc_auc_score(y, proba)
st.metric("AUC ROC", f"{auc_roc:.3f}")

# ROC
fpr, tpr, _ = roc_curve(y, proba)
fig1, ax1 = plt.subplots()
ax1.plot(fpr, tpr, label=f"ROC (AUC={auc_roc:.2f})")
ax1.plot([0,1],[0,1],"--")
ax1.set_xlabel("FPR"); ax1.set_ylabel("TPR"); ax1.legend()
st.pyplot(fig1)

# PR
prec, rec, _ = precision_recall_curve(y, proba)
pr_auc = auc(rec, prec)
fig2, ax2 = plt.subplots()
ax2.plot(rec, prec, label=f"PR (AUC={pr_auc:.2f})")
ax2.set_xlabel("Recall"); ax2.set_ylabel("Precision"); ax2.legend()
st.pyplot(fig2)

# Confusion au seuil choisi
pred = ( (1 - proba)*100 >= thr ).astype(int)
cm = confusion_matrix(y, pred)
fig3, ax3 = plt.subplots()
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax3)
ax3.set_xlabel("Prédit"); ax3.set_ylabel("Réel")
st.pyplot(fig3)
