
import streamlit as st
import pandas as pd

st.title("➕ Yeni Ürün Ekle")

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['STOK ID', 'STOK Kodu', 'Barkod', 'Ürün Adı', 'Kategori', 'Marka', 'Alış Fiyatı', 'Kar Marjı (%)', 'Satış Fiyatı', 'Piyasa Fiyatı', 'Tedarikçi', 'Ofis26 Satış', 'HEPCAZİP Satış', 'Güncel Stok', 'Raf', 'Kasa', 'Palet'])

with st.form("urun_form"):
    stok_id = st.text_input("STOK ID")
    stok_kodu = st.text_input("STOK Kodu")
    barkod = st.text_input("Barkod")
    ad = st.text_input("Ürün Adı")
    kategori = st.text_input("Kategori")
    marka = st.text_input("Marka")
    alis = st.number_input("Alış Fiyatı", min_value=0.0, step=0.1)
    kar = st.number_input("Kar Marjı (%)", min_value=0.0, max_value=100.0, step=1.0)
    satis = st.number_input("Satış Fiyatı (opsiyonel)", min_value=0.0, step=0.1)
    piyasa = st.number_input("Piyasa Fiyatı", min_value=0.0, step=0.1)
    tedarikci = st.text_input("Tedarikçi")
    ofis26 = st.number_input("Ofis26 Satış", min_value=0, step=1)
    hepcazip = st.number_input("HEPCAZİP Satış", min_value=0, step=1)
    raf = st.number_input("Raf", min_value=0, step=1)
    kasa = st.number_input("Kasa", min_value=0, step=1)
    palet = st.number_input("Palet", min_value=0, step=1)
    ekle = st.form_submit_button("Ürünü Ekle")

    if ekle:
        if satis == 0 and kar > 0:
            satis = round(alis * (1 + kar / 100), 2)
        elif satis > 0 and alis > 0:
            kar = round(((satis - alis) / alis) * 100, 2)

        stok = raf + kasa + palet

        yeni = {
            "STOK ID": stok_id, "STOK Kodu": stok_kodu, "Barkod": barkod, "Ürün Adı": ad, "Kategori": kategori,
            "Marka": marka, "Alış Fiyatı": alis, "Kar Marjı (%)": kar, "Satış Fiyatı": satis,
            "Piyasa Fiyatı": piyasa, "Tedarikçi": tedarikci,
            "Ofis26 Satış": ofis26, "HEPCAZİP Satış": hepcazip,
            "Güncel Stok": stok, "Raf": raf, "Kasa": kasa, "Palet": palet
        }

        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([yeni])], ignore_index=True)
        st.success("Ürün başarıyla eklendi.")
