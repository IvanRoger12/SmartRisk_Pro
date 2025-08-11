import streamlit as st
from pathlib import Path

LANG_CODES  = ["FR", "EN", "ES", "IT", "ZH"]
LANG_LABELS = ["Français", "English", "Español", "Italiano", "中文"]

def use_global_css(path: str = "assets/styles.css") -> None:
    """Charge le CSS global sur toutes les pages."""
    p = Path(path)
    if p.exists():
        st.markdown(f"<style>{p.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

def get_lang() -> str:
    """Affiche le sélecteur dans la sidebar et renvoie le code langue."""
    if "lang" not in st.session_state:
        st.session_state["lang"] = "FR"
    with st.sidebar:
        st.markdown("### Langue")
        idx_default = LANG_CODES.index(st.session_state["lang"])
        label = st.selectbox("", LANG_LABELS, index=idx_default, label_visibility="collapsed")
        st.session_state["lang"] = LANG_CODES[LANG_LABELS.index(label)]
    return st.session_state["lang"]
