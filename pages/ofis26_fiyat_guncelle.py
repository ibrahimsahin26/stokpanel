
import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport
import os

CSV_YOLU = "veri_kaynaklari/ana_urun_listesi.csv"

# SOAP servis bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1K1USEAD0VAXTVKP8FWGN3AE"

def urun_fiyatlarini_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

    try:
        UrunFiltre = client.get_type("ns0:UrunFiyatFiltre")
        UrunFiyat = client.get_type("ns0:UrunFiyat")
    except Exception as e:
        st.error(f"WSDL tipi alınamadı: {e}")
        return

    if not os.path.exists(CSV_YOLU):
        st.error("Ana ürün listesi dosyası bulunamadı.")
        return

    df = pd.read_csv(CSV_YOLU)
    if "Stok Kodu" not in df.columns:
        st.error("CSV'de 'Stok Kodu' sütunu bulunamadı.")
        return

    fiyatlar = []
    for stok_kodu in df["Stok Kodu"].dropna().unique():
        filtre = UrunFiltre(UyeKodu=UYE_KODU, StokKodu=stok_kodu)
        try:
            sonuc = client.service.UrunFiyatGetir(filtre)
            fiyat = sonuc.Fiyat if sonuc else None
        except:
            fiyat = None
        fiyatlar.append((stok_kodu, fiyat))

    fiyat_df = pd.DataFrame(fiyatlar, columns=["Stok Kodu", "Ofis26 Satış Fiyatı"])
    df = df.merge(fiyat_df, on="Stok Kodu", how="left")
    df.to_csv(CSV_YOLU, index=False)
    st.success("Fiyatlar başarıyla güncellendi.")
    st.dataframe(df)

st.set_page_config(layout="wide")
st.title("🔄 Ofis26 Satış Fiyatlarını Güncelle")

if st.button("💾 Fiyatları Güncelle (Ticimax)"):
    urun_fiyatlarini_cek()
