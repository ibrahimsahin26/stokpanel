
import streamlit as st
import pandas as pd
import os

# CSV dosyasının yolu
csv_path = os.path.join("pages", "veri_kaynaklari", "ana_urun_listesi.csv")

st.title("📦 Ana Ürün Listesi Paneli")

# CSV'den veri oku
try:
    df = pd.read_csv(csv_path)

    # Ürün adı filtreleme
    urun_adi = st.text_input("🔍 Ürün Adı ile Filtrele")
    if urun_adi:
        df = df[df["Ürün Adı"].str.contains(urun_adi, case=False, na=False)]

    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"CSV dosyası okunamadı: {e}")
