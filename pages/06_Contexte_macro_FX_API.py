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
