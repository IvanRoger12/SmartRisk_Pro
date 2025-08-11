import streamlit as st, pandas as pd, numpy as np, plotly.express as px
from i18n.strings import tr
lang = st.session_state.get("lang","FR")

st.header(tr("nav_eda", lang))
file = st.file_uploader("CSV (ex: cs-training.csv)", type=["csv"])

def quick_corr(df, k=12):
    num = df.select_dtypes(include=[np.number])
    c = num.corr().abs()
    s = c.unstack().sort_values(ascending=False)
    pairs = [(i,j,v) for (i,j),v in s.items() if i<j][:k]
    return pd.DataFrame(pairs, columns=["feat_1","feat_2","|corr|"])

if file:
    df = pd.read_csv(file)
    st.write("Shape:", df.shape)
    st.dataframe(df.head(10), use_container_width=True)

    na = (df.isna().mean()*100).sort_values(ascending=False)
    st.subheader("Valeurs manquantes (%)")
    st.bar_chart(na)

    num_cols = df.select_dtypes(include=[np.number]).columns[:6]
    if len(num_cols):
        st.subheader("Distributions")
        for c in num_cols:
            fig = px.histogram(df, x=c, nbins=40, marginal="box")
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top corrélations")
    st.dataframe(quick_corr(df), use_container_width=True)
else:
    st.caption("Chargez le CSV d'entraînement pour une EDA rapide.")
