import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax ayarları
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        # Filtre ayarları
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

        # Sayfalama ayarları
        urun_sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 100,
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC"
        }

        sonuc = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f=urun_filtre,
            s=urun_sayfalama
        )

        # Liste boşsa
        if not sonuc or not hasattr(sonuc, "UrunListesi") or not sonuc.UrunListesi:
            return pd.DataFrame(), "Ürün listesi boş veya çekilemedi."

        urunler = sonuc.UrunListesi
        df = pd.DataFrame([{
            "StokKodu": u.StokKodu,
            "SatisFiyati": u.SatisFiyati
        } for u in urunler])

        return df, None

    except Exception as e:
        return pd.DataFrame(), f"Ürün verisi çekilirken hata oluştu: {e}"

# Streamlit Arayüzü
st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

if st.button("📄 Satış Fiyatlarını Ticimax'ten Çek"):
    df, hata = satis_fiyatlarini_cek()
    if hata:
        st.error(hata)
    elif df.empty:
        st.warning("Ürün listesi boş veya çekilemedi.")
    else:
        st.success("Satış fiyatları başarıyla çekildi.")
        st.dataframe(df)
