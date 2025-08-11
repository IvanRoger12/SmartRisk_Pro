import streamlit as st, pandas as pd, joblib
from i18n.strings import tr
lang = st.session_state.get("lang","FR")

st.header(tr("nav_batch", lang))

@st.cache_resource
def load_model():
    return joblib.load("models/pipeline.joblib")
try:
    pipe = load_model()
except Exception:
    st.error(tr("needs_model", lang)); st.stop()

file = st.file_uploader(tr("upload", lang), type=["csv"])
if file:
    df = pd.read_csv(file)
    probs = pipe.predict_proba(df)[:,1]
    df["default_proba"] = probs
    df["score_0_100"] = (1 - probs)*100
    st.dataframe(df.head(25), use_container_width=True)
    st.download_button(tr("download", lang), df.to_csv(index=False), "predictions.csv")
else:
    st.caption("Le CSV doit contenir les colonnes du dataset public utilisé.")
