import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport
import os

# CSV yolu
CSV_PATH = "veri_kaynaklari/ana_urun_listesi.csv"

# SOAP servis bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1K1USEAD0VAXTVKP8FWGN3AE"

def urun_fiyatlarini_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))
    UrunFiltre = client.get_type("ns0:UrunFiltre")
    UrunFiyat = client.get_type("ns0:UrunFiyat")

    df = pd.read_csv(CSV_PATH)

    if "Stok Kodu" not in df.columns:
        st.error("CSV'de 'Stok Kodu' sütunu bulunamadı.")
        return

    ofis26_fiyatlar = []

    for stok_kodu in df["Stok Kodu"].dropna().astype(str).unique():
        try:
            filtre = UrunFiltre(UyeKodu=UYE_KODU, StokKodu=stok_kodu)
            sonuc = client.service.UrunListele(filtre)
            if sonuc and hasattr(sonuc, 'Urunler') and sonuc.Urunler:
                fiyat = sonuc.Urunler[0].SatisFiyati
                ofis26_fiyatlar.append((stok_kodu, fiyat))
            else:
                ofis26_fiyatlar.append((stok_kodu, None))
        except Exception as e:
            ofis26_fiyatlar.append((stok_kodu, None))

    fiyat_df = pd.DataFrame(ofis26_fiyatlar, columns=["Stok Kodu", "Ofis26 Satış Fiyatı"])
    df = df.merge(fiyat_df, on="Stok Kodu", how="left")
    df.to_csv(CSV_PATH, index=False)
    st.success("Ofis26 satış fiyatları başarıyla güncellendi!")

def main():
    st.set_page_config(layout="wide")
    st.title("🔄 Ofis26 Satış Fiyatlarını Güncelle")

    if not os.path.exists(CSV_PATH):
        st.error("Ana ürün listesi dosyası bulunamadı.")
        return

    if st.button("📥 Ofis26 Fiyatlarını Güncelle (Ticimax)"):
        urun_fiyatlarini_cek()

if __name__ == "__main__":
    main()
