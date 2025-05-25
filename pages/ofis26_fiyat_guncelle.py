import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# CSV dosya yolu
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

# Ticimax Ofis26 WSDL bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1K1USEAD0VAXTVKP8FWGN3AE"  # Ofis26 Üye kodu

def urun_fiyatlarini_cek():
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))
        SelectUrun = client.get_type("ns0:SelectUrun")

        df = pd.read_csv(CSV_YOLU)

        if "Stok Kodu" not in df.columns:
            st.error("CSV'de 'Stok Kodu' sütunu eksik.")
            return

        ofis26_fiyatlar = []

        for stok_kodu in df["Stok Kodu"].dropna():
            filtre = SelectUrun(
                UyeKodu=UYE_KODU,
                StokKodu=stok_kodu,
                Dil="tr"
            )
            try:
                sonuc = client.service.SelectUrun(filtre)
                if sonuc and hasattr(sonuc, 'Urun'):  # "Urun" alanı varsa
                    urunler = sonuc.Urun
                    if isinstance(urunler, list):
                        urun = urunler[0] if urunler else None
                    else:
                        urun = urunler

                    if urun and hasattr(urun, "SatisFiyati"):
                        ofis26_fiyatlar.append(urun.SatisFiyati)
                        continue
                ofis26_fiyatlar.append(None)
            except Exception as e:
                ofis26_fiyatlar.append(None)

        df["Ofis26 Satış Fiyatı"] = ofis26_fiyatlar
        df.to_csv(CSV_YOLU, index=False)
        st.success("Ofis26 satış fiyatları başarıyla güncellendi.")

    except Exception as e:
        st.error(f"Hata oluştu: {e}")

st.set_page_config(page_title="Ofis26 Fiyat Güncelle", layout="wide")
st.title("\U0001F504 Ofis26 Satış Fiyatlarını Güncelle")

if st.button("\U0001F4BE Fiyatları Güncelle (Ticimax)"):
    urun_fiyatlarini_cek()
