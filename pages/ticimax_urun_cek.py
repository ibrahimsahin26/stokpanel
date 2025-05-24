
import streamlit as st
from zeep import Client
import pandas as pd

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

def urun_to_dict(urun):
    varyasyon = None
    if urun.Varyasyonlar and "Varyasyon" in urun.Varyasyonlar:
        varyasyon_list = urun.Varyasyonlar["Varyasyon"]
        if isinstance(varyasyon_list, list) and len(varyasyon_list) > 0:
            varyasyon = varyasyon_list[0]
        elif isinstance(varyasyon_list, dict):
            varyasyon = varyasyon_list

    return {
        "Ürün ID": urun.ID,
        "Stok Kodu": varyasyon.get("StokKodu") if varyasyon else "",
        "Barkod": varyasyon.get("Barkod") if varyasyon else "",
        "Ürün Adı": urun.UrunAdi,
        "Ana Kategori": urun.AnaKategori,
        "Alt Kategori": "",  # Manuel tanımlanacak veya eşleştirme yapılacak
        "Marka": urun.Marka,
        "Alış Fiyatı": varyasyon.get("AlisFiyati") if varyasyon else 0,
        "Mikro Stok": urun.ToplamStokAdedi,
        "Hepcazip Satış": "",  # Sonradan girilecek veya eşleştirilecek
        "Ofis26 Satış": "",    # Sonradan girilecek veya eşleştirilecek
        "Kar Marjı": ""        # Panelde hesaplanacak
    }

if st.button("🔄 Ticimax'tan Ürünleri Al"):
    try:
        response = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f={},
            s={"Baslangic": 0, "Adet": 50}
        )
        if not response:
            st.warning("Hiç ürün bulunamadı.")
        else:
            data = [urun_to_dict(u) for u in response]
            df = pd.DataFrame(data)
            st.success(f"{len(df)} ürün başarıyla tabloya aktarıldı.")
            st.dataframe(df)
    except Exception as e:
        st.error(f"Hata oluştu: {e}")
