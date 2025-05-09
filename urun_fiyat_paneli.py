
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(layout="wide")
st.title("Ürün ve Fiyat Yönetimi Paneli")

# Varsayılan ürün listesi (demo amaçlı)
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=[
        "Barkod", "Ürün Adı", "Kategori", "Marka", 
        "Alış Fiyatı", "Kar Marjı (%)", "Satış Fiyatı", 
        "Piyasa Fiyatı", "Akakçe Linki"
    ])

df = st.session_state.df

# Yeni ürün ekleme formu
st.subheader("➕ Yeni Ürün Ekle / Fiyat Yönetimi")
with st.form("urun_ekle_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        barkod = st.text_input("Barkod")
        urun_adi = st.text_input("Ürün Adı")
        kategori = st.text_input("Kategori")
    with col2:
        marka = st.text_input("Marka")
        alis_fiyati = st.number_input("Alış Fiyatı", min_value=0.0, step=0.01)
        kar_marji = st.slider("Kar Marjı (%)", 0, 100, 20)
    with col3:
        piyasa_fiyati = st.number_input("Piyasa Fiyatı (opsiyonel)", min_value=0.0, step=0.01)
        akakce_linki = st.text_input("Akakçe Linki (opsiyonel)")
        submit = st.form_submit_button("Ürünü Ekle")

    if submit:
        satis_fiyati = round(alis_fiyati * (1 + kar_marji / 100), 2)
        new_row = {
            "Barkod": barkod,
            "Ürün Adı": urun_adi,
            "Kategori": kategori,
            "Marka": marka,
            "Alış Fiyatı": alis_fiyati,
            "Kar Marjı (%)": kar_marji,
            "Satış Fiyatı": satis_fiyati,
            "Piyasa Fiyatı": piyasa_fiyati,
            "Akakçe Linki": akakce_linki
        }
        st.session_state.df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        st.success("✅ Ürün başarıyla eklendi.")

# Ürün tablosu gösterimi
st.subheader("📋 Ürün Listesi ve Fiyatlar")
st.dataframe(st.session_state.df)

# Excel çıktısı
if st.button("📥 Excel Olarak İndir"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        st.session_state.df.to_excel(writer, index=False, sheet_name="Urunler")
    st.download_button(
        label="Excel İndir",
        data=output.getvalue(),
        file_name="urun_fiyat_paneli.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
