import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax ayarları
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

    # Filtre ayarları (tüm ürünler için boş filtre)
    urun_filtre = {
        "Aktif": -1,
        "Firsat": -1,
        "Indirimli": -1,
        "Vitrin": -1,
        "KategoriID": 0,
        "MarkaID": 0,
        "TedarikciID": -1,
        "ToplamStokAdediBas": 0,
        "ToplamStokAdediSon": 100,
        "UrunKartiID": 0
    }

    urun_sayfalama = {
        "BaslangicIndex": 0,
        "KayitSayisi": 200,
        "SiralamaDegeri": "ID",
        "SiralamaYonu": "DESC"
    }

    try:
        sonuc = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f=urun_filtre,
            s=urun_sayfalama
        )
        urun_listesi = sonuc["UrunListesi"] if sonuc and "UrunListesi" in sonuc else []
        return urun_listesi
    except Exception as e:
        st.error(f"Hata oluştu: {e}")
        return []

# Streamlit Arayüzü
st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")
if st.button("📉 Satış Fiyatlarını Ticimax'ten Çek"):
    veri = satis_fiyatlarini_cek()
    if veri:
        st.success("Veriler başarıyla çekildi.")
        df = pd.DataFrame(veri)
        st.dataframe(df)
    else:
        st.warning("Ürün listesi boş veya çekilemedi.")
