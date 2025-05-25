# pages/ofis26_fiyat_guncelle.py
import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# CSV yolu
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

# SOAP servis bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1K1USEAD0VAXTVKP8FWGN3AE"

st.set_page_config(layout="wide")
st.title("🔁 Ofis26 Satış Fiyatlarını Güncelle")

if st.button("💾 Fiyatları Güncelle (Ticimax)"):
    try:
        df = pd.read_csv(CSV_YOLU)

        if "Stok Kodu" not in df.columns:
            st.error("CSV'de 'Stok Kodu' sütunu bulunamadı.")
            st.stop()

        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))
        UrunFiltre = client.get_type("ns0:UrunFiltre")
        UrunListele = client.service.UrunListele

        fiyatlar = []

        for kod in df["Stok Kodu"]:
            try:
                filtre = UrunFiltre(StokKodu=kod)
                sonuc = UrunListele(UyeKodu=UYE_KODU, urunFiltre=filtre)
                if sonuc and sonuc[0].SatisFiyati:
                    fiyatlar.append(sonuc[0].SatisFiyati)
                else:
                    fiyatlar.append(None)
            except Exception as e:
                fiyatlar.append(None)

        df["Ofis26 Satış Fiyatı"] = fiyatlar
        df.to_csv(CSV_YOLU, index=False)
        st.success("Ofis26 satış fiyatları başarıyla güncellendi.")

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
