import streamlit as st

st.set_page_config(page_title="Tanımlamalar", layout="wide")
st.title("⚙️ Tanımlamalar")

def tanimla(label, key):
    yeni = st.text_input(f"Yeni {label}", key=key)
    if st.button(f"{label} Ekle", key=key+"_btn"):
        st.success(f"{yeni} kaydedildi.")

with st.expander("Kategori / Marka / Tedarikçi"):
    tanimla("Kategori", "kat")
    tanimla("Marka", "marka")
    tanimla("Tedarikçi", "ted")

with st.expander("Stok Yeri"):
    tanimla("Raf", "raf")
    tanimla("Kasa", "kasa")
    tanimla("Palet", "palet")
