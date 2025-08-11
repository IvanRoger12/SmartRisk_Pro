import streamlit as st, pandas as pd, numpy as np, joblib
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, auc, confusion_matrix
import plotly.graph_objects as go

from i18n.strings import tr
from src.ui import use_global_css, get_lang
from src.utils import find_best_threshold, compute_profit

# --- Style global + langue ---
use_global_css()
lang = get_lang()

st.header(tr("nav_metrics", lang) or "Métriques & seuil")

# --- Modèle en cache ---
@st.cache_resource(show_spinner=True)
def load_model():
    return joblib.load("models/pipeline.joblib")

try:
    pipe = load_model()
except Exception:
    st.error(tr("needs_model", lang) or "Modèle introuvable. Entraînez via src/train.py puis relancez.")
    st.stop()

# Colonnes attendues par le pipeline (si exposées)
expected_cols = getattr(pipe.named_steps.get("impute", pipe), "feature_names_in_", None)

def align_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Aligne df sur l'ordre/jeu de colonnes attendu; ajoute les manquantes en NaN."""
    if expected_cols is None:
        # à défaut, on garde les colonnes numériques
        return df.select_dtypes(include="number")
    out = df.copy()
    for c in expected_cols:
        if c not in out.columns:
            out[c] = np.nan
    return out[list(expected_cols)]

@st.cache_data(show_spinner=False)
def load_csv(_uploaded) -> pd.DataFrame:
    return pd.read_csv(_uploaded, low_memory=False)

uploaded = st.file_uploader(tr("val_csv", lang) or "CSV de validation (avec colonne SeriousDlqin2yrs)", type=["csv"])
if not uploaded:
    st.caption(tr("val_hint", lang) or "Chargez un CSV contenant la colonne cible SeriousDlqin2yrs.")
    st.stop()

df = load_csv(uploaded)
if "SeriousDlqin2yrs" not in df.columns:
    st.error(tr("missing_target", lang) or "Colonne cible 'SeriousDlqin2yrs' manquante.")
    st.stop()

y = df["SeriousDlqin2yrs"].astype(int).values
X = df.drop(columns=["SeriousDlqin2yrs"])
X = align_columns(X)

# Prédictions
try:
    proba = pipe.predict_proba(X)[:, 1]
except Exception as e:
    st.error(f"{tr('pred_error', lang) or 'Erreur de prédiction'} : {e}")
    st.stop()

# AUC
auc_roc = roc_auc_score(y, proba)
st.metric("AUC ROC", f"{auc_roc:.3f}")

# Paramètres business
colA, colB = st.columns(2)
with colA:
    revenue = st.number_input(tr("margin_per_good", lang) or "Marge par client sain (€)",
                              min_value=0, max_value=10000, value=400, step=50)
with colB:
    loss = st.number_input(tr("loss_per_default", lang) or "Perte si défaut (€)",
                           min_value=0, max_value=20000, value=2000, step=100)

# Seuil optimal orienté profit
t_opt, best_profit = find_best_threshold(y, proba, revenue, loss)
st.success(f"{tr('opt_threshold', lang) or 'Seuil optimal (profit)'} : {t_opt:.2f} | "
           f"{tr('est_profit', lang) or 'Profit estimé'} : {best_profit:,.0f} €".replace(",", " "))

# Seuil sélectionné
thresh = st.slider(tr("accept_threshold", lang) or "Seuil d'acceptation (1 = plus strict)",
                   0.0, 1.0, float(t_opt), step=0.01)

# Profit et confusion matrix au seuil choisi
profit, nb_ok, nb_bad, accepted = compute_profit(y, proba, thresh, revenue, loss)
tn, fp, fn, tp = confusion_matrix(y, (proba >= thresh).astype(int), labels=[0, 1]).ravel()

c1, c2, c3, c4 = st.columns(4)
c1.metric(tr("kpi_accepted", lang) or "Acceptés", int(accepted))
c2.metric(tr("kpi_ok", lang) or "OK acceptés", int(nb_ok))
c3.metric(tr("kpi_bad", lang) or "Bad acceptés", int(nb_bad))
c4.metric(tr("kpi_profit", lang) or "Profit estimé", f"{profit:,.0f} €".replace(",", " "))

# Courbe ROC
fpr, tpr, _ = roc_curve(y, proba)
fig = go.Figure()
fig.add_trace(go.Scatter(x=fpr, y=tpr, name=f"ROC AUC={auc_roc:.2f}", mode="lines"))
fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Référence", line=dict(dash="dash")))
fig.update_layout(xaxis_title="Taux de faux positifs (FPR)", yaxis_title="Taux de vrais positifs (TPR)")
st.plotly_chart(fig, use_container_width=True)

# Courbe Precision-Recall
prec, rec, _ = precision_recall_curve(y, proba)
pr_auc = auc(rec, prec)
fig2 = go.Figure(go.Scatter(x=rec, y=prec, name=f"PR AUC={pr_auc:.2f}", mode="lines"))
fig2.update_layout(xaxis_title="Recall", yaxis_title="Precision")
st.plotly_chart(fig2, use_container_width=True)

# Profit vs seuil
grid = np.linspace(0.01, 0.99, 60)
profits = [compute_profit(y, proba, float(t), revenue, loss)[0] for t in grid]
fig3 = go.Figure(go.Scatter(x=grid, y=profits, mode="lines+markers", name="Profit"))
fig3.add_vline(x=thresh, line_dash="dash", annotation_text=f"{tr('threshold', lang) or 'Seuil'} {thresh:.2f}")
fig3.update_layout(xaxis_title=tr("x_threshold", lang) or "Seuil (plus élevé = plus strict)",
                   yaxis_title=tr("y_profit", lang) or "Profit estimé (€)")
st.plotly_chart(fig3, use_container_width=True)

# Tableau seuils & KPI + export
def kpi_table(ths):
    rows = []
    for t in ths:
        pr, ok, bad, acc = compute_profit(y, proba, float(t), revenue, loss)
        yhat = (proba >= t).astype(int)
        tn2, fp2, fn2, tp2 = confusion_matrix(y, yhat, labels=[0, 1]).ravel()
        precision = tp2 / max(tp2 + fp2, 1)
        recall = tp2 / max(tp2 + fn2, 1)
        f1 = 2 * precision * recall / max(precision + recall, 1e-9)
        rows.append({
            "threshold": round(float(t), 3),
            "profit": pr,
            "accept_rate": acc / len(y),
            "precision": precision,
            "recall": recall,
            "f1": f1
        })
    return pd.DataFrame(rows)

tbl = kpi_table(grid)
st.subheader(tr("kpi_table_title", lang) or "KPI par seuil")
st.dataframe(tbl.round(4), use_container_width=True)
st.download_button(tr("download_table", lang) or "Télécharger le tableau",
                   tbl.to_csv(index=False).encode("utf-8"),
                   file_name="kpi_vs_threshold.csv", mime="text/csv")
