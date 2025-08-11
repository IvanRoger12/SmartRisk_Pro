# pages/06_Contexte_macro_FX_API.py
import os, textwrap, datetime as dt
import streamlit as st, pandas as pd, requests
from requests.adapters import HTTPAdapter, Retry
from pathlib import Path

from src.ui import use_global_css, get_lang
from i18n.strings import tr

# --- Style global + langue ---
use_global_css()
lang = get_lang()

st.header(tr("nav_macro", lang) or "Contexte macro (FX / API)")
st.caption("Sources: exchangerate.host → fallback Frankfurter (ECB). Si les APIs échouent, affichage d’un échantillon local.")

# ----------------------------
# Paramètres UI
# ----------------------------
base_ccy = st.selectbox("Devise de base", ["USD", "EUR", "GBP", "JPY", "CNY"], index=1)
symbols = st.multiselect("Devises à suivre", ["USD", "EUR", "GBP", "JPY", "CNY"], default=["USD", "GBP", "CNY"])
days = st.slider("Jours d'historique", 7, 120, 30)

# ----------------------------
# Données locales de secours
# ----------------------------
ASSET_PATH = Path("assets/fx_sample.csv")
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
    ASSET_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not ASSET_PATH.exists():
        ASSET_PATH.write_text(FX_SAMPLE_CSV, encoding="utf-8")

# ----------------------------
# Clients API
# ----------------------------
def session_with_retries():
    s = requests.Session()
    retries = Retry(total=3, backoff_factor=0.6, status_forcelist=[429, 500, 502, 503, 504])
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://", HTTPAdapter(max_retries=retries))
    return s

def get_exchangerate_host(base, syms, start, end):
    if not syms:
        return pd.DataFrame()
    url = (
        "https://api.exchangerate.host/timeseries"
        f"?start_date={start}&end_date={end}&base={base}&symbols={','.join(syms)}"
    )
    r = session_with_retries().get(url, timeout=12)
    r.raise_for_status()
    data = r.json().get("rates", {})
    if not data:
        raise RuntimeError("Réponse vide exchangerate.host")
    df = pd.DataFrame(data).T.sort_index()
    df.index = pd.to_datetime(df.index)
    return df

def get_frankfurter(base, syms, start, end):
    if not syms:
        return pd.DataFrame()
    url = f"https://api.frankfurter.app/{start}..{end}?from={base}&to={','.join(syms)}"
    r = requests.get(url, timeout=12)
    r.raise_for_status()
    data = r.json().get("rates", {})
    if not data:
        raise RuntimeError("Réponse vide frankfurter.app")
    df = pd.DataFrame(data).T.sort_index()
    df.index = pd.to_datetime(df.index)
    return df

# ----------------------------
# Fallback local avec conversion base
# Le snapshot est exprimé avec USD = 1.0
# rate(base->sym) = rate(USD->sym) / rate(USD->base)
# ----------------------------
def get_local_snapshot(base, syms):
    ensure_sample_exists()
    df = pd.read_csv(ASSET_PATH, parse_dates=["date"]).set_index("date").sort_index()
    all_cols = ["USD", "EUR", "GBP", "JPY", "CNY"]
    syms = [s for s in syms if s in all_cols and s != base]
    if base not in df.columns:
        return df[syms] if syms else df
    if base == "USD":
        return df[syms] if syms else df
    denom = df[base]  # USD->base
    converted = {s: (df[s] / denom) for s in syms}  # USD->sym / USD->base
    return pd.DataFrame(converted, index=df.index)

# ----------------------------
# Chargement des données (API → fallback API → local)
# ----------------------------
def load_fx(base, syms, days):
    if not syms:
        return None, "Aucune devise sélectionnée."
    end = dt.date.today()
    start = end - dt.timedelta(days=days)
    try:
        df = get_exchangerate_host(base, syms, start, end)
        return df, "Données temps réel via exchangerate.host"
    except Exception:
        try:
            df = get_frankfurter(base, syms, start, end)
            return df, "Données temps réel via Frankfurter (ECB)"
        except Exception:
            df = get_local_snapshot(base, syms)
            return df, "Affichage d’un instantané local (mode hors-ligne)"

# ----------------------------
# Affichage
# ----------------------------
df, msg = load_fx(base_ccy, symbols, days)

if df is None or df.empty:
    st.write("Aucune donnée à afficher. Vérifiez la sélection.")
else:
    st.caption(msg)
    st.line_chart(df, use_container_width=True)
    st.dataframe(df.tail(10), use_container_width=True)
    st.download_button(
        "Télécharger CSV",
        df.to_csv(index=True).encode("utf-8"),
        "fx_timeseries.csv",
        "text/csv"
    )
