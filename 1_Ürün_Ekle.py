
import streamlit as st

st.title("➕ Yeni Ürün Ekle")

with st.form("urun_form"):
    barkod = st.text_input("Barkod")
    ad = st.text_input("Ürün Adı")
    kategori = st.text_input("Kategori")
    marka = st.text_input("Marka")
    alis = st.number_input("Alış Fiyatı", min_value=0.0, step=0.1)
    kar = st.number_input("Kar Marjı (%)", min_value=0.0, max_value=100.0, step=1.0)
    piyasa = st.number_input("Piyasa Fiyatı", min_value=0.0, step=0.1)
    tedarikci = st.text_input("Tedarikçi")
    raf = st.text_input("Raf")
    kasa = st.text_input("Kasa")
    palet = st.text_input("Palet")
    ekle = st.form_submit_button("Ekle")

    if ekle:
        satis_fiyati = round(alis * (1 + kar / 100), 2)
        yeni = {
            "Barkod": barkod, "Ürün Adı": ad, "Kategori": kategori, "Marka": marka,
            "Alış Fiyatı": alis, "Kar Marjı (%)": kar, "Satış Fiyatı": satis_fiyati,
            "Piyasa Fiyatı": piyasa, "Tedarikçi": tedarikci, "Raf": raf, "Kasa": kasa, "Palet": palet
        }
        st.session_state.df = st.session_state.df.append(yeni, ignore_index=True)
        st.success("Ürün başarıyla eklendi.")
