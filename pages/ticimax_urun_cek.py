import streamlit as st
import pandas as pd
from zeep import Client

st.set_page_config(page_title="Ticimax Ürün Çek", layout="wide")
st.title("📦 Ticimax Ürünlerini Panele Yükle")

# Sabit bilgiler
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
SERVICE_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"

try:
    client = Client(wsdl=SERVICE_URL)
    st.success("Servis bağlantısı başarılı.")
except Exception as e:
    st.error(f"Servis bağlantısı başarısız: {e}")
    st.stop()

def urun_to_rows(urun):
    rows = []
    if urun.Varyasyonlar and "Varyasyon" in urun.Varyasyonlar:
        varyasyonlar = urun.Varyasyonlar["Varyasyon"]
        if not isinstance(varyasyonlar, list):
            varyasyonlar = [varyasyonlar]
        for v in varyasyonlar:
            rows.append({
                "Ürün ID": urun.ID,
                "Stok Kodu": v.get("StokKodu", ""),
                "Barkod": v.get("Barkod", ""),
                "Ürün Adı": urun.UrunAdi,
                "Ana Kategori": urun.AnaKategori,
                "Alt Kategori": "",  # Gerekirse eşleştirilecek
                "Marka": urun.Marka,
                "Alış Fiyatı": v.get("AlisFiyati", 0),
                "Mikro Stok": v.get("StokAdedi", urun.ToplamStokAdedi),
                "Hepcazip Satış": "",
                "Ofis26 Satış": "",
                "Kar Marjı": ""
            })
    else:
        rows.append({
            "Ürün ID": urun.ID,
            "Stok Kodu": "",
            "Barkod": "",
            "Ürün Adı": urun.UrunAdi,
            "Ana Kategori": urun.AnaKategori,
            "Alt Kategori": "",
            "Marka": urun.Marka,
            "Alış Fiyatı": 0,
            "Mikro Stok": urun.ToplamStokAdedi,
            "Hepcazip Satış": "",
            "Ofis26 Satış": "",
            "Kar Marjı": ""
        })
    return rows

if st.button("🔄 Tüm Ürünleri Ticimax'tan Al"):
    all_rows = []
    sayfa = 0
    batch = 50
    while True:
        try:
            st.info(f"{sayfa*batch + 1}-{(sayfa+1)*batch} arası ürünler alınıyor...")
            response = client.service.SelectUrun(
                UyeKodu=UYE_KODU,
                f={},
                s={"Baslangic": sayfa * batch, "Adet": batch}
            )
            if not response:
                break
            for urun in response:
                all_rows.extend(urun_to_rows(urun))
            if len(response) < batch:
                break
            sayfa += 1
        except Exception as e:
            st.error(f"Hata oluştu: {e}")
            break

    df = pd.DataFrame(all_rows)
    st.success(f"{len(df)} varyasyon başarıyla yüklendi.")
    st.dataframe(df)
