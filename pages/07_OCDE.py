import io, glob, requests
import pandas as pd
import streamlit as st
import plotly.express as px

st.header("Indicateurs OCDE")
st.caption("Charge un CSV OCDE local ou colle une URL CSV de l’API OCDE.")

@st.cache_data(show_spinner=False, ttl=3600)
def load_csv_from_url(url: str) -> pd.DataFrame:
    r = requests.get(url, timeout=20); r.raise_for_status()
    try:
        return pd.read_csv(io.BytesIO(r.content))
    except Exception:
        return pd.read_csv(io.BytesIO(r.content), sep=";", encoding="latin-1")

@st.cache_data(show_spinner=False)
def load_csv_from_path(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.read_csv(path, sep=";", encoding="latin-1")

tab1, tab2 = st.tabs(["Fichier local","URL API"])

df = None
with tab1:
    candidates = sorted(glob.glob("data/external/oecd/*.csv"))
    if candidates:
        choice = st.selectbox("Fichiers trouvés", ["—"] + candidates)
        if choice and choice != "—":
            df = load_csv_from_path(choice)
    uploaded = st.file_uploader("Uploader un CSV OCDE", type=["csv"])
    if uploaded: df = pd.read_csv(uploaded)

with tab2:
    url = st.text_input("URL CSV (export OCDE)", placeholder="https://stats.oecd.org/...csv")
    if url:
        try: df = load_csv_from_url(url)
        except Exception as e: st.error(f"URL invalide ou indisponible : {e}")

if df is None:
    st.stop()

# choix colonnes
time_candidates    = ["TIME_PERIOD","TIME","Year","year","DATE","Time","ObsTime"]
value_candidates   = ["Value","OBS_VALUE","value","obs_value","Data","OBS","Observation Value"]
country_candidates = ["LOCATION","Country","REF_AREA","GEO","LOCATION_NAME","Area","Country Name"]
indic_candidates   = ["SUBJECT","INDICATOR","MEASURE","Indicator","Series","Subject","INDICATOR_ID"]

def pick(cols, dfcols):
    for c in cols:
        if c in dfcols: return c
    return None

c1,c2,c3,c4 = st.columns(4)
time_col    = c1.selectbox("Colonne temps",    ["—"]+df.columns.tolist(), index=(["—"]+df.columns.tolist()).index(pick(time_candidates,df.columns)) if pick(time_candidates,df.columns) in df.columns else 0)
value_col   = c2.selectbox("Colonne valeur",   ["—"]+df.columns.tolist(), index=(["—"]+df.columns.tolist()).index(pick(value_candidates,df.columns)) if pick(value_candidates,df.columns) in df.columns else 0)
country_col = c3.selectbox("Colonne pays",     ["—"]+df.columns.tolist(), index=(["—"]+df.columns.tolist()).index(pick(country_candidates,df.columns)) if pick(country_candidates,df.columns) in df.columns else 0)
indic_col   = c4.selectbox("Colonne indicateur (opt.)", ["—"]+df.columns.tolist(), index=(["—"]+df.columns.tolist()).index(pick(indic_candidates,df.columns)) if pick(indic_candidates,df.columns) in df.columns else 0)

if time_col == "—" or value_col == "—":
    st.error("Choisis au minimum la colonne temps et la colonne valeur.")
    st.stop()

work = df.copy()
work[time_col] = work[time_col].astype(str)

ff1, ff2, ff3 = st.columns(3)
countries = ff1.multiselect("Pays", sorted(work[country_col].dropna().astype(str).unique())) if country_col!="—" else []
indics    = ff2.multiselect("Indicateur", sorted(work[indic_col].dropna().astype(str).unique())) if indic_col!="—" else []

# période (si année numérique)
try:
    years = sorted(list(map(int, work[time_col].astype(str).unique())))
    y_start, y_end = ff3.slider("Période (année)", min_value=min(years), max_value=max(years), value=(min(years), max(years)))
    work = work[work[time_col].astype(int).between(y_start, y_end)]
except Exception:
    pass

if countries: work = work[work[country_col].astype(str).isin(countries)]
if indics:    work = work[work[indic_col].astype(str).isin(indics)]

color_col = country_col if country_col!="—" else (indic_col if indic_col!="—" else None)
fig = px.line(work.sort_values(time_col), x=time_col, y=value_col, color=color_col, markers=False, title="Évolution")
st.plotly_chart(fig, use_container_width=True)
st.dataframe(work.head(50))
st.download_button("Télécharger les données filtrées", work.to_csv(index=False).encode("utf-8"), "oecd_filtered.csv", "text/csv")
