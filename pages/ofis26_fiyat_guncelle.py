import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport
import os

CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1K1USEAD0VAXTVKP8FWGN3AE"

st.set_page_config(layout="wide")
st.title("🔄 Ofis26 Satış Fiyatlarını Güncelle")

if not os.path.exists(CSV_YOLU):
    st.error("Ana ürün listesi dosyası bulunamadı.")
    st.stop()

if st.button("💾 Fiyatları Güncelle (Ticimax)"):
    try:
        df = pd.read_csv(CSV_YOLU)

        if "Stok Kodu" not in df.columns:
            st.error("CSV dosyasında 'Stok Kodu' sütunu bulunamadı.")
            st.stop()

        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        SelectUrun = client.service.SelectUrun
        fiyatlar = []

        for stok_kodu in df["Stok Kodu"]:
            try:
                urun = SelectUrun(UyeKodu=UYE_KODU, StokKodu=stok_kodu)
                satis_fiyati = urun.SatisFiyati if urun else None
            except Exception:
                satis_fiyati = None
            fiyatlar.append(satis_fiyati)

        df["Ofis26 Satış Fiyatı"] = fiyatlar
        df.to_csv(CSV_YOLU, index=False)
        st.success("Ofis26 satış fiyatları başarıyla güncellendi.")

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
