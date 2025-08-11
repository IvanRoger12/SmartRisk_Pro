import streamlit as st, pandas as pd, numpy as np, plotly.express as px
from i18n.strings import tr
from src.ui import use_global_css, get_lang  # ← ajout

# style global + langue
use_global_css()
lang = get_lang()

st.header(tr("nav_eda", lang) or "Analyse exploratoire")

file = st.file_uploader("CSV (ex: cs-training.csv)", type=["csv"])

def quick_corr(df, k=12):
    num = df.select_dtypes(include=[np.number])
    if num.shape[1] < 2:
        return pd.DataFrame(columns=["feat_1","feat_2","|corr|"])
    c = num.corr(numeric_only=True).abs()
    s = c.unstack().sort_values(ascending=False)
    pairs = [(i, j, v) for (i, j), v in s.items() if i < j][:k]
    return pd.DataFrame(pairs, columns=["feat_1", "feat_2", "|corr|"])

@st.cache_data(show_spinner=False)
def load_csv(_file):
    return pd.read_csv(_file)

if file:
    df = load_csv(file)
    st.write("Shape:", df.shape)
    st.dataframe(df.head(10), use_container_width=True)

    # Valeurs manquantes
    na = (df.isna().mean() * 100).sort_values(ascending=False).round(2)
    st.subheader("Valeurs manquantes (%)")
    st.bar_chart(na.to_frame("pct"))

    # Distributions sur quelques colonnes numériques
    num_cols = df.select_dtypes(include=[np.number]).columns[:6]
    if len(num_cols):
        st.subheader("Distributions")
        for c in num_cols:
            fig = px.histogram(df, x=c, nbins=40, marginal="box")
            st.plotly_chart(fig, use_container_width=True)

    # Top corrélations absolues
    st.subheader("Top corrélations")
    st.dataframe(quick_corr(df), use_container_width=True)
else:
    st.caption("Chargez le CSV d'entraînement pour une EDA rapide.")
