import streamlit as st
import pandas as pd
from pages.veri_kaynaklari.mikro_api_panel import stok_verisi_cek
from pages.veri_kaynaklari.ana_urun_listesi import yukle_ana_urun_listesi

st.title("📦 Ana Ürün Listesi Paneli")
st.write("Ürün Adı ile Filtrele")

# Ana ürün listesini yükle
df = yukle_ana_urun_listesi()

# Kullanıcıya stok ve alış fiyatı güncellemesi için buton
if st.button("📦 Mikro'dan Stok ve Alış Fiyatı Güncelle"):
    st.info("Mikro API'den veriler çekiliyor, lütfen bekleyin...")
    mikro_df = stok_verisi_cek()

    if mikro_df is not None and not mikro_df.empty:
        st.success("Veriler başarıyla güncellendi!")

        # Ana ürün listesi ile stok verisini stok kodu üzerinden eşleştir
        df = df.merge(mikro_df, how="left", left_on="Stok Kodu", right_on="stok")
        df.drop(columns=["stok"], inplace=True)
    else:
        st.error("Veri çekilemedi. Lütfen API erişimini veya sunucu bağlantısını kontrol edin.")

# Filtreleme
search = st.text_input("", placeholder="Ürün adı ara...")
if search:
    df = df[df['Ürün Adı'].str.contains(search, case=False, na=False)]

# Tabloyu göster
st.dataframe(df, use_container_width=True)
