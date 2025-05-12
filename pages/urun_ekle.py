import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ürün Ekle", layout="wide")
st.title("➕ Yeni Ürün Ekle")

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

with st.form("urun_ekle_form"):
    stok_kodu = st.text_input("Stok Kodu")
    barkod = st.text_input("Barkod")
    urun_adi = st.text_input("Ürün Adı")
    kategori = st.text_input("Kategori")
    marka = st.text_input("Marka")
    alis = st.number_input("Alış Fiyatı", 0.0)
    kar = st.number_input("Kar Marjı (%)", 0.0)
    tedarikci = st.text_input("Tedarikçi")

    ekle = st.form_submit_button("Ürünü Ekle")
    if ekle:
        yeni_urun = {
            "STOK KODU": stok_kodu,
            "Barkod": barkod,
            "Ürün Adı": urun_adi,
            "Kategori": kategori,
            "Marka": marka,
            "Alış Fiyatı": alis,
            "Kar Marjı (%)": kar,
            "Tedarikçi": tedarikci,
        }
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([yeni_urun])], ignore_index=True)
        st.success("Ürün başarıyla eklendi.")
