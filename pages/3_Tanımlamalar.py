
import streamlit as st

st.title("⚙️ Marka / Kategori / Tedarikçi Tanımları")

for key in ["markalar", "kategoriler", "tedarikciler"]:
    if key not in st.session_state:
        st.session_state[key] = []

def tanimlama_alani(label, key):
    st.subheader(label)
    yeni = st.text_input(f"Yeni {label}", key=f"{key}_input")
    if st.button(f"Ekle {label}", key=f"{key}_btn"):
        if yeni and yeni not in st.session_state[key]:
            st.session_state[key].append(yeni)
            st.success(f"{yeni} eklendi.")
    st.write("Tanımlı:", st.session_state[key])

tanimlama_alani("Marka", "markalar")
tanimlama_alani("Kategori", "kategoriler")
tanimlama_alani("Tedarikçi", "tedarikciler")
