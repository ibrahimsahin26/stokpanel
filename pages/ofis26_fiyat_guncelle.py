import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport
import os

# CSV dosyası yolu
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

# Ticimax SOAP servis bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1K1USEAD0VAXTVKP8FWGN3AE"

st.set_page_config(layout="wide")
st.title("🔄 Ofis26 Satış Fiyatlarını Güncelle")

# Ana ürün listesini yükle
if not os.path.exists(CSV_YOLU):
    st.error("Ana ürün listesi dosyası bulunamadı.")
    st.stop()

df = pd.read_csv(CSV_YOLU, dtype=str).fillna("")

if st.button("💾 Fiyatları Güncelle (Ticimax)"):
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))
        UrunFiyat = client.get_type("ns0:UrunFiyat")
        UrunFiyatFiltre = client.get_type("ns0:UrunFiyatFiltre")
        servis = client.service

        guncellenen = 0

        for i, row in df.iterrows():
            stok_kodu = row["Stok Kodu"].strip()
            if not stok_kodu:
                continue

            filtre = UrunFiyatFiltre(
                UyeKodu=UYE_KODU,
                StokKodu=stok_kodu
            )

            try:
                fiyat_sonucu = servis.UrunFiyat(filtre)
                if fiyat_sonucu and fiyat_sonucu.Fiyat:
                    df.at[i, "Ofis26 Satış Fiyatı"] = fiyat_sonucu.Fiyat
                    guncellenen += 1
            except Exception as e:
                continue  # sorunlu satırı atla

        # Kaydet
        df.to_csv(CSV_YOLU, index=False)
        st.success(f"Toplam {guncellenen} ürünün satış fiyatı güncellendi.")
    except Exception as e:
        st.error(f"Hata oluştu: {str(e)}")
