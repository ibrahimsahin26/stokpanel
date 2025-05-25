import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport
import os

# CSV yolu
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

# SOAP servis bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1K1USEAD0VAXTVKP8FWGN3AE"

st.set_page_config(layout="wide")
st.title("\U0001F504 Ofis26 Satış Fiyatlarını Güncelle")

def urun_detaylarini_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))
    try:
        df = pd.read_csv(CSV_YOLU)
    except FileNotFoundError:
        st.error("Ana ürün listesi dosyası bulunamadı.")
        return

    if "Stok Kodu" not in df.columns:
        st.error("CSV'de 'Stok Kodu' sütunu bulunamadı.")
        return

    ofis26_fiyatlar = []
    for index, row in df.iterrows():
        stok_kodu = row["Stok Kodu"]
        if pd.isna(stok_kodu):
            ofis26_fiyatlar.append(None)
            continue

        try:
            sonuc = client.service.UrunDetayGetir(UyeKodu=UYE_KODU, StokKodu=stok_kodu)
            satis_fiyat = sonuc["SatisFiyati"] if sonuc else None
        except Exception as e:
            satis_fiyat = None

        ofis26_fiyatlar.append(satis_fiyat)

    df["Ofis26 Satış Fiyatı"] = ofis26_fiyatlar
    df.to_csv(CSV_YOLU, index=False)
    st.success("Ofis26 satış fiyatları başarıyla güncellendi.")

dosya_var = os.path.exists(CSV_YOLU)
if not dosya_var:
    st.error("Ana ürün listesi dosyası bulunamadı.")
else:
    if st.button("\U0001F4BE Fiyatları Güncelle (Ticimax)"):
        urun_detaylarini_cek()
