import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport
import os

# 📁 CSV yolu
CSV_YOLU = "sayfalar/veri_kaynaklari/ana_urun_listesi.csv"

# 🔗 SOAP servis bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1K1USEAD0VAXTVKP8FWGN3AE"

def urun_fiyatlarini_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))
    UrunFiltre = client.get_type("ns0:UrunFiltre")
    UrunFiyat = client.get_type("ns0:UrunFiyat")

    if not os.path.exists(CSV_YOLU):
        st.error("Ana ürün listesi dosyası bulunamadı.")
        return

    df = pd.read_csv(CSV_YOLU)

    if "Stok Kodu" not in df.columns:
        st.error("'Stok Kodu' sütunu hatalı veya eksik.")
        return

    ticimax_fiyatlar = []

    for _, row in df.iterrows():
        stok_kodu = str(row["Stok Kodu"]).strip()
        if stok_kodu == "" or stok_kodu == "None":
            continue

        filtre = UrunFiltre(UyeKodu=UYE_KODU, StokKodu=stok_kodu)
        try:
            fiyat_bilgisi = client.service.UrunFiyat(filtre)
            satis_fiyat = fiyat_bilgisi.SatisFiyat1
        except Exception as e:
            satis_fiyat = None

        ticimax_fiyatlar.append(satis_fiyat)

    df["Ofis26 Satış Fiyatı"] = ticimax_fiyatlar

    st.success("Fiyatlar güncellendi.")
    st.dataframe(df)

st.set_page_config(layout="wide")
st.title("🔄 Ofis26 Satış Fiyatlarını Güncelle")

if st.button("💾 Fiyatları Güncelle (Ticimax)"):
    urun_fiyatlarini_cek()
