
import streamlit as st
from zeep import Client

st.set_page_config(page_title="Ticimax Ürün Çek", layout="wide")

st.title("📦 Ticimax Ürünlerini Panele Yükle")

# Yetki kodu ve servis adresi
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
SERVICE_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"

try:
    client = Client(wsdl=SERVICE_URL)
    st.success("Servis bağlantısı başarılı.")
except Exception as e:
    st.error(f"Servis bağlantısı başarısız: {e}")
    st.stop()

# Ürünleri çek
if st.button("🔄 Ticimax'tan Ürünleri Al"):
    try:
        response = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f={},
            s={"Baslangic": 0, "Adet": 5}
        )
        if not response:
            st.warning("Hiç ürün bulunamadı.")
        else:
            st.success(f"{len(response)} ürün başarıyla çekildi.")
            for idx, urun in enumerate(response, 1):
                st.write(f"**{idx}. Ürün:**")
                st.json(urun)
    except Exception as e:
        st.error(f"Hata oluştu: {e}")
