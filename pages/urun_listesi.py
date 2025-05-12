import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ürün Listesi", layout="wide")
st.title("📋 Ürün Tablosu ve Filtreler")

df = st.session_state.df.copy() if "df" in st.session_state else pd.DataFrame()
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.warning("Görüntülenecek ürün verisi bulunamadı.")
