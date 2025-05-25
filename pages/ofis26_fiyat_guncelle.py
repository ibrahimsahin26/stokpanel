import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport
import os

# CSV dosya yolu
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

# SOAP servis bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1K1USEAD0VAXTVKP8FWGN3AE"

st.set_page_config(layout="wide")
st.title("🔄 Ofis26 Satış Fiyatlarını Güncelle")

def fiyatlari_guncelle():
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))
        UrunDetayGetir = client.service.UrunDetayGetir

        # CSV'yi oku
        df = pd.read_csv(CSV_YOLU)

        if "Stok Kodu" not in df.columns:
            st.error("CSV dosyasında 'Stok Kodu' sütunu bulunamadı.")
            return

        yeni_fiyatlar = []

        for index, row in df.iterrows():
            stok_kodu = row["Stok Kodu"]
            try:
                cevap = UrunDetayGetir(UyeKodu=UYE_KODU, StokKodu=stok_kodu)
                satis_fiyat = cevap.SatisFiyati if hasattr(cevap, "SatisFiyati") else None
                yeni_fiyatlar.append(satis_fiyat)
            except Exception as e:
                yeni_fiyatlar.append(None)

        df["Ofis26 Satış Fiyatı"] = yeni_fiyatlar

        # CSV'yi güncelle
        df.to_csv(CSV_YOLU, index=False)

        st.success("✅ Ofis26 satış fiyatları başarıyla güncellendi.")

    except Exception as e:
        st.error(f"Hata oluştu: {str(e)}")

if st.button("💾 Fiyatları Güncelle (Ticimax)"):
    fiyatlari_guncelle()
