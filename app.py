import streamlit as st
from i18n.strings import LANGS, tr

st.set_page_config(page_title="SmartRisk Pro", layout="wide")
if "lang" not in st.session_state:
    st.session_state["lang"] = "FR"

with st.sidebar:
    st.session_state["lang"] = st.selectbox("🌍 Lang / Language", LANGS, index=LANGS.index(st.session_state["lang"]))

lang = st.session_state["lang"]
st.title(tr("brand", lang))
st.caption(tr("subtitle", lang))
st.markdown(f"> {tr('author', lang)}")
st.write("Utilise le menu **Pages** (à gauche) pour naviguer : Accueil · Analyse · Scoring individuel · Batch · Métriques · Macro (API) · OCDE.")
