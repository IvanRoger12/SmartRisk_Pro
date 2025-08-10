import streamlit as st, pandas as pd, requests, datetime as dt

st.header("Contexte macro (FX/API)")
st.caption("Source: exchangerate.host — API gratuite, sans clé.")

base_ccy = st.selectbox("Devise de base", ["USD","EUR","GBP","JPY","CNY"], index=1)
symbols = st.multiselect("Devises cibles", ["USD","EUR","GBP","JPY","CNY"], default=["USD","GBP","CNY"])
days = st.slider("Jours d'historique", 7, 90, 30)

if symbols:
    end = dt.date.today()
    start = end - dt.timedelta(days=days)
    url = f"https://api.exchangerate.host/timeseries?start_date={start}&end_date={end}&base={base_ccy}&symbols={','.join(symbols)}"
    try:
        r = requests.get(url, timeout=10)
        df = pd.DataFrame(r.json()["rates"]).T.sort_index()
        st.line_chart(df)
        st.dataframe(df.tail(5))
    except Exception:
        st.error("API FX indisponible. Réessayez en local / plus tard.")
