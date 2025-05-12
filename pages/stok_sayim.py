import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stok Sayımı", layout="wide")
st.title("📊 Stok Sayımı")

if "df" not in st.session_state:
    st.warning("Ürün verisi yüklenmemiş.")
else:
    aranan = st.text_input("Ürün Ara (Ad, Kod, Barkod)")
    df = st.session_state.df
    eslesen = df[df.apply(lambda r: aranan.lower() in str(r).lower(), axis=1)] if aranan else pd.DataFrame()

    if not eslesen.empty:
        urun = eslesen.iloc[0]
        st.markdown(f"### {urun['Ürün Adı']} - Mevcut: {urun.get('Güncel Stok', 0)}")

        raf = st.number_input("Raf", 0, step=1)
        kasa = st.number_input("Kasa", 0, step=1)
        palet = st.number_input("Palet", 0, step=1)

        toplam = raf + kasa + palet
        mevcut = int(urun.get("Güncel Stok", 0))
        fark = toplam - mevcut
        st.markdown(f"**Fark:** {fark}")
    else:
        st.info("Eşleşen ürün bulunamadı.")
