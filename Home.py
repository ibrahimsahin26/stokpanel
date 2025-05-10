
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ürün Yönetim Paneli", layout="wide")
st.title("📦 Ürün - Stok - Fiyat - Kar Yönetim Paneli")

st.markdown(
    '''
    Bu panel üzerinden ürün bilgilerini görebilir, yeni ürün ekleyebilir, stok sayımı yapabilir,
    fiyat ve kar marjı gibi verileri güncelleyebilirsiniz.
    '''
)

# Oturum içi örnek tablo başlat
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=[
        "Barkod", "Ürün Adı", "Kategori", "Marka", "Alış Fiyatı",
        "Kar Marjı (%)", "Satış Fiyatı", "Piyasa Fiyatı",
        "Tedarikçi", "Raf", "Kasa", "Palet"
    ])

st.dataframe(st.session_state.df, use_container_width=True)
