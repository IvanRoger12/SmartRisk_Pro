import streamlit as st
from src.ui import use_global_css, get_lang
from i18n.strings import tr

st.set_page_config(page_title="SmartRisk Pro", layout="wide", initial_sidebar_state="expanded")

# CSS global + langue (à appeler tout en haut)
use_global_css()
lang = get_lang()

# HERO
st.markdown(f"""
<div class="hero">
  <div class="title">SmartRisk Pro — {tr("brand", lang).split("—")[-1].strip()}</div>
  <div class="sub">{tr("subtitle", lang)}</div>
  <div class="badges">
    <span>Scoring temps réel</span>
    <span>Explicabilité</span>
    <span>Dashboard KPI</span>
    <span>Seuil orienté profit</span>
    <span>FR/EN/ES/IT/ZH</span>
  </div>
  <div class="cta">
    <a class="primary" href="#go" target="_self">Accéder aux pages</a>
    <a href="https://github.com/IvanRoger12/SmartRisk_Pro" target="_blank">GitHub</a>
    <a href="mailto:nfindaroger@gmail.com">Contact</a>
  </div>
</div>
""", unsafe_allow_html=True)

# Tuiles métriques
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="card"><div style="font-size:1.6rem;font-weight:800">0.80–0.85</div><div>AUC sur dataset public</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="card"><div style="font-size:1.6rem;font-weight:800">~10 ms</div><div>Latence de scoring</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="card"><div style="font-size:1.6rem;font-weight:800">5</div><div>Langues UI</div></div>', unsafe_allow_html=True)

# Accès rapide vers les pages
st.markdown('<div id="go"></div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("#### Analyse exploratoire")
    st.markdown(tr("home_eda", lang))
    st.page_link("pages/02_Analyse_exploratoire.py", label="Ouvrir")
with c2:
    st.markdown("#### Notation individuelle")
    st.markdown(tr("home_score", lang))
    st.page_link("pages/03_Scoring_individuel.py", label="Ouvrir")
with c3:
    st.markdown("#### Métriques et seuil")
    st.markdown("Optimisez le seuil selon profit/perte.")
    st.page_link("pages/05_Metriques_Explications.py", label="Ouvrir")

# Liens secondaires si tu les as
st.markdown("")
c4, c5, c6 = st.columns(3)
with c4:
    st.markdown("#### Lot de notation")
    st.page_link("pages/04_Batch_scoring.py", label="Ouvrir")
with c5:
    st.markdown("#### Macro (FX / API)")
    st.page_link("pages/06_Contexte_macro_FX_API.py", label="Ouvrir")
with c6:
    st.markdown("#### OCDE / Qualité & Drift")
    st.page_link("pages/07_OCDE.py", label="Ouvrir")

st.divider()
st.caption(f"{tr('author', lang)} — démo éducationnelle (non contractuelle).")
