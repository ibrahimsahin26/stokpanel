
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ürün Yönetim Paneli", layout="wide")
st.title("📦 Ürün - Stok - Fiyat - Kar Yönetim Paneli")

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['STOK ID', 'Barkod', 'Ürün Adı', 'Kategori', 'Marka', 'Alış Fiyatı', 'Kar Marjı (%)', 'Satış Fiyatı', 'Piyasa Fiyatı', 'Tedarikçi', 'Ofis26 Satış', 'HEPCAZİP Satış', 'Güncel Stok', 'Raf', 'Kasa', 'Palet'])

st.dataframe(st.session_state.df, use_container_width=True)
