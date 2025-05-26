import streamlit as st
import pandas as pd
from veri_kaynaklari.mikro_api_panel import mikro_guncelle
st.title("📦 HEpcazip Mikro API Entegrasyonu")

st.markdown("Lütfen ana_urun_listesi.csv dosyasını yükleyin")

uploaded_file = st.file_uploader("Drag and drop file here", type=["csv"], label_visibility="collapsed")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    if st.button("🔁 Mikro Verilerini Güncelle"):
        df = mikro_guncelle(df)
        st.success("Güncelleme tamamlandı.")
        st.dataframe(df)
