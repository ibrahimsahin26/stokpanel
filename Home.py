
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ürün Yönetim Paneli", layout="wide")
st.title("📦 Ürün - Stok - Fiyat - Kar Yönetim Paneli")

# Veri yapısı ve tanımlı listeler
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['STOK ID', 'STOK Kodu', 'Barkod', 'Ürün Adı', 'Kategori', 'Marka', 'Alış Fiyatı', 'Kar Marjı (%)', 'Satış Fiyatı', 'Piyasa Fiyatı', 'Tedarikçi', 'Ofis26 Satış', 'HEPCAZİP Satış', 'Güncel Stok', 'Raf', 'Kasa', 'Palet'])
if "markalar" not in st.session_state:
    st.session_state.markalar = []
if "kategoriler" not in st.session_state:
    st.session_state.kategoriler = []
if "tedarikciler" not in st.session_state:
    st.session_state.tedarikciler = []

st.markdown("### 🔍 Ürünleri Filtrele ve Ara")

col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
with col1:
    filtre_kategori = st.multiselect("Kategori", options=sorted(set(st.session_state.df["Kategori"].dropna())))
with col2:
    filtre_marka = st.multiselect("Marka", options=sorted(set(st.session_state.df["Marka"].dropna())))
with col3:
    filtre_tedarikci = st.multiselect("Tedarikçi", options=sorted(set(st.session_state.df["Tedarikçi"].dropna())))
with col4:
    arama = st.text_input("Ürün Adı, Barkod veya STOK Kodu ile Ara")

# Filtre uygula
df_filtered = st.session_state.df.copy()
if filtre_kategori:
    df_filtered = df_filtered[df_filtered["Kategori"].isin(filtre_kategori)]
if filtre_marka:
    df_filtered = df_filtered[df_filtered["Marka"].isin(filtre_marka)]
if filtre_tedarikci:
    df_filtered = df_filtered[df_filtered["Tedarikçi"].isin(filtre_tedarikci)]
if arama:
    df_filtered = df_filtered[df_filtered.apply(lambda row: arama.lower() in str(row).lower(), axis=1)]

st.dataframe(df_filtered, use_container_width=True)

# Excel yükleme
st.markdown("### 📥 Excel'den Veri Yükle")
uploaded_file = st.file_uploader("Excel Dosyası Yükleyin (.xlsx)", type=["xlsx"])
if uploaded_file:
    try:
       df_yeni = pd.read_excel(uploaded_file, engine="openpyxl")
        birlestir = st.checkbox("STOK Kodu ile eşleşen satırları birleştirerek güncelle", value=True)
        if birlestir:
            for _, yeni_satir in df_yeni.iterrows():
                eslesen = st.session_state.df["STOK Kodu"] == yeni_satir.get("STOK Kodu", "___YOK___")
                if eslesen.any():
                    st.session_state.df.loc[eslesen, :] = yeni_satir
                else:
                    st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([yeni_satir])], ignore_index=True)
            st.success("Veriler başarıyla birleştirildi veya eklendi.")
        else:
            st.session_state.df = df_yeni
            st.success("Excel'den veriler doğrudan yüklendi.")
    except Exception as e:
        st.error(f"Yükleme hatası: {e}")
