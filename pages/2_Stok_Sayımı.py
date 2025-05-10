
import streamlit as st
import pandas as pd

st.title("📊 Stok Sayımı")

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['STOK ID', 'STOK Kodu', 'Barkod', 'Ürün Adı', 'Kategori', 'Marka', 'Alış Fiyatı', 'Kar Marjı (%)', 'Satış Fiyatı', 'Piyasa Fiyatı', 'Tedarikçi', 'Ofis26 Satış', 'HEPCAZİP Satış', 'Güncel Stok', 'Raf', 'Kasa', 'Palet'])

if st.session_state.df.empty:
    st.warning("Henüz ürün eklenmedi.")
else:
    for i, row in st.session_state.df.iterrows():
        st.markdown(f"### {row['Ürün Adı']}")
        raf = st.number_input(f"Raf Adedi ({row['Barkod']})", min_value=0, value=int(row['Raf']) if pd.notna(row['Raf']) else 0, key=f"raf_{i}")
        kasa = st.number_input(f"Kasa Adedi ({row['Barkod']})", min_value=0, value=int(row['Kasa']) if pd.notna(row['Kasa']) else 0, key=f"kasa_{i}")
        palet = st.number_input(f"Palet Adedi ({row['Barkod']})", min_value=0, value=int(row['Palet']) if pd.notna(row['Palet']) else 0, key=f"palet_{i}")
        st.session_state.df.at[i, "Raf"] = raf
        st.session_state.df.at[i, "Kasa"] = kasa
        st.session_state.df.at[i, "Palet"] = palet
        st.session_state.df.at[i, "Güncel Stok"] = raf + kasa + palet

    st.success("Stok sayımı güncellendi.")
