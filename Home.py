
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ürün Yönetim Paneli", layout="wide")
st.title("📦 Ürün - Stok - Fiyat - Kar Yönetim Paneli")

# Oturum başında boş tablo oluştur
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['STOK ID', 'STOK Kodu', 'Barkod', 'Ürün Adı', 'Kategori', 'Marka', 'Alış Fiyatı', 'Kar Marjı (%)', 'Satış Fiyatı', 'Piyasa Fiyatı', 'Tedarikçi', 'Ofis26 Satış', 'HEPCAZİP Satış', 'Güncel Stok', 'Raf', 'Kasa', 'Palet'])

st.markdown("### 🔄 Ürün Tablosunu Güncelleyin")

# Düzenlenebilir tablo
edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)

# Güncelle
if st.button("Güncellemeleri Kaydet"):
    st.session_state.df = edited_df
    st.success("Tablo başarıyla güncellendi.")

# Excel yükleme
st.markdown("### 📥 Excel'den Veri Yükle")
uploaded_file = st.file_uploader("Excel Dosyası Yükleyin (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df_yeni = pd.read_excel(uploaded_file)
        st.session_state.df = df_yeni
        st.success("Excel'den veriler başarıyla yüklendi.")
    except Exception as e:
        st.error(f"Yükleme hatası: {e}")
