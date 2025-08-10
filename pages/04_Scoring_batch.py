import streamlit as st, pandas as pd, joblib

st.header("Scoring batch")

@st.cache_resource
def load_model(): return joblib.load("models/pipeline.joblib")

try:
    pipe = load_model()
except Exception:
    st.error("Modèle introuvable. Lance d'abord : python src/train.py")
    st.stop()

file = st.file_uploader("Importer un CSV clients (features Kaggle)", type=["csv"])
thr = st.slider("Seuil d'acceptation (score)", 0, 100, 60, 1)

if not file:
    st.caption("Le CSV doit contenir les colonnes du dataset Kaggle *Give Me Some Credit* (sans la cible).")
    st.stop()

df = pd.read_csv(file)
probs = pipe.predict_proba(df)[:,1]
df["default_proba"] = probs
df["score_0_100"] = (1 - probs)*100
df["decision"] = (df["score_0_100"] >= thr).map({True:"ACCEPTER", False:"REFUSER"})

st.dataframe(df.head(50))
st.download_button("Télécharger les prédictions", df.to_csv(index=False), "predictions.csv")
