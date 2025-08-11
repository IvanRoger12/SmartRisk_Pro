from pathlib import Path
import streamlit as st

CSS_PATH = Path("assets/styles.css")
LANGS = ["FR","EN","ES","IT","ZH"]  # pas de doublon, "IT" (pas "IL")

def use_global_css():
    try:
        css = CSS_PATH.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.write(f"[styles.css introuvable] {e}")

def get_lang():
    if "lang" not in st.session_state:
        st.session_state["lang"] = "FR"
    with st.sidebar:
        st.markdown("### Langue / Language")
        choice = st.selectbox("UI Language", LANGS, index=LANGS.index(st.session_state["lang"]))
        st.session_state["lang"] = choice
        # badge build pour vérifier que le bon code tourne
        st.caption("build: ui-v1.0")
    return st.session_state["lang"]
