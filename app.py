import streamlit as st
from i18n.strings import tr

st.set_page_config(page_title="SmartRisk Pro", layout="wide")

LANG_OPTIONS = {
    "Français": "FR",
    "English": "EN",
    "Español": "ES",
    "Italiano": "IT",
    "中文": "ZH",
}
if "lang" not in st.session_state:
    st.session_state["lang"] = "FR"
with st.sidebar:
    st.markdown("### Lang / Language")
    choice = st.selectbox("", list(LANG_OPTIONS.keys()), index=0, label_visibility="collapsed")
    st.session_state["lang"] = LANG_OPTIONS[choice]
lang = st.session_state["lang"]

st.markdown("""
<style>
.block-container { padding-top: 1.4rem; }
.hero { border-radius: 28px; padding: 56px; position: relative; overflow: hidden;
  background: radial-gradient(1000px 560px at 10% -20%, #e6f0ff 0%, transparent 60%),
              radial-gradient(1000px 560px at 110% 0%, #fff3e6 0%, transparent 60%),
              linear-gradient(135deg, #0B72E710, #22c1c311);
  border: 1px solid #edf2ff; }
.hero h1 { font-size: 3.2rem; line-height: 1.1; margin: 0 0 10px 0;
  background: linear-gradient(90deg, #0B72E7, #22c1c3);
  -webkit-background-clip: text; background-clip: text; color: transparent; font-weight: 800; }
.badges span{ display:inline-block; margin-right:10px; margin-top:10px; padding:7px 12px;
  border-radius: 999px; font-size:.9rem; background:#F5F7FB; border:1px solid #E6ECF5; }
.card { border-radius: 18px; padding: 18px; border:1px solid #eef2f7; background:#fff;
  box-shadow: 0 10px 26px rgba(20,20,20,.06); }
.cta {display:flex; gap:12px; margin-top:20px; flex-wrap: wrap;}
.cta a { text-decoration:none; padding:12px 16px; border-radius:12px; font-weight:700;
  border:1px solid #0B72E722; background:#0B72E710; color:#0B72E7; }
.cta a.primary { background:#0B72E7; color:#fff; border-color:#0B72E7; }
.small {opacity:.8}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="hero">
  <h1>SmartRisk Pro — {tr("brand", lang).split("—")[-1].strip()}</h1>
  <div class="small">{tr("subtitle", lang)}</div>
  <div class="badges">
    <span>Real-time scoring</span><span>Explainable AI</span>
    <span>KPI Dashboard</span><span>Profit-aware Threshold</span><span>FR/EN/ES/IT/ZH</span>
  </div>
  <div class="cta">
    <a class="primary" href="#go" target="_self">{tr("cta_start", lang)}</a>
    <a href="https://github.com/IvanRoger12/SmartRisk_Pro" target="_blank">GitHub</a>
    <a href="mailto:nfindaroger@gmail.com">Contact</a>
  </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.markdown('<div class="card"><div style="font-size:1.8rem;font-weight:800">0.80–0.85</div><div>AUC (dataset public)</div></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="card"><div style="font-size:1.8rem;font-weight:800">~10 ms</div><div>Latence scoring</div></div>', unsafe_allow_html=True)
with c3: st.markdown('<div class="card"><div style="font-size:1.8rem;font-weight:800">5</div><div>Langues UI</div></div>', unsafe_allow_html=True)

st.markdown('<div id="go"></div>', unsafe_allow_html=True)
st.write("")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("#### " + tr("nav_eda", lang))
    st.markdown(tr("home_eda", lang))
    st.page_link("pages/02_Analyse_exploratoire.py", label=tr("open_eda", lang))
with c2:
    st.markdown("#### " + tr("nav_score", lang))
    st.markdown(tr("home_score", lang))
    st.page_link("pages/03_Scoring_individuel.py", label=tr("open_score", lang))
with c3:
    st.markdown("#### Seuil & Profit")
    st.markdown("Optimisez le seuil selon coût du risque et marge.")
    st.page_link("pages/05_Metriques_Explications.py", label="Voir les métriques & seuil")

st.divider()
st.caption(f"© {tr('author', lang)} — démo éducationnelle, non contractuelle.")
