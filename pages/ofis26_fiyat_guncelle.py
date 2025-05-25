
import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport
import os

st.set_page_config(layout="wide")
st.title("🔄 Ofis26 Satış Fiyatlarını Güncelle")

# API bağlantı bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1K1USEAD0VAXTVKP8FWGN3AE"

# Ana ürün listesi dosya yolu
CSV_PATH = "veri_kaynaklari/ana_urun_listesi.csv"

# Ana tabloyu yükle
if not os.path.exists(CSV_PATH):
    st.error("Ana ürün listesi dosyası bulunamadı.")
    st.stop()

df = pd.read_csv(CSV_PATH, dtype=str).fillna("")

client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))
UrunFiltre = client.get_type("ns0:UrunFiltre")
UrunListele = client.service.UrunListele

# Güncelleme işlemi
if st.button("💡 Satış Fiyatlarını Güncelle (Ticimax / Ofis26)"):
    guncellenen = 0
    for idx, row in df.iterrows():
        stok_kodu = row.get("Stok Kodu", "").strip()
        if stok_kodu:
            try:
                urun = UrunFiltre(UyeKodu=UYE_KODU, StokKodu=stok_kodu)
                sonuc = UrunListele(urun)
                if sonuc and sonuc[0].SatisFiyati:
                    df.at[idx, "Ofis26 Satış Fiyatı"] = float(sonuc[0].SatisFiyati)
                    guncellenen += 1
            except Exception as e:
                st.warning(f"{stok_kodu} -> Hata: {str(e)}")
    df.to_csv(CSV_PATH, index=False)
    st.success(f"{guncellenen} ürünün satış fiyatı güncellendi.")
    st.dataframe(df)
