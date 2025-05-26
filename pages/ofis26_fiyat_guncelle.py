import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

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
        "UrunKartiID": 0,
    }

    urun_sayfalama = {
        "BaslangicIndex": 0,
        "KayitSayisi": 200,
        "SiralamaDegeri": "ID",
        "SiralamaYonu": "DESC",
    }

    try:
        sonuc = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f=urun_filtre,
            s=urun_sayfalama
        )

        if not sonuc:
            st.warning("Ürün listesi boş veya çekilemedi.")
            return None

        urunler = sonuc  # .UrunListesi yerine direkt liste
        df = pd.DataFrame(urunler)

        if "StokKodu" not in df.columns or "SatisFiyati" not in df.columns:
            st.error("Gelen veri sütunları eksik.")
            return None

        ana_liste = pd.read_csv(CSV_YOLU)

        # Sadece satış fiyatını eşleştir
        ana_liste = ana_liste.merge(df[["StokKodu", "SatisFiyati"]], how="left", on="StokKodu", suffixes=('', '_Ticimax'))

        # Güncellenmiş tabloyu yaz
        ana_liste.to_csv(CSV_YOLU, index=False)
        st.success("Ticimax satış fiyatları başarıyla güncellendi.")

        return ana_liste

    except Exception as e:
        st.error(f"Ürün verisi çekilirken hata oluştu: {e}")
        return None

# Streamlit Arayüz
st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")
if st.button("📉 Satış Fiyatlarını Ticimax'ten Çek"):
    satis_fiyatlarini_cek()
