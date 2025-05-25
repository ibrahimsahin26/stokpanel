# pages/ofis26_fiyat_guncelle.py
import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1K1USEAD0VAXTVKP8FWGN3AE"

st.set_page_config(layout="wide")
st.title("🔁 Ofis26 Satış Fiyatlarını Güncelle")

if st.button("💾 Fiyatları Güncelle (Ticimax)"):
    try:
        df = pd.read_csv(CSV_YOLU)
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        # API'den tüm ürünleri çekiyoruz (filtre olmadan)
        urunler = client.service.UrunListele(UyeKodu=UYE_KODU, urunFiltre=None)

        # Eşleştirme: CSV'deki stok kodu ile API'deki stok kodu
        fiyat_dict = {urun.StokKodu: urun.SatisFiyati for urun in urunler}

        # CSV'de yeni sütunu oluştur
        df["Ofis26 Satış Fiyatı"] = df["Stok Kodu"].map(fiyat_dict)

        # Kaydet
        df.to_csv(CSV_YOLU, index=False)
        st.success("Ofis26 satış fiyatları başarıyla güncellendi.")

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
