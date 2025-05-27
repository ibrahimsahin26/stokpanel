
import streamlit as st
import pandas as pd
from veri_kaynaklari.ofis26_fiyat_guncelle import ticimax_satis_fiyatlarini_guncelle

st.title("🛒 HEpcazip Ticimax Satış Fiyatı Entegrasyonu")

st.markdown("Lütfen `ana_urun_listesi.csv` dosyasını yükleyin.")

uploaded_file = st.file_uploader("Dosya seçin", type="csv", label_visibility="collapsed")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    if st.button("📦 Ticimax Satış Fiyatlarını Güncelle"):
        df = ticimax_satis_fiyatlarini_guncelle(df)
        st.success("Satış fiyatları başarıyla güncellendi.")
        st.dataframe(df)
