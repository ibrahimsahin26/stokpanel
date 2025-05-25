import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# CSV yolu
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

# SOAP servis bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1K1USEAD0VAXTVKP8FWGN3AE"

# Fiyat verilerini çekme fonksiyonu
def fiyatlari_guncelle():
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        # Ana tabloyu oku
        df = pd.read_csv(CSV_YOLU)

        if "Stok Kodu" not in df.columns:
            st.error("CSV'de 'Stok Kodu' alanı bulunamadı.")
            return

        # Select ile ürünleri çek
        sonuc = client.service.Select(UyeKodu=UYE_KODU)

        if not sonuc:
            st.warning("Ticimax'ten veri alınamadı veya boş döndü.")
            return

        ticimax_df = pd.DataFrame(sonuc)

        if "StokKodu" not in ticimax_df.columns or "SatisFiyati" not in ticimax_df.columns:
            st.error("Ticimax verilerinde beklenen alanlar yok: 'StokKodu' veya 'SatisFiyati'")
            return

        # Sadece gerekli alanları al
        ticimax_df = ticimax_df[["StokKodu", "SatisFiyati"]].dropna()

        # Stok kodu ile eşleşme yap ve fiyat güncelle
        df = df.merge(ticimax_df, how="left", left_on="Stok Kodu", right_on="StokKodu")
        df["Ofis26 Satış Fiyatı"] = df["SatisFiyati"]
        df.drop(columns=["StokKodu", "SatisFiyati"], inplace=True)

        # Sonucu CSV'ye kaydet
        df.to_csv(CSV_YOLU, index=False)
        st.success("Ofis26 satış fiyatları başarıyla güncellendi.")

    except Exception as e:
        st.error(f"Hata oluştu: {e}")

# Streamlit arayüz
st.set_page_config(layout="wide")
st.title("\U0001F501 Ofis26 Satış Fiyatlarını Güncelle")

if st.button("\U0001F4BE Fiyatları Güncelle (Ticimax)"):
    fiyatlari_guncelle()
