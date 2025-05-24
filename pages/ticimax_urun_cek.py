import streamlit as st
from zeep import Client
from zeep.helpers import serialize_object

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
            s={
                "BaslangicIndex": 0,
                "KayitSayisi": 5,
                "KayitSayisinaGoreGetir": True,
                "SiralamaDegeri": "",
                "SiralamaYonu": ""
            }
        )
        if not response:
            st.warning("Hiç ürün bulunamadı.")
        else:
            st.success(f"{len(response)} ürün başarıyla çekildi.")
            for idx, urun in enumerate(response, 1):
                st.markdown(f"### {idx}. Ürün")
                if urun is None:
                    st.warning("Bu ürün None döndü, atlanıyor.")
                    continue

                u = serialize_object(urun)
                if not isinstance(u, dict):
                    st.warning("Veri formatı beklenen şekilde değil.")
                    continue

                st.json(u)

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
