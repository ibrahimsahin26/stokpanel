
import streamlit as st
import pandas as pd
from pages.veri_kaynaklari.mikro_api_panel import mikro_guncelle
from pages.veri_kaynaklari.ana_urun_listesi import yukle_ana_urun_listesi

st.title("📦 Ana Ürün Listesi Paneli")
st.write("Ürün Adı ile Filtrele")

# Ana ürün listesini yükle
df = yukle_ana_urun_listesi()

# Kullanıcıya stok ve alış fiyatı güncellemesi için buton
if st.button("📦 Mikro'dan Stok ve Alış Fiyatı Güncelle"):
    mikro_guncelle()
    df = yukle_ana_urun_listesi()

# Filtreleme
search = st.text_input("", placeholder="Ürün adı ara...")
if search:
    df = df[df['Ürün Adı'].str.contains(search, case=False, na=False)]

# Tabloyu göster
st.dataframe(df, use_container_width=True)
