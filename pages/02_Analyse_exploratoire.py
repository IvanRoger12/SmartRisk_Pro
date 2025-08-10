import streamlit as st, pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns

lang = st.session_state.get("lang","FR")
st.header("Analyse exploratoire")

file = st.file_uploader("CSV (ex: cs-training.csv)", type=["csv"])
if not file:
    st.caption("Charge le CSV pour une EDA rapide.")
    st.stop()

df = pd.read_csv(file)
st.write("Shape:", df.shape)
st.dataframe(df.head(10))

st.subheader("Valeurs manquantes (%)")
na = df.isna().mean().sort_values(ascending=False) * 100
st.bar_chart(na)

st.subheader("Top corrélations avec la cible (si présente)")
if "SeriousDlqin2yrs" in df.columns:
    corr = df.corr(numeric_only=True)["SeriousDlqin2yrs"].dropna().sort_values(ascending=False)
    st.write(corr.to_frame("Correlation"))
else:
    st.info("Pas de colonne cible dans le CSV (SeriousDlqin2yrs).")

st.subheader("Distribution (quelques variables num.)")
cols = [c for c in df.columns if df[c].dtype != 'object'][:6]
for c in cols:
    fig, ax = plt.subplots()
    ax.hist(df[c].dropna(), bins=40)
    ax.set_title(c)
    st.pyplot(fig)
