
import streamlit as st

st.title("📊 Stok Sayımı")

if "df" not in st.session_state or st.session_state.df.empty:
    st.warning("Henüz ürün eklenmedi.")
else:
    for i, row in st.session_state.df.iterrows():
        st.markdown(f"**{row['Ürün Adı']}**")
        raf = st.number_input(f"Raf Adedi - {row['Barkod']}", min_value=0, key=f"raf_{i}")
        kasa = st.number_input(f"Kasa Adedi - {row['Barkod']}", min_value=0, key=f"kasa_{i}")
        palet = st.number_input(f"Palet Adedi - {row['Barkod']}", min_value=0, key=f"palet_{i}")
        st.session_state.df.at[i, "Raf"] = raf
        st.session_state.df.at[i, "Kasa"] = kasa
        st.session_state.df.at[i, "Palet"] = palet

    st.success("Stok sayımı güncellendi.")
