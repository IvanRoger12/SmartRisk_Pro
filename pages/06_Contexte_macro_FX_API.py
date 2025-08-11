import os, io, textwrap, datetime as dt
import streamlit as st, pandas as pd, requests
from requests.adapters import HTTPAdapter, Retry

st.header("Contexte macro (FX / API)")

base_ccy = st.selectbox("Devise de base", ["USD","EUR","GBP","JPY","CNY"], index=1)
symbols = st.multiselect("Devises à suivre", ["USD","EUR","GBP","JPY","CNY"], default=["USD","GBP","CNY"])
days = st.slider("Jours d'historique", 7, 120, 30)

ASSET_PATH = "assets/fx_sample.csv"

FX_SAMPLE_CSV = textwrap.dedent("""\
date,USD,GBP,JPY,CNY,EUR
2024-04-01,1.0000,0.7900,151.0,7.22,0.92
2024-04-08,1.0000,0.7850,152.5,7.23,0.93
2024-04-15,1.0000,0.8000,154.0,7.24,0.94
2024-04-22,1.0000,0.7980,153.2,7.20,0.93
2024-04-29,1.0000,0.8040,155.1,7.22,0.94
2024-05-06,1.0000,0.8120,156.3,7.24,0.93
2024-05-13,1.0000,0.8080,157.0,7.25,0.92
""")

def ensure_sample_exists():
    os.makedirs(os.path.dirname(ASSET_PATH), exist_ok=True)
    if not os.path.exists(ASSET_PATH):
        with open(ASSET_PATH, "w", encoding="utf-8") as f:
            f.write(FX_SAMPLE_CSV)

def session_with_retries():
    s = requests.Session()
    retries = Retry(total=3, backoff_factor=0.6, status_forcelist=[429,500,502,503,504])
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://", HTTPAdapter(max_retries=retries))
    return s

def get_exchangerate_host(base, symbols, start, end):
    url = f"https://api.exchangerate.host/timeseries?start_date={start}&end_date={end}&base={base}&symbols={','.join(symbols)}"
    r = session_with_retries().get(url, timeout=12)
    r.raise_for_status()
    data = r.json().get("rates", {})
    if not data: raise RuntimeError("Réponse vide exchangerate.host")
    df = pd.DataFrame(data).T.sort_index()
    df.index = pd.to_datetime(df.index)
    return df

def get_frankfurter(base, symbols, start, end):
    syms = ",".join(symbols)
    url = f"https://api.frankfurter.app/{start}..{end}?from={base}&to={syms}"
    r = requests.get(url, timeout=12)
    r.raise_for_status()
    data = r.json().get("rates", {})
    if not data: raise RuntimeError("Réponse vide frankfurter.app")
    df = pd.DataFrame(data).T.sort_index()
    df.index = pd.to_datetime(df.index)
    return df

def get_local_snapshot(base, symbols):
    ensure_sample_exists()
    df = pd.read_csv(ASSET_PATH, parse_dates=["date"]).set_index("date").sort_index()
    # Le snapshot est exprimé avec USD=1.0. On convertit en base demandée si possible
    all_cols = ["USD","EUR","GBP","JPY","CNY"]
    syms = [s for s in symbols if s in all_cols and s != base]
    if base not in df.columns:
        # si base absent du snapshot, on se contente d'afficher les colonnes disponibles
        return df[syms] if syms else df
    # Convertir via cross-rates: rate(base->sym) = rate(USD->sym) / rate(USD->base)
    if base != "USD":
        denom = df[base]
        df_conv = {}
        for s in syms:
            df_conv[s] = df[s] / denom
        df2 = pd.DataFrame(df_conv, index=df.index)
        return df2
    else:
        return df[syms] if syms else df

def load_fx(base, symbols, days):
    if not symbols:
        return None, "Aucune devise sélectionnée."
    end = dt.date.today()
    start = end - dt.timedelta(days=days)
    try:
        df = get_exchangerate_host(base, symbols, start, end)
        source = "exchangerate.host"
        return df, f"Données temps réel via {source}"
    except Exception:
        try:
            df = get_frankfurter(base, symbols, start, end)
            source = "Frankfurter (ECB)"
            return df, f"Données temps réel via {source}"
        except Exception:
            df = get_local_snapshot(base, symbols)
            return df, "Affichage d'un instantané local (mode hors-ligne)"

df, msg = load_fx(base_ccy, symbols, days)

if df is None or df.empty:
    st.info("Aucune donnée à afficher. Vérifiez la sélection.")
else:
    st.caption(msg)
    st.line_chart(df, use_container_width=True)
    st.dataframe(df.tail(10), use_container_width=True)
    st.download_button("Télécharger CSV", df.to_csv(index=True), "fx_timeseries.csv", "text/csv")
import streamlit as st, pandas as pd, requests, datetime as dt
from requests.adapters import HTTPAdapter, Retry
from i18n.strings import tr

lang = st.session_state.get("lang","FR")
st.header(tr("nav_macro", lang))
st.caption("Sources: exchangerate.host → fallback Frankfurter (ECB).")

base_ccy = st.selectbox("Base", ["USD","EUR","GBP","JPY","CNY"], index=1)
symbols = st.multiselect("Symbols", ["USD","EUR","GBP","JPY","CNY"], default=["USD","GBP","CNY"])
days = st.slider("Jours d'historique", 7, 90, 30)

def session_with_retries():
    s = requests.Session()
    retries = Retry(total=3, backoff_factor=0.6, status_forcelist=[429,500,502,503,504])
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://", HTTPAdapter(max_retries=retries))
    return s

def get_exchangerate_host(base, symbols, start, end):
    url = f"https://api.exchangerate.host/timeseries?start_date={start}&end_date={end}&base={base}&symbols={','.join(symbols)}"
    r = session_with_retries().get(url, timeout=15); r.raise_for_status()
    data = r.json().get("rates", {})
    if not data: raise RuntimeError("Empty rates from exchangerate.host")
    return pd.DataFrame(data).T.sort_index()

def get_frankfurter(base, symbols, start, end):
    syms = ",".join(symbols)
    url = f"https://api.frankfurter.app/{start}..{end}?from={base}&to={syms}"
    r = requests.get(url, timeout=15); r.raise_for_status()
    data = r.json().get("rates", {})
    if not data: raise RuntimeError("Empty rates from frankfurter.app")
    return pd.DataFrame(data).T.sort_index()

if symbols:
    end = dt.date.today()
    start = end - dt.timedelta(days=days)
    try:
        df = get_exchangerate_host(base_ccy, symbols, start, end)
        st.success("exchangerate.host OK")
    except Exception:
        try:
            df = get_frankfurter(base_ccy, symbols, start, end)
            st.warning("exchangerate.host indisponible — fallback Frankfurter (ECB) utilisé")
        except Exception:
            try:
                df = pd.read_csv("assets/fx_sample.csv", index_col=0, parse_dates=True)
                st.warning("APIs indisponibles — affichage via échantillon local (assets/fx_sample.csv)")
            except Exception:
                st.error("APIs indisponibles et aucun échantillon local. Ajoutez assets/fx_sample.csv.")
                st.stop()
    st.line_chart(df, use_container_width=True)
    st.dataframe(df.tail(5), use_container_width=True)
